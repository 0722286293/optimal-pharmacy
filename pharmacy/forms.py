from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.forms import Form
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from phonenumber_field.formfields import PhoneNumberField
from django.core.validators import RegexValidator

import json
      

class DateInput(forms.DateInput):
    input_type = "date"

class StockForm(forms.ModelForm):
    valid_to= forms.DateField(label="Expiry Date", widget=DateInput(attrs={"class":"form-control"}))

    class Meta:
        model=Stock
        fields='__all__'
        exclude=['valid_from','reorder_level','receive_quantity', 'prescrip_drug_acess']

class CategoryForm(forms.ModelForm):
    class Meta:
        model=Category
        fields='__all__'

class HodForm(ModelForm):
    class Meta:
        model=AdminHOD
        fields='__all__'
        exclude=['admin','gender','mobile','address']
 
class ReceiveStockForm(ModelForm):
    valid_to= forms.DateField(label="Expiry Date", widget=DateInput(attrs={"class":"form-control"}))

    class Meta:
        model=Stock
        fields='__all__'
        exclude=['category' ,'drug_name','valid_from','dispense_quantity','reorder_level','date_from','date_to','quantity','manufacture']


class ReorderLevelForm(forms.ModelForm):
	class Meta:
		model = Stock
		fields = ['reorder_level']

