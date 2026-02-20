Стек технологий:
    Python 3.11
    FastAPI
    SQLAlchemy
    Alembic
    PostgreSQL 16
    Docker + Docker Compose
    Pydantic
    Uvicorn ASGI Server

1. Собрать и запустить проект командой
    docker-compose up --build

2. Автоматически применятся все миграции

3. Зайти по ссылки http://127.0.0.1:8000/docs

4. В проекте 5 эндпоинтов:
    1. /api/v1/wallets/create - создаёт кошелёк с id и суммой
    2. /api/v1/wallets/operation - меняет сумму кошельку на добавление "DEPOSIT" на снятие "WITHDRAW"
    3. /api/v1/wallets/delete  - удаляет кошелёк по id
    4. /api/v1/wallets/list - выводит список всех кошельков
    5. /api/v1/wallets/get/{id} - выводит определённый кошелёк по ID
