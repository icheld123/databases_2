# 📚 Reading Platform – Databases II

This project implements the backend database architecture for a digital reading platform inspired by **Bookmate**. It supports books, audiobooks, user activity tracking, social interaction, and content-based recommendations through a hybrid setup using **PostgreSQL** and **MongoDB**.

---

## 📁 Project Structure

├── docs/
│ ├── paper_reading_platform.pdf # Final academic paper
│ ├── report_reading_platform.pdf # Extended technical report
│ ├── presentation_reading_platform.pdf # Slide presentation
│ └── poster_reading_platform.pdf # Academic poster
│
├── src/
│ ├── bookmate_tables.sql # Full PostgreSQL schema
│ ├── countries.sql # SQL to populate 'country' table
│ ├── script.py # Python script to populate PostgreSQL
│ ├── data_to_mongo.py # Python script to populate MongoDB
│ └── Generated data / libros_completo.json # Book content for MongoDB
│
├── README.md # This file


---

## 🎯 Project Objectives

- 📐 Design a normalized relational schema to support:
  - User profiles, books, audiobooks
  - Reading progress, reviews, favorites
  - Social features and content moderation
- 🗃️ Use **PostgreSQL** for structured data and **MongoDB** for unstructured content (e.g., PDF, MP3)
- ⚙️ Provide data generation and testing tools using **Python** and **Faker**
- 🧾 Include academic deliverables: paper, report, poster, and presentation

---

## ⚙️ Technologies Used

| Component     | Tool                        |
|---------------|-----------------------------|
| Relational DB | PostgreSQL 15               |
| NoSQL DB      | MongoDB 8 (mongosh shell)   |
| Scripting     | Python 3 + Faker            |
| Modeling      | Lucidchart (ER diagrams)    |
| Documentation | LaTeX (IEEE template)       |

---

## 🚀 Setup and Execution

### 🧩 PostgreSQL

1. Ensure the UUID extension is enabled:

```sql
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

2. Run schema and insert scripts:
psql -U postgres -d bookmate -f src/create_tables.sql
psql -U postgres -d bookmate -f src/countries.sql
python3 src/generate_inserts_postgres.py

### 🍃 MongoDB
mongosh
use bookmate
mongoimport --db bookmate --collection book_content --file src/libros_completo.json --jsonArray

