from django import forms
from django.contrib.auth.models import User
from .models import *

class CustomerRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    municipality = forms.ModelChoiceField(queryset=Municipality.objects.filter(is_approved=True))
    
    class Meta:
        model = Customer
        fields = ['phone', 'address', 'municipality']

class CollectionAgentForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = CollectionAgent
        fields = ['phone', 'address', 'vehicle_number', 'municipality']

class RecyclerForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = Recycler
        fields = ['company_name', 'phone', 'address', 'municipality']

class LinkBinForm(forms.Form):
    bin_id = forms.CharField(max_length=50)

class ManualBookingForm(forms.Form):
    collection_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

class RecyclerBookingForm(forms.ModelForm):
    class Meta:
        model = RecyclerBooking
        fields = ['recycler', 'waste_type', 'weight', 'collection_date']
        widgets = {
            'collection_date': forms.DateInput(attrs={'type': 'date'}),
        }

class EnquiryForm(forms.ModelForm):
    class Meta:
        model = Enquiry
        fields = ['subject', 'message']
