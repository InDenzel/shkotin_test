# shkotin_test
Тестовое задание. Шкотин Даниил

Необходимо создать веб-приложение с помощью фреймворка Falcon с использованием СУБД PostgreSQL c одной таблицей, а также реализовать возможность пользователю производить CRUD-операции с данной таблицей.
Во время работы над тестовым заданием было создано веб-приложение, а также реализована возможность создания репозитория с образами самого веб-приложения и БД в Docker.
Система была выложена на github, что также являлось частью тестового задания.

Инструкция:
В командной строке прописать данные команды:
1) git clone https://github.com/InDenzel/shkotin_test.git (создается локальная копия проекта из репозитория github)
2) cd shkotin_test (перейти в папку с проектом)
3) git checkout master (перейти на ветку master, благодаря чему подтянуться необходимые данные проекта)
4) docker-compose up -d (создаются и запускаются образы с контейнером с помощью файла docker-compose.yml)
5) Перейти в браузер и ввести http://localhost:8000/
