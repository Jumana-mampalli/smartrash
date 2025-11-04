from django.db import models
from django.contrib.auth.models import User

class Municipality(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    area = models.CharField(max_length=200)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    wallet_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    collection_rate = models.DecimalField(max_digits=10, decimal_places=2, default=50)
    is_approved = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    wallet_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    bin_id = models.CharField(max_length=50, blank=True, null=True, unique=True)
    is_approved = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.username

class CollectionAgent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    vehicle_number = models.CharField(max_length=50)
    is_approved = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.username

class Recycler(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    wallet_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    plastic_rate = models.DecimalField(max_digits=10, decimal_places=2, default=20)
    paper_rate = models.DecimalField(max_digits=10, decimal_places=2, default=15)
    metal_rate = models.DecimalField(max_digits=10, decimal_places=2, default=30)
    is_approved = models.BooleanField(default=False)
    
    def __str__(self):
        return self.company_name

class SmartBin(models.Model):
    bin_id = models.CharField(max_length=50, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE)
    current_level = models.IntegerField(default=0)  # 0-100 percentage
    is_full = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Bin {self.bin_id}"

class WasteCollection(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('assigned', 'Assigned'),
        ('collected', 'Collected'),
        ('verified', 'Verified'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    bin = models.ForeignKey(SmartBin, on_delete=models.CASCADE, null=True)
    municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE)
    collection_agent = models.ForeignKey(CollectionAgent, on_delete=models.SET_NULL, null=True, blank=True)
    collection_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    collected_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Collection {self.id} - {self.customer.user.username}"

class RecyclerBooking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('assigned', 'Assigned'),
        ('collected', 'Collected'),
    ]
    
    WASTE_TYPES = [
        ('plastic', 'Plastic'),
        ('paper', 'Paper'),
        ('metal', 'Metal'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    recycler = models.ForeignKey(Recycler, on_delete=models.CASCADE)
    collection_agent = models.ForeignKey(CollectionAgent, on_delete=models.SET_NULL, null=True, blank=True)
    waste_type = models.CharField(max_length=20, choices=WASTE_TYPES)
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    collection_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Recycler Booking {self.id}"

class Enquiry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    reply = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_replied = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Enquiry by {self.user.username}"
