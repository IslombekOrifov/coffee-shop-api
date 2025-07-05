# Coffee Shop API

**Проект FastAPI** для управления пользователями с регистрацией, аутентификацией, авторизацией и верификацией.

---

## **Возможности проекта**

✅ Регистрация пользователей с верификацией email
✅ JWT аутентификация (access и refresh токены)
✅ Хранение refresh токенов в базе данных
✅ Использование blacklist для отозванных токенов
✅ Роли пользователей (Admin и User)
✅ Эндпоинты управления пользователями (CRUD)
✅ Асинхронный SQLAlchemy (PostgreSQL)
✅ Aрхитектура (DAO + сервисы)

---

## **Технологический стек**

* **FastAPI** (backend framework)
* **SQLAlchemy** async ORM
* **PostgreSQL** (база данных)
* **Alembic** (миграции)
* **Pydantic** (валидация и схемы)
* **JWT (python-jose)** для генерации токенов
* **Passlib (bcrypt)** для хеширования паролей
* **Docker и docker-compose** (контейнеризация)

---

## **Структура проекта**

```
app/
  ├── config/            # Настройки и база данных
  ├── routers/           # Роутеры (auth, users)
  ├── models/            # SQLAlchemy модели
  ├── schemas/           # Pydantic схемы
  ├── services/          # Бизнес-логика (DAO, генерация токенов)
  ├── deps/              # Dependency injection
  ├── custom_jwt/        # JWT utils, SQLAlchemy модели, DAO 
main.py                  # Точка входа приложения FastAPI
```

---

## **Запуск проекта**

### **1. Клонируй репозиторий**

```bash
git clone https://github.com/IslombekOrifov/coffee-shop-api.git
cd coffee-shop-api
```

---

### **2. Настрой .env файл**

Создай файл `.env` в корне проекта:

```
SECRETF_KEY=your_new_secret_key
DEBUG=False

DB_HOST=coffee_db
DB_PORT=5432
DB_USER=admin
DB_PASS=admin
DB_NAME=cofee_shop

EMAIL_HOST_USER=your_user
EMAIL_HOST_PASSWORD=your pass
EMAIL_PORT=587

CELERY_BROKER_URL=redis://coffee_redis:6379/0
CELERY_RESULT_BACKEND=redis://coffee_redis:6379/1
```

---

### ✅ **3. Запусти через Docker Compose**

```bash
docker-compose up --build
```

API будет доступно по адресу: **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**

---


---

## **Архитектура проекта**

### **Слои**

* **Routers (api/)** – обработка HTTP-запросов
* **Schemas (schemas/)** – Pydantic модели для валидации
* **Models (models/)** – SQLAlchemy модели для БД
* **Services (services/)** – бизнес-логика, DAO, генерация токенов
* **JWT (ustom_jwt/)** – JWT utils, SQLAlchemy модели, DAO 
* **Deps (deps/)** – зависимости через Depends
* **Config (config/)** – конфигурация проекта, engine базы

---

### **Auth Flow**

1. **Signup** (`POST /auth/signup`)

   * Регистрация пользователя (email + password)
   * Генерация кода верификации (email)
   * Статус пользователя: `unverified`

2. **Verify** (`POST /auth/verify`)

   * Пользователь отправляет код
   * Статус обновляется на `verified`

3. **Login** (`POST /auth/login`)

   * Возвращает access и refresh токены

4. **Refresh** (`POST /auth/refresh`)

   * Обновляет access token

5. **Logout** (`POST /auth/logout`)

   * Добавляет refresh token в blacklist и удаляет из whitelist

---

### **Эндпоинты управления пользователями**

* `GET /users/me` – получить текущего пользователя
* `GET /users` – список пользователей (только admin)
* `GET /users/{id}` – получить пользователя по ID (только admin)
* `PATCH /users/{id}` – обновить данные пользователя (сам или admin)
* `DELETE /users/{id}` – удалить пользователя (только admin)

---

### **Безопасность**

* JWT токены со scope (`access_token`, `refresh_token`)
* Хранение refresh токенов в БД
* Таблица blacklist для отозванных refresh токенов
* Хеширование паролей через bcrypt
* Проверка прав доступа по ролям (admin, user)

---

## **Примечания для разработки**

* Все эндпоинты задокументированы в **Swagger UI** (`/docs`)
* Используется **AsyncSession** для неблокирующих операций с БД
* Архитектура проекта подготовлена для лёгкого масштабирования

---

### **Планы на улучшение**
* Добавить Celery-задачи (например, регулярная очистка просроченных токенов из blacklist)
* Написать Unit и integration tests (pytest)
* Настроить CI/CD pipeline для автодеплоя

---