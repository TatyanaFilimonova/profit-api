from django.urls import path

from . import views

urlpatterns = [
    path('equipment/', views.Equipments.as_view()),
    path('CalculateBudget/', views.CalculateBudget.as_view()),
    path('getformbody/', views.GetFormBody.as_view()),
    path('editor/', views.EditEquipment),
    path('editrow/<id>', views.EditRow),
    path('deleterow/<id>', views.DeleteRow),
    path('addrow/', views.AddRow),
    path('addrow//adddirection/', views.AddDirection),
    path('addrow//deldirection/', views.DelDirection),
    path('editrow/<id>/adddirection/', views.AddDirection),
    path('editrow/<id>/deldirection/', views.DelDirection),
    path('CreateProject/', views.CreateProject),
    path('test_secures/', views.test_secures),
]