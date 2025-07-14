

Чтобы запустить проект 

1 склонируйте на свой комп проект

git clone https://github.com/jas0n667/ecom.git
cd ecom

2 Поднимите все сервисы в yaml файле

docker compose up --build -d

3 Запустите скрипт который добавляет данные в бд

source venv/bin/activate

(venv) python3 add_db.py

Все 
Теперь API доступен на 8003 порту на localhost:8003/docs

Интерфейс базу данных доступен localhost:8080/docs



<img width="390" height="202" alt="изображение" src="https://github.com/user-attachments/assets/e1a960ca-9e9a-4c2f-ba34-026fe1045240" />

Данные для входа в Adminer:

    Сервер: postgres

    Пользователь: admin

    Пароль: admin123

    БД: mydb

