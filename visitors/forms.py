# import the standard Django Forms
# from built-in library
from django.forms import ModelForm
from visitors.models import Visitor 
  
# creating a form  
class InputForm(ModelForm): 
  
    class Meta:
        model = Visitor
        
