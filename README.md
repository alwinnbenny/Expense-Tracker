# Smart Expense Tracker

A modern, feature-rich expense management and analytics web application built with a Django REST API, a MySQL database, and a React.js (Vite) frontend.

It includes advanced features like:
- **CRUD Operations**: Log, view, edit, and delete expenses.
- **Daily Spending Limit**: Custom limits with warnings when spending is exceeded.
- **Suspicious Activity Detection**: Automatically flags expenses that exceed 5x the average spending in their category.
- **Visual Analytics**: Interactive charts using Recharts for monthly spending trends, category breakdowns, and limits.

---

## Project Structure

```
Expense Tracker/
├── backend/            # Django REST API (Python 3)
│   ├── backend/        # Configuration and settings
│   ├── expenses/       # Core app logic, models, views, and business logic
│   └── manage.py
├── frontend/           # React.js SPA (Vite + Javascript)
│   ├── src/            # Components, pages, and design system
│   ├── package.json
│   └── vite.config.js
└── README.md
```

---

## Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+
- MySQL Server (running locally on port 3306)

---

### Backend Setup (Django)

1. **Navigate to backend folder**:
   ```bash
   cd backend
   ```

2. **Install requirements**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Database**:
   Update `backend/.env` with your MySQL database configurations:
   ```env
   DB_NAME=expense_tracker
   DB_USER=root
   DB_PASSWORD=your_password
   DB_HOST=127.0.0.1
   DB_PORT=3306
   ```

4. **Create the database**:
   Make sure you create the `expense_tracker` database in MySQL.

5. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

6. **Seed sample data (Optional)**:
   ```bash
   python seed_data.py
   ```

7. **Start the Django server**:
   ```bash
   python manage.py runserver
   ```
   The backend API will run on `http://localhost:8000/`.

---

### Frontend Setup (React)

1. **Navigate to frontend folder**:
   ```bash
   cd ../frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start development server**:
   ```bash
   npm run dev
   ```
   The frontend application will run on `http://localhost:5173/`.
