from django import forms

SortChoice = (
        ("manufacture", "Brand/Manufacture"),
        ("size", "Size"),
        ("avialability", "Availability"),
    )

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
        # (1, ">=1"),
        # (0, "No require")
        (1, "Yes"),
        (0, "No")
    )

class MaskChoiceForm(forms.Form):
    sorting = forms.CharField(label="Sort", widget = forms.RadioSelect(choices=SortChoice))
    brand = forms.CharField(label="Brand/Manufacture", widget = forms.RadioSelect(choices=BrandChoice))
    size = forms.CharField(label="Size", widget = forms.RadioSelect(choices=SizeChoice))
    avai = forms.IntegerField(label="Availability", widget = forms.RadioSelect(choices=AvaiChoice))
