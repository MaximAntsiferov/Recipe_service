# Recipe_service
Сервис для публикации пользовательских рецептов<br>
<br>
Написан на языке Python 3.10.2<br>
База данных PosgreSQL 13
<br><br>

# Список используемых библиотек<br>
- fastapi
- pydantic
- uvicorn
- python-dotenv
- sqlalchemy
- databases
- asyncpg
- psycopg2
- python-jose
- passlib
- bcrypt
- python-multipart
<br><br>
# Инструкция по установке на сервер<br>
- sudo apt update
- sudo apt upgrade
- sudo apt install postgresql postgresql-client
- sudo -i -u postgres
- createdb bd
<br>

<br>
- sudo apt install git
- git clone https://github.com/MaximAntsiferov/Recipe_service
<br>
- cd Recipe_service/
- python3 -m venv .venv
- source .venv/bin/activate
- pip install requirements.txt

<br>
- переименовываем .env.example в .env 
- вписываем данные сервера и БД
<br>
- python app.py
