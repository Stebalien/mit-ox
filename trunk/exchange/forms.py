from django import forms
import tagging.forms
from exchange.models import *
from exchange.index import complete_indexer
from django.shortcuts import render_to_response

class SearchForm(forms.Form):
    category = forms.ChoiceField(choices=(("", "All Categories"),) + Item.CATEGORY_CHOICES, required=False, label='')
    tags = tagging.forms.TagField(
        label='',
        required=False,
        widget=forms.widgets.HiddenInput()
    )
    query = forms.CharField(required=False, label='')

class CategoryForm(forms.Form):
    mode = forms.ChoiceField(choices=Item.MODE_CHOICES, widget=forms.RadioSelect)
    category = forms.ChoiceField(choices=Item.CATEGORY_CHOICES, required=True, widget=forms.RadioSelect)

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        exclude = ("mode", "status", "owner", "customers", "date")
        widgets = {
            "description": forms.TextInput(
                attrs={'width':'35', 'height':'5'}
            ),
        }

class ClothsForm(ItemForm):
    class Meta(ItemForm.Meta):
        model = ClothsItem

class ElectronicsForm(ItemForm):
    class Meta(ItemForm.Meta):
        model = ElectronicsItem

class EntertainmentForm(ItemForm):
    class Meta(ItemForm.Meta):
        model = EntertainmentItem

class FoodForm(ItemForm):
    class Meta(ItemForm.Meta):
        model = FoodItem

class MaterialsForm(ItemForm):
    class Meta(ItemForm.Meta):
        model = MaterialsItem

class MiscellaneousForm(ItemForm):
    class Meta(ItemForm.Meta):
        model = MiscellaneousItem

class ServicesForm(ItemForm):
    class Meta(ItemForm.Meta):
        model = ServicesItem

class TextbooksForm(ItemForm):
    class Meta(ItemForm.Meta):
        model = TextbooksItem

class TransportationForm(ItemForm):
    class Meta(ItemForm.Meta):
        model = TransportationItem
