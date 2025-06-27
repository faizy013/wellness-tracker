from apscheduler.schedulers.background import BackgroundScheduler
from django.core.mail import send_mail
from django.utils import timezone
from django.contrib.auth.models import User
from .models import WaterLog, SleepLog, MoodLog, ExerciseLog

scheduler_started = False

def start_scheduler():
    global scheduler_started
    if scheduler_started:
        return

    scheduler_started = True
    scheduler = BackgroundScheduler()

    def send_reminder_emails():
        now = timezone.now()
        today = now.date()
        now_time = now.strftime('%H:%M')

        users = User.objects.all()
        for user in users:
            # Check all log types
            has_water = WaterLog.objects.filter(user=user, date=today).exists()
            has_sleep = SleepLog.objects.filter(user=user, start_time__date=today).exists()
            has_mood = MoodLog.objects.filter(user=user, date=today).exists()
            has_exercise = ExerciseLog.objects.filter(user=user, date=today).exists()

            if not (has_water or has_sleep or has_mood or has_exercise):
                send_mail(
                    '🧘‍♀️ Daily Wellness Reminder',
                    f'Hi { user.first_name } { user.last_name }, don’t forget to log your wellness activities today!',
                    'noreply@wellnesstracker.com',
                    [user.email],
                    fail_silently=True,
                )
                print(f"📧 Reminder sent to {user.username} at {now_time}")

    scheduler.add_job(send_reminder_emails, 'cron', hour='15,20', minute=11)
    scheduler.start()
    print("🕒 Daily reminder scheduler running...")
