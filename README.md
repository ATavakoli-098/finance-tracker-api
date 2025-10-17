# Finance Tracker API

A simple FastAPI-based finance tracking API that lets users manage categories, transactions, and get monthly summaries — built with SQLAlchemy and PostgreSQL (SQLite in dev).

Live Demo: https://finance-tracker-api-q7tk.onrender.com/docs

## Features
- Create users, categories, and transactions
- Filter transactions by user
- Monthly summaries with income, expense, and net totals
- Optional PostgreSQL support for production
- Clean RESTful structure
- Fully documented OpenAPI (/docs)
- Deployable via Docker or directly to Render

## Entity Model Overview
User: id, name  
Category: id, name, user_id  
Transaction: id, user_id, category_id, amount, type, description, timestamp

## Endpoints
POST /users — Create a new user  
POST /categories — Create a new category  
GET /categories?user_id={id} — List categories for a user  
POST /transactions — Create a transaction  
GET /transactions?user_id={id} — List transactions for a user  
GET /summary?user_id={id}&month={YYYY-MM} — Monthly summary

## Example Requests

POST /users
curl -X POST "https://finance-tracker-api-q7tk.onrender.com/users" -H "Content-Type: application/json" -d '{"name": "Arash"}'
Response:
{"id": 1, "name": "Arash"}

POST /transactions
curl -X POST "https://finance-tracker-api-q7tk.onrender.com/transactions" -H "Content-Type: application/json" -d '{"user_id":1,"amount":42.75,"type":"expense","category_id":1,"description":"Weekly groceries","timestamp":"2025-10-16T14:00:00"}'
Response:
{"id":1,"user_id":1,"amount":42.75,"type":"expense","category_id":1,"description":"Weekly groceries","timestamp":"2025-10-16T14:00:00"}

GET /summary?user_id=1&month=2025-10
curl -X GET "https://finance-tracker-api-q7tk.onrender.com/summary?user_id=1&month=2025-10"
Response:
{"month":"2025-10","totals":{"income":0,"expense":42.75,"net":-42.75},"by_category":[{"category_id":1,"category_name":"Groceries","total":42.75}]}

GET /transactions?user_id=1&limit=50&offset=0
curl -X GET "https://finance-tracker-api-q7tk.onrender.com/transactions?user_id=1&limit=50&offset=0"
Response:
[{"id":1,"user_id":1,"category_id":1,"amount":42.75,"type":"expense","description":"Weekly groceries","timestamp":"2025-10-16T14:00:00"}]

## Run Locally
git clone https://github.com/<your-username>/finance-tracker-api.git
cd finance-tracker-api
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
App runs at http://127.0.0.1:8000/docs

## Run with Docker
docker build -t finance-tracker-api .
docker run -d -p 8000:8000 -e DATABASE_URL="postgresql+psycopg2://USER:PASS@HOST:5432/DB" finance-tracker-api
Then open http://localhost:8000/docs
(If DATABASE_URL omitted, SQLite is used automatically.)

## Environment Variables
DATABASE_URL — PostgreSQL connection string  
PORT — default 8000  

## Authentication
None for demo; JWT planned for production.

## Limitations
- No authentication yet
- Minimal validation
- Monthly summary only
- No frontend UI
- SQLite default

## Roadmap
✅ CRUD API  
✅ Monthly summaries  
✅ Render deployment  
🔜 JWT Auth  
🔜 Unit tests  
🔜 React/Streamlit frontend  
🔜 CI/CD pipeline

## Author
Arash — CS Student @ Royal Holloway  
Built with FastAPI, SQLAlchemy, PostgreSQL

## License
MIT License. Free to use, modify, and deploy.
