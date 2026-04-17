migrant-med-service

Как запустить проект

Backend

1. Перейти в папку backend

macOS:
cd /Users/nerand/Desktop/FMS/migrant-med-service/backend

Windows:
cd C:\Users\nerand\Desktop\FMS\migrant-med-service\backend

2. Создать виртуальное окружение

macOS:
python3 -m venv .venv

Windows:
python -m venv .venv

3. Активировать виртуальное окружение

macOS:
source .venv/bin/activate

Windows:
.venv\Scripts\activate

4. Установить зависимости backend

pip install --upgrade pip
pip install fastapi "uvicorn[standard]" sqlalchemy pydantic email-validator python-multipart

5. Запустить backend

uvicorn app.main:app --reload --port 8000

Frontend

1. Открыть второй терминал и перейти в папку frontend

macOS:
cd /Users/nerand/Desktop/FMS/migrant-med-service/frontend

Windows:
cd C:\Users\nerand\Desktop\FMS\migrant-med-service\frontend

2. Установить зависимости frontend

npm install
npm install axios

3. Запустить frontend

npm run dev

Адреса

Frontend:
http://localhost:5173

Backend Swagger:
http://localhost:8000/docs

Если проект уже запускался раньше

Backend:
перейти в папку backend, активировать .venv и выполнить
uvicorn app.main:app --reload --port 8000

Frontend:
перейти в папку frontend и выполнить
npm run dev
