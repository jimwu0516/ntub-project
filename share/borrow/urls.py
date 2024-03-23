from django.urls import path
from . import views

urlpatterns = [
    path('available_borrow_items/', views.available_items, name='available_borrow_items'),
    path('available_borrow_item/<int:pk>/', views.available_item_detail, name='available_borrow_item'),
    path('borrow_item/<int:pk>/', views.borrow_item, name='borrow_item'), 
    path('user_orders/', views.user_orders, name='user_orders'),
    path('cancel_order/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('borrower_history_orders/', views.borrower_history_orders, name='borrower_history_orders'),
    
    path('view_pending_orders/', views.view_pending_orders, name='view_pending_orders'),
    path('update_order_status_approve/<int:order_id>/', views.update_order_status_approve, name='update_order_status_approve'),
    
    path('available/fashion/', views.available_fashion_items, name='available_fashion_items'),
    path('available/electronics', views.available_electronics_items, name='available_electronics_items'),
    path('available/sporting-goods', views.available_sporting_items, name='available_sporting_items'),
    path('available/books, movies and music', views.available_books_movie_and_music_items, name='available_books_movie_and_music_items'),
    path('available/home and garden', views.available_home_and_garden_items, name='available_home_and_garden_items'),
    path('available/Toys and Hobbies', views.available_toys_and_hobbies_items, name='available_toys_and_hobbies_items'),
    path('available/Everything Else', views.available_everything_else_items, name='available_everything_else_items'),





]

