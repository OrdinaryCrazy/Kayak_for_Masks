from django import forms

SortChoice = (
        ("size", "Size"),
        ("filtration", "Filtration"),
        ("name", "Name"),
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
        ("onesize", "OneSize"),
        ("XS", "XS: 4.7x5.3 inch (Toddler, Valveless, Non-Adjustable)"),
        ("M", "M: 5.9x7.5 inch"),
        ("S", "S: 5.5x6.7 inch")
    )
AvaiChoice = (
        # (1, ">=1"),
        # (0, "No require")
        (1, "Yes"),
        (0, "No")
    )

class MaskChoiceForm(forms.Form):
    sorting = forms.CharField(
        label="Sort", 
        widget = forms.RadioSelect(choices=SortChoice), 
        required=True,
        initial="name",

    )
    brand = forms.MultipleChoiceField(
        label="Brand/Manufacture", 
        choices=BrandChoice, 
        widget=forms.CheckboxSelectMultiple(), 
        required=True,
        # initial=["3m_vflex", "pod", "happy_mask", "flo_mask", "wayre", "carra", "cambridge", "honeywell"]
    )
    size = forms.MultipleChoiceField(
        label="Size", 
        choices=SizeChoice, 
        widget=forms.CheckboxSelectMultiple(), 
        required=True,
        initial=["small", "mid", "onesize", "XS", "M", "S"])
        
    avai = forms.IntegerField(
        label="Availability", 
        widget = forms.RadioSelect(choices=AvaiChoice), 
        required=True,
        # initial=1,
    )

