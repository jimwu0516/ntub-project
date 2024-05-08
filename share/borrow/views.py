from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404,redirect
from .models import Item ,Order 
from django.contrib import messages

from django.utils import timezone
from datetime import datetime,timedelta

from django.http import HttpResponseRedirect
from django.urls import reverse

from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse

from users.models import Review, Profile
from django.contrib.auth.models import User

from .web3 import returnDepositAndAirdrop, borrowerNotPickedUpReturnDeposit, cancelOrderReturnDeposit

from django.db.models import Avg, Count,  F, Q, DateField
from django.utils.timezone import now, timedelta
from django.db.models.functions import TruncWeek
from collections import OrderedDict
#----------------------borrower browse available items --------------------------------------------------------
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


#---------borrower choose date and submitting request ------------------------------------------------------------------------------
@login_required
def available_item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    context = {
        'item': item
    }
    return render(request, 'borrow/available_item_detail.html', context)

def calculate_airdrop_amount(contributor, base_amount=10):
    avg_breakage = Order.objects.filter(item__contributor=contributor).aggregate(Avg('breakage'))['breakage__avg'] or 0
    
    like_count = Review.objects.filter(
        username=contributor, review_result='like').count()
    dislike_count = Review.objects.filter(
        username=contributor, review_result='dislike').count()
    
    total_item_count = Item.objects.count()
    available_item_count = Item.objects.filter(item_available=True).count()

    airdrop_amount = base_amount + 10 * (100 - avg_breakage) / 100 + 10 * (like_count)/(like_count + dislike_count)+ 10 * ( 1 - ( available_item_count / total_item_count ))
    
    n = Order.objects.count()
    
    airdrop_amount = airdrop_amount * pow(0.95, n)

    return round(airdrop_amount)

@login_required
def borrow_item(request, pk):
    item = get_object_or_404(Item, pk=pk)

    if request.method == 'POST':
        start_time_str = request.POST.get('start_time')
        end_time_str = request.POST.get('end_time')
        transaction_status = request.POST.get('transaction_status', 'unpaid')
        
        start_time = timezone.make_aware(datetime.strptime(start_time_str, '%Y-%m-%dT%H:%M'))
        end_time = timezone.make_aware(datetime.strptime(end_time_str, '%Y-%m-%dT%H:%M'))
        
        airdrop_amount = calculate_airdrop_amount(item.contributor)
        
        order = Order.objects.create(
            borrower=request.user,
            item=item,
            start_time=start_time,
            end_time=end_time,
            status=transaction_status,
            airdropAmount=airdrop_amount
        )
        
        contributor_email=order.item.contributor.email
        borrow_item_name=order.item.item_name
        start_time=order.start_time
        end_time= order.end_time
        
        send_confirm_email(contributor_email,'You have a new borrow request',f'\n\nItem name: {borrow_item_name}' f'\n\nStart Time: {start_time}' f'\n\nEnd Time: {end_time}')
        
        item.item_available = False
        item.save()

        if transaction_status == 'unpaid':
            messages.error(request, 'Transaction failed! Please pay deposit within an hour') 
            return redirect('unpaid_user_orders') 
        else:
            messages.success(request, 'Pay deposit successfully, your request has been submitted') 
            return redirect('latest_status_user_orders')

    context = {
        'item': item,
    }

    return render(request, 'borrow/available_item_detail.html', context)


#-------------------contributor approves or denies request------------------------------------------------------------------------------
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
            
            borrower_profile = get_object_or_404(Profile, user=order.borrower)
            borrower_address = borrower_profile.airdrop_wallet_address
            deposit_amount = order.item.item_deposit_require
            send_confirm_email(borrower_email,'Request Denied',f'\n\nSorry {borrower} Your request has been denied' f'\n\nItem name: {borrow_item_name}')
            order.item.item_available = True
            order.item.save()
            cancelOrderReturnDeposit(borrower_address,deposit_amount)
        
        Order.objects.filter(order_id=order_id).update(status=new_status)
        return HttpResponseRedirect(reverse('contributor_order_status'))
    
def send_confirm_email(email_address,subject, message):
    send_mail(subject, message, 'sharetoearn999@gmail.com', [email_address])
    
def contributor_approve_expired(request, order_id):
    if request.method == 'POST':
        Order.objects.filter(order_id=order_id).update(status='approve_expired')
        order=Order.objects.get(order_id=order_id)
        order.item.item_available = True
        order.item.save()
        
        borrower_profile = get_object_or_404(Profile, user=order.borrower)
        borrower_address = borrower_profile.airdrop_wallet_address
        deposit_amount = order.item.item_deposit_require
        cancelOrderReturnDeposit(borrower_address,deposit_amount)
       
    
def borrower_not_picked_up(request, order_id):
    if request.method == 'POST':
        Order.objects.filter(order_id=order_id).update(status='not_picked_up')
        order=Order.objects.get(order_id=order_id)
        order.item.item_available = True
        order.item.save()
        
        contributor_profile = get_object_or_404(Profile, user=order.item.contributor)
        contributor_address = contributor_profile.airdrop_wallet_address
        borrower_profile = get_object_or_404(Profile, user=order.borrower)
        borrower_address = borrower_profile.airdrop_wallet_address
        depositAmount = order.item.item_deposit_require
        borrowerNotPickedUpReturnDeposit(borrower_address, contributor_address, depositAmount) 


#--------------------------------------filter user order status page---------------------------------------------------------------------------------
def latest_status_user_orders(request):
    desired_statuses = ['pending', 'accept','return_item', 'get_item','borrower_comment']
    latest_status_user_orders = Order.objects.filter(borrower=request.user, status__in=desired_statuses)    
    
    context = {
        'user_orders': latest_status_user_orders,
        'show_cancel_column': False,
        'show_action_column': True,
    }
    return render(request, 'borrow/user_orders.html', context)

def unpaid_user_orders(request):
    desired_statuses = ['unpaid','wait_to_pay']
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

@login_required
def update_order_status_to_pending(request, order_id):
    if request.method == 'POST':
        Order.objects.filter(order_id=order_id).update(status='pending')
        
        order = Order.objects.get(order_id=order_id)
        contributor_email=order.item.contributor.email
        borrow_item_name=order.item.item_name
        start_time=order.start_time
        end_time= order.end_time
        send_confirm_email(contributor_email,'You have a new borrow request',f'\n\nItem name: {borrow_item_name}' f'\n\nStart Time: {start_time}' f'\n\nEnd Time: {end_time}')
        
        messages.success(request, 'Pay deposit successfully, your request has been submitted') 
        return redirect('latest_status_user_orders')
    
def cancel_order_user_orders(request):
    desired_statuses = ['deny','cancel_order', 'approve_expired', 'not_picked_up' ]
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
    
    
#-----------------contributor order status page------------------------------------------------------------------------------------------
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


#----------------borrower get item page--------------------------------------------------------------------------------------
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
        
        overdue_minutes = int(request.POST.get('overdue_minutes', 0))
        profile = get_object_or_404(Profile, user=order.borrower)
        if profile.average_overdue_pick_up_time == 0:
            profile.average_overdue_pick_up_time = overdue_minutes
        else:
            profile.average_overdue_pick_up_time = (profile.average_overdue_pick_up_time + overdue_minutes) // 2
        profile.save()
        
        messages.success(request, 'Get item successfully.')

        return redirect('latest_status_user_orders')


#---------------contributor gets the item back-------------------------------------------------------------
@login_required    
def update_to_return_item(request, order_id):
    if request.method == "POST":
        order = Order.objects.get(order_id=order_id)
        order.status = 'return_item'
        order.save()
        
        item = order.item
        item.item_available = True 
        item.save()
        
        messages.success(request, 'Return item successfully.')
        
        return redirect('contributor_submit_review', order_id=order_id)
    
    
#-------------------contributor_submit_review------------------------------------------------------------------
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


#--------------borrower_submit_review---------------------------------------------------------------------
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
        
        txn_hash = handle_return_deposit_and_airdrop(order)
        
        order.status = 'finish'
        order.save()
        
        messages.success(request, 'Your review has been submitted.')

        return JsonResponse({'txn_hash': txn_hash})
        
    return render(request, 'borrow/borrower_submit_review.html', {'order_id': order_id})


#--------------------handle_return_deposit_and_airdrop ---------------------------------------------------
def handle_return_deposit_and_airdrop(order):
    contributor_profile = get_object_or_404(Profile, user=order.item.contributor)
    contributor_address = contributor_profile.airdrop_wallet_address
    
    borrower_profile = get_object_or_404(Profile, user=order.borrower)
    borrower_address = borrower_profile.airdrop_wallet_address
    
    depositAmount = order.item.item_deposit_require
    damage_percentage = order.breakage
    
    airdropAmount = order.airdropAmount

    return returnDepositAndAirdrop(borrower_address, contributor_address, depositAmount, damage_percentage, airdropAmount)


#-------------------show borrower history dashboard------------------#
def borrower_history_dashboard(request, borrower_id):
    borrower = get_object_or_404(User, pk=borrower_id)
    reviews = Review.objects.filter(username=borrower, review_type='as_borrower')
    
    like_count = Review.objects.filter(
        username=borrower, review_result='like').count()
    dislike_count = Review.objects.filter(
        username=borrower, review_result='dislike').count()
    
    denied_order_count = Order.objects.filter(borrower=borrower, status='deny').count()
    all_order_count_a = Order.objects.filter(borrower=borrower, status__in=['deny', 'pending', 'finish', 'get_item', 'return_item', 'borrower_comment']).count()
    deny_percentage = round((denied_order_count / all_order_count_a) * 100, 2)
    
    not_picked_up_count = Order.objects.filter(borrower=borrower, status='not_picked_up').count()
    all_order_count_b = Order.objects.filter(borrower=borrower, status__in=['not_picked_up', 'finish', 'get_item', 'return_item', 'borrower_comment']).count()
    not_picked_up_percentage = round((not_picked_up_count / all_order_count_b) * 100, 2)
    
    profile = get_object_or_404(Profile, user=borrower)
    average_overdue_pick_up_time = profile.average_overdue_pick_up_time
    
    average_breakage = round(Order.objects.filter(borrower=borrower, status='finish').aggregate(Avg('breakage'))['breakage__avg'], 2)
    
    #-----------------------
    end_date = now()
    start_date = end_date - timedelta(days=90)
    
    weekly_counts = OrderedDict()
    current_week = start_date - timedelta(days=start_date.weekday())
    
    while current_week < end_date:
        weekly_counts[current_week.date()] = 0 
        current_week += timedelta(weeks=1)
    
    orders_in_past_three_months = Order.objects.filter(
        borrower=borrower,
        status__in=['finish', 'get_item', 'return_item', 'borrower_comment'],
        end_time__gte=start_date
    )
    
    weekly_order_counts = orders_in_past_three_months.annotate(
        week=TruncWeek('end_time', output_field=DateField())
    ).values('week').annotate(
        count=Count('order_id')
    ).order_by('week')
    
    for entry in weekly_order_counts:
        weekly_counts[entry['week']] = entry['count']
    #-----------------------
    
    context = {
        'borrower': borrower,
        'reviews': reviews,
        'like_count': like_count,
        'dislike_count': dislike_count,
        'deny_percentage': deny_percentage,
        'not_picked_up_percentage': not_picked_up_percentage,
        'average_overdue_pick_up_time': average_overdue_pick_up_time,
        'average_breakage': average_breakage,
        'weekly_order_counts_in_past_three_months': weekly_counts.items()
    }
    return render(request, 'borrow/borrower_history_dashboard.html', context)
