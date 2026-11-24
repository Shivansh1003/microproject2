"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from accounts import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('study/', views.study, name='study'),
    path('study/linear-algebra/', views.show_subject, {'template_name': 'subject1.html'}, name='linear_algebra'),
    path('study/machine-learning/', views.show_subject, {'template_name': 'subject2.html'}, name='machine_learning'),
    path('study/digital-logic/', views.show_subject, {'template_name': 'subject3.html'}, name='digital_logic'),
    path('study/web-technology/', views.show_subject, {'template_name': 'subject4.html'}, name='web_technology'),
    path('study/programming/', views.show_subject, {'template_name': 'subject5.html'}, name='programming'),
]
