from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import JournalEntry, Mood
from .forms import JournalEntryForm, MoodForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime

# Create your views here.
@login_required
def index(request):
    context = {"title":"Called To Thrive"}
    user = request.user

    if request.method == 'POST':
        form = MoodForm(request.POST)
        if form.is_valid():
            mood = form.cleaned_data['mood']
            Mood.objects.update_or_create(
                user=user,
                date=datetime.now().date(),
                defaults={'mood': mood}
            )
    else:
        form = MoodForm()
    moods_list = ["Green","Yellow","Orange","Red"]
    mood_history = Mood.objects.filter(user=user).order_by('-date')[:7]
    converted_moods = []
    for i in mood_history:
        i.mood_string = moods_list[i.mood]
    return render(request, 'wellness/index.html', {'form': form, 'mood_history': mood_history, "title":"Called To Thrive"})


def custom_login(request, user=None):
    context = {"title":"Login"}
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('index')  # Redirect to your home page or another desired page
    else:
        form = AuthenticationForm()
    return render(request, 'wellness/login.html', {'form': form, 'title':'Login'})

def register(request):
    context = {"title":"Register"}
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')  # Redirect to your home page or another desired page
    else:
        form = UserCreationForm()
    return render(request, 'wellness/register.html', {'form': form,'title':'Register'})

def custom_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')

@login_required
def journal_entry(request, entry_id=None):
    context = {"title":"Called To Thrive"}
    user = request.user
    entries_list = JournalEntry.objects.filter(user=user).order_by('-created_at')
    paginator = Paginator(entries_list, 5)  # Show 5 entries per page

    page = request.GET.get('page')
    try:
        entries = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page.
        entries = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver the last page of results.
        entries = paginator.page(paginator.num_pages)

    selected_entry = None

    if entry_id:
        selected_entry = get_object_or_404(JournalEntry, id=entry_id, user=user)

    if request.method == 'POST':
        form = JournalEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = user
            entry.save()
            return redirect('journal')
    else:
        form = JournalEntryForm(initial={'title': selected_entry.title if selected_entry else '',
                                         'content': selected_entry.content if selected_entry else ''})

    return render(request, 'wellness/journal_entry.html', {'entries': entries, 'selected_entry': selected_entry, 'form': form, 'title':'Called To Thrive'})

@login_required
def resources(request):
    return render(request, 'wellness/resources.html')