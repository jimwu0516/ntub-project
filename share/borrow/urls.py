from django.urls import path
from . import views

urlpatterns = [
    path('available_borrow_items/', views.available_items, name='available_borrow_items'),
    path('available_borrow_item/<int:pk>/', views.available_item_detail, name='available_borrow_item'),
    path('borrow_item/<int:pk>/', views.borrow_item, name='borrow_item'), 
    
    path('update_order_status_approve/<int:order_id>/', views.update_order_status_approve, name='update_order_status_approve'),
    
    path('available/fashion/', views.available_fashion_items, name='available_fashion_items'),
    path('available/electronics', views.available_electronics_items, name='available_electronics_items'),
    path('available/sporting-goods', views.available_sporting_items, name='available_sporting_items'),
    path('available/books, movies and music', views.available_books_movie_and_music_items, name='available_books_movie_and_music_items'),
    path('available/home and garden', views.available_home_and_garden_items, name='available_home_and_garden_items'),
    path('available/Toys and Hobbies', views.available_toys_and_hobbies_items, name='available_toys_and_hobbies_items'),
    path('available/Everything Else', views.available_everything_else_items, name='available_everything_else_items'),

    path('orders/latest-status', views.latest_status_user_orders, name='latest_status_user_orders'),
    path('orders/unpaid-order', views.unpaid_user_orders, name='unpaid_user_orders'),
    path('update_order_status_to_pending/<int:order_id>/', views.update_order_status_to_pending, name='update_order_status_to_pending'),
    path('orders/cancel-order', views.cancel_order_user_orders, name='cancel_order_user_orders'),
    path('orders/hostory-order', views.history_user_orders, name='history_user_orders'),
    
    path('cancel_order/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('contributor_approve_expired/<int:order_id>/', views.contributor_approve_expired, name='contributor_approve_expired'),
    path('borrower_not_picked_up/<int:order_id>/', views.borrower_not_picked_up, name='borrower_not_picked_up'),

    
    path('contributor-orders/', views.contributor_order_status, name='contributor_order_status'), 
    
    path('borrower_get_item_page/<int:order_id>/', views.borrower_get_item_page, name='borrower_get_item_page'),
    path('update_to_get_item/<int:order_id>/', views.update_to_get_item, name='update_to_get_item'),
    
    path('update_to_return_item/<int:order_id>/', views.update_to_return_item, name='update_to_return_item'),
    
    path('contributor_submit_review/<int:order_id>/', views.contributor_submit_review, name='contributor_submit_review'),
    path('borrower_submit_review/<int:order_id>/', views.borrower_submit_review, name='borrower_submit_review'),
    
    path('borrower-history-dashboard/<int:borrower_id>/', views.borrower_history_dashboard, name='borrower_history_dashboard'),
    path('contributor-history-dashboard/<int:contributor_id>/', views.contributor_history_dashboard, name='contributor_history_dashboard'),


]

