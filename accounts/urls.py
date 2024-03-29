from django.contrib.auth import views as auth_views
from django.urls import path

urlpatterns = [
    # Login
    path('login/',
         auth_views.LoginView.as_view(
             template_name='accounts/login.html',
             redirect_authenticated_user=True),
         name='login'),

    # Logout
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
