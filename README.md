# 🛒 Grocery Compare API

A backend API for comparing grocery prices across stores, built using FastAPI and SQLAlchemy.

## 📌 Overview

This project focuses on designing a scalable backend system that:

- Stores raw scraped grocery data
- Normalizes products into canonical items
- Tracks prices across different stores
- Enables price comparison through API endpoints

## 🏗️ Tech Stack

- **Backend:** FastAPI
- **Database:** SQLite (for development)
- **ORM:** SQLAlchemy
- **Validation:** Pydantic

## 📂 Project Structure
.
├── main.py # Entry point
├── database.py # DB connection & session
├── models.py # SQLAlchemy models (tables)
├── schema.py # Pydantic schemas (request/response)
├── crud/
│ └── crud_stores.py # DB operations
├── routers/
│ └── router_stores.py # API endpoints

## ⚙️ Features Implemented

- Created a store, raw_items_table
- CRUD endpoints for store and raw_items
- Structured API using routers + CRUD separation
- Response validation using Pydantic
- Database integration using SQLAlchemy

## 🔌 API Endpoints

### Stores

- `POST /stores/` → Create a new store  
- `GET /stores/` → Get all stores  
- `GET /store/{id}` ->Get Store by id
- `Delete /stores/{id}` → Delete store by id
- `POST /items/` → Create a new item
- `GET /items/` → Get all items 
- `GET /stores/{id}` → Get item by id
- `DELETE /stores/{id}` → Delete item by id 

## 🧠 Key Learnings

- Separation of concerns (routers vs CRUD vs models)
- SQLAlchemy ORM fundamentals (engine, session, Base)
- FastAPI dependency injection (`Depends`)
- Request vs Response schema design
- Handling database sessions properly

## 🚧 Future Improvements

- Add items and pricing endpoints
- Implement canonical item matching logic
- Add authentication
- Migrate to PostgreSQL
- Build frontend UI

## ▶️ How to Run

```bash
pip install -r requirements.txt
uvicorn main:app --reload