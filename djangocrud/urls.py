from django.contrib import admin
from django.urls import path, include
from tasks import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('signup/', views.signup, name="signup"),
    path('tasks/', views.tasks, name='tasks'),
    path('tasks_completed/', views.tasks_completed, name='tasks_completed'),
    path('logout/', views.signout, name='logout'),
    path('signin/', views.signin, name='login'),
    path('tasks/create/', views.create_task, name='create'),
    path('tasks/<int:task_id>/', views.task_detail, name='task_detail'),
    path('tasks/<int:task_id>/complete', views.complete_task, name='complete_task'),
    path('tasks/<int:task_id>/delete', views.delete_task, name='delete_task'),
    path('dashboard/', views.dashboard, name='dashboard'),
    #passwords
    path('forget-password/',views.ForgetPassword,name='forget_password'),
    path('change-password/<token>/',views.ChangePassword,name='change_password'),
]
