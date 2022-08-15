# Recipe_service
Сервис для публикации пользовательских рецептов<br>
<br>
Написан на языке Python 3.8.1<br>
База данных PosgreSQL<br>
Система Ubuntu 20.04<br>
<br>

Список необходимых библиотек в файле requirements.txt

# Инструкция по установке на сервер
- sudo apt update
- sudo apt upgrade
- sudo apt install postgresql postgresql-client
- sudo -i -u postgres
- createdb bd

Ctrl + D

- sudo apt install git
- git clone https://github.com/MaximAntsiferov/Recipe_service

- sudo apt install python3.8-venv
- cd Recipe_service/
- python3 -m venv .venv
- source .venv/bin/activate
- pip install requirements.txt
