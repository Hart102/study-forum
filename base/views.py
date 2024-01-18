from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages # Helps to display Messages in the frontend(Error Or Success message)
from django.db.models import Q # Used to check if some letters exist in a string
from .models import Room, Topic, Message, User
from .forms import RoomForm, UserForm # Was used in creating dynamic form
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required # Is used tp prevent a user that is not looged in from accessing some pages
from django.contrib.auth.forms import UserCreationForm # Used to generate user registeration form




# Create your views here.

#========= Login route =========
def loginPage (request):
    page = "login"

    # Prevent loggedIn user from viewing the login page
    if request.user.is_authenticated:
        return redirect("home")
    
    if request.method == "POST":
        # Get input values
        username = request.POST.get("username").lower()
        password = request.POST.get("password")

        # Checking if user exists
        try:
            user = User.objects.get(username = username)
        except:
            messages.error(request, "User does not exit")

        user = authenticate(request, username = username, password = password)  # Athenticate user

        
        if user is not None: # If user exists, login user
            login(request, user)  # The login method creates a session in the database and broswer once a user is loggedIn
            return redirect("home")

        else:
            messages.error(request, "User does not exist")

    context = {"page": page}
    return render(request, 'base/login_register.html', context)


#========= Logout route =========
def logoutUser(request):
    logout(request) # Deletes the session on the browser and database
    return redirect("home")


#========= Register route =========
def registerPage (request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False) # Save user info in a momory, so as to access user info for further operations
            user.username = user.username.lower()
            user.save() # Save use to database
            login(request, user) # Log user in to create session
            return redirect("home")
            
        else:
            messages.error(request, "An error occured during registeration")

    context = {"form": form}
    return render(request, "base/login_register.html", context)


#========== Home route ==========
def home (request):
    q = request.GET.get('q') if request.GET.get('q') != None else ""
    # __icontains check for statements that contains some letters of the query string

    rooms = Room.objects.filter( #Search by topic or name or description
        Q(topic__name__icontains = q) |
         Q(name__icontains = q) | 
          Q(description__icontains = q)
    )

    topics = Topic.objects.all()[0:5] # Get all the rooms topic
    rooms_count = rooms.count() # Get total number of rooms
    room_messages = Message.objects.filter(Q(room__topic__name__icontains = q)) # Get all the messages of a room

    context = {'rooms': rooms, 'topics': topics, 'rooms_count': rooms_count, "room_messages": room_messages}
    return render(request, 'base/home.html', context)


# =========Get all Rooms =========
def room (request, pk):
    room = Room.objects.get(id = pk) # Get a particular room from the database is the id

    """ message_set.all(): is a method used to select all the child elements of an object
    message is a child model of the room model, as it was seen in the model.py.
    Here we're selecting all the messages of a particular room """

    # Get all the participants in a room from the database``
    participants = room.participants.all() # Many to many relationship

    room_messages = room.message_set.all()  # .order_by("-created")  Get all the messages of a room from room table in the database


    if request.method == "POST":
        message = Message.objects.create( # Create a message when a user posts a new message
            user = request.user,
            room = room,
            body = request.POST.get("body")
        )

        room.participants.add(request.user) # Add participant to the group were he/she just commnented

        return redirect("room", pk = room.id) # After creating message, Refresh and return user to that exact room

    context = {'room': room, 'room_messages': room_messages, 'participants': participants}
    return render (request, 'base/room.html', context)


#======= User Profile =======
def userProfile (request, pk):
    user = User.objects.get(id = pk) # Get user using the user's Id
    rooms = user.room_set.all() # Get all the rooms associted to a particular user
    room_messages = user.message_set.all() # Get all the messages associted to a particular user (activity)
    topics = Topic.objects.all()

    context = {'user': user, 'rooms': rooms, 'room_messages': room_messages, 'topics': topics}
    return render(request, 'base/profile.html', context)


#======== Create a new Room ========
@login_required(login_url = "login") # Prevent unAuthenticated user from viewing this page
def createRoom (request):
    form = RoomForm()
    topics = Topic.objects.all() # Get all the topics
    
    if request.method == "POST":
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name = topic_name)

        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description')
        )
        return redirect("home")

        # form = RoomForm(request.POST)
        # if form.is_valid(): # Validate form and save form data in the database
        #     room = form.save(commit = False) # Get the instance of this room
        #     room.host = request.user
        #     room.save()

    context = {"form": form, "topics": topics}
    return render(request, 'base/room_form.html', context)


#========== Update a Room ==========
@login_required(login_url = "login") # Prevent unAuthenticated user from viewing this page
def updateRoom (request, pk):
    room = Room.objects.get(id = pk) # Get the room to be edited with it's id
    form = RoomForm(instance = room) # This fills the form with the details of the room to be edited
    topics = Topic.objects.all() # Get all the topics


    # Only allow the owner of the room to update the room
    if request.user != room.host:
        return HttpResponse("You are not allowed here!!")

    if request.method == "POST":
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name = topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()

        return redirect("home")

        # form = RoomForm(request.POST, instance = room) # Selecte the actual room to update
        # if form.is_valid:
        #     form.save()

    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, 'base/room_form.html', context)


#========== Delete Room ==========
@login_required(login_url = "login") # Prevent unAuthenticated user from viewing this page
def deleteRoom (request, pk):
    room = Room.objects.get(id = pk)

    # Only allow the owner of the room to delete the room
    if request.user != room.host:
        return HttpResponse("You are not allowed here!!")

    if request.method == "POST":
        room.delete() # Delete room from the database
        return redirect("home")

    return render(request, 'base/delete.html', {"obj": room})


#========== Delete Message ==========
@login_required(login_url = "login") # Prevent unAuthenticated user from viewing this page
def deleteMessage (request, pk):
    message = Message.objects.get(id = pk)

    # Only allow the owner of the room to delete the room
    if request.user != message.user:
        return HttpResponse("You are not allowed here!!")

    if request.method == "POST":
        message.delete() # Delete room from the database
        return redirect("home")

    return render(request, 'base/delete.html', {"obj": message})


@login_required(login_url = "login")
def updateUser (request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == "POST":
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("user-profile", pk=user.id)
       

    context = {"form": form}
    return render(request, "base/update-user.html", context)


# ==================Moble Screens==================


def topicsPage (request):
    q = request.GET.get('q') if request.GET.get('q') != None else ""
    topics = Topic.objects.filter(name__icontains = q)

    return render(request, "base/topics.html", { "topics": topics })

def activityPage (request):
    room_messages = Message.objects.all()
    return render(request, "base/activity.html", { "room_messages": room_messages })
# NOTE
# In Many-to-Many relationship: .all() is used to get all the related properties of an obect
# In Many-to-One relationship: _set.all() is used to get all the related properties of an object
