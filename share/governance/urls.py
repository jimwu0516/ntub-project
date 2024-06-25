from django.urls import path
from . import views

urlpatterns = [
    path('create-proposal/', views.create_proposal, name='create_proposal'),
]