from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control,never_cache
from django.contrib import messages

# Create your views here.

@never_cache
@login_required(login_url='signin')
def index(request):
    return render(request,'index.html')

@cache_control(no_cache = True,must_revalidate =True,no_storage = True)
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        re_password = request.POST['pass2']

        
        #checking password with retyped password
        if User.objects.filter(username = username).exists():
            messages.info(request,'User name already exists.Try with other name')
            return redirect('signup')

        elif len(username) < 4:
            messages.info(request,'Username should be of 4 Characters or more')

        elif str(username) != str(username.capitalize()):
            messages.info(request,'First letter of username should be in caps.')

        elif email == '':
            messages.error(request,'email field empty')
            return redirect('signup')

        elif User.objects.filter(email = email).exists():
            messages.info(request,'User with same email already exist')
            return redirect('signup')

        elif password != re_password:
            messages.info(request,'passwords doesnt match with each other')

        else:
            user = User.objects.create_user(username = username,email = email,password = password)
            user.save()
            return redirect('signin')

    return render(request,'signup.html')

@cache_control(no_cache = True,must_revalidate =True,no_storage = True)
def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username = username,password = password)

        if user is not None:
            auth.login(request,user)
            return redirect('home')
        else:
            messages.info(request,'credentials not valid')
            return render(request,'login.html')
    else:
        return render(request,'login.html')

@login_required(login_url='signin')
def signout(request):
     auth.logout(request)
     return redirect('signin')
