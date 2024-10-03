from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path
from .views import register_view, register_success_view, login_view, LogoutView, CreateContestantProfileView

urlpatterns = [
    path('register/', register_view, name='register'),
    path('register_success', register_success_view, name='register-success'),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("create_profile", CreateContestantProfileView, name="create profile"),
    path('login/', login_view, name='login'),
    path('password-reset/', PasswordResetView.as_view(template_name='password_reset.html', html_email_template_name='password_reset_email.html'), name='password-reset'),
    path('password-reset/done', PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
]
