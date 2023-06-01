"""temp_admin_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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

from django.urls import path, re_path
from django.views.static import serve

from adminapp import views
from mini_api import views as views_mini
from temp_admin_api import settings


urlpatterns = [

    path('admin/', admin.site.urls),

    path('login/', views.Login.as_view()),
    path('loginout/', views.LoginOut.as_view()),

    path('uploadimg/', views.UploadImg.as_view()),
    # path('media/(?P.*)$', serve, {"document_root":settings.MEDIA_ROOT}),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),

    path('records/', views.RecordsView.as_view()),
    re_path('records/(\d+)', views.RecordsViewdetail.as_view()),

    path('images/', views.ImagesView.as_view()),
    re_path('images/(\d+)', views.ImagesViewdetail.as_view()),

    path('admins/', views.AdminsView.as_view()),
    re_path('admins/(\d+)', views.AdminsViewdetail.as_view()),

    path('users/', views.UsersView.as_view()),
    re_path('users/(\d+)', views.UsersViewdetail.as_view()),

    path('resetpassw/', views.Resetpassw.as_view()),

    path('lunbo/', views.LunboView.as_view()),
    re_path('lunbo/(\d+)', views.LunboViewdetail.as_view()),
    #
    # Wechat miniprogram
    path('getopenid/', views_mini.Getopenid.as_view()),
    path('lunbomini/', views_mini.Lunbomini.as_view()),
    path('recordsmini/', views_mini.RecordsView.as_view()),
    re_path('recordsmini/(\d+)', views_mini.RecordsminiViewdetail.as_view()),
    re_path('miniupdate/(\d+)', views_mini.Userminiupdate.as_view()),
    path('miniinsert/', views_mini.Userminiinsert.as_view()),
    path('imagesmini/', views_mini.ImagesminiView.as_view()),
    re_path('imagesmini/(\d+)', views_mini.ImagesminiViewdetail.as_view()),
]
