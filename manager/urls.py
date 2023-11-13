from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import LoginForm

app_name = 'manager'

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('home/', views.home, name='home'),
    path('list/', views.list, name='list'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html', authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('new/', views.new, name='new'),
    path('<int:pk>/', views.detail, name='detail'),
    path('<int:pk>/delete/', views.delete, name='delete'),
    path('<int:pk>/edit/', views.edit, name='edit'),

    path('configuration/', views.configuration, name='configuration'),
    path('<int:pk>/mark_completed/', views.mark_completed_task, name='mark_completed'),
    path('<int:pk>/<int:cfg_obj>/configuration_delete/', views.configuration_delete, name='configuration_delete'),

    path('search/', views.search, name='search'),
]