from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from diginxthltadmin.models import Roles, Modules, Access_modules
from django.contrib import messages
from urllib.parse import parse_qs
from django.urls import reverse

#Function for unique list
def unique(list):
    # initialize a null list
    unique_list = [] 
    # traverse for all elements
    for x in list:
        # check if exists in unique_list or not
        if x not in unique_list:
            unique_list.append(x)
    return unique_list

def permissions_list(request):
    context={}
    context['username'] = request.session["username"]
    context['list_roles'] = Roles.objects.all()
    return render(request,'permissions/permissions-list.html',context)

def permissions_add(request):
    if request.method == 'GET':
        context={}
        context['username'] = request.session["username"]
        context['all_modules'] = Modules.objects.all()
        return render(request,'permissions/permissions-add.html',context)  
    if request.method == 'POST':
        try: 
            payload = parse_qs(request.body.decode('utf-8')) 
            req_role = ''.join(payload['role'])
            #Checking role exists in db or not
            if Roles.objects.filter(name = req_role).exists():
                messages.error(request, "Role already exist")
                return redirect("permissions_add")
            else:
                #Saving role into db
                Roles(name = req_role).save()
                #Getting seved role id
                role_id = Roles.objects.get(name = req_role).id
                payload.pop('csrfmiddlewaretoken', None)
                payload.pop('role', None) 
                #Creating list of Access_modules objects
                access_modules_objects = []
                print(payload.keys())
                for perm in payload.keys():
                    print(perm)
                    #Split paylod keys into module_name & module_action
                    module_name = (perm).split('-')[0]
                    module_action = (perm).split('-')[1]
                    access_modules_objects.append(Access_modules(roles_id = role_id, modules_name = module_name, actions = module_action))
                #Insert bulk list data into db
                Access_modules.objects.bulk_create(access_modules_objects)                    
                messages.success(request, "Form submited successfully")
                return redirect("permissions_list")
        except Exception as e:
            messages.error(request, "Failed to add :"+ str(e))
            return redirect("permissions_list")                                                          

def permissions_edit(request,id):
    if request.method == 'GET':
        try:
            myListData=[]                
            [myListData.append(i.modules_name+'-'+i.actions) for i in Access_modules.objects.filter(roles_id=id)]
            get_role = Roles.objects.get(pk=id)
            context={}
            context['get_role_id'] =get_role.id
            context['get_role_name'] =get_role.name
            context['myListData'] = unique(myListData)
            context['all_modules'] = Modules.objects.all()
            context['username'] = request.session["username"]
            return render(request,'permissions/permissions-edit.html',context) 
        except Exception as e:
            messages.error(request, "Failed to edit :"+ str(e))
            return redirect("permissions_list")
    if request.method == 'POST':
        myListData=[]                
        [myListData.append(i.modules_name+'-'+i.actions) for i in Access_modules.objects.filter(roles_id=id)]
        print('DB Value : ',myListData)
        dbdata = myListData
        try:
            payload = parse_qs(request.body.decode('utf-8')) 
            payload.pop('csrfmiddlewaretoken', None)
            print('Req Value : ',list(payload.keys()))
            reqData = list(payload.keys())
            access_modules_objects = []
            for i in reqData:
                if i in dbdata:
                    pass
                else:
                    print('Val in req not in db',i)
                    access_modules_objects.append(Access_modules(roles_id = id, modules_name = i.split('-')[0], actions = i.split('-')[1]))
            #Insert bulk list data into db
            Access_modules.objects.bulk_create(access_modules_objects) 

           
            for j in dbdata:
                if j in reqData:
                    pass
                else:
                    print('val in db not in req',j) 
                    Access_modules.objects.filter(roles_id = id, modules_name = j.split('-')[0], actions = j.split('-')[1]).delete()       
            messages.success(request, "Data updated successfully")
            return redirect("permissions_list")
        except Exception as e:
            messages.error(request, "Failed to edit :"+ str(e))
            return HttpResponseRedirect(reverse('permissions_edit', args=[id]))
               

def permissions_del(request,id):
    try:
        is_role_bind = Access_modules.objects.filter(roles_id=id)
        print(is_role_bind)
        if is_role_bind.exists():
            messages.error(request, "Failed to delete data bind with others")
            return redirect("permissions_list")
        else:    
            Roles.objects.filter(pk=id).delete()
            messages.success(request, "Role deleted successfully")
            return redirect("permissions_list")
    except Exception as e:
        messages.error(request, "Failed to delete :"+ str(e))
        return redirect("permissions_list")              

