@echo off

@Rem activate virtual environment
call .venv/Scripts/activate.bat

@Rem open server
start python manage.py runserver 8000 & start http://127.0.0.1:8000/
