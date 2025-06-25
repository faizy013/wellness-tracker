from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import WaterLogForm, ExerciseLogForm, SleepLogForm, MoodLogForm
from datetime import timedelta, date
from django.utils.timezone import now
from django.db.models import Sum
from django.contrib import messages
from .models import WaterLog, ExerciseLog, SleepLog, MoodLog
from django.db.models import Q
from django.core.paginator import Paginator
from datetime import datetime, time
from .forms import SignUpForm 
# import pytz
from django.utils.timezone import make_aware, is_aware, get_current_timezone
from datetime import datetime
def filter_by_search(queryset, search_term):
    if not search_term:
        return queryset
    search_term = search_term.lower()
    return [obj for obj in queryset if search_term in obj.search_text.lower()]




@login_required
def dashboard_view(request):
    today = date.today()
    week_ago = today - timedelta(days=6)

    water_logs = WaterLog.objects.filter(user=request.user, date__range=[week_ago, today])
    exercise_logs = ExerciseLog.objects.filter(user=request.user, date__range=[week_ago, today])
    sleep_logs = SleepLog.objects.filter(user=request.user, start_time__date__range=[week_ago, today])
    mood_logs = MoodLog.objects.filter(user=request.user, date__range=[week_ago, today])

    # 👇 NEW: Check if user hasn't logged anything today
    missing_logs = []

    if not WaterLog.objects.filter(user=request.user, date=today).exists():
        missing_logs.append("💧 water")
    if not ExerciseLog.objects.filter(user=request.user, date=today).exists():
        missing_logs.append("🏋️ exercise")
    if not SleepLog.objects.filter(user=request.user, start_time__date=today).exists():
        missing_logs.append("😴 sleep")
    if not MoodLog.objects.filter(user=request.user, date=today).exists():
        missing_logs.append("😊 mood")

    # Only show once per day
    if missing_logs and request.session.get('reminder_shown') != str(today):
        msg = "👋 You haven't logged your " + ", ".join(missing_logs) + " today!"
        messages.warning(request, msg)
        request.session['reminder_shown'] = str(today)


    # Weekly Data Prep
    dates = [(week_ago + timedelta(days=i)) for i in range(7)]

    water_data = []
    exercise_data = []
    sleep_data = []
    mood_data = []

    for d in dates:
        water = water_logs.filter(date=d).aggregate(Sum('amount_ml'))['amount_ml__sum'] or 0
        exercise = exercise_logs.filter(date=d).aggregate(Sum('duration_minutes'))['duration_minutes__sum'] or 0

        sleep_entries = sleep_logs.filter(start_time__date=d)
        total_sleep_hours = sum([(s.end_time - s.start_time).total_seconds() / 3600 for s in sleep_entries])

        moods = list(mood_logs.filter(date=d).values_list('mood', flat=True))
        mood_data.append(", ".join(moods) if moods else "No Entry")

        water_data.append(water)
        exercise_data.append(exercise)
        sleep_data.append(round(total_sleep_hours, 1))

    context = {
        'dates': [d.strftime("%b %d") for d in dates],
        'water_data': water_data,
        'exercise_data': exercise_data,
        'sleep_data': sleep_data,
        'mood_data': mood_data,
    }

    return render(request, 'tracker/dashboard.html', context)

@login_required
def view_logs(request):
    user = request.user

    # Filters from GET
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    activity_type = request.GET.get('activity_type')
    search_term = request.GET.get('search_term', '').strip()

    # Base querysets
    water_logs = WaterLog.objects.filter(user=user)
    exercise_logs = ExerciseLog.objects.filter(user=user)
    sleep_logs = SleepLog.objects.filter(user=user)
    mood_logs = MoodLog.objects.filter(user=user)

    # Apply date filters
    if start_date:
        water_logs = water_logs.filter(date__gte=start_date)
        exercise_logs = exercise_logs.filter(date__gte=start_date)
        sleep_logs = sleep_logs.filter(start_time__date__gte=start_date)
        mood_logs = mood_logs.filter(date__gte=start_date)

    if end_date:
        water_logs = water_logs.filter(date__lte=end_date)
        exercise_logs = exercise_logs.filter(date__lte=end_date)
        sleep_logs = sleep_logs.filter(start_time__date__lte=end_date)
        mood_logs = mood_logs.filter(date__lte=end_date)

    # Filter by activity_type if specified
    if activity_type:
        if activity_type == 'water':
            filtered_logs = water_logs
        elif activity_type == 'exercise':
            filtered_logs = exercise_logs
        elif activity_type == 'sleep':
            filtered_logs = sleep_logs
        elif activity_type == 'mood':
            filtered_logs = mood_logs
        else:
            filtered_logs = []

        # Apply search filtering in Python for that queryset
        filtered_logs = filter_by_search(filtered_logs, search_term)

    else:
        # No activity type selected: combine all and filter by search
        combined_logs = list(water_logs) + list(exercise_logs) + list(sleep_logs) + list(mood_logs)
        filtered_logs = [log for log in combined_logs if search_term.lower() in log.search_text.lower()] if search_term else combined_logs

    # Add model_name for template
    for log in filtered_logs:
        log.model_name = log.__class__.__name__

    # Sort logs by date/time
    def sort_key(log):
        dt = getattr(log, 'date', None)
        if dt is None:
            dt = getattr(log, 'start_time', None)

        if dt is None:
            return datetime.min.replace(tzinfo=get_current_timezone())

        if isinstance(dt, datetime):
            if not is_aware(dt):
                return make_aware(dt, get_current_timezone())
            return dt

        aware_dt = datetime.combine(dt, time.min)
        return make_aware(aware_dt, get_current_timezone())

    filtered_logs.sort(key=sort_key, reverse=True)

    # Pagination
    paginator = Paginator(filtered_logs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'start_date': start_date,
        'end_date': end_date,
        'activity_type': activity_type,
        'search_term': search_term,
    }

    return render(request, 'tracker/view_logs.html', context)


@login_required
def add_water_log(request):
    if request.method == 'POST':
        form = WaterLogForm(request.POST)
        if form.is_valid():
            water_log = form.save(commit=False)
            water_log.user = request.user
            water_log.save()
            return redirect('dashboard')
    else:
        form = WaterLogForm()
    return render(request, 'tracker/add_water_log.html', {'form': form})

@login_required
def add_exercise_log(request):
    if request.method == 'POST':
        form = ExerciseLogForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.user = request.user
            log.save()
            return redirect('dashboard')
    else:
        form = ExerciseLogForm()
    return render(request, 'tracker/add_exercise_log.html', {'form': form})

@login_required
def add_sleep_log(request):
    if request.method == 'POST':
        form = SleepLogForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.user = request.user
            log.save()
            return redirect('dashboard')
    else:
        form = SleepLogForm()
    return render(request, 'tracker/add_sleep_log.html', {'form': form})

@login_required
def add_mood_log(request):
    if request.method == 'POST':
        form = MoodLogForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.user = request.user
            log.save()
            return redirect('dashboard')
    else:
        form = MoodLogForm()
    return render(request, 'tracker/add_mood_log.html', {'form': form})


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'tracker/signup.html', {'form': form})



