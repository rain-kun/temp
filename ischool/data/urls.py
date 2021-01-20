from django.urls import path, include
from . import views


urlpatterns = [
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('', views.index, name='index'),
    path('division/', views.division, name='division')
    path('student/', views.student, name='student')
]