from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone



class WellnessLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    activity_type = models.CharField(max_length=100)
    value = models.CharField(max_length=100)

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    level = models.CharField(max_length=20, default='info') 
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)



class WaterLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount_ml = models.PositiveIntegerField()
    date = models.DateField(default=timezone.now)
    timestamp = models.DateTimeField(default=timezone.now)

    @property
    def search_text(self):
        return f"Water {self.user.username} - {self.amount_ml}ml on {self.date}"

    def __str__(self):
        return f"{self.user.username} - {self.amount_ml}ml on {self.date}"

class ExerciseLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()  # Remove auto_now_add if you want manual input
    type = models.CharField(max_length=100)
    duration_minutes = models.IntegerField()
    notes = models.TextField(blank=True, null=True)  # optional notes

    @property
    def search_text(self):
        return f" Exercise {self.user.username} - {self.type} for {self.duration_minutes} min"

    def __str__(self):
        return f"{self.user.username} - {self.type} for {self.duration_minutes} min"


class SleepLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    @property
    def search_text(self):
        # No notes, so just format start/end time as string
        return f"Sleep {self.user.username} - Sleep from {self.start_time} to {self.end_time}"
    def __str__(self):
        return f"{self.user.username} - Sleep from {self.start_time} to {self.end_time}"

class MoodLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    mood = models.CharField(max_length=50)
    note = models.TextField(blank=True, null=True)

    @property
    def search_text(self):
        return f"{self.user.username} - Mood: {self.mood} on {self.date}"

    def __str__(self):
        return f"{self.user.username} - Mood: {self.mood} on {self.date}"
