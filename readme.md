
# WHO BE

## The way to run project
- Step 1: `pip install poetry`
- Step 2: `poetry install`
- Step 3: `cd database/`
- Step 4: `docker compose up -d`
- Step 5: `cd ..`
- Step 3: `python manage.py makemigrations`
- Step 4: `python manage.py migrate`
- Step 5: `python manage.py runserver`
- Step 6: Go to visit on the website api -> http://127.0.0.1:8000/