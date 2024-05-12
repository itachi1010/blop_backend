from django.urls import path
from . import views
from .views import RegisterView


urlpatterns = [
    path('home/', views.HomeView.as_view(), name ='home'),
    path('logout/', views.LogoutView.as_view(), name ='logout'),
    path('register/', RegisterView.as_view(), name='register'),

]