from django.shortcuts import render, redirect
import random
from .forms import Login, Registration, For_tip
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .models import Tip, Vot

def upgrate(request):
    id = request.GET.get('id')
    nam = request.user.username
    if request.method == 'POST':
        form = For_tip(request.POST)
        if form.is_valid():
            text = form.cleaned_data.get('text')

            tips = Tip.objects.get(id=id)
            tips.content = text
    else:
        form = For_tip()
    return redirect('../')

def delete(request):
    id = request.GET.get('id')
    print(id)
    tips = Tip.objects.get(id=id)
    tips.delete()
    return redirect('../')

def logins(request):
    if request.method == 'POST':
        form = Login(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=name, password=password)
            if user is not None:
                print(user)
                login(request, user=user)
                return redirect('../')
    else:
        form = Login()
    return render(request, 'LifeProTips/login.html', {'form': form})


def logout_me(request):
    logout(request)
    return redirect('../')

def registration(request):
    if request.method == 'POST':
        form = Registration(request.POST)
        if form.is_valid():
            password = form.clean_password2()
            name = form.cleaned_data.get("name")
            print(name + ' ' + password)
            user = authenticate(request, username=name, password=password)
            if user is None:
                us1 = User.objects.create_user(name, None, password)
                us1.save()
            else:
                messages.error(request, 'User already exits!')
    else:
        form = Registration()
    return render(request, 'LifeProTips/registration.html', {'form': form})


def like_vote(request):
    id = request.GET.get('id')
    print(id)
    nam = request.user.id
    try:
        u = User.objects.get(id=nam)
    except:
        return redirect('../')
    print(nam)
    tips = Tip.objects.get(id=id)
    try:
        v = Vot.objects.get(user=u, tip=tips)
        if (v.upvote == 1):
            tips.downvote -= 1
            tips.upvote += 1
            v.upvote = 0
            tips.save()
            v.save()
        return redirect('../')
    except:
        print(1)
    uder = Vot.objects.create(user=u, tip=tips, upvote=0)
    tips.upvote += 1
    tips.save()
    uder.save()
    return redirect('../')


def dislike_vote(request):
    id = request.GET.get('id')
    tips = Tip.objects.get(id=id)
    nam = request.user.id
    v = Vot.objects.get(user=nam, tip=id)
    if v:
        if (v.upvote == 0):
            tips.downvote += 1
            tips.upvote -= 1
            v.upvote = 1
            tips.save()
            v.save()
        return redirect('..')
    uder = Vot.objects.create(user=nam, tip=id, upvote=1)
    tips.downvote += 1
    tips.save()
    uder.save()
    return redirect('../')


def home(request):
    if not request.user.is_authenticated:
        if 'user' not in request.session:
            name = random.choice(settings.NAME)
            request.session['user'] = name
            request.session.set_expiry(42)
        nam = request.session.get('user')
        log_out = 0
        form = 0
        tips = 0
    else:
        nam = request.user.username
        log_out = 1
        if request.method == 'POST':
            form = For_tip(request.POST)
            if form.is_valid():
                text = form.cleaned_data.get('text')
                tip1 = Tip.objects.create(content=text, author=User.objects.get(username=nam))
                tip1.save()
        else:
            form = For_tip()
        tips = Tip.objects.all()
    return render(request, 'LifeProTips/index.html', {'name': nam, 'logout': log_out, 'form': form, 'tips': tips})







