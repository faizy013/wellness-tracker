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
# import pytz
from django.utils.timezone import make_aware, is_aware, get_current_timezone


@login_required
def dashboard_view(request):
    today = date.today()
    week_ago = today - timedelta(days=6)

    water_logs = WaterLog.objects.filter(user=request.user, date__range=[week_ago, today])
    exercise_logs = ExerciseLog.objects.filter(user=request.user, date__range=[week_ago, today])
    sleep_logs = SleepLog.objects.filter(user=request.user, start_time__date__range=[week_ago, today])
    mood_logs = MoodLog.objects.filter(user=request.user, date__range=[week_ago, today])

    # 👇 NEW: Check if user hasn't logged anything today
    has_logs_today = (
        WaterLog.objects.filter(user=request.user, date=today).exists() or
        ExerciseLog.objects.filter(user=request.user, date=today).exists() or
        SleepLog.objects.filter(user=request.user, start_time__date=today).exists() or
        MoodLog.objects.filter(user=request.user, date=today).exists()
    )
    if not has_logs_today:
        messages.warning(request, "👋 Don't forget to log your wellness activities today!")

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

    # Get filters
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    activity_type = request.GET.get('activity_type')
    search_term = request.GET.get('search_term', '').strip()

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

    # Filter by activity type and search term
    if activity_type:
        if activity_type == 'water':
            filtered_logs = water_logs.order_by('-date')
        elif activity_type == 'exercise':
            filtered_logs = (exercise_logs.filter(type__icontains=search_term).order_by('-date')
                             if search_term else exercise_logs.order_by('-date'))
        elif activity_type == 'sleep':
            filtered_logs = sleep_logs.order_by('-start_time')
        elif activity_type == 'mood':
            filtered_logs = (mood_logs.filter(Q(mood__icontains=search_term) | Q(note__icontains=search_term)).order_by('-date')
                             if search_term else mood_logs.order_by('-date'))
        else:
            filtered_logs = []
        # Add model_name attr for filtered logs so template knows the type
        for log in filtered_logs:
            log.model_name = log.__class__.__name__
    else:
        # Combine all logs and add model_name attribute
        combined_logs = list(water_logs) + list(exercise_logs) + list(sleep_logs) + list(mood_logs)
        for log in combined_logs:
            log.model_name = log.__class__.__name__

        # Sorting helper: convert date to datetime for consistent comparison
        def sort_key(log):
            dt = getattr(log, 'date', None)
            if dt is None:
                dt = getattr(log, 'start_time', None)

            if dt is None:
                return datetime.min.replace(tzinfo=get_current_timezone())  # fallback

            if isinstance(dt, datetime):
                if not is_aware(dt):
                    # make naive datetime aware in current timezone
                    return make_aware(dt, get_current_timezone())
                return dt

            # dt is a date object, make aware datetime with time.min
            aware_dt = datetime.combine(dt, time.min)
            return make_aware(aware_dt, get_current_timezone())

        combined_logs.sort(key=sort_key, reverse=True)
        filtered_logs = combined_logs

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

# @login_required
# def view_logs(request):
#     user = request.user

#     # Get filter params from GET request
#     start_date = request.GET.get('start_date')
#     end_date = request.GET.get('end_date')
#     activity_type = request.GET.get('activity_type')
#     search_term = request.GET.get('search_term', '').strip()

#     is_filtered = start_date or end_date or activity_type or search_term

#     water_logs = WaterLog.objects.filter(user=user)
#     exercise_logs = ExerciseLog.objects.filter(user=user)
#     sleep_logs = SleepLog.objects.filter(user=user)
#     mood_logs = MoodLog.objects.filter(user=user)

#     if is_filtered:
#         if start_date:
#             water_logs = water_logs.filter(date__gte=start_date)
#             exercise_logs = exercise_logs.filter(date__gte=start_date)
#             sleep_logs = sleep_logs.filter(start_time__date__gte=start_date)
#             mood_logs = mood_logs.filter(date__gte=start_date)

#         if end_date:
#             water_logs = water_logs.filter(date__lte=end_date)
#             exercise_logs = exercise_logs.filter(date__lte=end_date)
#             sleep_logs = sleep_logs.filter(start_time__date__lte=end_date)
#             mood_logs = mood_logs.filter(date__lte=end_date)

#         if activity_type == 'water':
#             filtered_logs = water_logs.order_by('-date')
#         elif activity_type == 'exercise':
#             filtered_logs = exercise_logs.order_by('-date')
#             if search_term:
#                 filtered_logs = filtered_logs.filter(type__icontains=search_term)
#         elif activity_type == 'sleep':
#             filtered_logs = sleep_logs.order_by('-start_time')
#         elif activity_type == 'mood':
#             filtered_logs = mood_logs.order_by('-date')
#             if search_term:
#                 filtered_logs = filtered_logs.filter(
#                     Q(mood__icontains=search_term) | Q(note__icontains=search_term)
#                 )
#         else:
#             filtered_logs = []
#     else:
#         # No filters used: show all logs together (default view)
#         combined_logs = list(water_logs) + list(exercise_logs) + list(sleep_logs) + list(mood_logs)
#         combined_logs.sort(key=lambda log: getattr(log, 'date', getattr(log, 'start_time', date.min)), reverse=True)
#         filtered_logs = combined_logs

#     # Pagination
#     paginator = Paginator(filtered_logs, 10)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)

#     context = {
#         'page_obj': page_obj,
#         'start_date': start_date,
#         'end_date': end_date,
#         'activity_type': activity_type,
#         'search_term': search_term,
#     }
#     return render(request, 'tracker/view_logs.html', context)


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
        form = UserCreationForm()
    return render(request, 'tracker/signup.html', {'form': form})




@login_required
def dashboard_view(request):
    return render(request, 'tracker/dashboard.html')
