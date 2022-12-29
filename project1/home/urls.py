from django.urls import path
from . import views

urlpatterns = [
    path('',views.signin,name = 'signin'),
    path('signup/',views.signup,name = 'signup'),
    path('home/',views.index,name ='home'),
    path('signin/',views.signin,name = 'signin'),
    path('logout/',views.signout,name='logout')
]
