from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import result_page


urlpatterns = [
    path('result_page/<str:status>/<str:message>/', result_page, name='result_page'),
    
]
