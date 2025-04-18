import random
import string
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from products.models import Order

def generate_otp(length=6):
    characters = string.digits
    otp = ''.join(random.choice(characters) for _ in range(length))
    return otp

def send_otp_email(email, otp):
    subject = 'Your OTP for Login'
    message = f'Your OTP is: {otp}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)

def send_due_payment_emails():
    today = timezone.now().date()
    orders = Order.objects.filter(
        next_due_date__isnull=False,
        due_amount__gt=0
    )

    for order in orders:
        reminder_date = order.next_due_date - timedelta(days=7)

        if reminder_date == today:
            customer = order.customer
            subject = "Payment Reminder: Your installment is due soon!"
            message = (
                f"Hello {customer.username},\n\n"
                f"This is a reminder that your next installment of {order.due_amount} "
                f"for '{order.product.name}' is due on {order.next_due_date}.\n\n"
                "Please make sure to complete the payment by the due date.\n\n"
                "Thank you for shopping with us!"
            )
            send_mail(
                subject,
                message,
                'mubassir.work@gmail.com',  
                [customer.email],
                fail_silently=False
            )