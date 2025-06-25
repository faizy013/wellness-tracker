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
