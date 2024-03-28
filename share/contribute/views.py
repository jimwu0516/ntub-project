from django.shortcuts import render,get_object_or_404
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Item
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic.detail import DetailView
from borrow.models import Order
import os 
# Create your views here.

def home(request):
    return render(request, 'home.html')


class ItemList(LoginRequiredMixin, ListView):
    model = Item
    context_object_name = 'items'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = context['items'].filter(
            contributor=self.request.user)
        return context


class ItemCreate(LoginRequiredMixin, CreateView):
    model = Item
    fields = ['item_name', 'item_description', 'item_category','item_address', 'item_deposit_require', 'item_image']
    success_url = reverse_lazy('items')

    def form_valid(self, form):
        form.instance.contributor = self.request.user
        messages.success(self.request, "The item was created successfully.")
        return super().form_valid(form)
    
    
class ItemDetail(LoginRequiredMixin, DetailView):
    model = Item
    context_object_name = 'item'
    
    def get_queryset(self):
        base_qs = super(ItemDetail, self).get_queryset()
        return base_qs.filter(contributor=self.request.user)

class ItemUpdate(LoginRequiredMixin, UpdateView):
    model = Item
    fields = ['item_name', 'item_description', 'item_category', 'item_address', 'item_deposit_require', 'item_image']
    success_url = reverse_lazy('items')
    
    def form_valid(self, form):
        item_instance = form.instance

        if not item_instance.item_available:
            messages.error(self.request, "This item has been borrowing now !!")
            return super(ItemUpdate, self).form_invalid(form)

        if 'item_image' in form.changed_data and item_instance.item_image:
            old_image_path = item_instance.item_image.path
            if os.path.exists(old_image_path):
                os.remove(old_image_path)

        messages.success(self.request, "The item was updated successfully.")
        return super(ItemUpdate, self).form_valid(form)
    
    def get_queryset(self):
        base_qs = super(ItemUpdate, self).get_queryset()
        return base_qs.filter(contributor=self.request.user)

class ItemDelete(LoginRequiredMixin, DeleteView):
    model = Item
    context_object_name = 'item'
    success_url = reverse_lazy('items')
    
    def form_valid(self, form):
        item_instance = self.get_object()
        
        if item_instance.item_image:
            image_path = item_instance.item_image.path
            if os.path.exists(image_path):
                os.remove(image_path)
                
        messages.success(self.request, "The item was deleted successfully.")
        return super(ItemDelete,self).form_valid(form)
      
    def get_queryset(self):
        base_qs = super(ItemDelete, self).get_queryset()
        return base_qs.filter(contributor=self.request.user)
