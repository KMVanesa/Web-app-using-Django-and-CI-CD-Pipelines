from first_app import views
from django.urls import path

app_name = 'home'

urlpatterns = [

    path('', views.index, name="index"),
    # path('form/', views.form_view, name="form"),
    # path('register/', views.register_form, name="register"),
    path('login/', views.user_login, name="login"),
    # path('logout/', views.user_logout, name="logout"),
    # path('update/', views.profile, name="update"),
    path('update_password/', views.change_password, name="password_change"),
    path('reset_password/', views.reset_password, name="password_reset"),

]
