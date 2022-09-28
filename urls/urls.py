from appname import views
from django.urls import path

urlpatterns = [
    #permissions
    path('permissions_list/',views.permissions_list,name="permissions_list" ),
    path('permissions_add/',views.permissions_add,name="permissions_add" ),
    path('permissions_edit/<int:id>/',views.permissions_edit,name="permissions_edit"),
    path('permissions_del/<int:id>/',views.permissions_del,name="permissions_del"),
    #permissions
]