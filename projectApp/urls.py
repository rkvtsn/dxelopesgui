from django.conf.urls import patterns, url

from projectApp import views

###
### TODO: мрак...
###

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^registration/$', views.registration, name='registration'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^projectlist/$', views.project_list, name='project_list'),
    url(r'^projectlist/newproject/$', views.new_project, name='new_project'),
    url(r'^projectlist/(?P<project>[\w\s\.]+)/delete/$', views.delete_project,
       name='delete_project'),
    url(r'^account/$', views.account, name='account'),
    url(r'^loginpage/$', views.login_page, name='login_page'),


    # url(r'^project/$', views.data, name='data'),
    url(r'^project/(?P<project>[\w\s\.]+)/data/$', views.data, name='data'),
    url(r'^project/(?P<project>[\w\s\.]+)/data/formData$', views.form_data, name='form_data'),
    url(r'^project/(?P<project>[\w\s\.]+)/data/(?P<name>[\w\s\.]+)/$', views.data_detail,
       name='data_detail'),
    url(r'^project/(?P<project>[\w\s\.]+)/data/(?P<name>[\w\s\.]+)/change/$', views.data_change,
       name='data_change'),
    url(r'^project/(?P<project>[\w\s\.]+)/data/(?P<name>[\w\s\.]+)/form_change/$', views.form_change,
       name='form_change'),
    url(r'^project/(?P<project>[\w\s\.]+)/data/(?P<name>[\w\s\.]+)/delete/$', views.data_delete,
       name='data_delete'),


    url(r'^project/(?P<project>[\w\s\.]+)/env/$', views.env,
        name='env'),
    url(r'^project/(?P<project>[\w\s\.]+)/env/add$', views.env_add,
        name='env_add'),
    url(r'^project/(?P<project>[\w\s\.]+)/env/delete$', views.env_delete,
        name='env_delete'),
    url(r'^project/(?P<project>[\w\s\.]+)/env/(?P<id>[\w\s\.-]+)$', views.env_details,
        name='env_details'),


    url(r'^project/(?P<project>[\w\s\.]+)/taskconf/$', views.taskconf,
       name='taskconf'),
    url(r'^project/(?P<project>[\w\s\.]+)/taskconf/save/$', views.taskconf_save,
       name='taskconf_save'),
    url(r'^project/(?P<project>[\w\s\.]+)/taskconf/getalg/(?P<task>[\w\s\.]+)/$', views.taskconf_alg,
       name='taskconf_alg'),
    url(r'^project/(?P<project>[\w\s\.]+)/taskconf/getfuncopt/(?P<func>[\w\s\.]+)/$',
       views.taskconf_func_opt,
       name='taskconf_func_opt'),
    url(r'^project/(?P<project>[\w\s\.]+)/taskconf/getalgopt/(?P<alg>[\w\s\.]+)/$',
       views.taskconf_alg_opt, name='taskconf_alg_opt'),






    url(r'^project/(?P<project>[\w\s\.]+)/models/$', views.models, name='models'),


    url(r'^project/(?P<project>[\w\s\.]+)/history/$', views.history, name='history'),


    url(r'^project/(?P<project>[\w\s\.]+)/tasks/$', views.tasks, name='tasks'),
    url(r'^project/(?P<project>[\w\s\.]+)/tasks/new_task/$', views.new_task, name='new_task'),
    url(r'^project/(?P<project>[\w\s\.]+)/tasks/(?P<name>[\w\s\.]+)/$', views.detail_task,
       name="detail_task"),
    url(r'^project/(?P<project>[\w\s\.]+)/tasks/(?P<name>[\w\s\.]+)/delete/$', views.delete_task,
       name='delete_task'),
    url(r'^project/(?P<project>[\w\s\.]+)/tasks/assignment/$', views.assignment, name='step2'),
    url(r'^project/(?P<project>[\w\s\.]+)/tasks/get_assignment_settings/$',
       views.get_assignment_settings, name='get_assignment_settings'),
]
