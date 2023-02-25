from posApp.models import StockNotifications
from pharmacy.models import Stock, EmailReceivers
from django.conf import settings

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib import messages

def low_stock(request):
    notifications = StockNotifications.objects.filter(resolved=False)
    len_notifications = len(notifications)
    return dict(low_stock_notifications=len_notifications)

def make_notifications(request):
    products = Stock.objects.all()
    nots = StockNotifications.objects.filter(resolved=False)
    out_of_stock_list = []

    if products:
        for prod in products:
            if prod.is_low_stock:
                    check_if_exists = StockNotifications.objects.filter(drug__id=prod.id, resolved=False)
                    if check_if_exists:
                        pass
                    else:
                        StockNotifications.objects.create(title=f"{prod.drug_name} is running out of stock", drug=prod)
                        out_of_stock_list.append(prod)
    
    if len(out_of_stock_list) > 0:
        # send email
        try:
            subject = 'DRUGS RUNNING OUT OF STOCK'
            html_message = render_to_string('posApp/mails/new_out_of_stock.html', {'drugs': out_of_stock_list})
            # plain_message = strip_tags(html_message)
            from_email = settings.DEFAULT_FROM_EMAIL
            receivers = EmailReceivers.objects.filter(active=True)
            to = []
            if receivers:
                for r in receivers:
                    to.append(r.email)
            else:
                to.append("tolybrian6@gmail.com")
            
            message = EmailMessage(subject, html_message, from_email, to)
            message.content_subtype = 'html'
            message.send()
            
            messages.success(request, "Low stock email sent successfully")
        except Exception as e:
            print(e)
            messages.error(request, "Error while sending email for low stock, please contact the developer")

    return {"True": True}
                        

def resolve_stock_notifaction(request):
    nots = StockNotifications.objects.filter(resolved=False)
    if nots:
        for n in nots:
            p_id = n.drug.id
            product = Stock.objects.get(id=p_id)
            if product.is_low_stock:
                n.resolved = False
                n.save()
            elif product.is_low_stock == False:
                n.resolved = True
                n.save()
        return {"True": True}
    else:
        return {"False": False}
    
