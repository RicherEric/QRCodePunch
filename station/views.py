from django.shortcuts import render, get_object_or_404
from .models import Station, Checkpoint, Checkin
from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponse

class CustomLoginView(LoginView):
    template_name = 'login.html'
    next_page = reverse_lazy('home')

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('home')

def home(request):
    return render(request, 'home.html')

def station_list(request):
    stations = Station.objects.all()
    return render(request, 'station/list.html', {'stations': stations})

def station_detail(request, pk):
    station = get_object_or_404(Station, pk=pk)
    checkpoints = station.checkpoint_set.all()
    return render(request, 'station/detail.html', {'station': station, 'checkpoints': checkpoints})

from django.shortcuts import render, redirect
from .forms import StationForm, CheckpointForm

def add_station(request):
    if request.method == 'POST':
        form = StationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('station_list')  # Redirect to the list of stations
    else:
        form = StationForm()
    return render(request, 'station/add_station.html', {'form': form})

def add_checkpoint(request):
    if request.method == 'POST':
        form = CheckpointForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('station_list')  # Adjust the redirect as needed
    else:
        form = CheckpointForm()
    return render(request, 'station/add_checkpoint.html', {'form': form})

def delete_station(request, pk):
    station = get_object_or_404(Station, pk=pk)
    station.delete()
    return HttpResponseRedirect(reverse('station_list'))

def delete_checkpoint(request, pk):
    checkpoint = get_object_or_404(Checkpoint, pk=pk)
    checkpoint.delete()
    return HttpResponseRedirect(reverse('station_list'))

def scan_qrcode(request, checkpoint_id):
    checkpoint = get_object_or_404(Checkpoint, pk=checkpoint_id)
    Checkin.objects.create(checkpoint=checkpoint)
    return HttpResponse("打卡成功")