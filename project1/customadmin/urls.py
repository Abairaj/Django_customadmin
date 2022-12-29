from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('',views.admin_login,name = 'signin'),
    path('dashboard/',views.dashboard,name = 'dashboard'),
    path('userlist/',views.userlist,name ='userlist'),
    path('logout/',views.signout,name = 'logout'),
    path('searchbar/',views.searchbar,name='search'),
    path('add/',views.add,name='add'),
    path('update/<str:id>/',views.update,name='update'),
    path('delete/<str:id>/',views.delete,name='delete'),

    
    
]