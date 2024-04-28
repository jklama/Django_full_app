from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RoomForm
from .models import Room, Topic
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
# Create your views here.
# room=[
#     {'id': 1, 'name': 'lets learn python'},
#     {'id': 2, 'name': 'Design with me '},
#     {'id': 3, 'name': 'Frontend development'},
# ]

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')
            return redirect('login')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Incorrect username or password')
            return redirect('login')
    
        # if user.check_password(password):
        #     request.session['username'] = username
        #     return redirect('home')
        # else:
        #     messages.error(request, 'Incorrect password')
        #     return redirect('login')
    context={'page': page}
    return render(request, 'home/login_register.html',context)
            

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    
    form= UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            messages.success(request, 'Account was created successfully')
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration')
            return redirect('register')

    return render(request, 'home/login_register.html',{'form': form})


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q,) |
        Q(name__icontains = q) | 
        Q(description__icontains = q)
                                 )
    topics = Topic.objects.all()
    room_count = rooms.count()
    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count}
    return render (request, 'home/home.html', context)

def room(request,pk):
    room= Room.objects.get(id=pk)
    context = {'room': room}
    return render(request, 'home/room.html', context)

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home') 
    else:
        form = RoomForm()
    context={'form': form}
    return render(request, 'home/room_form.html', context)

@login_required(login_url='login')
def updateRoom(request,pk):
    room = Room.objects.get(id=pk) 
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('You are not allowed to edit this room')
    
    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = RoomForm(instance=room)
    context={"form": form}
    return render(request, 'home/room_form.html', context)


@login_required(login_url='login')
def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)
    if request.method == "POST":
        room.delete()
        return redirect('home') 
    return render(request, 'home/delete.html', {'obj': room})


