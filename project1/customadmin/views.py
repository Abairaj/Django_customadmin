from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control,never_cache
from django.contrib.auth.hashers import make_password


# Create your views here.

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_login(request):
    try:
        if request.user.is_authenticated:
             return redirect('dashboard')
        
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = User.objects.filter(username = username)

            if not user.exists():
                messages.info(request,'Account not found')

            
            user = authenticate(username = username,password = password)

            if user and user.is_superuser:
                login(request,user)
                return redirect('dashboard')
            
            messages.info(request,'Invalid password')
            return redirect('/admin')

        return render(request,'admin_login.html')
    
    except Exception as e:
        print(e)




@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def dashboard(request):
    if request.user.is_authenticated:
        return render(request,'dashboard.html')
    else:
        return redirect('/admin')




def userlist(request):

    usr ={
        'user':User.objects.all()
    }
    if request.user.is_authenticated:
        return render(request,'contact_list.html',usr)
    else:
        return redirect('/admin')



def signout(request):
    logout(request)
    return redirect('/admin')


def searchbar(request):
    if request.method == 'GET':
        search = request.GET.get('query')
        usr= User.objects.all().filter(username__icontains=search)
        return render(request,'searchbar.html',{'usr':usr})

    else:
        print('Nothing similar')
        return redirect('userlist',{})


    


def add(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        pass2 = request.POST['pass2']



        if password != pass2:
            messages.info(request,'Passwords not match')

        elif not len(first_name + last_name) >= 4:
            messages.info(request,'Username should be of 4 characters or more.')

        elif User.objects.filter(first_name = first_name).exists():
            messages.info(request,f'username {first_name} is already taken')

        elif User.objects.filter(email = email).exists():
            messages.info(request,f'{email} is already registered.')

        elif first_name == '' and email == '':
            messages.info(request,'Username and email can\'t be empty ')

        else:
             usr =User(
                 username = str(first_name + last_name),
                 password = make_password(password),
                 email = email,
                 first_name = first_name,
                 last_name = last_name,
                
                
            )


             usr.save()
             
    
    return redirect('userlist')



def update(request,id):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        pass2 = request.POST['pass2']

        if password != pass2:
            messages.info(request,'Passwords not match')

        elif not len(first_name + last_name) >= 4:
            messages.info(request,'Username should be of 4 characters or more.')

        elif User.objects.filter(first_name = first_name).exists():
            messages.info(request,f'username {first_name} is already taken')

        elif User.objects.filter(email = email).exists():
            messages.info(request,f'{email} is already registered.')

        elif first_name == '' and email == '':
            messages.info(request,'Username and email can\'t be empty ')
        

        
        usr =User(
                id = id,
                username = str(first_name + last_name),
                email = email,
                first_name = first_name,
                last_name = last_name,
                password = make_password(password)
                
            )

        usr.save()

        
    return redirect('userlist')



def delete(request,id):
    usr = User.objects.filter(id = id).delete()
    return redirect('userlist')

