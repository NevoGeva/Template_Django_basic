from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static








urlpatterns = [
    #home path
    path('', views.index),
    
    #image path
    path('upload_image',views.APIViews.as_view()),
    path('get_all_images', views.getImages),


    # login/register path
    path('login',TokenObtainPairView.as_view()),
    path('register', views.register),
    
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



