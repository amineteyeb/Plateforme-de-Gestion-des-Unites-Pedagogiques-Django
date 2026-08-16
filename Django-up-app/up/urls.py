from django.urls import path,include
from . import views

urlpatterns = [
    path('employee/', views.employee_form,name='employee_insert'), # get and post req. for insert operation
    path('employee/<int:id>/', views.employee_form,name='employee_update'), # get and post req. for update operation
    path('employee/delete/<int:id>/',views.employee_delete,name='employee_delete'),
    path('employee/list/',views.employee_list,name='employee_list'), # get req. to retrieve and display all records
    path('comp/', views.comp_form,name='comp_insert'), # get and post req. for insert operation
    path('comp/<int:id>/', views.comp_form,name='comp_update'), # get and post req. for update operation
    path('comp/delete/<int:id>/',views.comp_delete,name='comp_delete'),
    path('mod/delete/<int:id>/',views.mod_delete,name='mod_delete'),
    path('module/<int:id>/', views.module_form,name='mod_update'),
    path('module/update/<int:id>/', views.module_update,name='mod_upd'),
    path('comp/list/',views.comp_list,name='comp_list'), # get req. to retrieve and display all records
    path('workspace/<int:id>/',views.affect,name='workspace'), # get req. to retrieve and display all records
    path('module/',views.module_form,name='module_form'), # get req. to retrieve and display all records
    path('module/list',views.mod_list,name='mod_list'), # get req. to retrieve and display all records
    path('workspace/delete/<int:id>/',views.annuler_affect,name='annuler_affect'),
    path('workspace/',views.affect,name='workspace'), # get req. to retrieve and display all records
    path('classe/',views.class_form,name='classe_insert'),
    path('login/', views.login,name='login'), # login
    path('logout/', views.logout, name='logout'), # logout
    path('mes_modules/',views.mes_modules,name='mes_modules'),
    path('',views.login,name='login'),
    path('forgot_password/',views.reset_page,name='forgot_password'),
    path('change_password/<token>/',views.change_password,name='change_password'),
    path('classe/list/',views.class_list,name='classe_list'),
    path('classe/delete/<int:id>/',views.class_delete,name='classe_delete'),
    path('classe/update/<int:id>/',views.class_form,name='classe_update'),
    path('option/delete/<int:id>/',views.option_delete,name='option_delete'),
    path('option/update/<int:id>/',views.class_form,name='option_update'),
    path('niveau/delete/<int:id>/',views.niveau_delete,name='niveau_delete'),
    path('niveau/update/<int:id>/',views.class_form,name='niveau_update'),
    path('gestion/list/',views.gestion_list,name='liste_niv'),
    path('option/', views.option_form,name='option_insert'),
    path('niveau/', views.niveau_form,name='niveau_insert'),
    path('option/<int:id>/', views.option_form,name='option_update'),
    path('reset_all/',views.reset_all,name='reset_all'),
    path('historique/',views.historique,name='historique'), # get and post req. for insert operation
     path('actuels/',views.actuels,name='actuels'), # get and post req. for insert operation
    path('employee/indispo/',views.update_employee_disp,name='employe_update'),
    path('employee/dispo/',views.employe_dispo,name='employe_dispo'),

]