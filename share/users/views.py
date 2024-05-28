from django.shortcuts import render,redirect
from django.contrib.auth import login
from django.urls import reverse_lazy
from .forms import RegisterForm, ProfileForm
from django.views.generic.edit import FormView
from .models import Profile
from django.contrib.auth.views import LoginView
from django.contrib import messages

from .forms import ProfileEditForm, UserEditForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View

from django.contrib.auth.decorators import login_required
from .models import Review, Profile
from borrow.models import Order
from contribute.models import Item

from django.http import JsonResponse
from borrow.web3 import get_next_unlock, unlock_tokens, get_airdrop_mint, get_top_token_holders


from django.db.models import Avg, Count,  F, Q, DateField, Sum
from django.utils.timezone import now, timedelta
from django.db.models.functions import TruncWeek
from collections import OrderedDict


# Create your views here.
class RegisterView(FormView):
    template_name = 'users/register.html'
    form_class = RegisterForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('items')
    
    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field.capitalize()}: {error}")
        return super().form_invalid(form)

    def form_valid(self, form):
        user = form.save(commit=False)
        user.save()

        profile = Profile.objects.create(
            user=user,
            user_place=form.cleaned_data['user_place'],
            airdrop_wallet_address=form.cleaned_data['airdrop_wallet_address']
        )

        login(self.request, user)
        messages.success(self.request,"Success Register")

        return super().form_valid(form)

class MyLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        user = self.request.user
        if user.is_staff:
            return reverse_lazy('admin_dashboard')
        else:
            messages.success(self.request, 'Success Login')
            return reverse_lazy('items') 


    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))

class MyProfile(LoginRequiredMixin, View):
    def get(self, request):
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        
        context = {
            'user_form': user_form,
            'profile_form': profile_form
        }
        
        return render(request, 'users/profile.html', context)
    
    def post(self,request):
        user_form = UserEditForm(
            request.POST, 
            instance=request.user
        )
        profile_form = ProfileEditForm(
            request.POST,
            request.FILES,
            instance=request.user.profile
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            
            messages.success(request,'Your profile has been updated successfully')
            
            return redirect('profile')
        else:            
            context = {
                'user_form': user_form,
                'profile_form': profile_form
            }
            messages.error(request,'Error updating you profile')
            
            return render(request, 'users/profile.html', context)

class AdminDashboardView(UserPassesTestMixin, View):
    
    def test_func(self):
        return self.request.user.is_superuser 

    def get(self, request):
        next_unlock = get_next_unlock() 
        airdrop_mint = get_airdrop_mint() / 10**18
        user_count = Profile.objects.count()
        average_breakage = int(Order.objects.filter(status='finish').aggregate(Avg('breakage'))['breakage__avg'])

        like_count = Review.objects.filter(review_result='like').count()
        dislike_count =  Review.objects.filter(review_result='dislike').count()
        
        average_overdue_pick_up_time = Profile.objects.filter(average_overdue_pick_up_time__gt=0).aggregate(Avg('average_overdue_pick_up_time'))['average_overdue_pick_up_time__avg']
        average_overdue_pick_up_time = round(average_overdue_pick_up_time, 2) if average_overdue_pick_up_time is not None else 0

        average_decision_making_minute = Profile.objects.filter(average_decision_making_minute__gt=0).aggregate(Avg('average_decision_making_minute'))['average_decision_making_minute__avg']
        average_decision_making_minute = round(average_decision_making_minute, 2) if average_decision_making_minute is not None else 0


        top_token_holders = get_top_token_holders()
        
        place_counts = Profile.objects.values('user_place').annotate(total=Count('user_place')).order_by('user_place')
        
        
        #-----------------------------------------------------------------
        end_date = now()
        start_date = end_date - timedelta(days=90)
        
        weekly_counts = OrderedDict()
        current_week = start_date - timedelta(days=start_date.weekday())
        
        while current_week < end_date:
            weekly_counts[current_week.date()] = 0 
            current_week += timedelta(weeks=1)
        
        orders_in_past_three_months = Order.objects.filter(
            status__in=['finish'],
            end_time__gte=start_date
        )
        
        weekly_order_counts = orders_in_past_three_months.annotate(
            week=TruncWeek('end_time', output_field=DateField())
        ).values('week').annotate(
            count=Count('order_id')
        ).order_by('week')
        
        for entry in weekly_order_counts:
            weekly_counts[entry['week']] = entry['count']
        #-----------------------------------------------------------------
        category_counts = Item.objects.values('item_category').annotate(count=Count('item_category'))
        
        category_proportions = []
        for category in category_counts:
            
            category_proportions.append({
                'category': category['item_category'],
                'count': category['count'],
            })
        #-----------------------------------------------------------------
        
        three_months_ago = now() - timedelta(days=90)

        top_get_airdrop_contributors = Order.objects \
            .filter(end_time__gte=three_months_ago, status='finish') \
            .values('item__contributor__username') \
            .annotate(total_airdrop=Sum('airdropAmount')) \
            .order_by('-total_airdrop')[:5]

        for contributor in top_get_airdrop_contributors:
            print(contributor['item__contributor__username'], contributor['total_airdrop'])
        
        
        context = {
            'username': self.request.user.username,
            'days_until_unlock': next_unlock['days'],
            'hours_until_unlock': next_unlock['hours'],
            'airdrop_mint': airdrop_mint , 
            'user_count' : user_count,
            'like_count' : like_count,
            'dislike_count' : dislike_count,
            'weekly_order_counts_in_past_three_months': weekly_counts.items(),
            'average_breakage' : average_breakage,
            'category_proportions' : category_proportions,
            'average_overdue_pick_up_time' : average_overdue_pick_up_time,
            'average_decision_making_minute' : average_decision_making_minute,
            'top_token_holders' : top_token_holders,
            'place_counts' : place_counts,
            'top_get_airdrop_contributors': top_get_airdrop_contributors
            
        }
        return render(request, 'admin/admin_dashboard.html', context)
    
def api_next_unlock(self, request):
    next_unlock = get_next_unlock()
    return JsonResponse(next_unlock)
