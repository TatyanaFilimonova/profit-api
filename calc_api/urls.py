from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('equipment/', views.Equipments.as_view()),
    path('CalculateBudget/', views.CalculateBudget.as_view()),
    path('getformbody/', views.GetFormBody.as_view()),
]