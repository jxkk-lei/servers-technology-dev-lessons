# Контрольная работа №4

Каждое задание находится в отдельной папке по формату предыдущих контрольных:

- `project9.1` - Alembic, SQLAlchemy-модель `Product`, две миграции SQLite.
- `project10.1` - пользовательские исключения и обработчики ошибок FastAPI.
- `project10.2` - Pydantic-валидация JSON и кастомный обработчик ошибок валидации.
- `project11.1` - модульные тесты FastAPI через `TestClient`.
- `project11.2` - асинхронные тесты через `pytest-asyncio`, `httpx.AsyncClient`, `ASGITransport` и `Faker`.

## Установка

```bash
cd Task4
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Если нужна переменная окружения для базы данных, создайте `.env` из примера:

```bash
copy .env.example .env
```

## Задание 9.1

```bash
cd project9.1
alembic upgrade head
uvicorn app.main:app --reload
```

Проверка:

```bash
curl http://127.0.0.1:8000/products
```

Миграции:

- `20260511_0001_create_products.py` создает таблицу `products` и добавляет две записи.
- `20260511_0002_add_description_to_products.py` добавляет поле `description NOT NULL`.

## Задание 10.1

```bash
cd project10.1
uvicorn app.main:app --reload
```

Проверка:

```bash
curl http://127.0.0.1:8000/custom-a
curl http://127.0.0.1:8000/custom-b/42
```

## Задание 10.2

```bash
cd project10.2
uvicorn app.main:app --reload
```

Проверка валидного запроса:

```bash
curl -X POST http://127.0.0.1:8000/validate-user ^
  -H "Content-Type: application/json" ^
  -d "{\"username\":\"alex\",\"age\":25,\"email\":\"alex@example.com\",\"password\":\"password123\"}"
```

Проверка ошибки валидации:

```bash
curl -X POST http://127.0.0.1:8000/validate-user ^
  -H "Content-Type: application/json" ^
  -d "{\"username\":\"alex\",\"age\":18,\"email\":\"wrong\",\"password\":\"short\"}"
```

## Задание 11.1

```bash
cd project11.1
pytest
```

Тесты проверяют создание, получение, удаление пользователя и ошибки `404`.

## Задание 11.2

```bash
cd project11.2
pytest
```

Тесты асинхронные, используют `httpx.AsyncClient` с `ASGITransport`, Faker-данные и очистку in-memory состояния между кейсами.

Из папки `Task4` можно запустить оба набора тестов сразу:

```bash
pytest
```
