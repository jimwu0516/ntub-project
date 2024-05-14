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
from .models import Review

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
        context = {
            'username': self.request.user.username
        }
        return render(request, 'admin/admin_dashboard.html', context)