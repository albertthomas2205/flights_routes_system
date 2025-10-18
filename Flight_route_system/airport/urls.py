from django.urls import path
from . import views

urlpatterns = [
    path('', views.airport_list, name='airport_list'),
    path('create/', views.airport_create, name='airport_create'),
    path('update/<int:pk>/', views.airport_update, name='airport_update'),
    path('delete/<int:pk>/', views.airport_delete, name='airport_delete'),
    path('add_next/', views.add_next_airport_view, name='add_next_airport'),
    path('shortest_path/', views.shortest_path_view, name='shortest_path'),
]
