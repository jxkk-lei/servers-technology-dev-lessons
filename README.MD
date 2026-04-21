Это репозиторий с задачами и работами выполнеными в рамках дисциплины Технологии серверной разработки 3-его семестра

Task #n - Номер контрольной работы
project#n - номер конкретной задачи из контрольной работы

Пояснение к контрольной №3

Создаёсм и запускаем виртуальное окружение

python -m venv venv
venv\Scripts\activate

Устанавливаем зависимости
pip install -r requirements.txt

Запуск осуществяллется через uvicorn

нужно зайти в директорию задания
К примеру cd project6.1
и прописать uvicorn app.main:app --reload

Тестирования энд-поинтов(Postman)

project6.1 

Тест 1
Метод: GET
URL: http://127.0.0.1:8000/login
Authorization: Basic Auth (username: admin, password: admin)

Ожидаемый ответ "message": "Successfully"

Тест 2

Повторить действия с Тест 1, но с неправильными данными

Ожидаемый ответ status 401

project6.2 

Тест 1
Метод: POST
URL: http://127.0.0.1:8000/register
Body:
{
  "username": "test",
  "password": "test"
}

Ожидаемый ответ "message": "User created"

Тест 2

Метод: GET
URL: http://127.0.0.1:8000/login
Authorization:
Type: Basic Auth
username: test
password: test

Ожидаемый ответ "message": "Welcome, test!"

project6.3 

.env укажите нужны режим для тестирования

тестирование можно провесити командами указанами в методичке к заданию

project6.4 

Тест 1
Метод: POST
URL: http://127.0.0.1:8000/login
Body:
{
  "username": "admin",
  "password": "123"
}

Ожидаемый ответ должны получить токен в поле "access_token"

Тест 2

Метод: GET
URL: http://127.0.0.1:8000/protected_resource
Authorization:
Type: Bearer Token
Token: "полученый токен"

Ожидаемый ответ "message": "Access granted"

project6.5 

Тест 1
Метод: POST
URL: http://127.0.0.1:8000/reqister
Body:
{
  "username": "test",
  "password": "test"
}

Ожидаемый ответ: "message": "New user created"

При повторной регистрации с теми же данными ожидается: "detail": "User already exists" (Status 409)

Тест 2

Метод: POST
URL: http://127.0.0.1:8000/login
Body:
{
  "username": "test",
  "password": "test"
}

Ожидаемый ответ "message":
  "access_token": "",
  "token_type": "bearer"

!!!По условиям данной задачи должен быть установлен "rate limit", можно просто отправить несколько запросов и получить ошибку (для регистрации 1 раз и для авторизации 5 раз)
Ожидаемый статус: 429 - "detail": "Too many requests"