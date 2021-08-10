import django.contrib.auth.forms
from django.urls import path
from myapp import views

app_name = 'myapp'

urlpatterns = [
    path(r'', views.index, name = 'index'),
    path(r'user_login/', views.user_login, name = 'user_login'),
    path(r'user_logout/', views.user_logout, name = 'user_logout'),
    path(r'about/', views.about, name = 'about'),
    path(r'findcourses/', views.findcourses, name = 'findcourses'),
    path(r'place_order/', views.place_order, name = 'place_order'),
    path(r'review/', views.review, name = 'review'),
    path(r'<int:topic_id>/', views.detail, name = 'topic_id'),
    path(r'myaccount/', views.myaccount, name = 'myaccount'),
    path(r'register/', views.register, name = 'register')
]