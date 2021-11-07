from django import forms

BrandChoice = ()
SizeChoice = ()
AvaiChoice = ()

class MaskChoiceForm(forms.Form):
    brand = forms.CharField(label="Brand/Manufacture", widget = forms.RadioSelect())
    size = forms.CharField(label="Size", widget = forms.RadioSelect())
    avai = forms.IntegerField(label="Availability", widget = forms.RadioSelect())