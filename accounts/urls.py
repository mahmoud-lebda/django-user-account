from django.urls import path
from django.contrib.auth import views as auth_views
from .views import signup, load_cities, account_activation_sent, activate,\
    profile, update_profile, email_change, activate_change


urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('password-change/', auth_views.PasswordChangeView.as_view(
        template_name='accounts/change-password.html'), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='accounts/password_change_done.html'), name='password_change_done'),

    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('signup/', signup, name='signup'),

    path('ajax/load-cities/', load_cities, name='ajax_load_cities'),  # <-- ajx for cities filter

    path('account_activation_sent/', account_activation_sent, name='account_activation_sent'),
    path('activate/<str:uidb64>/<str:token>', activate, name='activate'),

    path('profile/', profile, name='profile'),
    path('update-profile/', update_profile, name='update_profile'),
    path('change-email/', email_change, name='chane_email'),
    path('change-email/<str:uidb64>/<str:token>', activate_change, name='activate_change'),
]




