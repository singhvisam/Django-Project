from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('room/', views.room),
    path('search_job', views.search_job, name='search_job'),
    path('edit_job', views.edit_job, name='edit_job'),
    path('delete_job/<str:title>/', views.delete_job, name="delete_job"),
    path('edit_in_mongo', views.edit_in_mongo, name="edit_in_mongo")
]