### Hexlet tests and linter status:
[![Actions Status](https://github.com/julverik/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/julverik/python-project-83/actions)

https://page-analyzer-5ze8.onrender.com  -  ссылка по которой можно проверить
## SonarCloud

[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=julverik_python-project-83&metric=coverage)](https://sonarcloud.io/summary/new_code?id=julverik_python-project-83)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=julverik_python-project-83&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=julverik_python-project-83)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=julverik_python-project-83&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=julverik_python-project-83)

## Описание

**Page Analyzer** — это веб-приложение для SEO-анализа страниц. Оно позволяет:

- Добавлять сайты для анализа
- Запускать проверки SEO-параметров
- Хранить историю всех проверок

### Установка и запуск

```bash
# 1. Клонировать репозиторий
git clone https://github.com/julverik/python-project-83.git
cd python-project-83

# 2. Установить зависимости
make install

# 3. Создать базу данных
createdb page_analyzer_development

# 4. Применить SQL-схему
psql -d page_analyzer_development -f database.sql

# 5. Создать файл .env с настройками
echo "DATABASE_URL=postgresql://localhost:5432/page_analyzer_development" > .env
echo "SECRET_KEY=your-secret-key-here" >> .env

# 6. Запустить приложение
make dev