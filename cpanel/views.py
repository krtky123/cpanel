from django.shortcuts import render, redirect
import pyrebase
from Crypto.PublicKey import RSA
from django.contrib import auth

config = {
    'apiKey': "AIzaSyAJE-_i96l4mY7WvAkQUwbNZEfrvg-3bDA",
    'authDomain': "cpanel-fd186.firebaseapp.com",
    'databaseURL': "https://cpanel-fd186.firebaseio.com",
    'projectId': "cpanel-fd186",
    'storageBucket': "cpanel-fd186.appspot.com",
    'messagingSenderId': "348716814819",
    'appId': "1:348716814819:web:6039d33a94e5c9187710d6",
    'measurementId': "G-GLJZEXFZKL"
}

firebase = pyrebase.initialize_app(config)

authe = firebase.auth()


def signin(request):
    return render(request, "home.html")


def postsignin(request):
    email = request.POST.get('email')
    passw = request.POST.get('pass')

    try:
        user = authe.sign_in_with_email_and_password(email,passw)
    except:
        message = "invalid credentials"
        return render(request, "home.html", {"messg": message})

    print(user['idToken'])
    session_id = user['idToken']
    request.session['uid'] = str(session_id)
    return render(request, "welcome.html", {"e": email})


def logout(request):
    auth.logout(request)
    return redirect('/')


def signup(request):
    return render(request, "signup.html")
