# Лабораторна робота №6-7 — REST API «користувачі / публікації / коментарі»

Це Python‑реалізація лабораторної роботи №6-7: REST сервіс на FastAPI + SQLAlchemy + MySQL, що надає CRUD та фільтри для трьох сутностей — користувачі, публікації та коментарі.

```
├─ rest_lab6_python
│  ├─ app/
│  │  ├─ main.py        # FastAPI маршрути, CRUD, фільтри
│  │  ├─ models.py      # SQLAlchemy моделі (users, posts, comments)
│  │  ├─ schemas.py     # Pydantic DTO / відповіді
│  │  └─ database.py    # підключення до MySQL, session factory
│  ├─ main.py           # точка входу (uvicorn runner)
│  ├─ requirements.txt  # список залежностей
│  └─ .env.example      # приклад налаштувань
├─ rest_lab6.sql        # схема БД + стартові дані
├─ run_tests.ps1        # сценарій, що виконує всі приклади запитів
└─ README.md
```

## Технологічний стек

- Python 3.11+
- FastAPI 0.110, Pydantic 1.10
- SQLAlchemy 2.x, PyMySQL
- Uvicorn (ASGI сервер)
- MySQL 8.x (можна через XAMPP / Docker)

## Підготовка бази даних

1. Запустіть MySQL та створіть користувача (можна використовувати `root` без пароля в XAMPP).
2. Імпортуйте схему та дані:
   ```bash
   mysql -u root -p < rest_lab6.sql
   ```
   Скрипт створить БД `rest_lab6` з таблицями `users`, `posts`, `comments`, індексами та тестовими записами.

## Налаштування Python сервісу

```bash
cd rest_lab6_python
python -m venv .venv
.\\.venv\\Scripts\\activate          # PowerShell / cmd, у bash — source .venv/bin/activate
pip install -r requirements.txt
copy .env.example .env               # Windows; у bash: cp .env.example .env
```

У `.env` відредагуйте `DATABASE_URL` (формат `mysql+pymysql://user:pass@host:3306/rest_lab6`). Необовʼязкові змінні:

- `APP_PORT` — порт HTTP сервера (за замовчуванням 8080).
- `UVICORN_RELOAD=true` — автоматичний перезапуск під час розробки.
- `UVICORN_APP` — альтернативний імпорт (за замовчуванням `rest_lab6_python.app.main:app`).

## Запуск

```bash
python -m rest_lab6_python.main
# або
uvicorn rest_lab6_python.app.main:app --host 0.0.0.0 --port 8080 --reload
```

Після старту API доступний за `http://127.0.0.1:8080`. У браузері можна відкрити інтерактивну документацію:

- Swagger UI: `http://127.0.0.1:8080/docs`
- ReDoc: `http://127.0.0.1:8080/redoc`

## Ресурси та кінцеві точки

### Користувачі (`/users`)

- `POST /users` — створити користувача (тіло: `firstName`, `lastName`, `birthDate`, `email`, `active`, `role=user|admin`).
- `GET /users` — список із фільтрами: `name`, `surname`, `birthFrom`, `birthTo`, `role`, `active`.
- `GET /users/{id}` — деталі за ID.
- `PUT /users/{id}` — часткове оновлення (будь-яка підмножина полів).
- `DELETE /users/{id}` — видалити (каскадно видаляються публікації та коментарі).

### Публікації (`/posts`)

- `POST /posts` — створити публікацію (`title`, `body`, `link?`, `userId`).
- `GET /posts` — список із фільтрами `title`, `userId`.
- `GET /posts/{id}`, `PUT /posts/{id}`, `DELETE /posts/{id}` — повний CRUD.

### Коментарі (`/comments`)

- `POST /comments` — створити коментар (`body`, `userId`, `postId`).
- `GET /comments` — фільтри `userId`, `postId`.
- `GET /comments/{id}`, `PUT /comments/{id}`, `DELETE /comments/{id}`.
- `GET /posts/{postId}/comments` — усі коментарі публікації з додатковим фільтром `userId`.

Кожен маршрут повертає коректні HTTP статуси (`201`, `200`, `204`, `404`, `400`) та валідує дані. Зовнішні ключі контролюються на рівні БД і застосунку (перевірка на існування користувача/публікації перед створенням/оновленням).

## Приклади запитів (curl)

```bash
# Health-check
curl http://127.0.0.1:8080/health

# Створити користувача
curl -X POST http://127.0.0.1:8080/users \
  -H "Content-Type: application/json" \
  -d '{"firstName":"Oleh","lastName":"Shevchenko","birthDate":"1998-04-12","email":"oleh.shevchenko@example.com","active":true,"role":"user"}'

# Фільтр за іменем та роллю
curl "http://127.0.0.1:8080/users?name=Іва&role=admin&birthFrom=1990-01-01"

# Оновити користувача
curl -X PUT http://127.0.0.1:8080/users/4 \
  -H "Content-Type: application/json" \
  -d '{"email":"oleh.updated@example.com","active":false}'

# Створити публікацію
curl -X POST http://127.0.0.1:8080/posts \
  -H "Content-Type: application/json" \
  -d '{"title":"Security checklist","body":"Нагадування про 2FA.","link":"https://example.com/security","userId":1}'

# Коментарі публікації з фільтром за автором
curl "http://127.0.0.1:8080/posts/1/comments?userId=2"
```

> У PowerShell завершіть рядок символом `` ` `` або пишіть команду в один рядок. У `cmd.exe` використовуйте `^`.

## Автоматизована перевірка через PowerShell

Скрипт `run_tests.ps1` послідовно виконує весь сценарій (health-check → CRUD для кожного ресурсу) і друкує відповіді у форматі JSON.

```powershell
pwsh -ExecutionPolicy Bypass -File .\run_tests.ps1 -BaseUrl http://127.0.0.1:8080
```

Параметр `-BaseUrl` необовʼязковий. Скрипт автоматично підставляє ID створених сутностей у наступні кроки.

## Розробка та супровід

- `uvicorn rest_lab6_python.app.main:app --reload` — гаряче оновлення для локальної розробки.
- `pytest` (якщо додасте тести) або `run_tests.ps1` — швидка базова перевірка.
- Дотримуйтесь структури DTO з `schemas.py`, щоб не ламати клієнтські запити та тестовий сценарій.
