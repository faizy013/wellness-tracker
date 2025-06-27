================================================================================
                              🌿 WELLNESS TRACKER
================================================================================

A simple Django-based web application to help users track their daily wellness 
activities like 💧 Water Intake, 🏋️ Exercise, 😴 Sleep, and 😊 Mood.

Built with 💚 using:
- Django
- Chart.js
- Celery + Redis
- Push Notifications via VAPID
- Custom green UI theme: #004526, #006241, #2E8B57, #00674b

--------------------------------------------------------------------------------
📦 INSTALLATION & SETUP
--------------------------------------------------------------------------------

Step 1: Clone the project and navigate to the directory  
git clone https://github.com/faizy013/wellness-tracker.git
cd wellness_tracker

Step 2: Create and activate a virtual environment  

**On Linux/macOS:**
python3 -m venv venv
source venv/bin/activate

**On Windows:**
python -m venv venv
venv\Scripts\activate


Step 3: Install all dependencies
pip install -r requirements.txt


--------------------------------------------------------------------------------
⚙️ DATABASE MIGRATIONS
--------------------------------------------------------------------------------

Run the following commands:

python manage.py makemigrations
python manage.py migrate


--------------------------------------------------------------------------------
🚀 RUN THE APPLICATION
--------------------------------------------------------------------------------

Start the Django development server

**Linux/macOS:**
source venv/bin/activate
python manage.py runserver

**Windows:**
venv\Scripts\activate
python manage.py runserver


Visit: `http://127.0.0.1:8000`

--------------------------------------------------------------------------------
🔔 PUSH NOTIFICATIONS SETUP (WebPush + VAPID)
--------------------------------------------------------------------------------

1. Install WebPush-related libraries:
pip install django-webpush pywebpush cryptography


2. Run migration for webpush:

python manage.py migrate webpush



Note:

If you don’t have a `requirements.txt`, use:
pip install django
pip install django-webpush pywebpush cryptography
pip install celery django-celery-beat

--------------------------------------------------------------------------------
📧 DAILY EMAIL REMINDER SYSTEM (APScheduler)
--------------------------------------------------------------------------------

Automatically reminds users twice a day via email to log their wellness activity.

⏰ Schedule:
- 08:00 AM
- 08:00 PM

🔁 Logic:
- For each user, check if they’ve logged any of these today:
  💧 WaterLog, 🏋️ ExerciseLog, 😴 SleepLog, 😊 MoodLog
- If not → send them an email reminder

🛠 Libraries used:
pip install apscheduler

📂 Main File:
tracker/scheduler.py

👁 Inside scheduler.py:
- Uses `BackgroundScheduler` from APScheduler
- Imports Django models
- Sends email using `send_mail()` from Django

📄 In `tracker/apps.py`:
Auto-start scheduler when server starts:

```python
def ready(self):
    if 'runserver' in sys.argv:
        from tracker.scheduler import start_scheduler
        start_scheduler()




EXTRAS:


📊 SUPPORTED CHART TYPES (Chart.js)

📈 line

📊 bar

🥧 pie

🍩 doughnut

📉 radar

🎯 polarArea

💠 bubble

🔵 scatter

Note: horizontalBar is deprecated in Chart.js v3+, use bar with indexAxis: 'y'

💚 UI THEME COLORS

#004526
#006241
#2E8B57
#00674b


| Use Case         | Color Code | Description                |
| ---------------- | ---------- | -------------------------- |
| Button (primary) | `#ff6f61`  | Coral pink                 |
| Button hover     | `#e63946`  | Deeper coral               |
| Title headings   | `#d63384`  | Bright pink / magenta tint |
| Input border     | `#ff8c94`  | Soft pink border           |
| Secondary button | `#6a5acd`  | Lavender purple            |
| Secondary hover  | `#483d8b`  | Deep lavender              |
| Highlights       | `#20c997`  | Minty sea green            |
| Warnings/alerts  | `#ffa500`  | Orange                     |
