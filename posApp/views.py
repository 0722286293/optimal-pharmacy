from pickle import FALSE
from django.urls import reverse
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Count, Sum
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import json, sys
from datetime import date, datetime
from django.views.generic import DeleteView
from django.conf import settings
from pharmacy.models import Stock, Sales, DrugItemsSales
from .models import StockNotifications

@login_required
def pos(request):
    products = Stock.objects.filter(quantity__gte=1, valid_to__date__lte=datetime.now().date())
    product_json = []
    
    for product in products:
        product_json.append({'id':product.id, 'name':product.drug_name, 'price':float(product.selling_price)})
        
    context = {
        'page_title' : "Point of Sale",
        'products' : products,
        'product_json' : json.dumps(product_json)
    }
    return render(request, 'posApp/pos.html', context)

@login_required
def checkout_modal(request):
    grand_total = 0
    if 'grand_total' in request.GET:
        grand_total = request.GET['grand_total']
    context = {
        'grand_total' : grand_total,
    }
    return render(request, 'posApp/checkout.html', context)

@login_required
def save_pos(request):
    resp = {'status':'failed','msg':''}
    print(resp)
    data = request.POST
    print(data)
    pref = datetime.now().year + datetime.now().year
    i = 1
    while True:
        code = '{:0>5}'.format(i)
        i += int(1)
        check = Sales.objects.filter(code=str(pref) + str(code)).all()
        if len(check) <= 0:
            break
    code = str(pref) + str(code)

    try:
        sales = Sales(
            code=code, customer_name=data["customer"], customer_id=["customer_id"], sub_total = data['sub_total'], 
            grand_total = data['grand_total'], tax = data['tax'], tax_amount = data['tax_amount'], tendered_amount = data['tendered_amount'], 
            amount_change = data['amount_change'])
        sales.save()

        sale_id = Sales.objects.last().pk
        i = 0

        for prod in data.getlist('product_id[]'):
            product_id = prod 
            sale = Sales.objects.filter(id=sale_id).first()
            product = Stock.objects.filter(id=product_id).first()
            qty = data.getlist('qty[]')[i] 

            if int(qty) <= product.quantity:
                product.quantity -= int(qty)
                product.save()

            price = data.getlist('price[]')[i]
            total = float(qty) * float(price)
            print({'sale_id' : sale, 'product_id' : product, 'qty' : qty, 'price' : price, 'total' : total})
            DrugItemsSales(sale_id = sale, drug = product, qty = qty, price = price, total = total).save()
            i += int(1)
        resp['status'] = 'success'
        resp['sale_id'] = sale_id
        messages.success(request, "Sale Record has been saved.")
    except:
        resp['msg'] = "An error occured"
        print("Unexpected error:", sys.exc_info()[0])
    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def receipt(request):
    id = request.GET.get('id')
    sales = Sales.objects.filter(id=id).first()
    transaction = {}
    for field in Sales._meta.get_fields():
        if field.related_model is None:
            transaction[field.name] = getattr(sales,field.name)
    if 'tax_amount' in transaction:
        transaction['tax_amount'] = format(float(transaction['tax_amount']))

    ItemList = DrugItemsSales.objects.filter(sale_id = sales).all()
    context = {
        "transaction" : transaction,
        "salesItems" : ItemList
    }
    return render(request, 'posApp/receipt.html',context)

@login_required
def notify(request):
    products = Stock.objects.all()
    low_stock_products = []
    nots = StockNotifications.objects.filter(resolved=False)
    if products:
        for prod in products:
            if prod.is_low_stock:
                    low_stock_products.append(prod)
                    check_if_exists = StockNotifications.objects.filter(drug__id=prod.id, resolved=False)
                    if check_if_exists:
                        pass
                    else:
                        StockNotifications.objects.create(
                            title=f"{prod.drug_name} is running out of stock", drug=prod
                        )
                        messages.info(request, f"{prod.drug_name}: is running low in stock")
    
    drugs = Stock.objects.all()
    context = {
        "low_stock_products": low_stock_products,
        "nots": nots,
    }
    return render(request, "posApp/sstock_notify.html", context)
