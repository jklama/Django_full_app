from django.shortcuts import render

# Create your views here.
room=[
    {'id': 1, 'name': 'lets learn python'},
    {'id': 2, 'name': 'Design with me '},
    {'id': 3, 'name': 'Frontend development'},
]
def home(request):
    context = {'rooms': room}
    return render (request, 'home/home.html', context)

def Room(request,pk):
    rooms = None
    for i in room:
        if i['id'] == int(pk):
            rooms = i
    context = {'room': rooms}
    return render(request, 'home/room.html', context)