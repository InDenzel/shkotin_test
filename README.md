# shkotin_test
Тестовое задание. Шкотин Даниил

Необходимо создать веб-приложение с помощью фреймворка Falcon с использованием СУБД PostgreSQL c одной таблицей, а также реализовать возможность пользователю производить CRUD-операции с данной таблицей.  

Во время работы над тестовым заданием было создано веб-приложение, а также реализована возможность создания репозитория с образами самого веб-приложения и БД в Docker.  
Система была выложена на github, что также являлось частью тестового задания.

Инструкция:  
В командной строке прописать данные команды:
1) git clone https://github.com/InDenzel/shkotin_test (создается локальная копия проекта из репозитория github)
2) cd shkotin_test (перейти в папку с проектом)
3) docker-compose up -d (создаются и запускаются образы с контейнером с помощью файла docker-compose.yml)
4) Перейти в браузер и ввести http://localhost:8000/  
В случае если страница не открывается, повторить 3 пункт и перезапустить страницу

Веб-приложение:  
Главная страница является демонстрацией стека технологий, который был задействован для реализации тестового задания.  
Вкладка "Добавить клиента" откроет страницу для добавления клиента в БД.  
После добавления будет открыта страница "Информация" с выводом клиентов из БД (на момент запуска будет пустой).  
Для изменения и удаления клиента необходимо нажать на его данные, после чего откроется страница с возможностью удаления и изменения.
