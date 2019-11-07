"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from cmdbs import views


urlpatterns = [
    url(r'admin/', include(admin.site.urls)),
    url(r'permission/$', views.permissions),
    url(r'index/$', views.index, name='index'),
    url(r'check_permissions/$', views.check_permissions),
    url(r'platform_base_page/$', views.platform_base_page),
    url(r'pcu/$', views.package_update),
    url(r'platform_show_ajax/$', views.platform_show_ajax),
    url(r'server_base_page/$', views.server_base_page),
    url(r'show_ajax_server/$', views.show_ajax_server),
    url(r'look_per/$', views.look_per),
    url(r'is_login/$', views.is_login, name='login'),
    url(r'is_logout/$', views.is_logout),
    url(r'home/$', views.home),
    url(r'add_del_permissions/$', views.add_del_permissions),
    url(r'record_operation_log/$', views.record_operation_log),
    url(r'logs/$', views.page_record_operation_log),
    url(r'db_check/$', views.db_check),
    url(r'server_action/$', views.server_action),
    url(r'create_servers/$', views.create_servers),
    url(r'search_add_servers/$', views.search_add_servers),
    url(r'del_servers/$', views.del_servers),
    url(r'platform_action/$', views.platform_action),
    url(r'client_update/$', views.client_update),
    url(r'user_page/$', views.user_page),
    url(r'manage_user_turn_page/$', views.manage_user_turn_page),
    url(r'add_del_edit_user/$', views.add_del_edit_user),
    url(r'add_servers_page/$', views.add_servers_page),
    url(r'edit_servers_page/$', views.edit_servers_page),
    url(r'add_user/$', views.add_user_page),
    url(r'edit_servers/$', views.edit_servers),
    url(r'upload/$', views.recv_file),
    url(r'add_platform/$', views.add_platform),
    url(r'edit_platform_page/$', views.edit_platform_page),
    url(r'editplas/$', views.edit_platform),
    url(r'deleteplas/$', views.del_platform),
    url(r'user_infos_page/$', views.user_infos_page),
    url(r'userinfo/$', views.userinfo),
    url(r'platform_img/$', views.platform_img),
    url(r'group_permissions/$', views.group_permissions),
    url(r'gcheckperm/$', views.group_check_permission),
    url(r'geditpermi/$', views.group_edit_permissions),
    url(r'api/$', views.servers_api),
]
