from django import forms
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, ListView
from django.views import View
from .models import Product
# Create your views here.

"""def homePageView(request):
    return HttpResponse('Hello World!')"""
    
class HomePageView(TemplateView):
    template_name = 'pages/home.html'

template_name="pages/products/product_success.html"
    
class AboutPageView(TemplateView):
    template_name = 'pages/about.html'
    
    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs) 
        context.update({ 
            "title": "About us - Online Store", 
            "subtitle": "About us", 
            "description": "This is an about page ...", 
            "author": "Developed by: Jennifer", 
        }) 
 
        return context

class ContactPageView(TemplateView):
    template_name = 'pages/contact.html'
    
    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs) 
        context.update({ 
            "title": "Our contact - Online Store", 
            "subtitle": "Our contact", 
            "description": "email: Onlina@gmail.com/n address: Cra 57 #65-2/n Phone number:+57 310 000 0000", 
            "author": "Developed by: Jennifer", 
        }) 
 
        return context

"""class Product: 
    products = [ 
        {"id":"1", "name":"TV", "description":"Best TV"}, 
        {"id":"2", "name":"iPhone", "description":"Best iPhone"}, 
        {"id":"3", "name":"Chromecast", "description":"Best Chromecast"}, 
        {"id":"4", "name":"Glasses", "description":"Best Glasses"} 
    ] """
 
class ProductIndexView(View): 
    template_name = 'pages/products/index.html' 
 
    def get(self, request): 
        viewData = {} 
        viewData["title"] = "Products - Online Store" 
        viewData["subtitle"] =  "List of products" 
        viewData["products"] = Product.objects.all() 
 
        return render(request, self.template_name, viewData) 
 
class ProductShowView(View): 
    template_name = 'pages/products/show.html' 
 
 
    def get(self, request, id): 
        try:
            product_id = int(id)
            if product_id < 1:
                raise ValueError("Product id must be 1 or greater")
            product = get_object_or_404(Product, pk=product_id) 
             
        except(ValueError, IndexError): 
            return HttpResponseRedirect(reverse('home'))
        
        viewData = {} 
        product = get_object_or_404(Product, pk=product_id) 
        viewData["title"] = product.name + " - Online Store" 
        viewData["subtitle"] =  product.name + " - Product information" 
        viewData["product"] = product 
 
        return render(request, self.template_name, viewData)
    
class ProductForm(forms.ModelForm): 
    #name = forms.CharField(required=True) 
    #price = forms.FloatField(required=True) 
    class Meta:
        model = Product
        fields = ['name','price']
        
 
class ProductCreateView(View): 
    template_name = 'pages/products/create.html' 
 
    def get(self, request): 
        form = ProductForm() 
        viewData = {} 
        viewData["title"] = "Create product" 
        viewData["form"] = form 
        return render(request, self.template_name, viewData) 
 
    def post(self, request): 
        form = ProductForm(request.POST) 
        if form.is_valid(): 
            form.save()
            messages.success(request, "Product created successfully!")
            return redirect('product_success')  
        else: 
            return render(request, self.template_name, {"title": "Create product", "form": form})
        
class SuccessView(TemplateView):
    template_name = 'pages/products/product_success.html'
    
class ProductListView(ListView): 
    model = Product 
    template_name = 'product_list.html' 
    context_object_name = 'products'  # This will allow you to loop through 'products' in your template 
 
    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs) 
        context['title'] = 'Products - Online Store' 
        context['subtitle'] = 'List of products' 
        return context    