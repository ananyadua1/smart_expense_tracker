# 💰 Smart Expense Tracker (Streamlit)

A secure, user-centric expense tracking application built using **Streamlit** that enables users to log expenses safely, visualize spending patterns, and gain actionable financial insights through interactive analytics dashboards.
---

## 🌐 Live Demo

🔗 **App Link:**  
https://smartexpensetracker-ananyadua1.streamlit.app/

---

## 📌 Features

### 🔐 Secure Authentication
- User registration and login
- Passwords stored securely using **bcrypt hashing**
- Session-based access control

### 🧾 Expense Management
- Add expenses with amount, category, date, and description
- User-specific expense storage
- Clean and intuitive UI

### 📊 Analytics Dashboard
- Category-wise spending distribution (pie chart)
- Monthly spending trends (line chart)
- Interactive visualizations using **Plotly**

### 🧠 Smart Insights
- Automatic detection of overspending patterns
- Identification of highest spending categories
- Designed to support better financial decision-making

---

## 🛠 Tech Stack

| Layer | Technology |
|------|------------|
| Frontend | Streamlit |
| Backend | Python |
| Database | SQLite |
| Authentication | bcrypt |
| Data Analysis | Pandas |
| Visualization | Plotly |

---

## 📂 Project Structure

```

smart_expense_tracker/
│
├── app.py              # Main Streamlit application
├── auth.py             # Authentication logic
├── database.py         # Database connection & schema
├── expenses.py         # Expense CRUD operations
├── analytics.py        # Spending insights logic
├── requirements.txt    # Python dependencies
└── expenses.db         # SQLite database (auto-created)

````

---

## 🚀 Getting Started

### 1️⃣ Prerequisites
- Python **3.10+** recommended
- pip installed

Check:
```bash
python --version
python -m pip --version
````

---

### 2️⃣ Clone or Download the Project

```bash
git clone <repository-url>
cd smart_expense_tracker
```

Or download the ZIP and extract it.

---

### 3️⃣ (Recommended) Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

---

### 4️⃣ Install Dependencies

```bash
python -m pip install -r requirements.txt
```

---

### 5️⃣ Run the Application

```bash
python -m streamlit run app.py
```

The app will open in your browser at:

```
http://localhost:8501
```

---

## 🔒 Security Practices Used

* Password hashing using **bcrypt**
* Parameterized SQL queries
* Session-based user authentication
* User-specific data isolation
* No plain-text credential storage

---

## 🧠 How It Works (High-Level)

1. User logs in or registers
2. Expenses are securely stored in a SQLite database
3. Data is processed using Pandas
4. Spending patterns are visualized using interactive charts
5. Smart rules detect overspending trends and provide insights

---

## 📈 Future Enhancements

* Budget setting and alerts
* Machine learning-based expense prediction
* Auto-categorization using NLP
* PDF report generation
* Cloud database integration
* Multi-currency support

---

## 🧑‍💻 Author

**Ananya Dua**
Built as a hands-on project to explore secure data handling, analytics dashboards, and financial decision support systems using Streamlit.

---
Just tell me 👍
```
