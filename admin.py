from django.contrib import admin
from .models import (
    UserProfile, Municipality, Wallet, WalletTransaction,
    SmartBin, WasteCollection, RecyclingRequest, Enquiry, PriceConfiguration
)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_type', 'phone', 'is_approved', 'created_at']
    list_filter = ['user_type', 'is_approved', 'municipality']
    search_fields = ['user__username', 'user__email', 'phone']

@admin.register(Municipality)
class MunicipalityAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'phone', 'email']
    search_fields = ['name', 'city']

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ['user', 'balance', 'updated_at']
    search_fields = ['user__username']

@admin.register(WalletTransaction)
class WalletTransactionAdmin(admin.ModelAdmin):
    list_display = ['transaction_id', 'wallet', 'transaction_type', 'amount', 'created_at']
    list_filter = ['transaction_type', 'created_at']
    search_fields = ['transaction_id', 'wallet__user__username']

@admin.register(SmartBin)
class SmartBinAdmin(admin.ModelAdmin):
    list_display = ['bin_id', 'customer', 'status', 'fill_percentage', 'is_linked']
    list_filter = ['status', 'is_linked', 'municipality']
    search_fields = ['bin_id', 'customer__username']

@admin.register(WasteCollection)
class WasteCollectionAdmin(admin.ModelAdmin):
    list_display = ['bin', 'customer', 'collection_agent', 'scheduled_date', 'status', 'amount']
    list_filter = ['status', 'payment_status', 'scheduled_date']
    search_fields = ['bin__bin_id', 'customer__username']

@admin.register(RecyclingRequest)
class RecyclingRequestAdmin(admin.ModelAdmin):
    list_display = ['customer', 'waste_type', 'quantity', 'total_amount', 'status', 'scheduled_date']
    list_filter = ['status', 'waste_type', 'scheduled_date']
    search_fields = ['customer__username', 'recycler__username']

@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ['user', 'subject', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__username', 'subject']

@admin.register(PriceConfiguration)
class PriceConfigurationAdmin(admin.ModelAdmin):
    list_display = ['waste_type', 'price', 'unit', 'municipality', 'recycler']
    list_filter = ['waste_type']
