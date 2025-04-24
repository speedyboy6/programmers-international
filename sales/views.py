from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Enquiry
from .forms import EnquiryForm # Import the form
from django.contrib import messages # Import messages framework
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from io import BytesIO
from datetime import datetime

# Create your views here.

def product_list(request):
    products = Product.objects.all()
    return render(request, 'sales/product_list.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        # Handle enquiry form submission
        form = EnquiryForm(request.POST)
        if form.is_valid():
            enquiry = form.save(commit=False)
            enquiry.product = product
            enquiry.save()
            messages.success(request, f'Your enquiry for "{product.name}" has been submitted successfully!')
            return redirect('sales:product_detail', pk=product.pk) # Redirect to same page after success
        else:
            # Form is invalid, render the page again with errors
            messages.error(request, 'There was an error with your submission. Please check the form.')
            pass # Fall through to render the template with the invalid form
    else:
        form = EnquiryForm() # Create a blank form for GET request

    return render(request, 'sales/product_detail.html', {'product': product, 'form': form})

# PDF export is handled via admin action now.
