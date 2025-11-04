from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout_view'),
    path('register/customer/', views.customer_register, name='customer_register'),
    
    # Customer
    path('customer/dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('customer/link-bin/', views.link_bin, name='link_bin'),
    path('customer/wallet/', views.customer_wallet, name='customer_wallet'),
    path('customer/book-recycler/', views.book_recycler, name='book_recycler'),
    path('customer/verify/<int:collection_id>/', views.verify_collection, name='verify_collection'),
    
    # Collection Agent
    path('agent/dashboard/', views.agent_dashboard, name='agent_dashboard'),
    path('agent/collect/<int:collection_id>/', views.collect_waste, name='collect_waste'),
    
    # Municipality
    path('municipality/dashboard/', views.municipality_dashboard, name='municipality_dashboard'),
    path('municipality/approve-customer/<int:customer_id>/', views.approve_customer, name='approve_customer'),
    path('municipality/assign-task/<int:bin_id>/', views.assign_collection_task, name='assign_collection_task'),
    
    # Recycler
    path('recycler/dashboard/', views.recycler_dashboard, name='recycler_dashboard'),
    path('recycler/assign/<int:booking_id>/', views.assign_recycler_task, name='assign_recycler_task'),
    
    # Admin
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    
    # API
    path('api/bin/update/', views.update_bin_status, name='update_bin_status'),
]