from django.urls import path
from django.contrib.auth import views as auth_views
from .views import Home, HomeNotPrivileges

app_name = 'bases'

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('not-privileges/', HomeNotPrivileges.as_view(), name='home_not_privileges'),
    path('login/', auth_views.LoginView.as_view(template_name='bases/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout')
]