from asyncio.windows_events import NULL
from http.client import HTTPResponse
from turtle import position
from types import NoneType
from django.shortcuts import render, redirect
from .forms import AffectationForm, ClasseForm, CompetenceForm, EnseignantForm, ModuleForm, NiveauForm, OptionForm
from .models import Affectation, Annee_univ, Classe, Competence, Enseignant, Message, Module, Niveau, Notify, Option, Periode, PersonSkill, Up
from django.contrib.auth.hashers import make_password,check_password
# Create your views here.
from django.core.mail import send_mail
from django.conf import settings
import uuid
from django.contrib import messages
from django.db.models import Q
from copy import deepcopy
from datetime import datetime
from itertools import groupby
from django.db.models import Count

def employee_list(request):
    try:
      current_user = request.session['user']
      usr = Enseignant.objects.get(pk=current_user)
      notif = Notify.objects.filter(read_by=usr).order_by('-id')[:10][::-1]
      up= Up.objects.get(name=request.session['up'])
      messages = Message.objects.filter(room=up) [0:25]
      year= Annee_univ.objects.get(pk=request.session['year'])
      print(request.session['year'])

    except KeyError:
      return redirect('/login')
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string=request.GET.get('q')
        seens=Enseignant.objects.filter(fullname__icontains=query_string).filter(up=usr.up)
        context = {'employee_list': seens,'periode':Periode.objects.all(),'current_user': usr,'notif':notif,'message' : messages,'year':year}
        return render(request, "employee_register/employee_list.html", context)
    else:
        seens=Enseignant.objects.filter(up=usr.up)
        context = {'employee_list': Enseignant.objects.all(),'current_user': usr,'periode':Periode.objects.all(),'notif':notif,'message' : messages,'year':year,'years':Annee_univ.objects.all()}
    return render(request, "employee_register/employee_list.html", context)
    




def employee_form(request, id=0):
    try:
      current_user = request.session['user']
      usr = Enseignant.objects.get(pk=current_user)
      notif = Notify.objects.filter(read_by=usr).order_by('-id')[:10][::-1]
      up= Up.objects.get(name=request.session['up'])
      messages = Message.objects.filter(room=up) [0:25]
      year= Annee_univ.objects.get(pk=request.session['year'])
    except KeyError:
      return redirect('/login')
    if request.method == "GET":
        if id == 0:
            form = EnseignantForm()
        else:
            employee = Enseignant.objects.get(pk=id)
            form = EnseignantForm(instance=employee)
        return render(request, "employee_register/employee_form.html", {'form': form,'message' : messages,'current_user': usr,'notif':notif,'year':year,'years':Annee_univ.objects.all()})
    else:
        if id == 0:
            form = EnseignantForm(request.POST)
           
        else:
            employee = Enseignant.objects.get(pk=id)
            form = EnseignantForm(request.POST,instance= employee)
            
        if form.is_valid():
            user = form.save(commit=False)
            user.pwd = make_password(user.cin,'azert','md5')
            user.role =request.POST.get('mainselect')
            user.up =up
            
            print(user.cin)
            print(user.type_r)
            print(user.type_e)
            if user.type_r is None:
             user.charge_maximale = 378
            else:
              user.charge_maximale = 336



            print (request.POST.get('mainselect'))
            user.save()
            form.save_m2m()
        else:
         print(form.errors.as_data()) 
    return redirect('/employee/list')

def employee_delete(request,id):
    try:
      current_user = request.session['user']
      
    except KeyError:
      return redirect('/login')
    employee = Enseignant.objects.get(pk=id)
    employee.delete()
    return redirect('/employee/list')
    
def comp_form(request, id=0):
    try:
      current_user = request.session['user']
      usr = Enseignant.objects.get(pk=current_user)
      notif = Notify.objects.filter(read_by=usr).order_by('-id')[:10][::-1]
      up= Up.objects.get(name=request.session['up'])
      messages = Message.objects.filter(room=up) [0:25]
      year= Annee_univ.objects.get(pk=request.session['year'])
    except KeyError:
      return redirect('/login')
    if request.method == "GET":
        if id == 0:
            form_comp = CompetenceForm()
        else:
            competence = Competence.objects.get(pk=id)
            form_comp = CompetenceForm(instance=competence)
        return render(request, "competence/competence_form.html", {'form_comp': form_comp,'message':messages,'current_user': usr,'notif':notif,'year':year,'years':Annee_univ.objects.all()})
    else:
        if id == 0:
            form_comp = CompetenceForm(request.POST)
        else:
            competence = Competence.objects.get(pk=id)
           
            form_comp = CompetenceForm(request.POST,instance= competence)
        if form_comp.is_valid():
         form_comp.save()
        return redirect('/comp/list')


def comp_list(request):
    try:
      current_user = request.session['user']
      usr = Enseignant.objects.get(pk=current_user)
      notif = Notify.objects.filter(read_by=usr).order_by('-id')[:10][::-1]
      up= Up.objects.get(name=request.session['up'])
      messages = Message.objects.filter(room=up) [0:25]
      year= Annee_univ.objects.get(pk=request.session['year'])
    except KeyError:
      return redirect('/login')
    context = {'comp_list': Competence.objects.all(),'current_user': usr,'notif':notif,'message':messages,'year':year,'years':Annee_univ.objects.all()}
    return render(request, "competence/competence_list.html", context)
    
def comp_delete(request,id):
    try:
      current_user = request.session['user']
    except KeyError:
      return redirect('/login')
    competence = Competence.objects.get(pk=id)
    competence.delete()
    return redirect('/comp/list')

def module_form(request, id=0):
    try:
     current_user = request.session['user']
     usr = Enseignant.objects.get(pk=current_user)
     notif = Notify.objects.filter(read_by=usr).order_by('-id')[:10][::-1]
     up= Up.objects.get(name=request.session['up'])
     messages = Message.objects.filter(room=up) [0:25]
     year= Annee_univ.objects.get(pk=request.session['year'])
    except KeyError:
      return redirect('/login')
    if request.method == "GET":
        if id == 0:
            form_mod = ModuleForm()
        else:
            
            module = Module.objects.get(pk=id)
            form_mod = ModuleForm(instance=module)
        return render(request, "module/module_form.html", {'form_mod': form_mod,'current_user': usr,'notif':notif,'message':messages,'year':year,'years':Annee_univ.objects.all()})
    else:
        if id == 0:
            form_comp = ModuleForm(request.POST)
         
        else:
            module = Module.objects.get(pk=id)
            form_comp = ModuleForm(request.POST,instance= module)
     
        if form_comp.is_valid():
          
         form_comp.save()
         classe_set = Classe.objects.filter(option=Module.objects.latest('id').option,niveau=Module.objects.latest('id').niveau)
        
        for classe in classe_set:
         affect=  Affectation(hours=Module.objects.latest('id').charge,person= None ,Module=Module.objects.latest("id"),classe=classe)
         affect.save()  
         current = form_comp.save(commit=False)
         current.up = up
         current.save()
        return redirect('/module/list')

def module_update(request,id):
    try:
     current_user = request.session['user']
     usr = Enseignant.objects.get(pk=current_user)
     notif = Notify.objects.filter(read_by=usr).order_by('-id')[:10][::-1]
     up= Up.objects.get(name=request.session['up'])
     messages = Message.objects.filter(room=up) [0:25]
     year= Annee_univ.objects.get(pk=request.session['year'])
    except KeyError:
      return redirect('/login')
    if request.method == "GET":
       
      module = Module.objects.get(pk=id)
      form_mod = ModuleForm(instance=module)
      return render(request, "module/module_form.html", {'form_mod': form_mod,'current_user': usr,'notif':notif,'message':messages,'year':year,'years':Annee_univ.objects.all()})
    else:
       
            module = Module.objects.get(pk=id)
            form_comp = ModuleForm(request.POST,instance= module)
     
    if form_comp.is_valid():
         form_comp.save()
         classe_set = Classe.objects.filter(option=Module.objects.latest('id').option,niveau=Module.objects.latest('id').niveau)
        
         
         
    return redirect('/module/list')
        


def mod_list(request):
    try:
      current_user = request.session['user']
      usr = Enseignant.objects.get(pk=current_user)
      notif = Notify.objects.filter(read_by=usr).order_by('-id')[:10][::-1]
      up= Up.objects.get(name=request.session['up'])
      messages = Message.objects.filter(room=up) [0:25]
      year= Annee_univ.objects.get(pk=request.session['year'])
    except KeyError:
      return redirect('/login')
      
    if ('q' in request.GET) and request.GET['q'].strip() and  request.method == "GET":
        query_string=request.GET.get('q')
        seens=Module.objects.filter(Q(name__icontains=query_string) | Q(charge__icontains=query_string)| Q(skillmodule__title__icontains=query_string)).filter(up=usr.up)
        context = {'mod_list': seens,'current_user': usr,'notif':notif,'message' : messages}
        return render(request, "module/module_list.html", context)
    else:
        seens=Enseignant.objects.filter(up=usr.up)
        context = {'mod_list': Module.objects.all(),'current_user': usr,'notif':notif,'message' : messages,'year':year,'years':Annee_univ.objects.all()}
    return render(request, "module/module_list.html", context)

def mod_delete(request,id):
    try:
      current_user = request.session['user']
    except KeyError:
      return redirect('/login')
    module = Module.objects.get(pk=id)
    
    affect_set = Affectation.objects.filter(Module=module,active=True)
    
    for affect in affect_set:
     if affect.person!=None:
      person = affect.person
      print(affect.hours)
      person.charge_actuelle = person.charge_actuelle- affect.hours
           
      person.save()
    module.delete()
    return redirect('/module/list')
    

def annuler_affect(request,id):
    try:
      current_user = request.session['user']
    except KeyError:
      return redirect('/login')
    affectation = Affectation.objects.get(pk=id)
    ensgg= affectation.person
    ensgg.charge_actuelle = ensgg.charge_actuelle- affectation.hours
    ensgg.save()
    affectation.person=None
    
    affectation.save()
    return redirect('/workspace')

def affect(request,id=0):
    try:
      current_user = request.session['user']
      usr = Enseignant.objects.get(pk=current_user)
      notif = Notify.objects.filter(read_by=usr).order_by('-id')[:10][::-1]
      up= Up.objects.get(name=request.session['up'])
      messages = Message.objects.filter(room=up) [0:25]
      year= Annee_univ.objects.get(pk=request.session['year'])
      years=Annee_univ.objects.all()
    except KeyError:
      return redirect('/login')
    
    if request.method == 'GET':
       
        if id == 0:
         
         
         form = AffectationForm()
         if ('year' in request.GET) and request.GET['year'].strip():  
      
          year= Annee_univ.objects.get(pk=request.GET['year'])
          request.session['year']=year.id
         else:
          year= Annee_univ.objects.get(pk=request.session['year'])
      
        else:
            employee = Affectation.objects.get(pk=id)
            
            form = AffectationForm(instance=employee)
           # form.person.queryset = Enseignant.objects.filter(position=employee.Module.id_comp)
            print( request.GET.get('f'))

        context = {'current_user': usr,'notif':notif,'workspace': Affectation.objects.filter(active=True,annee_univ=year).order_by('Module'),'form': form,'year':year,'ensg': Enseignant.objects.all(),'skill':PersonSkill.objects.all(),'message':messages,'years':years}
        return render(request, "workspace/workspace.html", context)
    else:
        if id == 0:
           
            form = AffectationForm(request.POST)
           # form.person.queryset = Enseignant.objects.filter(position=employee.Module.id_comp)
           
        else:
            
            employee = Affectation.objects.get(pk=id)
            form = AffectationForm(request.POST,instance= employee)
           # form.fields['person'].queryset = Enseignant.objects.filter(position=employee.Module.id_comp)
            print (request.POST.get('org_list'))
            if request.POST.get('org_list')=='None':
               return  redirect('/workspace')  
        if form.is_valid():
            ensg = PersonSkill.objects.get(pk=request.POST.get('org_list'))
            ensgg = ensg.person
            ensgg.charge_actuelle = ensgg.charge_actuelle + employee.hours
            
            ensgg.save()
            current = form.save(commit=False)
            current.person = ensgg
            current.save()
            send_mail('Affectation', 'vous êtes affecté pour enseigner le module : '+ str(employee.Module.name)+' à la classe '+str(employee.classe.niveau)+str(employee.classe.option)+str(employee.classe.name)+' durant la '+str(employee.Module.semestre)+' periode '+str(employee.Module.periode)+'.  Veuillez consulter votre espace UP', settings.EMAIL_HOST_USER, [ensgg.email])
            notification=Notify(notify_detail='vous êtes affecté pour enseigner le module : '+ str(employee.Module.name)+' à la classe '+str(employee.classe.niveau)+str(employee.classe.option)+str(employee.classe.name)+' durant la '+str(employee.Module.semestre)+' periode '+str(employee.Module.periode)+".",status = True,read_by=ensgg)
            notification.save()
        return redirect('/workspace')

def class_form(request, id=0):
    try:
     current_user = request.session['user']
     usr = Enseignant.objects.get(pk=current_user)
     notif = Notify.objects.filter(read_by=usr).order_by('-id')[:10][::-1]
     up= Up.objects.get(name=request.session['up'])
     messages = Message.objects.filter(room=up) [0:25]
     year= Annee_univ.objects.get(pk=request.session['year'])
    except KeyError:
      return redirect('/login')
    if request.method == "GET":
        if id == 0:
            form_class = ClasseForm()
        else:
            classe = Classe.objects.get(pk=id)
            form_class = ClasseForm(instance=classe)
        return render(request, "workspace/classe_form.html", {'form_class': form_class,'current_user': usr,'notif':notif,'message':messages,'year':year,'years':Annee_univ.objects.all()})
    else:
        if id == 0:
            form_class = ClasseForm(request.POST)
        else:
            classe = Classe.objects.get(pk=id)
            form_class = ClasseForm(request.POST,instance= classe)
        if form_class.is_valid():
         numb=Classe.objects.filter(option=form_class.cleaned_data['option'],niveau=form_class.cleaned_data['niveau'],annee_univ=year).count()
         print (numb)
         number=int(request.POST.get('number'))
        
        for i in range(numb+1, number+1):
          classe=Classe(option=form_class.cleaned_data['option'],niveau=form_class.cleaned_data['niveau'],name=str(i),annee_univ=year)
          
          classe.save()
          module_set = Module.objects.filter(option=Classe.objects.latest('id').option,niveau=Classe.objects.latest('id').niveau)
        
          for module in module_set:
            affect=  Affectation(hours=module.charge,person= None ,Module=module,classe=Classe.objects.latest('id'),up=up,annee_univ=year)
            affect.save()  
    return redirect('/workspace')

def login(request):
   if request.method == "GET":
    return render(request, "main/main.html")
   else: 
    msg=''
    if request.method =="POST": 
     email=request.POST.get('email')
     pwd=request.POST.get('password')
     encryptedpassword=make_password(pwd,'azert','md5')
   
    user=Enseignant.objects.filter(email=email,pwd=encryptedpassword).count()
    
    if user> 0:
     msg='Success Ful1'
     print('success')
     usercurrent=Enseignant.objects.get(email=email,pwd=encryptedpassword)
     usercurrent.isactive = True
     usercurrent.save()
     request.session['user'] = usercurrent.id
     request.session['name']= usercurrent.fullname
     request.session['up']=usercurrent.up.name
      
     currentYear = datetime.now().year
     currentYearplus = currentYear+1
     currentminus = currentYear-1
     currentDay = datetime.now().day
     currentMonth = datetime.now().month
     print(currentYear)
     print(currentMonth)
     print(currentDay)
     if currentMonth >=8:
          
          year = Annee_univ.objects.get(sem1_year=str(currentYear))
          print(year)
          request.session['year']=year.id
          request.session['current_year']=year.id
        

     else:
        
          year = Annee_univ.objects.get(sem1_year=str(currentminus))
          request.session['year']=year.id
          request.session['current_year']=year.id
          print(year)
     
     

     
     if usercurrent.role=='1': 
        request.session['a']='Enseignant '+usercurrent.get_type_e_display()
        print(request.session['a'])
        return redirect('/module/list')  
        
     else: 
        if usercurrent.type_r=='1':
         request.session['a']=usercurrent.get_type_r_display()
         print(request.session['a'])
         return redirect('/workspace')
        else:
            request.session['a']=usercurrent.get_type_r_display()
            print(request.session['a'])
            return redirect('/actuels ')

        
            
    else:
     msg='Invalide,vérifiez vos paramètres'
     print('fail')
    
    return render(request, "main/main.html",{'msg':msg})
def logout(request):
    try:
        usercurrent=Enseignant.objects.get(pk=request.session['user'])
        usercurrent.isactive = False
        usercurrent.save()
        del request.session['user']
        del request.session['name']
        del request.session['year']
        del request.session['up']
        del request.session['a']
    except:
        return redirect('login')
    return redirect('login')

def mes_modules(request,id=0):
    try:
      current_user = request.session['user']
      usr = Enseignant.objects.get(pk=current_user)
      notif = Notify.objects.filter(read_by=usr).order_by('-id')[:10][::-1]
      up= Up.objects.get(name=request.session['up'])
      messages = Message.objects.filter(room=up) [0:25]
      year= Annee_univ.objects.get(pk=request.session['year'])
    except KeyError:
      return redirect('/login')
    
    if request.method == 'GET':
    
       
      years= Annee_univ.objects.all()
      employee = Affectation.objects.all()
            
        
      year_set = Annee_univ.objects.all()
      value_list = Affectation.objects.values_list('annee_univ', flat=True).distinct()
      group_by_value = {}
      for value in value_list:
       group_by_value[value] = Affectation.objects.filter(annee_univ=value)
       print(group_by_value[value])
      workspace=Affectation.objects.all().order_by('Module')
           # form.person.queryset = Enseignant.objects.filter(position=employee.Module.id_comp)
            
      context = {'current_user': usr,'notif':notif,'workspace': workspace,'years':Annee_univ.objects.all(),'years':Annee_univ.objects.all(),'ensg': Enseignant.objects.all(),'skill':PersonSkill.objects.all(),'message':messages,'year':year}
    return render(request, "workspace/mes_modules.html", context)
def historique(request,id=0):
    try:
      current_user = request.session['user']
      usr = Enseignant.objects.get(pk=current_user)
      notif = Notify.objects.filter(read_by=usr).order_by('-id')[:10][::-1]
      up= Up.objects.get(name=request.session['up'])
      messages = Message.objects.filter(room=up) [0:25]
      year= Annee_univ.objects.get(pk=request.session['year'])
    except KeyError:
      return redirect('/login')
    
    if request.method == 'GET':
    
       
       
      employee = Affectation.objects.filter(person=usr,active=False)
            
      
           # form.person.queryset = Enseignant.objects.filter(position=employee.Module.id_comp)
            
      context = {'current_user': usr,'notif':notif,'workspace': employee,'ensg': Enseignant.objects.all(),'years':Annee_univ.objects.all(),'skill':PersonSkill.objects.all(),'message':messages,'year':year,'years':Annee_univ.objects.all()}
      return render(request, "workspace/historique.html", context)     
def actuels(request,id=0):
    try:
      current_user = request.session['user']
      usr = Enseignant.objects.get(pk=current_user)
      notif = Notify.objects.filter(read_by=usr).order_by('-id')[:10][::-1]
      up= Up.objects.get(name=request.session['up'])
      messages = Message.objects.filter(room=up) [0:25]
      year= Annee_univ.objects.get(pk=request.session['year'])
    except KeyError:
      return redirect('/login')
    
    if request.method == 'GET':
    
       
       
      employee = Affectation.objects.filter(person=usr,active=True)
            
      
           # form.person.queryset = Enseignant.objects.filter(position=employee.Module.id_comp)
            
      context = {'current_user': usr,'notif':notif,'workspace': employee,'ensg': Enseignant.objects.all(),'skill':PersonSkill.objects.all(),'message':messages,'year':year,'years':Annee_univ.objects.all()}
      return render(request, "workspace/actuels.html", context)     
     
def reset_page(request):
   if request.method == "GET":
    
    
    return render(request, "main/forgot_password.html")
  
   else: 
    if request.method =="POST": 
     email=request.POST.get('email')
    user=Enseignant.objects.filter(email=email).count()
    
    if user> 0:
     msg="Un email de confirmation envoyé à l'adresse email indiquée, Consultez  votre boîte de réception"
     usr=Enseignant.objects.get(email=email)
     usr.forget_password_token=str(uuid.uuid4())
     usr.save()
     print('success')
     send_mail('Récuperation Mot de Passe Systeme UP', "Bonjour "+usr.fullname+",\n\nUne demande de réinitialisation de mot de passe a été demandée pour votre\ncompte utilisateur sur ESPRIT On Line - UP System.\n\nPour confirmer cette demande et définir un nouveau mot de passe, veuillez cliquer sur le lien ci-dessous :http://localhost:8000/change_password/"+usr.forget_password_token+"\n\nSi cette demande de réinitialisation n'a pas été effectuée par vous-même,\naucune action n'est nécessaire et vous pouvez ignorer ce message.\n\nSi vous avez besoin d'aide, veuillez contacter l''administrateur du site,\n\nAdmin Utilisateur\n\nservice.affectation@gmail.com ", settings.EMAIL_HOST_USER, [email])
    else:
     msg='Compte introuvable , Adresse e-mail incorrecte.'
    context={'msg':msg}
    return render(request, "main/forgot_password.html",context)

def change_password(request,token):
 context = {}
 try:
    profile_obj = Enseignant.objects.filter(forget_password_token=token).first()
    context = {'user_id': profile_obj.id}
    if request.method == "POST":
     new_password = request.POST.get ('password')
     confirm_password = request.POST.get('confirm_password')
    
   
     
    profile_obj.pwd=make_password(new_password,'azert','md5')
    profile_obj.forget_password_token=None
    profile_obj.save()
    return redirect ("/login")

 except Exception as e:
   print (e)
   return render (request,'main/forgot_password.html', context)

def class_list(request):
    try:
      current_user = request.session['user']
      usr = Enseignant.objects.get(pk=current_user)
      notif = Notify.objects.filter(read_by=usr).order_by('-id')[:10][::-1]
      up= Up.objects.get(name=request.session['up'])
      messages = Message.objects.filter(room=up) [0:25]
      year= Annee_univ.objects.get(pk=request.session['year'])
    except KeyError:
      return redirect('/login')

    context = {'classe_list': Classe.objects.filter(annee_univ=year),'current_user': usr,'notif':notif,'message':messages,'year':year,'years':Annee_univ.objects.all()}
    return render(request, "classe/classe_list.html", context)

def class_delete(request,id):
    try:
      current_user = request.session['user']
      year= Annee_univ.objects.get(pk=request.session['year'])
    except KeyError:
      return redirect('/login')
    classe = Classe.objects.get(pk=id)
    
    affect_set = Affectation.objects.filter(classe=classe,active=True,annee_univ=year)
    
    for affect in affect_set:
     if affect.person!=None:
      person = affect.person
      print(affect.hours)
      person.charge_actuelle = person.charge_actuelle- affect.hours
      person.save()
    classe.delete()
    return redirect('/classe/list')

def option_delete(request,id):
    try:
      current_user = request.session['user']
    except KeyError:
      return redirect('/login')
    classe = Option.objects.get(pk=id)
    
    affect_set = Affectation.objects.filter(classe__option=classe)
    
    for affect in affect_set:
     if affect.person!=None:
      person = affect.person
      print(affect.hours)
      person.charge_actuelle = person.charge_actuelle-affect.hours
           
      person.save()
      classe.delete()
    return redirect('/gestion/list')

def niveau_delete(request,id):
    try:
      current_user = request.session['user']
    except KeyError:
      return redirect('/login')
    classe = Niveau.objects.get(pk=id)
    
    affect_set = Affectation.objects.filter(classe__niveau=classe)
    
    for affect in affect_set:
      person = affect.person
      print(affect.hours)
      person.charge_actuelle = person.charge_actuelle-affect.hours
           
      person.save()
      classe.delete()
    return redirect('/gestion/list')

def gestion_list(request):
    try:
      current_user = request.session['user']
      usr = Enseignant.objects.get(pk=current_user)
      notif = Notify.objects.filter(read_by=usr).order_by('-id')[:10][::-1]
      up= Up.objects.get(name=request.session['up'])
      messages = Message.objects.filter(room=up) [0:25]
      year= Annee_univ.objects.get(pk=request.session['year'])
    except KeyError:
      return redirect('/login')
    context = {'opt_list': Option.objects.all(),'niv_list': Niveau.objects.all(),'current_user': usr,'notif':notif,'message':messages,'year':year,'years':Annee_univ.objects.all()}
    return render(request, "options/options_niv.html", context)   
def option_form(request, id=0):
    try:
     current_user = request.session['user']
     usr = Enseignant.objects.get(pk=current_user)
     notif = Notify.objects.filter(read_by=usr).order_by('-id')[:10][::-1]
     up= Up.objects.get(name=request.session['up'])
     messages = Message.objects.filter(room=up) [0:25]
     year= Annee_univ.objects.get(pk=request.session['year'])
    except KeyError:
      return redirect('/login')
    if request.method == "GET":
        if id == 0:
            form_option= OptionForm()
        else:
            option = Option.objects.get(pk=id)
            form_option = OptionForm(instance=option)
        return render(request, "options/option_form.html", {'form_option': form_option,'current_user': usr,'notif':notif,'message':messages,'year':year,'years':Annee_univ.objects.all()})
    else:
        if id == 0:
            form_option = OptionForm(request.POST)
        else:
            option = Option.objects.get(pk=id)
            form_option = OptionForm(request.POST,instance= option)
        if form_option.is_valid():
         form_option.save()
      
        return redirect('/gestion/list')
def niveau_form(request, id=0):
    try:
     current_user = request.session['user']
     usr = Enseignant.objects.get(pk=current_user)
     notif = Notify.objects.filter(read_by=usr).order_by('-id')[:10][::-1]
     up= Up.objects.get(name=request.session['up'])
     messages = Message.objects.filter(room=up) [0:25]
     year= Annee_univ.objects.get(pk=request.session['year'])
    except KeyError:
      return redirect('/login')
    if request.method == "GET":
        if id == 0:
            form_niv= NiveauForm()
        else:
            niveau = Niveau.objects.get(pk=id)
            form_niv = NiveauForm(instance=niveau)
        return render(request, "options/niveau_form.html", {'form_niv': form_niv,'current_user': usr,'notif':notif,'message':messages,'year':year,'years':Annee_univ.objects.all()})
    else:
        if id == 0:
            form_niv = NiveauForm(request.POST)
        else:
            niveau = Niveau.objects.get(pk=id)
            form_niv = NiveauForm(request.POST,instance= niveau)
        if form_niv.is_valid():
         form_niv.save()
        return redirect('/gestion/list')        
def reset_all(request, id=0):
    try:
     current_user = request.session['user']
     usr = Enseignant.objects.get(pk=current_user)
     notif = Notify.objects.filter(read_by=usr).order_by('-id')[:10][::-1]
     up= Up.objects.get(name=request.session['up'])
     messages = Message.objects.filter(room=up) [0:25]
     year= Annee_univ.objects.get(pk=request.session['year'])
    except KeyError:
      return redirect('/login')
    affect_set = Affectation.objects.filter(active=True)
    
    for affect in affect_set:
      if affect.person!=None:
       person = affect.person
       print(affect.hours)
       person.charge_actuelle = person.charge_actuelle-affect.hours
       affect.active=False
       new_instance = deepcopy(affect)
       new_instance.id = None
       new_instance.active=True
       new_instance.person=None
       
      
           
       person.save()
       new_instance.person=None
       
       
       affect.save()
       new_instance.save()

    return redirect('/workspace')

    
def update_employee_disp(request):
 
    
     id=request.POST.get('id')
     check=request.POST.get('checked')
     check_text=request.POST.get('dispo_desc')
     date=request.POST.get('periode')
     periode=request.POST.get('p')
     
     year= Annee_univ.objects.get(pk=request.session['year'])

     user=Enseignant.objects.filter(pk=id).count()
     
    
     if user> 0:
     
     
      usercurrent=Enseignant.objects.get(pk=id)
     print (usercurrent.fullname)
     print (id)
     print (check)
     print (check_text)
     print ("date"+date)
     usercurrent.is_dispo = check
     usercurrent.dispo_desc = check_text
     usercurrent.periode_indispo = Periode.objects.get(pk=date)
     usercurrent.periode=periode
     usercurrent.year_indispo=year
     usercurrent.save()
     return redirect('/employee/list')
     
     
def employe_dispo(request):
 
    
     id=request.POST.get('id')
    
     year= Annee_univ.objects.get(pk=request.session['year'])

     user=Enseignant.objects.filter(pk=id).count()
     
    
     if user> 0:
     
     
      usercurrent=Enseignant.objects.get(pk=id)
     print (usercurrent.fullname)
     print (id)
     
     usercurrent.is_dispo = True
     usercurrent.dispo_desc = None
     usercurrent.periode_indispo = None
     usercurrent.periode= None

     usercurrent.save()
     return redirect('/employee/list')
     
     