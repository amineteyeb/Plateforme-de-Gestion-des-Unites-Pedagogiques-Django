from asyncio import ensure_future
from turtle import position
from django import forms
from .models import Affectation, Classe, Competence, Enseignant, Module, Niveau, Option

class DateInput(forms.DateInput):
    input_type = 'date'

class EnseignantForm(forms.ModelForm):

    class Meta:
        model = Enseignant
        fields = ('fullname','email','cin','mobile','emp_code','position','type_e','type_r',)
        labels = {
            'fullname':'Full Name',
            'Identifiant':'EMP. Code',
            'email' : 'Email',
            'cin' : 'Cin',
            'position':'Competences',
            'type_e':'Type Enseignant',
            'type_r':'Type Responsable',
            
        }
        widgets = {
            'position': forms.CheckboxSelectMultiple(),
            'email' : forms.EmailInput(),
            'mobile' :forms.NumberInput(),
            'cin' : forms.NumberInput()
            
        }

    def __init__(self, *args, **kwargs):
        super(EnseignantForm,self).__init__(*args, **kwargs)
        self.fields['position'].empty_label = "Select"
        self.fields['emp_code'].required = False
        self.fields['type_e'].required = False
        self.fields['type_r'].required = False

class CompetenceForm(forms.ModelForm):

    class Meta:
        model = Competence
        fields = ('title',)
        labels = {
            'title':'title',
            
        }

def __init__(self, *args, **kwargs):
        super(CompetenceForm,self).__init__(*args, **kwargs)
        self.fields['title'].empty_label = "Select"
        
class ModuleForm(forms.ModelForm):

    class Meta:
        model = Module
        fields = ('name','semestre','periode','charge','skillmodule','option','niveau',)
        labels = {
            'name':'Nom Module',
            'periode': 'Periode Deroulement',
            'semestre': 'Semestre ',
            'charge':'Charge Horaire',
            'skillmodule':'Competence Requise',
            'option':'Option',
            'niveau':'Niveau',
        }
        widgets = {
            'date_debut': DateInput(),
            'date_fin': DateInput(),
            

        }
        
def __init__(self, *args, **kwargs):
        super(ModuleForm,self).__init__(*args, **kwargs)
        self.fields['option'].empty_label = "Select"
        self.fields['niveau'].empty_label = "Select"
       
class AffectationForm(forms.ModelForm):

    class Meta:
        
        model = Affectation
        fields = ('person',)
        labels = {
            'person':'Choisir Enseignant',
            
        }
        
    
       
class ClasseForm(forms.ModelForm):

    class Meta:
        model = Classe
        fields = ('option','niveau',)
        labels = {
            
            'option':'Option',
            'niveau':'Niveau'
        }

    def __init__(self, *args, **kwargs):
        super(ClasseForm,self).__init__(*args, **kwargs)
        self.fields['option'].empty_label = "Select"
        self.fields['niveau'].empty_label = "Select"
       
        self.fields['option'].required = True
        self.fields['niveau'].required = True

class EnseignantLogin(forms.ModelForm):

    class Enseignant:
        model = Classe
        fields = ('email','pwd',)
      
class OptionForm(forms.ModelForm):

    class Meta:
        model = Option
        fields = ('name',)
        labels = {
            'name':"Nom de l'Option",
           
        }

    def __init__(self, *args, **kwargs):
        super(OptionForm,self).__init__(*args, **kwargs)
        
        self.fields['name'].required = True
class NiveauForm(forms.ModelForm):

    class Meta:
        model = Niveau
        fields = ('name',)
        labels = {
            'name':"Niveau",
           
        }

    def __init__(self, *args, **kwargs):
        super(NiveauForm,self).__init__(*args, **kwargs)
        
        self.fields['name'].required = True        
        

