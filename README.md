# Quizles V1 🎓📝

**Quizles V1** is a Flask-based multi-user quiz management and exam preparation web application. It supports an admin (Quiz Master) who manages subjects, chapters, quizzes, and users, and users who register, attempt quizzes, and track their scores.

---

## 🔑 Features

### 👑 Admin (Quiz Master)
- Admin login with root access (no registration required)
- CRUD operations for:
  - Subjects
  - Chapters (under Subjects)
  - Quizzes (under Chapters)
  - Questions (MCQs with one correct option)
  - Users
- Set quiz date and duration
- Search bar for users, subjects, quizzes (case-insensitive, partial match)
- Summary Charts:
  - 📊 Bar Chart: Branch-wise top scores
  - 🥧 Pie Chart: Branch-wise user attempts

### 🙋‍♂️ User
- User registration and login
- Attempt quizzes based on selected subject and chapter
- View scores after each quiz
- View history of all attempts
- Summary Charts:
  - 📊 Bar Chart: Subjects where top scores were achieved
  - 🥧 Pie Chart: Correct vs Attempted questions

---

## 💻 Tech Stack

| Layer        | Technology      | Reason |
|--------------|------------------|--------|
| Backend      | Flask             | Lightweight Python web framework |
| Templating   | Jinja2            | Flask’s default templating engine |
| Frontend     | HTML, CSS, Bootstrap | Responsive and clean UI |
| Database     | SQLite            | Lightweight DB for local development |
| Charting     | Chart.js (Optional) | Interactive visualizations |
| Form Handling| Flask Forms       | Backend validation for admin forms |

---

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Riddhim-r/Quizles.git
cd Quizles
```

2. **Create a virtual environment:**  
```
python -m venv env
source env/bin/activate # For Linux/Mac
env\Scripts\activate # For Windows
```

3. **Install dependencies:**  
```
pip install -r requirements.txt
```

4. **Run the application:**  
```
python main.py
```

5. **Access the app:**  
Open your browser and navigate to `http://127.0.0.1:5000`. 

---
