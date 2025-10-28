from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import SmartBin, CollectionRequest

@login_required
def customer_dashboard(request):
    bins = SmartBin.objects.filter(customer=request.user)
    pending_requests = CollectionRequest.objects.filter(customer=request.user, status='pending')
    
    return render(request, 'customers/dashboard.html', {
        'bins': bins,
        'pending_requests': pending_requests
    })

@login_required
def book_collection(request, bin_id):
    if request.method == 'POST':
        bin = SmartBin.objects.get(bin_id=bin_id, customer=request.user)
        CollectionRequest.objects.create(
            bin=bin,
            customer=request.user,
            status='pending'
        )
        return redirect('customer_dashboard')