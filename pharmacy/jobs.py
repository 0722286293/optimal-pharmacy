from io import BytesIO
import pytz
import datetime

from config.settings import DEFAULT_FROM_EMAIL
from .utils import render_to_pdf
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage
from django.template.loader import get_template, render_to_string
from xhtml2pdf import pisa

from pharmacy.models import Stock, EmailReceivers

utc = pytz.UTC
get_today = datetime.datetime.now().replace(tzinfo=utc)

def send_expiring_stock_email():
    this_month = get_today + datetime.timedelta(days=30)
    expiring_this_month = Stock.objects.filter(
        valid_to__lte=this_month
    )
    receivers = []
    mail_receivers = EmailReceivers.objects.filter(active=True)
    if len(mail_receivers) > 0:
        receivers = mail_receivers
    else:
        receivers = [DEFAULT_FROM_EMAIL]
    
    from_email = DEFAULT_FROM_EMAIL
    to_email = receivers
    subject = "ITEMS IN STOCK ABOUT TO EXPIRE"
    html_content = "pharmacy/mails/expiring_stock.html"