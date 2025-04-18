from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_due_payment_email(email, due_date):
    send_mail(
        'Payment Reminder',
        f'You have a payment due on {due_date}. Please make sure to pay it on time.',
        'mubassir.work@gmail.com',
        [email],
        fail_silently=False,
    )