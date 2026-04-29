from django.urls import path
from . import views

urlpatterns = [
    path('', views.add_expense),
    path('delete/<int:id>/', views.delete_expense),
    path('edit/<int:id>/', views.edit_expense),
     path('signup/', views.signup),   
    path('login/', views.user_login), 
    path('logout/', views.user_logout)
]