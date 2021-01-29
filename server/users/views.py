from django.http import HttpResponse
from django.shortcuts import render,redirect
from users.models import Users
import uuid

def login(request):
    if request.method == "GET":
        return render(request,'login.html',context=None)

    if request.method == "POST":
        u = Users.objects.filter(username=request.POST.get('username'),password=request.POST.get('password'))
        if u:
            u[0].token = uuid.uuid4()
            u[0].avtive = 1
            u[0].save()
            response = redirect('/home')
            response.set_cookie('token',u[0].token)
            return response
        else:
            return HttpResponse('not found',status = 404)



def logout(request):
    try:
        token = request.COOKIES["token"]
        u = Users.objects.get(token = token)
        u.token = None
        u.save()
        del check_login
    except:
        pass
    return redirect('/users/login')


def signin(request):
    users = Users.objects.all()
    for u in users:
        if request.POST.get('username_signin') == u.username:
            return redirect('/users/login')

    new_user_signin = Users(
                    first_name = request.POST.get('first_name_signin'),
                    last_name = request.POST.get('last_name_signin'),
                    username = request.POST.get('username_signin'),
                    password = request.POST.get('password_signin'),
                    avatar = '123',
                    token = uuid.uuid4(),
                )
    new_user_signin.save()
    new_user_signin = Users.objects.get(username = request.POST.get('username_signin'))
    response = redirect('/home')
    response.set_cookie('token',new_user_signin.token)
    check_login = 1
    return response


def home(request):
    sender_token = request.COOKIES['token']

    try:
        sender = Users.objects.get(token=sender_token)

        if request.method == "GET":
            return render(request,'home.html',context=None)
            # return HttpResponse(' found',status = 404)
        else:
            return HttpResponse('not found',status = 404)
    except:
        return redirect('/')
