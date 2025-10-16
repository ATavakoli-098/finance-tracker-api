# Finance Tracker API

[![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.1x-brightgreen.svg)](https://fastapi.tiangolo.com/)
[![CI](https://github.com/ATavakoli-098/finance-tracker-api/actions/workflows/ci.yml/badge.svg)](https://github.com/ATavakoli-098/finance-tracker-api/actions/workflows/ci.yml)

FastAPI service for users, categories, transactions, and a monthly summary endpoint. SQLite by default; Postgres via `DATABASE_URL`.

## Quickstart

```bash
python -m venv .venv
# Windows
.\.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
