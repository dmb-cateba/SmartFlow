from django import forms
from .models import Location, Container

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = '__all__'

class ContainerForm(forms.ModelForm):
    class Meta:
        model = Container
        fields = ['barcode', 'container_type', 'current_location', 'status']
