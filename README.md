### Hexlet tests and linter status:
[![Actions Status](https://github.com/bulbaattacks/python-project-83/workflows/hexlet-check/badge.svg)](https://github.com/bulbaattacks/python-project-83/actions)

[![Maintainability](https://api.codeclimate.com/v1/badges/47ebe37ff75503196def/maintainability)](https://codeclimate.com/github/bulbaattacks/python-project-83/maintainability)

[![Test Coverage](https://api.codeclimate.com/v1/badges/47ebe37ff75503196def/test_coverage)](https://codeclimate.com/github/bulbaattacks/python-project-83/test_coverage)

## About
Web-приложение «Анализатор страниц» анализирует страницы на SEO-пригодность по аналогии с PageSpeed Insights(https://pagespeed.web.dev). Приложение написано на базе фреймворка Flask. Фронтенд - на bootstrap.Для работы с базой данных PosgreSQL применена библиотека psycopg.

The Page Analyzer web application analyzes pages for SEO suitability similar to PageSpeed ​​Insights(https://pagespeed.web.dev). The application is written based on the Flask framework. Frontend - on bootstrap. The psycopg library is used to work with the PosgreSQL database.

### How to run 
1. Clone this repository
2. Install dependencies by poetry install
3. Copy the content from .env.sample and paste it in your .env file.
`
cp .env.sample .env
`

4. Run one of commands make dev or make start

Build with:
- Python
- Flask
- Bootstrap
- Jinja2
- Beautiful Soup
- Requests
- Pytest
- PostgreSQL
- Flake8
