from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages
import bcrypt
from datetime import datetime


def index(request):

    return render(request, 'first_app/index.html')


def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/main')
    else:
        post = request.POST
        hash1 = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        new_user = User.objects.create(
            name=post['name'], username=post['username'], password=hash1)
        request.session['id'] = new_user.id
        return redirect('/travels')


def login(request):
    post = request.POST
    user = User.objects.filter(username=request.POST['username'])
    if not user:
        messages.error(request, 'Wrong Username')
        return redirect('/main')
    login_user = User.objects.get(username=request.POST['username'])
    if not bcrypt.checkpw(request.POST['password'].encode(), login_user.password.encode()):
        messages.error(request, "Loggin Error")
        return redirect('/main')
    else:
        request.session['id'] = login_user.id
        return redirect('/travels')


def travels(request):
    if 'id' not in request.session:
        messages.error(request, 'please login first')
        return render(request, 'first_app/index.html')
    else:
        context = {
            'user': User.objects.get(id=request.session['id']),
            'other_trips': Trip.objects.exclude(travllers=request.session['id'])
        }
        print (context['other_trips'])
        return render(request, 'first_app/travels.html', context)


def add_plan(request):
    if 'id' not in request.session:
        messages.error(request, 'please login first')
        return render(request, 'first_app/index.html')
    else:
        return render(request, 'first_app/plan.html')


def process_add(request):
    errors = {}
    if len(request.POST['destination']) < 3:
        errors["destination"] = "Destination should be at least 3 characters"
    if len(request.POST['description']) < 3:
        errors["description"] = "Description should be at least 3 characters"
    if (request.POST['start_date'] < str(datetime.now())):
        errors["start_time"] = "Star trip time should later than today"
    if (request.POST['start_date'] > request.POST['end_date']):
        errors["start_time"] = "End trip time should later than start"
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/travels/add')

    else:
        user = User.objects.get(id=request.session['id'])
        new_trip = Trip.objects.create(
            destination=request.POST['destination'], description=request.POST['description'],
            start_date=request.POST['start_date'], end_date=request.POST['end_date'])
        new_trip.travllers.add(user)
        new_trip.save()
        return redirect('/travels')


def logout(request):
    request.session.clear()
    return redirect('/main')


def jointrip(request, tripid):
    user = User.objects.get(id=request.session['id'])
    trip = Trip.objects.get(id=int(tripid))
    trip.travllers.add(user)
    trip.save()
    return redirect('/travels')


def destination(request, placeid):
    if 'id' not in request.session:
        messages.error(request, 'please login first')
        return render(request, 'first_app/index.html')
    else:
        context = {
            'place': Trip.objects.get(id=int(placeid)),
            'users': User.objects.exclude(trips=placeid)
        }
        return render(request, 'first_app/destination.html', context)
