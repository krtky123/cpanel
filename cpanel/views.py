from django.shortcuts import render, redirect
import pyrebase
from Crypto.PublicKey import RSA
from django.contrib import auth

config = {
    # user specific
}

firebase = pyrebase.initialize_app(config)

authe = firebase.auth()
db = firebase.database()

def home(request):
    return render(request, "home.html")


def signin(request):
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


def postsignup(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    passw = request.POST.get('pass')
    try:
        user = authe.create_user_with_email_and_password(email, passw)
        uid = user['localId']
        data = {"name": name, "status": "1"}
        db.child("users").child(uid).child("details").set(data)
    except:
        message = "Try Again"
        return render(request, "signup.html", {"messg": message})

    return render(request, "home.html")

def create(request):
    return render(request,"create.html")


def postcreate(request):

    import time
    from datetime import timezone, datetime
    import pytz
    tz = pytz.timezone('Asia/Kolkata')
    time_now = datetime.now(timezone.utc).astimezone(tz)
    ms = int(time.mktime(time_now.timetuple()))
    print(str(ms))

    work = request.POST.get('work')
    progress = request.POST.get('progress')
    idtoken = request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users'][0]['localId']
    print(str(a))

    data = {
        "work":work,
        "progress": progress
    }
    db.child('users').child(a).child('reports').child(ms).set(data)
    name = db.child('users').child(a).child('details').child('name').get().val()
    return render(request, "welcome.html", {'e': name})