from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
import random
import string

def generate_bin_id():
    """Generate unique bin ID"""
    return 'BIN' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

def send_notification_email(to_email, subject, message):
    """Send notification email"""
    try:
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [to_email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def notify_bin_full(bin):
    """Notify when bin is full"""
    if bin.customer:
        message = f"Your smart bin {bin.bin_id} is {bin.fill_percentage}% full. Collection will be scheduled soon."
        send_notification_email(
            bin.customer.email,
            'Smart Bin Alert - Collection Needed',
            message
        )
    
    if bin.municipality:
        message = f"Smart bin {bin.bin_id} at {bin.location} is {bin.fill_percentage}% full and needs collection."
        send_notification_email(
            bin.municipality.email,
            'Smart Bin Alert - Collection Required',
            message
        )

def notify_collection_assigned(collection):
    """Notify when collection is assigned"""
    # Notify customer
    customer_message = f"Waste collection scheduled for {collection.scheduled_date.strftime('%Y-%m-%d %H:%M')}."
    send_notification_email(
        collection.customer.email,
        'Waste Collection Scheduled',
        customer_message
    )
    
    # Notify collection agent
    if collection.collection_agent:
        agent_message = f"New collection task assigned. Bin: {collection.bin.bin_id}, Date: {collection.scheduled_date.strftime('%Y-%m-%d %H:%M')}"
        send_notification_email(
            collection.collection_agent.email,
            'New Collection Task',
            agent_message
        )

def calculate_collection_charge(municipality):
    """Calculate collection charge"""
    try:
        price_config = municipality.price_configs.filter(waste_type='general').first()
        if price_config:
            return price_config.price
        return 50.00  # Default price
    except:
        return 50.00
