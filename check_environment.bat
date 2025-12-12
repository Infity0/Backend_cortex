@echo off
chcp 65001 > nul
echo ================================================
echo Cortex AI - Проверка окружения
echo ================================================
echo.

:: Проверка виртуального окружения
echo [1] Проверка виртуального окружения...
if exist venv (
    echo [OK] Виртуальное окружение существует
) else (
    echo [ОШИБКА] Виртуальное окружение не найдено
    echo Запустите: setup.bat
    pause
    exit /b 1
)
echo.

:: Активация venv
call venv\Scripts\activate.bat

:: Проверка Python
echo [2] Проверка Python...
python --version
echo.

:: Проверка зависимостей
echo [3] Проверка установленных пакетов...
pip list | findstr /i "fastapi sqlalchemy uvicorn"
echo.

:: Проверка .env
echo [4] Проверка конфигурации...
if exist .env (
    echo [OK] Файл .env существует
    
    :: Проверка секретного ключа
    findstr /C:"SECRET_KEY=your-secret-key" .env >nul 2>&1
    if %errorlevel% equ 0 (
        echo [!!!] ПРЕДУПРЕЖДЕНИЕ: SECRET_KEY не изменен!
        echo      Сгенерируйте новый ключ:
        echo      python -c "import secrets; print(secrets.token_urlsafe(32))"
    ) else (
        echo [OK] SECRET_KEY установлен
    )
    
    :: Проверка пароля БД
    findstr /C:"password@localhost" .env >nul 2>&1
    if %errorlevel% equ 0 (
        echo [!!!] ПРЕДУПРЕЖДЕНИЕ: Пароль MySQL не изменен!
        echo      Укажите реальный пароль в DATABASE_URL
    ) else (
        echo [OK] DATABASE_URL настроен
    )
) else (
    echo [ОШИБКА] Файл .env не найден
    echo Запустите: setup.bat
)
echo.

:: Проверка подключения к БД
echo [5] Проверка подключения к базе данных...
python -c "from app.core.config import settings; print(f'База данных: {settings.DB_NAME}'); print('URL:', settings.DATABASE_URL.split('@')[1] if '@' in settings.DATABASE_URL else 'настроен')" 2>nul
if %errorlevel% neq 0 (
    echo [ОШИБКА] Не удалось загрузить конфигурацию
    echo Проверьте .env файл
) else (
    echo [OK] Конфигурация загружена
)
echo.

:: Проверка структуры директорий
echo [6] Проверка структуры проекта...
if exist app\main.py (echo [OK] app\main.py) else (echo [ОШИБКА] app\main.py не найден)
if exist schema.sql (echo [OK] schema.sql) else (echo [ОШИБКА] schema.sql не найден)
if exist alembic (echo [OK] alembic\) else (echo [ОШИБКА] alembic\ не найден)
if exist uploads (echo [OK] uploads\) else (echo [!!!] uploads\ не найден - будет создан автоматически)
echo.

echo ================================================
echo Проверка завершена!
echo ================================================
echo.
echo Если все проверки прошли успешно, запустите:
echo start_server.bat
echo.
pause
