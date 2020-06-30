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

    session_id = user['idToken']
    request.session['uid'] = str(session_id)
    return render(request, "welcome.html", {"e": email})


def logout(request):
    try:
        del request.session['uid']
    except KeyError:
        pass
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

    try:
        idtoken = request.session['uid']
        a = authe.get_account_info(idtoken)
        a = a['users'][0]['localId']
        print(str(a))

        data = {
            "work":work,
            "progress": progress
        }
        db.child('users').child(a).child('reports').child(ms).set(data,idtoken)
        name = db.child('users').child(a).child('details').child('name').get(idtoken).val()
        return render(request, "welcome.html", {'e': name})
    except KeyError:
        message = "Oops! User Logged out. Please sign in again"
        return render(request, "home.html", {"messg": message})


def check(request):
    import datetime
    idtoken = request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users'][0]['localId']

    ts = db.child('users').child(a).child('reports').shallow().get(idtoken).val()

    lis = []
    for i in ts:
        lis.append(i)
    lis.sort(reverse = True)

    work = []
    for i in lis:
        wor = db.child('users').child(a).child('reports').child(i).child('work').get(idtoken).val()
        work.append(wor)

    date=[]
    for i in lis:
        i = float(i)
        dat = datetime.datetime.fromtimestamp(i).strftime('%H:%M %d-%m-%Y')
        date.append(dat)

    comb = zip(lis, date,work)
    name = db.child('users').child(a).child('details').child('name').get(idtoken).val()

    return render(request,"check.html", {'comb': comb, 'e': name})

def postcheck(request):
    import datetime
    time = request.GET.get('z')
    idtoken = request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users'][0]['localId']

    work = db.child('users').child(a).child('reports').child(time).child('work').get(idtoken).val()
    progress = db.child('users').child(a).child('reports').child(time).child('progress').get(idtoken).val()

    print(work)
    print("\n")
    print(progress)
    i = float(time)
    dat = datetime.datetime.fromtimestamp(i).strftime('%H:%M %d-%m-%Y')
    name = db.child('users').child(a).child('details').child('name').get(idtoken).val()

    return render(request, "postcheck.html", {'w': work, 'p': progress, 'dat': dat, 'e':name})