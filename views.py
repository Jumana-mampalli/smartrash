from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, date
import json

# Home and Authentication Views
def home(request):
    return render(request, 'home.html')

def customer_register(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            customer = form.save(commit=False)
            customer.user = user
            customer.save()
            messages.success(request, 'Registration successful! Wait for approval.')
            return redirect('login_view')
    else:
        form = CustomerRegistrationForm()
    return render(request, 'register_customer.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        
        if user:
            login(request, user)
            
            # Check user type and redirect
            if hasattr(user, 'customer'):
                if user.customer.is_approved:
                    return redirect('customer_dashboard')
                else:
                    messages.error(request, 'Your account is pending approval')
                    logout(request)
            elif hasattr(user, 'collectionagent'):
                if user.collectionagent.is_approved:
                    return redirect('agent_dashboard')
                else:
                    messages.error(request, 'Your account is pending approval')
                    logout(request)
            elif hasattr(user, 'municipality'):
                return redirect('municipality_dashboard')
            elif hasattr(user, 'recycler'):
                if user.recycler.is_approved:
                    return redirect('recycler_dashboard')
                else:
                    messages.error(request, 'Your account is pending approval')
                    logout(request)
            elif user.is_superuser:
                return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid credentials')
    
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

# Customer Views
@login_required
def customer_dashboard(request):
    customer = request.user.customer
    bin = SmartBin.objects.filter(customer=customer).first()
    collections = WasteCollection.objects.filter(customer=customer).order_by('-created_at')[:5]
    recycler_bookings = RecyclerBooking.objects.filter(customer=customer).order_by('-created_at')[:5]
    
    context = {
        'customer': customer,
        'bin': bin,
        'collections': collections,
        'recycler_bookings': recycler_bookings,
    }
    return render(request, 'customer_dashboard.html', context)

@login_required
def link_bin(request):
    customer = request.user.customer
    
    if request.method == 'POST':
        form = LinkBinForm(request.POST)
        if form.is_valid():
            bin_id = form.cleaned_data['bin_id']
            try:
                bin = SmartBin.objects.get(bin_id=bin_id, customer=None)
                bin.customer = customer
                bin.save()
                messages.success(request, 'Bin linked successfully!')
                return redirect('customer_dashboard')
            except SmartBin.DoesNotExist:
                messages.error(request, 'Invalid bin ID or already linked')
    else:
        form = LinkBinForm()
    
    return render(request, 'link_bin.html', {'form': form})

@login_required
def customer_wallet(request):
    customer = request.user.customer
    
    if request.method == 'POST':
        amount = float(request.POST.get('amount', 0))
        if amount > 0:
            customer.wallet_balance += amount
            customer.save()
            messages.success(request, f'₹{amount} added to wallet!')
    
    return render(request, 'customer_wallet.html', {'customer': customer})

@login_required
def book_recycler(request):
    customer = request.user.customer
    
    if request.method == 'POST':
        form = RecyclerBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.customer = customer
            
            # Calculate amount based on waste type and weight
            recycler = booking.recycler
            weight = booking.weight
            if booking.waste_type == 'plastic':
                booking.amount = weight * recycler.plastic_rate
            elif booking.waste_type == 'paper':
                booking.amount = weight * recycler.paper_rate
            elif booking.waste_type == 'metal':
                booking.amount = weight * recycler.metal_rate
            
            booking.save()
            messages.success(request, 'Recycler booking created!')
            return redirect('customer_dashboard')
    else:
        form = RecyclerBookingForm()
    
    recyclers = Recycler.objects.filter(is_approved=True, municipality=customer.municipality)
    return render(request, 'book_recycler.html', {'form': form, 'recyclers': recyclers})

# Collection Agent Views
@login_required
def agent_dashboard(request):
    agent = request.user.collectionagent
    tasks = WasteCollection.objects.filter(
        collection_agent=agent,
        status__in=['assigned', 'collected']
    ).order_by('collection_date')
    
    recycler_tasks = RecyclerBooking.objects.filter(
        collection_agent=agent,
        status__in=['assigned']
    ).order_by('collection_date')
    
    context = {
        'agent': agent,
        'tasks': tasks,
        'recycler_tasks': recycler_tasks,
    }
    return render(request, 'agent_dashboard.html', context)

@login_required
def collect_waste(request, collection_id):
    collection = get_object_or_404(WasteCollection, id=collection_id)
    
    if request.method == 'POST':
        bin_id = request.POST.get('bin_id')
        
        if collection.bin and collection.bin.bin_id == bin_id:
            collection.status = 'collected'
            collection.collected_at = datetime.now()
            collection.save()
            messages.success(request, 'Waste collected! Waiting for customer verification.')
        else:
            messages.error(request, 'Invalid bin ID')
        
        return redirect('agent_dashboard')
    
    return render(request, 'collect_waste.html', {'collection': collection})

@login_required
def verify_collection(request, collection_id):
    collection = get_object_or_404(WasteCollection, id=collection_id)
    customer = request.user.customer
    
    if collection.customer == customer and collection.status == 'collected':
        if customer.wallet_balance >= collection.amount:
            customer.wallet_balance -= collection.amount
            customer.save()
            
            collection.municipality.wallet_balance += collection.amount
            collection.municipality.save()
            
            collection.status = 'verified'
            collection.save()
            
            messages.success(request, 'Collection verified and payment completed!')
        else:
            messages.error(request, 'Insufficient wallet balance')
    
    return redirect('customer_dashboard')

# Municipality Views
@login_required
def municipality_dashboard(request):
    municipality = request.user.municipality
    
    pending_customers = Customer.objects.filter(municipality=municipality, is_approved=False)
    pending_agents = CollectionAgent.objects.filter(municipality=municipality, is_approved=False)
    pending_recyclers = Recycler.objects.filter(municipality=municipality, is_approved=False)
    
    full_bins = SmartBin.objects.filter(municipality=municipality, is_full=True, customer__isnull=False)
    
    pending_collections = WasteCollection.objects.filter(
        municipality=municipality,
        status='pending'
    )
    
    context = {
        'municipality': municipality,
        'pending_customers': pending_customers,
        'pending_agents': pending_agents,
        'pending_recyclers': pending_recyclers,
        'full_bins': full_bins,
        'pending_collections': pending_collections,
    }
    return render(request, 'municipality_dashboard.html', context)

@login_required
def approve_customer(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    customer.is_approved = True
    customer.save()
    messages.success(request, f'Customer {customer.user.username} approved!')
    return redirect('municipality_dashboard')

@login_required
def assign_collection_task(request, bin_id):
    bin = get_object_or_404(SmartBin, id=bin_id)
    municipality = request.user.municipality
    
    if request.method == 'POST':
        agent_id = request.POST.get('agent_id')
        collection_date = request.POST.get('collection_date')
        
        agent = get_object_or_404(CollectionAgent, id=agent_id)
        
        collection = WasteCollection.objects.create(
            customer=bin.customer,
            bin=bin,
            municipality=municipality,
            collection_agent=agent,
            collection_date=collection_date,
            amount=municipality.collection_rate,
            status='assigned'
        )
        
        bin.is_full = False
        bin.save()
        
        messages.success(request, 'Task assigned successfully!')
        return redirect('municipality_dashboard')
    
    agents = CollectionAgent.objects.filter(municipality=municipality, is_approved=True)
    return render(request, 'assign_task.html', {'bin': bin, 'agents': agents})

# Recycler Views
@login_required
def recycler_dashboard(request):
    recycler = request.user.recycler
    
    pending_bookings = RecyclerBooking.objects.filter(
        recycler=recycler,
        status='pending'
    )
    
    assigned_bookings = RecyclerBooking.objects.filter(
        recycler=recycler,
        status='assigned'
    )
    
    context = {
        'recycler': recycler,
        'pending_bookings': pending_bookings,
        'assigned_bookings': assigned_bookings,
    }
    return render(request, 'recycler_dashboard.html', context)

@login_required
def assign_recycler_task(request, booking_id):
    booking = get_object_or_404(RecyclerBooking, id=booking_id)
    recycler = request.user.recycler
    
    if request.method == 'POST':
        agent_id = request.POST.get('agent_id')
        agent = get_object_or_404(CollectionAgent, id=agent_id)
        
        booking.collection_agent = agent
        booking.status = 'assigned'
        booking.save()
        
        messages.success(request, 'Collection agent assigned!')
        return redirect('recycler_dashboard')
    
    agents = CollectionAgent.objects.filter(municipality=recycler.municipality, is_approved=True)
    return render(request, 'assign_recycler_task.html', {'booking': booking, 'agents': agents})

# Admin Views
@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect('home')
    
    municipalities = Municipality.objects.all()
    return render(request, 'admin_dashboard.html', {'municipalities': municipalities})

# API for Smart Bin (IoT)
@csrf_exempt
def update_bin_status(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            bin_id = data.get('bin_id')
            level = int(data.get('level', 0))
            
            bin = SmartBin.objects.get(bin_id=bin_id)
            bin.current_level = level
            bin.is_full = level >= 75
            bin.save()
            
            return JsonResponse({'status': 'success', 'message': 'Bin status updated'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})
