# 🌿 Wellness Tracker

A full-featured Django web application to help users track their daily wellness activities — water intake, exercise, sleep, and mood — with automated reminders and interactive charts.

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=flat&logo=django&logoColor=white)
![Celery](https://img.shields.io/badge/Celery-37814A?style=flat&logo=celery&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=flat&logo=redis&logoColor=white)

---

## ✨ Features

- 💧 **Water Intake Tracker** — log daily water consumption
- 🏋️ **Exercise Logger** — record workout sessions
- 😴 **Sleep Tracker** — monitor sleep hours and quality
- 😊 **Mood Logger** — track daily mood patterns
- 📊 **Interactive Charts** — visualize progress via Chart.js (line, bar, pie, doughnut, radar)
- 🔔 **Browser Push Notifications** — real-time alerts via WebPush (VAPID)
- 📧 **Automated Email Reminders** — twice-daily reminders (8 AM & 8 PM) via APScheduler
- 🎨 **Custom Green UI Theme** — clean wellness-focused design

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django |
| Async Tasks | Celery + Redis |
| Scheduling | APScheduler |
| Push Notifications | django-webpush (VAPID) |
| Charts | Chart.js |
| Frontend | HTML, CSS, JavaScript |

---

## ⚙️ Installation & Setup

**1. Clone the repository**
```bash
git clone https://github.com/faizy013/wellness-tracker.git
cd wellness-tracker
```

**2. Create and activate a virtual environment**
```bash
# Linux / macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Run database migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

**5. Start the development server**
```bash
python manage.py runserver
```

Visit: `http://127.0.0.1:8000`

---

## 🔔 Push Notifications Setup (WebPush + VAPID)

```bash
pip install django-webpush pywebpush cryptography
python manage.py migrate webpush
```

Generate your VAPID keys and add them to `settings.py`.

---

## 📧 Email Reminder System

Reminders are sent automatically at **8:00 AM** and **8:00 PM** to users who haven't logged any activity that day.

Scheduler auto-starts with the server via `tracker/apps.py`:

```python
def ready(self):
    if 'runserver' in sys.argv:
        from tracker.scheduler import start_scheduler
        start_scheduler()
```

---

## 📁 Project Structure

```
wellness-tracker/
├── tracker/              # Main app (models, views, scheduler)
├── wellness_tracker/     # Django project settings
├── manage.py
├── requirements.txt
└── README.md
```

---

## 🤝 Author

**Muhammad Umar Farooq**
[GitHub](https://github.com/faizy013) · [LinkedIn](https://linkedin.com/in/YOUR-LINKEDIN)
