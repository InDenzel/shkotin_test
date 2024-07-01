import falcon
import os
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, Session

# локально
#engine = create_engine('postgresql://postgres:123@localhost:5432/MYDB?client_encoding=utf8')
# для docker
engine = create_engine('postgresql://postgres:123@postgresql:5432/MYDB?client_encoding=utf8')

Base = declarative_base()
session = Session(bind=engine)

class Users(Base):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key = True)
    name = Column(String(20))
    last_name = Column(String(20))
    phone = Column(String(11))
Base.metadata.create_all(engine)



menu = '''<body style="padding-top: 50px;" bgcolor=#233157>
        <div class = "menu" align = center>
            <meta charset="UTF-8">
            <a href="/">Главная</a>
            <a href="/input">Добавить клиента</a>
            <a href="/output">Информация</a>
        </div>'''

style_css = '''<style>
                    td, th {border: 1px solid grey;}
                    table {width: 400px;border: 1px solid grey; background-color: white;}
                    a {color: black;}
                    input {margin-bottom: 10px;}
                    h1 {text-align: center; color: white;}
                    img {width: 200px; height: 200px;}

                    .menu {
                        top: 0;
                        position: fixed;
                        background-color: #233157;
                        width: 100%;
                        font-size:20px ;
                        font-family:Lobster, cursive;
                        height: 50px;
                        text-shadow: 5px 5px 5px black;
                        z-index: 2;
                    }

                    .menu a {
                        color: #f2f2f2;
                    }
                </style></body>'''
class MainMenu:
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = 'text/html'
        resp.text = menu + '''<h1>Для реализации тестового задания был использован следующий стек технологий</h1>
        <div style="display: flex;  flex-direction: row;  justify-content: center; justify-content: space-around">
            <div><h1>Python</h1><img src="/static/python.png"></div>
            <div><h1>Falcon</h1><img src="/static/falcon.png"></div>
            <div><h1>PostgreSQL</h1><img src="/static/postgresql.png"></div>
            <div><h1>SQLAlchemy</h1><img src="/static/SQLAlchemy.png"></div>
            <div><h1>Docker</h1><img src="/static/docker.png"></div>
            <div><h1>Git</h1><img src="/static/git.png"></div>
        </div>''' + style_css

class InputUsers:
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = 'text/html'
        resp.text = menu + '''

        <h1>Добавление клиентов</h1>
        <form method="POST" action="/output">
            <input type="hidden" name="previous_path" value="/input">
            <div style="display: flex;  flex-direction: column;  justify-content: space-between; align-items: center;">
                <input type="text" name="name_data" placeholder="Введите имя" required>
                <input type="text" name="last_name_data" placeholder="Введите фамилию" required>
                <input type="tel" name="phone_data" placeholder="Введите телефон" pattern="[0-9]{11}" required oninvalid="setCustomValidity('Введите номер телефона (11 цифр)')" oninput="setCustomValidity('')" onkeypress="return event.charCode >= 48 && event.charCode <= 57">
                <input type="submit" value="Подтвердить">   
            <div>
        </form>''' + style_css

class OutputUsers:
    def output(self, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = 'text/html'
        full_info = session.query(Users.id, Users.name, Users.last_name, Users.phone).order_by(Users.id).all()
        if len(full_info) > 0:
            info = '<br>'
            for detailed_user in full_info:
                info += f'''<tr align="center">
                                            <td><a href=/output/{detailed_user.id}>{detailed_user.id}</a></td>
                                            <td><a href=/output/{detailed_user.id}>{detailed_user.name}</a></td>
                                            <td><a href=/output/{detailed_user.id}>{detailed_user.last_name}</a></td>
                                            <td><a href=/output/{detailed_user.id}>{detailed_user.phone}</a></td>
                                        </tr>'''
            resp.text = menu + f'''
                                    <h1>Вывод клиентов</h1>
                                    <table align="center">
                                        <th>ID</th>
                                        <th>Имя</th>
                                        <th>Фамилия</th>
                                        <th>Телефон</th>
                                            {info}
                                    </table> ''' + style_css
        else:
            resp.text = menu + f'''
                        <h1>Вывод клиентов</h1>
                        <table align="center">
                            <th>ID</th>
                            <th>Имя</th>
                            <th>Фамилия</th>
                            <th>Телефон</th>
                                <tr align="center">
                            <td colspan=4>
                            <p>В базе данных отсутствуют записи</p>
                            </td>
                            </tr>
                        </table> ''' + style_css

    def on_get(self, req, resp):
        self.output(resp)

    def on_post(self, req, resp, id_user=None):
        if req.media.get('previous_path') == '/input':
            new_user = Users(
                name=req.media.get('name_data'),
                last_name=req.media.get('last_name_data'),
                phone=req.media.get('phone_data')
            )
            session.add(new_user)
            session.commit()
        self.output(resp)

class DetailedOutputUsers:
    def output(self, req, resp, id_user):
        detailed_user = \
        session.query(Users.id, Users.name, Users.last_name, Users.phone).filter(Users.id == id_user).all()[0]
        resp.status = falcon.HTTP_200
        resp.content_type = 'text/html'
        resp.text = menu + f'''
                <h1>Вывод {detailed_user.id} клиента</h1>
                <table align="center">
                    <th>ID</th>
                    <th>Имя</th>
                    <th>Фамилия</th>
                    <th>Телефон</th>

                    <tr align="center">
                        <td>{detailed_user.id}</td>
                        <td>{detailed_user.name}</td>
                        <td>{detailed_user.last_name}</td>
                        <td>{detailed_user.phone}</td>
                    </tr>

                    <tr align="center">
                        <td colspan=2>
                            <p align="center"><a href="/output/{id_user}/delete" class="btn btn_danger">Удалить</a></p>
                        </td>
                        <td colspan=2>
                            <p align="center"><a href="/output/{id_user}/update" class="btn btn_danger">Обновить</a></p>
                        </td>
                    </tr>
                </table>''' + style_css

    def on_get(self, req, resp, id_user):
        self.output(req, resp, id_user)

    def on_post(self, req, resp, id_user):
        session.query(Users).filter(Users.id == id_user).update({'name' : req.media.get('name_data'),
                                                                  'last_name' : req.media.get('last_name_data'),
                                                                  'phone' : req.media.get('phone_data')})
        session.commit()
        self.output(req, resp, id_user)

class DeleteUser:
    def on_get(self, req, resp, id_user):
        session.query(Users).filter(Users.id == id_user).delete()
        session.commit()
        resp.status = falcon.HTTP_302
        resp.set_header('Location', '/output')

class UpdateUser:
    def on_get(self, req, resp, id_user):
        detailed_user = \
        session.query(Users.id, Users.name, Users.last_name, Users.phone).filter(Users.id == id_user).all()[0]
        resp.status = falcon.HTTP_200
        resp.content_type = 'text/html'
        s = ''
        html_vivod = (menu + f'<h1>Редактирование {id_user} клиента</h1>'+'''
                <form method="POST" action="/output/{}">
                    <div style="display: flex;  flex-direction: column;  justify-content: space-between; align-items: center;">'''+
                     f'<input type="text" name="name_data" placeholder="Введите имя" value = {detailed_user.name} required >'+
                     f'<input type="text" name="last_name_data" placeholder="Введите фамилию" value = {detailed_user.last_name} required>'+
                     f'<input type="tel" name="phone_data" placeholder="Введите телефон" value="{detailed_user.phone}" pattern="[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]" required oninvalid="setCustomValidity("Введите номер телефона (11 цифр)")" oninput="setCustomValidity('')" onkeypress="return event.charCode >= 48 && event.charCode <= 57">'+
                     '''<input type="submit" value="Подтвердить">
                    <div>
                </form>''')
        resp.text = html_vivod.format(id_user) + style_css


app = falcon.App()

static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
app.add_static_route('/static', static_dir)

app.add_route('/', MainMenu())
app.add_route('/input', InputUsers())
app.add_route('/output', OutputUsers())
app.add_route('/output/{id_user}', DetailedOutputUsers())
app.add_route('/output/{id_user}/delete', DeleteUser())
app.add_route('/output/{id_user}/update', UpdateUser())

if __name__ == '__main__':
    from wsgiref import simple_server
    httpd = simple_server.make_server('0.0.0.0', 8000, app)
    httpd.serve_forever()