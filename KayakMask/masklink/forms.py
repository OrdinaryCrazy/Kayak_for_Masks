from django import forms

BrandChoice = (
        ("3m_vflex", "3M Vflex"),
        ("pod", "POD"),
        ("happy_mask", "Happy Mask"),
        ("flo_mask", "Flomask"),
        ("wayre", "Wayre"),
        ("carra", "Caraa Tailored Junior Mask"),
        ("cambridge", "Cambridge"),
        ("honeywell", "Honeywell"),
    )
SizeChoice = (
        ("small", "Small"),
        ("mid", "Medium"),
    )
AvaiChoice = (
        ("more_one", ">=1"),
        ("no_require", "No require")
    )

class MaskChoiceForm(forms.Form):
    brand = forms.CharField(label="Brand/Manufacture", widget = forms.RadioSelect(choices=BrandChoice))
    size = forms.CharField(label="Size", widget = forms.RadioSelect(choices=SizeChoice))
    avai = forms.IntegerField(label="Availability", widget = forms.RadioSelect(choices=AvaiChoice))