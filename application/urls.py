from django.urls import path
from application import views

urlpatterns = [
    path('',views.main, name='mainpage'),
    path('home/',views.home,name="homepage"),
    path('login/',views.login_account, name="loginpage"),
    path('signup/',views.signup,name="signuppage"),
    path("about/",views.about,name="aboutpage"),
    path("logout/",views.user_logout,name="logoutoption"),
    path("history/",views.history,name="historypage"),
    path("reminder/",views.reminder,name="reminderpage"),
    path("reminder/delete/<int:reminder_id>/",views.delete_reminder,name="reminder_delete"),
   
]
