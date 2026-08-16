from email import message
from turtle import up
from xmlrpc.client import DateTime
from django.db import models
from datetime import datetime
# Create your models here.
class Up(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    slug=models.SlugField(unique=True)

class Annee_univ(models.Model):
     id = models.AutoField(primary_key=True)
     sem1_year=models.CharField(max_length=4,default=datetime.now,blank=True)  
     sem2_year=models.CharField(max_length=4,default=datetime.now,blank=True)    
     def __str__(self):
      return self.sem1_year+'/'+self.sem2_year   


class Competence(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title
class Niveau(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.IntegerField(default=None, blank=True, null=True)
    def __str__(self):
        return str(self.name)

    
class Option(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256,default=None, blank=True, null=True)
    def __str__(self):
        return self.name
class Periode(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=1000)
    date_debut = models.DateField(default=None, blank=True, null=True)
    date_inter = models.DateField(default=None, blank=True, null=True)
    date_fin = models.DateField(default=None, blank=True, null=True)

    def __str__(self):
        return self.name

class Module(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256,default=None, blank=True, null=True)
    charge= models.FloatField(default=None, blank=True, null=True)
    skillmodule= models.ForeignKey(Competence, on_delete=models.SET_NULL,default=None, blank=True, null=True)
    option = models.ForeignKey(Option, on_delete=models.CASCADE,default=None, blank=True, null=True)
    niveau = models.ForeignKey(Niveau, on_delete=models.CASCADE,default=None, blank=True, null=True)
    up = models.ForeignKey(Up, on_delete=models.CASCADE,default=None, blank=True, null=True) 
    PERIODE_CHOICES = (('1', 'Periode 1'),('2', 'Periode 2'),('3','Tout'),)
    semestre=models.ForeignKey(Periode,on_delete=models.SET_NULL,default=None, blank=True, null=True)
    periode=models.CharField(max_length=10,choices=PERIODE_CHOICES,default=None,blank=True,null=True)
   

    
class Enseignant(models.Model):
    id = models.AutoField(primary_key=True)
    fullname = models.CharField(max_length=100)
    emp_code = models.CharField(max_length=11)
    email = models.CharField(max_length=50,default=None)
    cin = models.CharField(max_length=20,default=None)
    pwd = models.CharField(max_length=255,default=None)
    ROLE_CHOICES = (('1', 'Enseignant'),('2', 'Responsable'),)
    TYPEE_CHOICES = (
        ('1', 'Permanant'),
        ('2', 'Vacataire'), 
        ('3', 'Alternant'), 
    )
    TYPER_CHOICES = (
        ('1', 'Coordinateur Up'),
        ('2', 'Cooridnateur projet'), 
        ('3', 'Responsable Option'),
        ('4', 'Responsable Stage'),
    )
    role = models.CharField(max_length=10,choices=ROLE_CHOICES,default=None,blank=True,null=True)
    type_e  = models.CharField(max_length=10,choices=TYPEE_CHOICES,default=None,blank=True,null=True)
    type_r  = models.CharField(max_length=10,choices=TYPER_CHOICES,default=None,blank=True,null=True)
    mobile= models.CharField(max_length=8)
    charge_actuelle= models.FloatField(default=0, blank=True, null=True)
    charge_maximale= models.FloatField(default=0, blank=True, null=True)
    position= models.ManyToManyField(Competence, through='PersonSkill', related_name='persons')
    modules= models.ManyToManyField(Module, through='Affectation', related_name='modules')
    up = models.ForeignKey(Up, on_delete=models.CASCADE,default=None, blank=True, null=True)
    isactive = models.BooleanField(default=0)
    forget_password_token=models.CharField(max_length=10000,default=None,null=True)
    is_dispo = models.BooleanField(default=1)
    dispo_desc = models.CharField(max_length=1000,blank=True)
    periode_indispo = models.ForeignKey(Periode,on_delete=models.SET_NULL,default=None, blank=True, null=True)
    PERIODE_CHOICES = (('1', 'Periode 1'),('2', 'Periode 2'),)
    
    periode=models.CharField(max_length=10,choices=PERIODE_CHOICES,default=None,blank=True,null=True)
    year_indispo=models.ForeignKey(Annee_univ,on_delete=models.SET_NULL,default=None, blank=True, null=True)
    def __str__(self):
        return self.fullname
class Classe(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.IntegerField(default=None, blank=True, null=True)
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
    niveau = models.ForeignKey(Niveau, on_delete=models.CASCADE)
    annee_univ=models.ForeignKey(Annee_univ,on_delete=models.SET_NULL,default=None, blank=True, null=True)
  
    


class PersonSkill(models.Model):
    id = models.AutoField(primary_key=True)
    person = models.ForeignKey(Enseignant, on_delete=models.CASCADE)
    skill =  models.ForeignKey(Competence, on_delete=models.CASCADE)

class Affectation(models.Model):
    id = models.AutoField(primary_key=True)
    hours = models.FloatField(default=None, blank=True, null=True)
    active = models.BooleanField(default=True)
    person = models.ForeignKey(Enseignant, on_delete=models.SET_NULL,default=None, blank=True, null=True)
    Module = models.ForeignKey(Module, on_delete=models.CASCADE)
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE ,default=None, blank=True, null=True)
    up=models.ForeignKey(Up, on_delete=models.CASCADE ,default=None, blank=True, null=True)
    annee_univ=models.ForeignKey(Annee_univ,on_delete=models.SET_NULL,default=None, blank=True, null=True)


class Notify(models.Model):
    id = models.AutoField(primary_key=True)
    notify_detail=models.TextField()
    status=models.BooleanField()
    read_by=models.ForeignKey(Enseignant,on_delete=models.CASCADE,null=True)
def __str__(self):
        return self.notify_detail

class Message(models.Model):
    id = models.AutoField(primary_key=True)
    date=models.DateTimeField(default=datetime.now,blank=True)
    message=models.CharField(max_length=100000000)
    user=models.ForeignKey(Enseignant,on_delete=models.CASCADE,null=True)
    room=models.ForeignKey(Up,on_delete=models.CASCADE,null=True)
def __str__(self):
        return self.notify_detail

