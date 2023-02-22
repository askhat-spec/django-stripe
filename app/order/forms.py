from django import forms


class OrderAddItemForm(forms.Form):
    quantity = forms.IntegerField(initial=1, min_value=1, max_value=999, label='')
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)