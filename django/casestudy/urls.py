"""casestudy URL Configuration.


The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

from casestudy.views import LoginView
from casestudy.views import SecurityView
from casestudy.views import UserSecurityView

urlpatterns = [
    # The only url defined in the casestudy application are the admin urls. The admin urls are defined in the
    # django.contrib.admin application, and provide a GUI for viewing and managing the database models like 'Email'.
    # https://docs.djangoproject.com/en/4.2/ref/contrib/admin/
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name='login'),
    path('user/security/', UserSecurityView.as_view(), name='user_security'),
    path('security/', SecurityView.as_view(), name='security'),
]
