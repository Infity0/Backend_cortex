@echo off
chcp 65001 > nul
echo ================================================
echo Cortex AI Backend - Автоматическая установка
echo ================================================
echo.

echo [1/5] Проверка Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ОШИБКА] Python не установлен!
    echo Скачайте Python 3.10+ с https://www.python.org/downloads/
    pause
    exit /b 1
)
python --version
echo.

echo [2/5] Создание виртуального окружения...
if exist venv (
    echo Виртуальное окружение уже существует
) else (
    python -m venv venv
    echo [OK] Виртуальное окружение создано
)
echo.

echo [3/5] Установка зависимостей...
call venv\Scripts\activate.bat
pip install --upgrade pip
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ОШИБКА] Не удалось установить зависимости
    pause
    exit /b 1
)
echo [OK] Все зависимости установлены
echo.

echo [4/5] Настройка конфигурации...
if exist .env (
    echo [OK] Файл .env уже существует
) else (
    copy .env.example .env >nul
    echo [OK] Создан файл .env из шаблона
    echo [!!!] ВАЖНО: Отредактируйте .env файл и укажите:
    echo      - Пароль MySQL (DATABASE_URL)
    echo      - Секретный ключ (SECRET_KEY)
)
echo.

echo [5/5] Следующие шаги...
echo.
echo ================================================
echo ВАЖНО! Необходимо настроить базу данных:
echo ================================================
echo.
echo 1. Запустите MySQL и выполните:
echo    mysql -u root -p
echo.
echo 2. Создайте базу данных:
echo    CREATE DATABASE cortex_ai CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
echo    exit;
echo.
echo 3. Примените схему:
echo    mysql -u root -p cortex_ai ^< schema.sql
echo.
echo 4. Отредактируйте .env файл:
echo    - Укажите пароль MySQL в DATABASE_URL
echo    - Смените SECRET_KEY (используйте длинную случайную строку)
echo.
echo 5. Запустите сервер:
echo    start_server.bat
echo.
echo ================================================
echo Установка завершена!
echo ================================================
pause
