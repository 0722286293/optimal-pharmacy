from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect

from django.contrib import messages
from .decorators import *
from .models import *
from django.utils.translation import gettext_lazy as _

from slick_reporting.views import SlickReportView
from slick_reporting.fields import SlickReportField
from django.db.models import Sum

@unautheticated_user
def loginPage(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user != None:
            login(request, user)
            user_type = user.user_type
            if user_type == '1':
                return redirect('/')
                
            elif user_type == '2':
                return redirect('pharmacist_home')

            elif user_type == '3':
                return redirect('doctor_home')
            elif user_type == '4':
                return redirect('clerk_home')
            elif user_type == '5':
                return redirect('patient_home')
                
           
            else:
                messages.error(request, "Invalid Login!")
                return redirect('login')
        else:
            messages.error(request, "Invalid Login Credentials!")
            return redirect('login')
    
    return render(request,'login.html')

@login_required
def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required
def pos(request):
    drugs = Stock.objects.filter(quantity__gte=1)
    product_json = []
    for product in drugs:
        product_json.append({"id":product.id, "name":product.drug_name, "price":float(product.selling_price)})

    return render(request, "hod_templates/pos.html", context={
        "products": drugs,
        "product_json": product_json,
    })

@login_required
def checkout_modal(request):
    grand_total = 0
    if 'grand_total' in request.GET:
        grand_total = request.GET['grand_total']

    return render(request, "hod_templates/checkout_modal", context={"grand_total": grand_total})

@login_required
def save_pos(request):
    pass

@login_required
def receipt(request):
    id = request.GET.get('id')
    sales = Sales.objects.filter(id = id).first()
    transaction = {}
    for field in Sales._meta.get_fields():
        if field.related_model is None:
            transaction[field.name] = getattr(sales, field.name)
    
    ItemList = DrugItemsSales.objects.filter(sale_id=sales).all()

    context = {
        "transaction" : transaction,
        "salesItems" : ItemList
    }
    return render(request, 'hod_templates/receipt.html',context)

class SalesReportView(SlickReportView):
   report_model = DrugItemsSales
   date_field = 'created'
   group_by = 'drug'
   columns = ['drug_name', '__time_series__',
               SlickReportField.create(Sum, 'total', name='total__sum', verbose_name=_('Grand Total (Ksh.)')),
               ]
   time_series_pattern = 'monthly'
   time_series_columns = [
       SlickReportField.create(Sum, 'total', name='total__sum', verbose_name=_('Sales (Ksh.)'))
   ]

   chart_settings = [
        {'type': 'bar',
         'data_source': ['total__sum'],
         'title_source': ['drug_name'],
         'title': 'Sales per month',
         'plot_total': True,
         }
    ]
   
class DrugsReportView(SlickReportView):
    report_model = DrugItemsSales
    date_field = 'created'
    group_by = 'drug'
    columns = ['drug_name', '__time_series__',
               SlickReportField.create(Sum, 'qty', name='total__qty', verbose_name=_('Total Sold')),
               ]
    
    time_series_columns = [
        SlickReportField.create(Sum, 'qty', name='total__qty', verbose_name=_('Total Sold')),
    ]

    chart_settings = [
        {'type': 'pie',
         'data_source': ['total__qty'],
         'title_source': ['drug_name'],
         'title': 'Total Drugs Sold Per month',
         'plot_total': True,
         },
         {'type': 'bar',
         'data_source': ['total__qty'],
         'title_source': ['drug_name'],
         'title': 'Total Drugs Sold Per month',
         'plot_total': True,
         }
    ]