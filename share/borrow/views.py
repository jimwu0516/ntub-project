from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404,redirect
from .models import Item ,Order
from django.contrib import messages

from django.utils import timezone
from datetime import datetime

from django.http import HttpResponseRedirect
from django.urls import reverse

from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse

from users.models import Review

@login_required
def available_item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    context = {
        'item': item
    }
    return render(request, 'borrow/available_item_detail.html', context)


@login_required
def borrow_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    
    if request.method == 'POST':
        start_time_str = request.POST.get('start_time')
        end_time_str = request.POST.get('end_time')
        
        start_time = timezone.make_aware(datetime.strptime(start_time_str, '%Y-%m-%dT%H:%M'))
        end_time = timezone.make_aware(datetime.strptime(end_time_str, '%Y-%m-%dT%H:%M'))
        
        order = Order.objects.create(
            borrower=request.user,
            item=item,
            start_time=start_time,
            end_time=end_time,
            status='wait_to_pay'
        )
        
        item.item_available = False
        item.save()
        #call smart contract 
        #if success paid 
        #   status == pending 
        #   messages.success(request,'Item borrowed request successfully sent')
        #else :
        #   status == unpaid 
        #   messages.alert(request,'please complete pay ')
        #   
         
        return redirect('user_orders')
    
    return render(request, 'borrow/available_item_detail.html', {'item': item})
"""
@login_required
def view_pending_orders(request):
    orders = Order.objects.filter(
        status='pending',
        item__contributor__username=request.user.username
    )

    context = {
        'orders': orders
    }
    return render(request, 'borrow/approve_order.html', context)
"""

@login_required
def update_order_status_approve(request, order_id):
    if request.method == 'POST':
        decision = request.POST.get('decision')
        if decision == 'accept':
            new_status= 'accept'
            order = Order.objects.get(order_id=order_id)
            contributor_email = order.item.contributor.email
            borrower_email = order.borrower.email
            borrower = order.borrower.username
            start_time = order.start_time
            end_time = order.end_time
            borrow_item_name = order.item.item_name
            borrow_item_addr = order.item.item_address
            send_confirm_email(borrower_email,'Request Approved',f'\n\nHi {borrower} Your request has been approved' f'\n\nItem name: {borrow_item_name}' f'\n\nAddress: {borrow_item_addr}' f'\n\nStart Time: {start_time}' f'\n\nEnd Time: {end_time}')
            send_confirm_email(contributor_email,'Request Approved',f'\n\nYou has approved request'  f'\n\nItem name: {borrow_item_name}' f'\n\nAddress: {borrow_item_addr}'f'\n\nStart Time: {start_time}' f'\n\nEnd Time: {end_time}')
        else:
            new_status= 'deny'
            order = Order.objects.get(order_id=order_id)
            borrower_email = order.borrower.email
            borrow_item_name = order.item.item_name
            borrower = order.borrower.username
            send_confirm_email(borrower_email,'Request Denied',f'\n\nSorry {borrower} Your request has been denied' f'\n\nItem name: {borrow_item_name}')
            order.item.item_available = True
            order.item.save()
            #return deposit to borrower call smart contract 
        
        Order.objects.filter(order_id=order_id).update(status=new_status)
        return HttpResponseRedirect(reverse('contributor_order_status'))
    
def send_confirm_email(email_address,subject, message):
    send_mail(subject, message, 'sharetoearn999@gmail.com', [email_address])


@login_required
def available_items(request):
    
    available_items = Item.objects.filter(item_available=True).exclude(contributor=request.user)

    context = {
        'available_items': available_items
    }
    return render(request, 'borrow/available_borrow_items.html', context)


@login_required
def available_fashion_items(request):
    available_fashion_items = Item.objects.filter(item_available=True, item_category='fashion').exclude(contributor=request.user)

    context = {
        'available_items': available_fashion_items
    }
    return render(request, 'borrow/available_borrow_items.html', context)

@login_required
def available_electronics_items(request):
    available_electronics_items = Item.objects.filter(item_available=True, item_category='electronics').exclude(contributor=request.user)

    context = {
        'available_items': available_electronics_items
    }
    return render(request, 'borrow/available_borrow_items.html', context)


@login_required
def available_sporting_items(request):
    available_sporting_items = Item.objects.filter(item_available=True, item_category='sporting-goods').exclude(contributor=request.user)

    context = {
        'available_items': available_sporting_items
    }
    return render(request, 'borrow/available_borrow_items.html', context)


@login_required
def available_books_movie_and_music_items(request):
    available_books_movie_and_music_items = Item.objects.filter(item_available=True, item_category='books, movies & music').exclude(contributor=request.user)
    context = {
        'available_items': available_books_movie_and_music_items
    }
    return render(request, 'borrow/available_borrow_items.html', context)


@login_required
def available_home＿and_garden_items(request):
    available_home＿and_garden_items = Item.objects.filter(item_available=True, item_category='home & garden').exclude(contributor=request.user)
    context = {
        'available_items': available_home＿and_garden_items
    }
    return render(request, 'borrow/available_borrow_items.html', context)

@login_required
def available_toys_and_hobbies_items(request):
    available_toys_and_hobbies_items = Item.objects.filter(item_available=True, item_category='toys & hobbies').exclude(contributor=request.user)
    context = {
        'available_items': available_toys_and_hobbies_items
    }
    return render(request, 'borrow/available_borrow_items.html', context)

@login_required
def available_everything_else_items(request):
    available_everything_else_items = Item.objects.filter(item_available=True, item_category='everything else').exclude(contributor=request.user)
    context = {
        'available_items': available_everything_else_items
    }
    return render(request, 'borrow/available_borrow_items.html', context)

#---------------------------------------------------------------------


    
#def make a trainsit (By pressing pay button)
    #call smart contract 
    #if true update status to pending 
    
    
#smart contract func 
#   return true or false 
    
def latest_status_user_orders(request):
    desired_statuses = ['wait_to_pay', 'pending', 'accept','return_item', 'get_item','borrower_comment']
    latest_status_user_orders = Order.objects.filter(borrower=request.user, status__in=desired_statuses)    
    
    context = {
        'user_orders': latest_status_user_orders,
        'show_cancel_column': False,
        'show_action_column': True,
    }
    return render(request, 'borrow/user_orders.html', context)

def unpaid_user_orders(request):
    desired_statuses = ['unpaid']
    unpaid_user_orders = Order.objects.filter(borrower=request.user, status__in=desired_statuses)
    unpaid_orders_exist = Order.objects.filter(borrower=request.user, status='unpaid').exists()
    show_cancel_column = unpaid_orders_exist
    context = {
        'user_orders': unpaid_user_orders,
        'unpaid_orders_exist': unpaid_orders_exist,
        'show_cancel_column': show_cancel_column,
        'show_action_column': False,
    }
    return render(request, 'borrow/user_orders.html', context)

    #if success paid 
        #   status == pending 
        #   messages.success(request,'Item borrowed request successfully sent')
        #else :
        #   messages.alert(request,'please complete pay ')
    
def cancel_order_user_orders(request):
    desired_statuses = ['deny','cancel_order']
    cancel_order_user_orders = Order.objects.filter(borrower=request.user, status__in=desired_statuses)

    context = {
        'user_orders': cancel_order_user_orders,
        'show_cancel_column': False,
        'show_action_column': False,
    }
    return render(request, 'borrow/user_orders.html', context)

def history_user_orders(request):
    desired_statuses = ['finish']
    history_user_orders = Order.objects.filter(borrower=request.user, status__in=desired_statuses)

    context = {
        'user_orders': history_user_orders,
        'show_cancel_column': False,
        'show_action_column': False,
    }
    return render(request, 'borrow/user_orders.html', context)


def cancel_order(request, order_id):
    if request.method == 'POST':
        Order.objects.filter(order_id=order_id).update(status='cancel_order')
        order=Order.objects.get(order_id=order_id)
        order.item.item_available = True
        order.item.save()
        messages.success(request, 'Order has been cancelled') 
        return redirect('latest_status_user_orders')

@login_required
def contributor_order_status(request):
    desired_statuses = ['pending','accept','get_item','return_item']
      
    contributor_orders = Order.objects.filter(
        status__in=desired_statuses,
        item__contributor__username=request.user.username
    )

    context = {
        'contributor_orders': contributor_orders
    }
    
    return render(request, 'borrow/contributor_order_status.html', context)

#--------------------------------------------------------------------------------------------------------------------
@login_required
def borrower_get_item_page(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    item_address = order.item.item_address
    context = {
        'order': order,
        'item_address': item_address,
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY
        
    }
    return render(request, 'borrow/borrower_get_item.html', context)

    
@login_required
def update_to_get_item(request, order_id):
    if request.method == "POST":
        order = get_object_or_404(Order, order_id=order_id)
        order.status = 'get_item'
        order.save()
        
        messages.success(request, 'Get item successfully.')

        return redirect('latest_status_user_orders')

#--------------------------------------------------------------------------------------------------------------------
@login_required
def update_to_return_item(request, order_id):
    if request.method == "POST":
        order = get_object_or_404(Order, order_id=order_id)
        order.status = 'return_item'
        order.item.item_available = True
        order.save()
        
        messages.success(request, 'Return item successfully.')
        
        return redirect('contributor_submit_review', order_id=order_id)
    
#------------------------------------------------------------------------------------------------------------------------
@login_required
def contributor_submit_review(request, order_id):    
    order = get_object_or_404(Order, order_id=order_id)
    
    if request.method == 'POST':
        review_comment = request.POST['review_comment']
        review_result = request.POST['review_result']
        breakage = request.POST['breakage']

        Review.objects.create(
            username=order.borrower,
            review_type='as_borrower',
            review_comment=review_comment,
            review_result=review_result
        )
        
        order.breakage = breakage
        order.status = 'borrower_comment'
        order.save()
        
        messages.success(request, 'Your review has been submitted.')
        return redirect('contributor_order_status') 

    return render(request, 'borrow/contributor_submit_review.html', {'order_id': order_id,'breakage_choices': Order.BREAKAGE_CHOICES})

#------------------------------------------------------------------------------------------------------------------------
@login_required
def borrower_submit_review(request, order_id):    
    order = get_object_or_404(Order, order_id=order_id)
    
    if request.method == 'POST':
        review_comment = request.POST['review_comment']
        review_result = request.POST['review_result']

        Review.objects.create(
            username=order.item.contributor,
            review_type='as_contributor',
            review_comment=review_comment,
            review_result=review_result
        )
        
        order.status = 'finish'
        order.save()
        #return deposit
        #airdrop token
        
        messages.success(request, 'Your review has been submitted.')
        return redirect('latest_status_user_orders') 

    return render(request, 'borrow/borrower_submit_review.html', {'order_id': order_id})

