from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid

class BaseModel(models.Model):
    """Abstract base model with common fields"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        abstract = True

class UserProfile(BaseModel):
    """Base user profile for all user types"""
    USER_TYPES = (
        ('customer', 'Customer'),
        ('agent', 'Collection Agent'),
        ('municipality', 'Municipality'),
        ('recycler', 'Recycler'),
        ('admin', 'Admin'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    user_type = models.CharField(max_length=20, choices=USER_TYPES)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=100, default='')
    state = models.CharField(max_length=100, default='Kerala')
    pincode = models.CharField(max_length=6, default='')
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    municipality = models.ForeignKey('Municipality', on_delete=models.SET_NULL, 
                                    null=True, blank=True, related_name='users')
    
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.user_type}"
    
    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

class Municipality(BaseModel):
    """Municipality/Local Government"""
    name = models.CharField(max_length=200)
    admin_user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='municipality_admin')
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, default='Kerala')
    pincode = models.CharField(max_length=6)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Municipalities'

class Wallet(BaseModel):
    """Digital wallet for payments"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    def __str__(self):
        return f"{self.user.username} - ₹{self.balance}"
    
    def add_money(self, amount):
        """Add money to wallet"""
        self.balance += amount
        self.save()
        
        # Create transaction record
        WalletTransaction.objects.create(
            wallet=self,
            transaction_type='credit',
            amount=amount,
            description='Money added to wallet'
        )
        return True
        
    def deduct_money(self, amount, description=''):
        """Deduct money from wallet"""
        if self.balance >= amount:
            self.balance -= amount
            self.save()
            
            # Create transaction record
            WalletTransaction.objects.create(
                wallet=self,
                transaction_type='debit',
                amount=amount,
                description=description or 'Payment made'
            )
            return True
        return False
    
    class Meta:
        verbose_name = 'Wallet'
        verbose_name_plural = 'Wallets'

class WalletTransaction(BaseModel):
    """Wallet transaction history"""
    TRANSACTION_TYPES = (
        ('credit', 'Credit'),
        ('debit', 'Debit'),
    )
    
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    transaction_id = models.CharField(max_length=50, unique=True)
    
    def save(self, *args, **kwargs):
        if not self.transaction_id:
            self.transaction_id = f"TXN{uuid.uuid4().hex[:12].upper()}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.wallet.user.username} - {self.transaction_type} - ₹{self.amount}"
    
    class Meta:
        verbose_name = 'Wallet Transaction'
        verbose_name_plural = 'Wallet Transactions'
        ordering = ['-created_at']

class SmartBin(BaseModel):
    """IoT Smart Waste Bin"""
    BIN_STATUS = (
        ('empty', 'Empty'),
        ('partial', 'Partially Full'),
        ('full', 'Full'),
        ('overflow', 'Overflow'),
    )
    
    bin_id = models.CharField(max_length=50, unique=True)
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, 
                                related_name='bins')
    municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE, 
                                    related_name='bins')
    location = models.CharField(max_length=200)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    status = models.CharField(max_length=20, choices=BIN_STATUS, default='empty')
    fill_percentage = models.IntegerField(default=0)
    last_collection_date = models.DateTimeField(null=True, blank=True)
    next_collection_date = models.DateTimeField(null=True, blank=True)
    is_linked = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.bin_id} - {self.status}"
    
    def update_status(self, fill_percentage):
        """Update bin status based on fill percentage"""
        self.fill_percentage = fill_percentage
        
        if fill_percentage < 25:
            self.status = 'empty'
        elif fill_percentage < 75:
            self.status = 'partial'
        elif fill_percentage < 90:
            self.status = 'full'
        else:
            self.status = 'overflow'
        
        self.save()
    
    class Meta:
        verbose_name = 'Smart Bin'
        verbose_name_plural = 'Smart Bins'

class WasteCollection(BaseModel):
    """Waste collection records"""
    COLLECTION_STATUS = (
        ('pending', 'Pending'),
        ('assigned', 'Assigned'),
        ('collected', 'Collected'),
        ('verified', 'Verified'),
        ('cancelled', 'Cancelled'),
    )
    
    bin = models.ForeignKey(SmartBin, on_delete=models.CASCADE, related_name='collections')
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='waste_collections')
    collection_agent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, 
                                        related_name='assigned_collections')
    municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE)
    scheduled_date = models.DateTimeField()
    collection_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=COLLECTION_STATUS, default='pending')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_status = models.CharField(max_length=20, default='pending')
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.bin.bin_id} - {self.scheduled_date.date()} - {self.status}"
    
    class Meta:
        verbose_name = 'Waste Collection'
        verbose_name_plural = 'Waste Collections'
        ordering = ['-scheduled_date']

class RecyclingRequest(BaseModel):
    """Recycling requests from customers"""
    REQUEST_STATUS = (
        ('pending', 'Pending'),
        ('assigned', 'Assigned'),
        ('collected', 'Collected'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    WASTE_TYPES = (
        ('plastic', 'Plastic'),
        ('paper', 'Paper'),
        ('metal', 'Metal/Tins'),
        ('glass', 'Glass'),
        ('electronics', 'Electronics'),
        ('other', 'Other'),
    )
    
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recycling_requests')
    recycler = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recycling_tasks')
    collection_agent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, 
                                        related_name='recycling_collections')
    waste_type = models.CharField(max_length=20, choices=WASTE_TYPES)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, help_text='in kg')
    scheduled_date = models.DateTimeField()
    collection_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=REQUEST_STATUS, default='pending')
    price_per_kg = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_status = models.CharField(max_length=20, default='pending')
    notes = models.TextField(blank=True, null=True)
    
    def save(self, *args, **kwargs):
        self.total_amount = self.quantity * self.price_per_kg
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.customer.username} - {self.waste_type} - {self.quantity}kg"
    
    class Meta:
        verbose_name = 'Recycling Request'
        verbose_name_plural = 'Recycling Requests'
        ordering = ['-scheduled_date']

class Enquiry(BaseModel):
    """Enquiry/Complaint system"""
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enquiries')
    subject = models.CharField(max_length=200)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    response = models.TextField(blank=True, null=True)
    responded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, 
                                    related_name='responded_enquiries')
    response_date = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name_plural = 'Enquiries'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.subject}"

class PriceConfiguration(BaseModel):
    """Price configuration for waste collection and recycling"""
    municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE, 
                                    related_name='price_configs', null=True, blank=True)
    recycler = models.ForeignKey(User, on_delete=models.CASCADE, 
                                related_name='price_configs', null=True, blank=True)
    waste_type = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=20, default='per collection')
    
    def __str__(self):
        owner = self.municipality.name if self.municipality else self.recycler.username
        return f"{owner} - {self.waste_type} - ₹{self.price}"
    
    class Meta:
        verbose_name = 'Price Configuration'
        verbose_name_plural = 'Price Configurations'
