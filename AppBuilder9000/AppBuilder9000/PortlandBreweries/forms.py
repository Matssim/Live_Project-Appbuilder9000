from django.forms import ModelForm
from .models import Brewery

#Creates a brewery entry form based on the Brewery model
class BreweryForm(ModelForm):
    class Meta:
        model = Brewery
        fields = '__all__'
