from pharmacy.models import Stock, EmailReceivers
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib import messages
from apscheduler.schedulers.background import BackgroundScheduler
import datetime
from django.conf import settings

def day_check_notification():
    nearing_expiry_date = Stock.objects.filter(valid_to__date__gt=datetime.datetime.now().date(),
        valid_to__date__lte=datetime.datetime.now().date() + datetime.timedelta(days=30))
    out_of_stock = Stock.objects.filter(quantity__lte=1)

    if nearing_expiry_date or out_of_stock:
        try:
            recievers = EmailReceivers.objects.filter(active=True)
            to = []
            from_email = settings.DEFAULT_FROM_EMAIL
            if recievers:
                for r in recievers:
                    to.append(r.email)
            else:
                to.append("tolybrian6@gmail.com")

            subject = 'DAILY STOCK CHECK'
            html_message = render_to_string('posApp/mails/daily_stock.html', {
                'nearing_expiry_date': nearing_expiry_date, 'out_of_stock': out_of_stock,
                'out_of_stock_number': len(out_of_stock), 'nearing_expiry_date_number': len(nearing_expiry_date)})

            message = EmailMessage(subject, html_message, from_email, to)
            message.content_subtype = 'html'
            message.send()
        except Exception as e:
            print(e)
            # messages.error(request, "Error sening daily stock check email please contact the developer")
    else:
        pass

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(day_check_notification, 'interval', minutes=1440) # every day: 1440 minuttes
    scheduler.start()