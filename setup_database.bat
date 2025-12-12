@echo off
chcp 65001 > nul
echo ================================================
echo Cortex AI - Настройка базы данных MySQL
echo ================================================
echo.

echo Этот скрипт поможет настроить базу данных
echo.

:: Запрос пароля MySQL
set /p MYSQL_PASSWORD="Введите пароль root для MySQL: "
echo.

echo [1/2] Создание базы данных...
echo.


mysql -u root -p%MYSQL_PASSWORD% -e "CREATE DATABASE IF NOT EXISTS cortex_ai CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;" 2>nul

if %errorlevel% neq 0 (
    echo [ОШИБКА] Не удалось подключиться к MySQL
    echo Проверьте:
    echo   1. MySQL запущен
    echo   2. Пароль введен правильно
    echo   3. Пользователь root имеет права
    pause
    exit /b 1
)

echo [OK] База данных cortex_ai создана или уже существует
echo.

echo [2/2] Применение схемы БД...
mysql -u root -p%MYSQL_PASSWORD% cortex_ai < schema.sql

if %errorlevel% neq 0 (
    echo [ОШИБКА] Не удалось применить схему
    pause
    exit /b 1
)

echo [OK] Схема успешно применена
echo.

echo ================================================
echo База данных настроена!
echo ================================================
echo.
echo Следующий шаг:
echo 1. Отредактируйте .env файл
echo 2. Укажите пароль MySQL в DATABASE_URL:
echo    DATABASE_URL=mysql+aiomysql://root:%MYSQL_PASSWORD%@localhost:3306/cortex_ai
echo.
echo 3. Запустите сервер: start_server.bat
echo.
pause
