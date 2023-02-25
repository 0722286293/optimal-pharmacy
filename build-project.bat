@echo off

@Rem Remove previous .env folder
rmdir /s /q .venv

@Rem Create virtual environment
python -m venv .venv

@Rem Timeout for 10 seconds
timeout 10

rem activate virtual environment
call .venv/Scripts/activate.bat

@Rem install requirements
pip install -r requirements.txt

@Rem run migrations
python manage.py makemigrations
python manage.py migrate