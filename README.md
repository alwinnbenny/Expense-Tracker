# 💸 Smart Expense Tracker

A modern, full-stack expense management and analytics web application built with a **Django REST API** backend, **MySQL** database, and a **React.js + Vite** frontend.

---

## ✨ Features

- **📋 Expense Management** — Log, view, edit, and delete expenses with amount, category, date, and description
- **🚨 Suspicious Activity Detection** — Automatically flags expenses that exceed 5× the average spending in their category
- **📅 Daily Spending Limit** — Set a custom daily budget with real-time warnings when exceeded
- **📊 Visual Analytics** — Interactive charts (monthly trends, category breakdowns, daily spending) powered by Recharts
- **🔗 RESTful API** — Clean Django REST Framework API with full CRUD support

---

## 🛠 Tech Stack

| Layer     | Technology                              |
|-----------|-----------------------------------------|
| Frontend  | React 18, Vite, React Router, Recharts  |
| Backend   | Django 5, Django REST Framework         |
| Database  | MySQL                                   |
| HTTP      | Axios                                   |
| Config    | python-decouple, django-cors-headers    |

---

## 📁 Project Structure

```
Expense Tracker/
├── backend/                    # Django REST API
│   ├── backend/                # Project settings, URLs, WSGI
│   │   ├── settings.py
│   │   └── urls.py
│   ├── expenses/               # Core app
│   │   ├── models.py           # Expense & AppSettings models
│   │   ├── views.py            # API ViewSets
│   │   ├── serializers.py
│   │   ├── business_logic.py   # Suspicious activity detection
│   │   └── urls.py
│   ├── manage.py
│   ├── seed_data.py            # Optional sample data seeder
│   └── requirements.txt
├── frontend/                   # React + Vite SPA
│   ├── src/
│   │   ├── pages/              # Dashboard, Expenses, Analytics
│   │   ├── components/         # Sidebar, StatCard, ExpenseForm, etc.
│   │   ├── api/                # Axios API calls
│   │   └── main.jsx
│   ├── index.html
│   └── package.json
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- **Python** 3.11+
- **Node.js** 18+
- **MySQL** server running locally on port 3306

---

### 🐍 Backend Setup (Django)

1. **Navigate to the backend folder:**
   ```bash
   cd backend
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create the MySQL database:**
   ```sql
   CREATE DATABASE expense_tracker;
   ```

5. **Configure environment variables:**
   Create a `.env` file inside the `backend/` folder:
   ```env
   DB_NAME=expense_tracker
   DB_USER=root
   DB_PASSWORD=your_mysql_password
   DB_HOST=127.0.0.1
   DB_PORT=3306
   SECRET_KEY=your_django_secret_key
   DEBUG=True
   ```

6. **Run database migrations:**
   ```bash
   python manage.py migrate
   ```

7. **(Optional) Seed sample data:**
   ```bash
   python seed_data.py
   ```

8. **Start the Django development server:**
   ```bash
   python manage.py runserver
   ```
   > API available at `http://localhost:8000/api/`

---

### ⚛️ Frontend Setup (React)

1. **Navigate to the frontend folder:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm run dev
   ```
   > App available at `http://localhost:5173/`

---

## 📡 API Endpoints

Base URL: `http://localhost:8000/api/`

| Method   | Endpoint               | Description                     |
|----------|------------------------|---------------------------------|
| `GET`    | `/expenses/`           | List all expenses                |
| `POST`   | `/expenses/`           | Create a new expense             |
| `GET`    | `/expenses/{id}/`      | Retrieve a specific expense      |
| `PUT`    | `/expenses/{id}/`      | Update an expense                |
| `DELETE` | `/expenses/{id}/`      | Delete an expense                |
| `GET`    | `/settings/`           | Get app settings (daily limit)   |
| `PUT`    | `/settings/{id}/`      | Update app settings              |

---

## 🧠 Business Logic

### Suspicious Activity Detection
An expense is automatically flagged as **suspicious** when its amount exceeds **5× the average** of all previous expenses in the same category. The reason is stored alongside the expense for transparency.

### Daily Spending Limit
A configurable daily spending limit is stored in the `AppSettings` singleton. The frontend displays a warning banner on the Dashboard when today's total spending exceeds this limit.

---

## 📸 Pages

| Page        | Description                                                         |
|-------------|---------------------------------------------------------------------|
| **Dashboard**  | Overview stats, recent expenses, and daily limit status          |
| **Expenses**   | Full expense table with add, edit, delete, and suspicious badges |
| **Analytics**  | Monthly trends, category pie chart, and daily spending bar chart |

---

## 🔒 Environment Variables

The `backend/.env` file is excluded from version control via `.gitignore`. Never commit secrets to the repository.

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
