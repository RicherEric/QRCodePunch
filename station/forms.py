from django import forms
from .models import Station, Checkpoint

class StationForm(forms.ModelForm):
    class Meta:
        model = Station
        fields = ['name', 'address']

class CheckpointForm(forms.ModelForm):
    class Meta:
        model = Checkpoint
        fields = ['station', 'name']