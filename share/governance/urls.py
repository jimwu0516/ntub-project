from django.urls import path
from . import views

urlpatterns = [
    path('create-proposal/', views.create_proposal, name='create_proposal'),
    path('admin-all-proposal', views.admin_show_all_proposal, name='admin_all_proposal'),
]