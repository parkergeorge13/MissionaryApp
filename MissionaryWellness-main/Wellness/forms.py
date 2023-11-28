from django import forms
from .models import JournalEntry, Mood

class JournalEntryForm(forms.ModelForm):
    class Meta:
        model = JournalEntry
        fields = ['title', 'content']

class MoodForm(forms.ModelForm):
    class Meta:
        model = Mood
        fields = ['mood']