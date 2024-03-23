from django.urls import path
from .views import home, ItemList,ItemCreate,ItemDetail,ItemUpdate, ItemDelete

urlpatterns = [
    path('',home, name='home'),
    path('items/', ItemList.as_view(),name='items'),
    path('item/create/', ItemCreate.as_view(),name='item-create'),
    path('item/<int:pk>/', ItemDetail.as_view(),name='item'),
    path('item/update/<int:pk>/', ItemUpdate.as_view(),name='item-update'),
    path('item/delete/<int:pk>/', ItemDelete.as_view(),name='item-delete'),  
]
