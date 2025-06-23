from django.db import models
from django.contrib.auth.models import User

class WaterLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    amount_ml = models.IntegerField()

    def __str__(self):
        return f"{self.user.username} - {self.amount_ml}ml on {self.date}"

class ExerciseLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()  # Remove auto_now_add if you want manual input
    type = models.CharField(max_length=100)
    duration_minutes = models.IntegerField()
    notes = models.TextField(blank=True, null=True)  # optional notes

    def __str__(self):
        return f"{self.user.username} - {self.type} for {self.duration_minutes} min"


class SleepLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f"{self.user.username} - Sleep from {self.start_time} to {self.end_time}"

class MoodLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    mood = models.CharField(max_length=50)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - Mood: {self.mood} on {self.date}"
