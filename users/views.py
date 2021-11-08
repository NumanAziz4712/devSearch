from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .form import CustomUserCreationForm, MessageForm, ProfileForm, SkillsForm
from django.contrib.auth.decorators import login_required
from users.models import Profiles, Skills
from .utils import profilesPaginations, searchProfiles
from .models import Message
# login
def loginUser(request):
    page ='register'
    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'user doe not exist')
        
        # this return the instance of a user if the pass and username are correct. and return None otherwise.
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.error(request, 'You are no logged in')
            return redirect(request.GET.get('next') if 'next' in request.GET else 'account')

        else:
            messages.error(request, 'username or password is not correct')

    return render(request, 'users/login_register.html')


# signup user
def registerUser(request):
    page ='register'
    form = CustomUserCreationForm()
    if request.method =='POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username= user.username.lower()
            user.save()
            messages.success(request, 'Account was created')

            login(request, user)
            return redirect('edit-account')
        else:
            messages.error(request, 'An error occured during registration')


    context ={
        'page':page,
        'form':form,
    }
    return render(request, 'users/login_register.html', context)

# logout
def logoutUser(request):
    logout(request)
    messages.success(request, 'username or password is not correct')
    return redirect('login')


# profiles

def profiles(request):
    profiles, search_query = searchProfiles(request)
    custome_range, profiles = profilesPaginations(request, profiles, 6)
    context = {
        'profiles':profiles,
        'search_query':search_query,
        'custome_range':custome_range,
    }

    return render(request, 'users/profiles.html', context)


def userProfile(request, pk):
    profile = Profiles.objects.get(id=pk)
    topSkills = profile.skills_set.exclude(description__exact="")
    otherSkills = profile.skills_set.filter(description='')
    context ={
        'profile':profile,
        'topSkills':topSkills,
        'otherSkills':otherSkills,
    }

    return render(request, 'users/user-profile.html', context)

# user page
def userAccount(request):
    profile = request.user.profiles
    context ={
        'profile':profile,
    }
    return render(request, 'users/account.html', context)


# edit account
@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profiles
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account was updated successfully')
            return redirect('profiles')
    context ={
        'form':form,
    }
    return render(request, 'users/profile_form.html', context)

# skillform view
@login_required(login_url='login')
def addSkills(request):
    form = SkillsForm()
    if request.method == 'POST':
        form = SkillsForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = request.user.profiles
            skill.save()
            return redirect('account')
    context = {
        'form':form,
    }
    return render(request, 'users/add_skills.html', context)

# update skills 
@login_required(login_url='login')
def updateSkills(request, pk):
    skill = request.user.profiles.skills_set.get(id=pk)
    form = SkillsForm(instance=skill)
    if request.method == 'POST':
        form = SkillsForm(request.POST, instance=skill)
        if form.is_valid():
            # skill = form.save(commit=False)
            # skill.owner = request.user.profiles
            # skill.save()
            form.save()
            return redirect('account')
    context = {
        'form':form,
    }
    return render(request, 'users/add_skills.html', context)

# delete skills
def deleteSkills(request, pk):
    skill = request.user.profiles.skills_set.get(id=pk)
    if request.method == 'POST':
        skill.delete()
        return redirect('account')
    context = {
        'item':skill,
    }
    return render(request, 'delete_project.html', context)


# inbox
@login_required(login_url='login')
def inbox(request):
    profile = request.user.profiles
    msgRequest = profile.messages.all()
    unreadCount = msgRequest.filter(is_read=False).count()

    context = {
        'msgRequest':msgRequest,
        'unreadCount':unreadCount,
    }
    return render(request, 'users/inbox.html', context)

# messages
@login_required(login_url='login')
def message(request, pk):
    
    unreadMsg = request.user.profiles.messages.get(id=pk)
    if unreadMsg.is_read == False:
        unreadMsg.is_read = True
        unreadMsg.save()
        
    context = {
        'unreadMsg':unreadMsg,
    }

    return render(request, 'users/message.html', context)

# create message
def createMessage(request,pk):

    recipient = Profiles.objects.get(id=pk)
    form = MessageForm()

    try:
        sender = request.user.profiles
    except:
        sender = None

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()
            messages.success(request, 'Your message was successfully sent')
            return redirect('user-profile', pk=recipient.id)
    context = {
        'recipient':recipient,
        'form':form,
    }
    return render(request, 'users/message_form.html', context)