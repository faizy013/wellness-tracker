from django.contrib import admin
from .models import WaterLog, ExerciseLog, SleepLog, MoodLog

admin.site.register(WaterLog)
admin.site.register(ExerciseLog)
admin.site.register(SleepLog)
admin.site.register(MoodLog)
