from django.urls import path
from . import views

urlpatterns = [
    path('add-liquidity/', views.add_liquidity, name='add_liquidity'),
    path('remove-liquidity/', views.remove_liquidity, name='remove_liquidity'),
    path('swap-token/', views.swap_token, name='swap_token'),
    path('liquidity-reserves/', views.liquidity_reserves, name='liquidity_reserves'),
]
