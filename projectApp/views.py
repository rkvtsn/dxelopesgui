from django.shortcuts import render, redirect
from django.http import *  # HttpResponse, JsonResponse, HttpResponseRedirect, HttpResponseNotAllowed
import json
from django.template.loader import render_to_string
import httplib2
from urllib.request import quote
import re

import collections

options_resp = [
    {
        "type": {
            "id": "MultiThread",
            "images": [
                "image 1",
                "image 2",
                "image 3",
                "image 4"
            ]
        },
        "createParameters": {
            "enviromentParameters": [
                {
                    "regexp": ".+",
                    "type": "String",
                    "name": "envName",
                    "displayName": "Enviroment Name"
                },
                {
                    "values": [
                        "image 1",
                        "image 2",
                        "image 3",
                        "image 4"
                    ],
                    "type": "ListBox",
                    "name": "image",
                    "displayName": "Image"
                }
            ],
            "serversParameters": {
                "identical": [
                    {
                        "max": 24,
                        "min": 1,
                        "type": "Integer",
                        "name": "cpus",
                        "displayName": "CPU's count"
                    },
                    {
                        "values": [
                            "1024",
                            "2048",
                            "4096",
                            "8192",
                            "16384"
                        ],
                        "type": "ListBox",
                        "name": "ram",
                        "displayName": "RAM"
                    },
                    {
                        "max": 512,
                        "min": 1,
                        "type": "Integer",
                        "name": "hdd",
                        "displayName": "HDD"
                    }
                ]
            }
        }
    },
    {
        "type": {
            "id": "ModelActor",
            "images": [
                "b2b24c7b-07ec-42ab-b4ec-3d387aa6f457"
            ]
        },
        "createParameters": {
            "enviromentParameters": [
                {
                    "regexp": ".+",
                    "type": "String",
                    "name": "envName",
                    "displayName": "Enviroment Name"
                },
                {
                    "max": 24,
                    "min": 1,
                    "type": "Integer",
                    "name": "serverCount",
                    "displayName": "Servers count"
                },
                {
                    "max": 24,
                    "min": 1,
                    "type": "Integer",
                    "name": "actorCount",
                    "displayName": "Actors count"
                },
                {
                    "values": [
                        "identical",
                        "difference"
                    ],
                    "type": "CheckBox",
                    "name": "options",
                    "displayName": "Servers Type"
                }
            ],
            "serversParameters": {
                "difference": [
                    {
                        "max": 24,
                        "min": 1,
                        "type": "Integer",
                        "name": "cpus",
                        "displayName": "CPU's count"
                    },
                    {
                        "values": [
                            "1024",
                            "2048",
                            "4096",
                            "8192",
                            "16384"
                        ],
                        "type": "ListBox",
                        "name": "ram",
                        "displayName": "RAM"
                    },
                    {
                        "max": 512,
                        "min": 1,
                        "type": "Integer",
                        "name": "hdd",
                        "displayName": "HDD"
                    },
                    {
                        "max": 24,
                        "min": 1,
                        "type": "Integer",
                        "name": "actors",
                        "displayName": "Actors count"
                    }
                ],
                "identical": [
                    {
                        "max": 24,
                        "min": 1,
                        "type": "Integer",
                        "name": "cpus",
                        "displayName": "CPU's count"
                    },
                    {
                        "values": [
                            "1024",
                            "2048",
                            "4096",
                            "8192",
                            "16384"
                        ],
                        "type": "ListBox",
                        "name": "ram",
                        "displayName": "RAM"
                    },
                    {
                        "max": 512,
                        "min": 1,
                        "type": "Integer",
                        "name": "hdd",
                        "displayName": "HDD"
                    }
                ]
            }
        }
    }
]

get_env1_resp = {
    "id": "abccbfe5-47c7-4e9e-b440-fd5f47aaf223",
    "name": "model4",
    "type": "ModelActor",
    "image": "image 5",
    "servers": [
        {
            "id": "f6aa1de6-bd97-43e6-9c90-a4c1abf2b839",
            "status": "ACTIVE",
            "name": "model4-server-0",
            "cpus": "2",
            "ram": "512",
            "hdd": "25",
            "fixedIp": "fixedIp",
            "floatIp": "floatIp",
            "actors": "2"
        },
        {
            "id": "f7038ad7-dd23-4c27-b2a5-2bb93b3eefe1",
            "status": "ACTIVE",
            "name": "model4-server-1",
            "cpus": "2",
            "ram": "512",
            "hdd": "25",
            "fixedIp": "fixedIp",
            "floatIp": "floatIp",
            "actors": "2"
        }
    ]
}

get_env2_resp = {
    "id": "88da4d05-2d9f-4f59-882a-2084a7c1bdf1",
    "name": "model5",
    "type": "ModelActor",
    "image": "image 4",
    "servers": [
        {
            "id": "a9c49f04-79cf-4b81-825f-51083e8f8b74",
            "status": "SLEEP",
            "name": "model5-server-0",
            "cpus": "1",
            "ram": "512",
            "hdd": "25",
            "fixedIp": "fixedIp",
            "floatIp": "floatIp",
            "actors": "1"
        },
        {
            "id": "9bcee38a-984d-4e79-bbb2-1a30520054e9",
            "status": "ACTIVE",
            "name": "model5-server-1",
            "cpus": "2",
            "ram": "1024",
            "hdd": "25",
            "fixedIp": "fixedIp",
            "floatIp": "floatIp",
            "actors": "2"
        }
    ]
}

get_env3_resp = {
    "id": "bc5e23fa-231b-4a17-a146-c3288331b1b8",
    "name": "MultiThread 4",
    "type": "MultiThread",
    "image": "image 5",
    "servers": [
        {
            "id": "a64d5070-eb23-46eb-bbcf-317a979a1dbd",
            "status": "ACTIVE",
            "name": "MultiThread 4-server-0",
            "cpus": "4",
            "ram": "512",
            "hdd": "25",
            "fixedIp": "fixedIp",
            "floatIp": "floatIp"
        }
    ]
}

env_resp = list([get_env1_resp, get_env2_resp, get_env3_resp])

env_list_resp = {
    "88da4d05-2d9f-4f59-882a-2084a7c1bdf1": "model5",
    "abccbfe5-47c7-4e9e-b440-fd5f47aaf223": "model4",
    "bc5e23fa-231b-4a17-a146-c3288331b1b8": "MultiThread 4"
}

MAIN_URL = "http://localhost:8080/dmcapi-rest/"
DATA_URL = "http://localhost:8080/DataType/MetaData/"


def make_url(user, project):
    return MAIN_URL + "user/" + quote(user, '') + "/project/" + quote(project, '')


# check that user login
def custom_login_required(f):
    def tmp(request, *args, **kwargs):
        if 'user' not in request.session and 'password' not in request.session:
            return redirect('login_page')
        else:
            return f(request, *args, **kwargs)

    return tmp


# PUT and POST request
def send_message(user, password, url, method, message, headers):
    h = httplib2.Http()
    h.add_credentials(user, password)
    resp, content = h.request(url, method=method, body=message, headers=headers)
    return resp, content


# GET and DELETE message
def get_message(user, password, url, method, headers):
    h = httplib2.Http()
    h.add_credentials(user, password)
    resp, content = h.request(url, method=method, headers=headers)
    return resp, content


def decode_json(content):
    string = content.decode("utf-8")
    return json.loads(string)


def code_json(dic):
    string = json.dumps(dic)
    return bytes(string.encode('utf-8'))


def index(request):
    if 'user' in request.session:
        user_name = request.session['user']
        return render(request, 'index.html', {'user': user_name})
    else:
        return render(request, 'index.html')


def login_page(request):
    if 'user' not in request.session and 'password' not in request.session:
        return render(request, 'login.html')
    else:
        return redirect('index')


def login(request):
    result = {'result': 'error'}
    name = request.POST['name']
    password = request.POST['password']

    if name != "" and password != "":

        h = httplib2.Http()
        h.add_credentials(name, password)
        resp, content = h.request(MAIN_URL, 'GET')

        if resp.status == 200:
            result = {'result': 'success'}
            request.session['user'] = name
            request.session['password'] = password

    return JsonResponse(result)


def make_request(url, method, request=None, data=None):
    pkg = json.dumps(data)
    body = bytes(pkg.encode('utf-8'))

    h = httplib2.Http()
    if request is not None:
        h.add_credentials(request.session['user'], request.session['password'])

    return h.request(url, method=method, body=body, headers={'content-type': 'application/json;charset=UTF-8',
                                                             'accept': 'application/json'})


def registration(request):
    result = {'result': 'error'}
    name = request.POST['name']
    password = request.POST['password']

    if name != "" and password != "":

        url = MAIN_URL + "user"

        pkg = json.dumps(data)
        body = bytes(pkg.encode('utf-8'))

        h = httplib2.Http()
        h.add_credentials('admin', 'admin')

        resp, content = h.request(url, method='PUT', body=body,
                                  headers={'content-type': 'application/json;charset=UTF-8',
                                           'accept': 'application/json'})

        if resp.status == 201:
            result = {'result': 'success'}
            request.session['user'] = name
            request.session['password'] = password

    return JsonResponse(result)


def logout(request):
    result = {'result': 'error'}
    del request.session['user']
    del request.session['password']
    return JsonResponse(result)


@custom_login_required
def project_list(request):
    user_name = request.session['user']

    h = httplib2.Http()
    h.add_credentials(request.session['user'], request.session['password'])

    url = MAIN_URL + "user/" + user_name + "/project"
    resp, content = h.request(url, method='GET', headers={'accept': 'application/json'})

    if resp.status == 200:
        string = content.decode('utf-8')
        json_data = json.loads(string)
        projectlist = json_data["projectNames"]

        return render(request, 'projectlist.html', {'user': user_name, 'projectlist': projectlist})
    else:
        return render(request, 'projectlist.html', {'user': user_name, 'error': "Error!"})


@custom_login_required
def new_project(request):
    result = {'result': 'error'}

    proj_name = request.POST['projname']
    dic = {'projectName': proj_name}
    string = json.dumps(dic)
    body = bytes(string.encode('utf-8'))

    url = MAIN_URL + "user/" + request.session['user'] + "/project"

    h = httplib2.Http()
    h.add_credentials(request.session['user'], request.session['password'])
    resp, content = h.request(url, method="PUT", body=body, headers={'content-type': 'application/json;charset=UTF-8',
                                                                     'accept': 'application/json'})

    if resp.status == 201:
        result = {'result': 'success'}

    return JsonResponse(result)


@custom_login_required
def delete_project(request, project):
    result = {'result': 'error'}

    url = MAIN_URL + "user/" + request.session['user'] + "/project/" + quote(project, '')

    h = httplib2.Http()
    h.add_credentials(request.session['user'], request.session['password'])
    resp, content = h.request(url, method="DELETE", body=project, headers={'accept': 'application/json'})

    if resp.status == 200:
        result = {'result': 'success'}

    return JsonResponse(result)


@custom_login_required
def account(request):
    user_name = request.session['user']
    return render(request, 'account.html', {'user': user_name})


# Данные ------------------------------------------------------------------------------------------------------
# DATA_URL = "http://10.146.7.1:8080/dmcapi-rest/DataType/MetaData/"


@custom_login_required
def data(request, project):
    user = request.session['user']
    password = request.session['password']

    url = make_url(user, project) + "/dataType/metaData/"

    resp, content = get_message(user, password, url, "GET", {'accept': 'application/json'})

    saved_data = decode_json(content)

    return render(request, 'data/data.html', {'title': 'Данные',
                                              'saved_data': saved_data,
                                              'user': user,
                                              'project_name': project})


@custom_login_required
def form_data(request, project):
    user = request.session['user']
    password = request.session['password']
    data_type = request.POST['radioData']
    dic = {}

    if data_type == 'file':
        if request.POST['file'] == '' or request.POST['name'] == '':
            result = {'result': 'error', 'message': 'You must fill all fields.'}
            JsonResponse(result)
        else:
            dic = {'dataName': request.POST['name'], 'dataPath': request.POST['file'], 'dataType': data_type,
                   'attribute': {}}

    if data_type == 'table':
        if request.POST['url'] == '' or request.POST['name'] == '':
            result = {'result': 'error', 'message': 'You must fill all fields.'}
            JsonResponse(result)
        else:
            dic = {'dataName': request.POST['name'], 'dataPath': request.POST['url'], 'dataType': data_type,
                   'attribute': {}}

    body = code_json(dic)

    url = MAIN_URL + "user/" + quote(user, '') + "/project/" + quote(project, '') + "/dataType/metaData/"

    resp, content = send_message(user, password, url, "PUT", body, {'content-type': 'application/json',
                                                                    'accept': 'application/json'})

    if resp.status == 201:
        data_name = request.POST['name']
        result = {'result': 'success', 'data_name': data_name}
        return JsonResponse(result)

    else:
        result = {'result': 'error', 'message': 'Error uploaded data set.'}
        return JsonResponse(result)


@custom_login_required
def data_detail(request, project, name):
    url = "http://localhost:8080/dmcapi-rest/" + "user/" + quote(request.session['user'], '') + "/project/" + quote(
        project, '') + "/dataType/metaData/" + quote(name, '')

    h = httplib2.Http()
    h.add_credentials(request.session['user'], request.session['password'])
    resp, content = h.request(url, method='GET', headers={'accept': 'application/json'})
    string = content.decode('utf-8')
    json_data = json.loads(string)

    data_name = json_data['dataName']
    data_path = json_data['dataPath']
    data_type = json_data['dataType']
    attribute = json_data['attribute']

    attributeContaners = attribute['attributeContaners']

    data = {}

    for attr in attributeContaners:
        for k, v in attr.items():
            if k == 'physicalDTO':
                name = v['name']
                val = v['dataType']
                data[name] = val

    user_name = request.session['user']
    project_name = project

    return render(request, 'data/detail.html', {'name': data_name,
                                                'path': data_path,
                                                'type': data_type,
                                                'data': data,
                                                'user': user_name,
                                                'project_name': project_name})


def data_change(request, project, name):
    data_name = name
    return render(request, 'data/change.html', {'name': data_name})


def form_change(request, project, name):
    return HttpResponse(name)


@custom_login_required
def data_delete(request, project, name):
    user = request.session['user']
    password = request.session['password']

    url = "http://localhost:8080/dmcapi-rest/" + "user/" + quote(user, '') + "/project/" + quote(
        project, '') + "/dataType/metaData/" + quote(name, '')

    resp, content = get_message(user, password, url, "DELETE", {'accept': 'application/json'})

    if resp.status == 200:
        return JsonResponse({"result": "success"})
    else:
        return JsonResponse({"result": "error", "error": resp.status})


# Environment configuration -----------------------------------------------------------------------------------
# @env

@custom_login_required
def env(request, project):
    user_name = request.session['user']
    # resp, content = make_request(url=MAIN_URL + "/user/" + quote(user_name, '') + "/project/" + quote(project, '') + "/env/types", request=request, method='GET')
    # if resp.status != 200:
    #    return render(request, 'my404.html')

    # s_data = content.decode('utf-8')
    # options = json.loads(s_data)
    options = json.dumps(options_resp)

    env_data = env_list_resp

    # resp, content = make_request(url=MAIN_URL + "/user/" + quote(user_name, '') + "/project/" + quote(project, '') + "/env/", request=request, method='GET')
    # environments = content.decode('utf-8')

    return render(request, 'environment/environment.html', {'options': options,
                                                            'user': user_name,
                                                            'env_data': env_data,
                                                            'project_name': project})


def env_details(request, project, id):
    user_name = request.session['user']
    result = []

    #url = MAIN_URL + "user/%s/project/%s/env/%s" % (quote(user_name, ''), quote(project, ''), quote(id, ''))

    #env = get_env1_resp
    if id in ('0', '1', '2'):
        environment = env_resp[int(id)]
    else:
        environment = env_resp[0]

    environment = collections.OrderedDict(sorted(environment.items()))
    # if len(result) == 0:
    #     return render(request, 'my404.html', {'user': user_name,
    #                                           'project_name': project})

    return render(request, 'environment/details.html', {'env_data': environment,
                                                        'user': user_name,
                                                        'project_name': project})


def validate_env_options(opt, options, is_server=False):
    error = None
    value = None

    try:
        if not is_server:
            value = (options[opt['name']][0])
        else:
            value = (options[opt['name'] + '[]'][0])

        # String
        if 'regexp' in opt and not re.match(opt['regexp'], value):
            error = opt['displayName'] + ' wrong input!'

        # Integer
        if 'max' in opt:
            if not is_server:
                options[opt['name']][0] = int(value)
            else:
                options[opt['name'] + '[]'][0] = int(value)
            if int(value) > opt['max'] or int(value) < opt['min']:
                error = opt['displayName'] + ' value must be in range: ' + str(opt['min']) + ' - ' + str(opt['max'])

        # ListBox
        if 'values' in opt and value not in opt['values']:
            error = opt['displayName'] + ' wrong input from ListBox'
    except Exception as e:
        print(e)
    return error


@custom_login_required
def env_add(request, project):
    result = {'result': 'error', 'msg': 'Unknown error!'}

    post_data = dict(request.POST)

    errors = []

    options_typed = [t for t in options_resp if t['type']['id'] == post_data['type'][0]][0]['createParameters']
    for opt1 in options_typed:
        for opt2 in options_typed[opt1]:
            if type(opt2) is str:
                for opt in options_typed[opt1][opt2]:
                    try:
                        error = validate_env_options(opt, post_data, True)
                        if error is not None:
                            errors.append(error)
                    except:
                        errors.append("Wrong input!")
            else:
                try:
                    error = validate_env_options(opt2, post_data)
                    if error is not None:
                        errors.append(error)
                except:
                    errors.append("Wrong input!")

    if len(errors) != 0:
        return JsonResponse({'result': 'error', 'errors': errors})

    d = {}
    for k, v in post_data.items():
        if k.startswith('csrf'):
            continue
        if not k.endswith('[]'):
            d[k] = v[0]

    if 'serverCount' not in d:
        d['serverCount'] = 1
    server_count = int(d['serverCount'])

    d['servers'] = [dict() for _ in range(server_count)]

    server_params = [x for x in post_data.items() if x[0].endswith('[]')]

    for i in range(server_count):
        for k, v in server_params:
            d['servers'][i][k.replace('[]', '')] = v[i]

    user = request.session['user']
    resp, content = make_request(url=MAIN_URL + 'user/' + quote(user, '') + '/project/' + quote(project, '') + '/env/',
                                 method='PUT', request=request, data=d)

    if resp.status == 200:
        result = {'result': 'success'}

    return JsonResponse(result)


@custom_login_required
def env_delete(request, project):
    result = {'result': 'error'}
    user = request.session['user']
    password = request.session['password']

    id = request.POST['id']

    url = MAIN_URL + "user/%s/project/%s/env/%s" % (quote(user, ''), quote(project, ''), quote(id, ''))

    resp, content = make_request(url, 'DELETE', request)
    if resp.status == 200:
        result = {'result': 'success'}

    return JsonResponse(result)


# Task configuration ------------------------------------------------------------------------------------------


@custom_login_required
def taskconf(request, project):
    task_list = ["Classification", "Regression", "Association rules", "Clustering"]
    alg_list = ["Classification algorithm 1", "Classification algorithm 2", "Classification algorithm 3"]

    user_name = request.session['user']

    h = httplib2.Http()
    h.add_credentials(request.session['user'], request.session['password'])

    url = make_url(user_name, project)
    resp, content = h.request(url, method='GET', headers={'accept': 'application/json'})

    saved_data = []

    if resp.status == 200:
        string = content.decode('utf-8')
        json_data = json.loads(string)

    # saved_data = json_data["projectNames"]

    return render(request, 'task/task.html', {'task_list': task_list,
                                              'alg_list': alg_list,
                                              'user': user_name,
                                              'project_name': project,
                                              'saved_data': saved_data})


def taskconf_save(request, project):
    result = {'result': 'success'}
    return JsonResponse(result)


def taskconf_alg(request, project, task):
    alg_list = []

    if task == "Classification":
        alg_list = ["Classification algorithm 1", "Classification algorithm 2", "Classification algorithm 3"]
    if task == "Regression":
        alg_list = ["Regression algorithm 1", "Regression algorithm 2", "Regression algorithm 3"]
    if task == "Association rules":
        alg_list = ["Association rules algorithm 1", "Association rules algorithm 2", "Association rules algorithm 3"]
    if task == "Clustering":
        alg_list = ["Clustering algorithm 1", "Clustering algorithm 2", "Clustering algorithm 3"]

    result = {'alg_list': alg_list}

    return JsonResponse(result)


def taskconf_func_opt(request, project, func):
    option_list = {}

    if func == "Classification":
        option_list = {'Classification opt 1': 'int',
                       'Classification opt 2': 'string',
                       'Classification opt 3': 'string'}
    if func == "Regression":
        option_list = {'Regression opt 1': 'int',
                       'Regression opt 2': 'string',
                       'Regression opt 3': 'int',
                       'Regression opt 4': 'string'}
    if func == "Association rules":
        option_list = {'Association rules opt 1': 'int',
                       'Association rules opt 2': 'string'}
    if func == "Clustering":
        option_list = {'Clustering opt 1': 'int', 'Clustering opt 2': 'string'}

    result = {'option_list': option_list}
    return JsonResponse(result)


def taskconf_alg_opt(request, project, alg):
    option_list = {'label name 1': 'int', 'label name 2': 'string'}
    result = {'option_list': option_list}
    return JsonResponse(result)


# Задачи ------------------------------------------------------------------------------------------------------


@custom_login_required
def tasks(request, project):
    user = request.session['user']
    password = request.session['password']

    # url for get data sets
    url_data = MAIN_URL + "user/" + quote(user, '') + "/project/" + quote(project, '') + "/dataType/metaData"

    # url for get saved tasks
    url_task = MAIN_URL + "user/" + quote(user, '') + "/project/" + quote(project, '') + "/miningTask"

    # get data sets
    resp_data, content_data = get_message(user, password, url_data, "GET", {'accept': 'application/json'})
    json_data = decode_json(content_data)
    list_physical_data_set = json_data

    # get saved tasks
    resp_task, content_task = get_message(user, password, url_task, "GET", {'accept': 'application/json'})
    saved_data = decode_json(content_task)

    # get environment list
    # environment_list = []#["environment 1", "environment 2", "environment 3"]

    # get mining function list
    mining_function_list = []  # ["mining function 1", "mining function 2", "mining function 3"]

    # result inf
    result_data = {'listPhysicalDataSet': list_physical_data_set, 'saved_data': saved_data,
                   'user': user, 'project_name': project, 'environment_list': [],
                   'mining_function_list': mining_function_list}

    return render(request, 'tasks/tasks.html', result_data)


@custom_login_required
def new_task(request, project):
    user = request.session['user']
    password = request.session['password']

    url = MAIN_URL + "user/" + quote(user, '') + "/project/" + quote(project, '') + "/miningTask"

    # get data array
    data_name_list = request.POST['arr_selects'].split(',')
    data_val_list = []

    for data_name in data_name_list:
        data_val_list.append(request.POST[data_name])

    # get data parameters
    data_arr = []

    for data_val in data_val_list:
        url_data = MAIN_URL + "user/" + quote(user, '') + "/project/" + quote(project,
                                                                              '') + "/dataType/metaData/" + quote(
            data_val, '')
        resp, content = get_message(user, password, url_data, "GET", {'accept': 'application/json'})
        json_data = decode_json(content)
        data_arr.append({"dataPath": json_data['dataPath'],
                         "dataName": data_val,
                         "dataType": json_data['dataType'],
                         "attribute": json_data['attribute']})

    dic = {"miningTaskName": request.POST['name'], "dataSourceDTO": data_arr}
    body = code_json(dic)

    resp, content = send_message(user, password, url, "PUT", body, {'content-type': 'application/json',
                                                                    'accept': 'application/json'})

    if resp.status == 201:
        result = {'result': 'success', 'task_name': request.POST['name']}
    else:
        result = {'result': 'error', 'error': resp.status}

    return JsonResponse(result)


@custom_login_required
def detail_task(request, project, name):
    user = request.session['user']
    password = request.session['password']

    url = MAIN_URL + "user/" + quote(user, '') + "/project/" + quote(project, '') + "/miningTask/" + quote(name, '')

    resp, content = get_message(user, password, url, "GET", {'accept': 'application/json'})
    json_data = decode_json(content)

    data_source_dto = json_data['dataSourceDTO']

    data_source = []

    for data in data_source_dto:
        for k, v in data.items():
            if k == 'dataName':
                data_source.append(v)

    result_data = {'user': user, 'project_name': project, 'name': name, 'data_source': data_source}

    return render(request, 'tasks/detail.html', result_data)


@custom_login_required
def delete_task(request, project, name):
    user = request.session['user']
    password = request.session['password']

    url = MAIN_URL + "user/" + quote(user, '') + "/project/" + quote(project, '') + "/miningTask/" + quote(name, '')

    resp, content = get_message(user, password, url, "DELETE", {'accept': 'application/json'})

    if resp.status == 200:
        result = {'result': 'success', 'error': resp.status}
    else:
        result = {'result': 'error', 'error': resp.status}

    return JsonResponse(result)


@custom_login_required
def assignment(request, project):
    typeTransform = ["Direct Assignment", "Pivot Assignment", "Set Assignment", "Reverse Pivot Assignment"]

    physicalData = [
        ['physicalName1', 'string'],
        ['physicalName2', 'integer'],
        ['physicalName3', 'double'],
        ['physicalName4', 'string'],
        ['physicalName5', 'integer'],
        ['physicalName6', 'double'],
        ['physicalName7', 'boolean']
    ]

    logicalData = [
        ['logicalName1', 'categorical'],
        ['logicalName2', 'numerical'],
        ['logicalName3', 'numerical'],
        ['logicalName4', 'categorical'],
        ['logicalName5', 'numerical'],
        ['logicalName6', 'numerical'],
        ['logicalName7', 'categorical']
    ]

    typeLogicalData = ['categorical', 'numerical']

    user_name = request.session['user']
    project_name = project

    data = {
        'typeTransform': typeTransform,
        'physicalData': physicalData,
        'logicalData': logicalData,
        'typeLogicalData': typeLogicalData,
        'user': user_name,
        'project_name': project_name
    }

    return render(request, 'tasks/assignment.html', data)


def get_assignment_settings(request, project):
    if request.method == 'GET':
        if request.GET.get('type') == 'Direct Assignment':

            # получить данные
            attributes = [
                ['physicalName1', 'string', 'logicalName1', 'categorical'],
                ['physicalName2', 'integer', 'logicalName2', 'numerical'],
                ['physicalName3', 'double', 'logicalName3', 'numerical'],
                ['physicalName4', 'string', 'logicalName4', 'categorical'],
                ['physicalName5', 'integer', 'logicalName5', 'numerical'],
                ['physicalName6', 'double', 'logicalName6', 'numerical'],
                ['physicalName7', 'boolean', 'logicalName7', 'categorical']
            ]

            types_logical_attr = ["numerical", "categorical", "ordinal", "notSpecified"]

            html = render_to_string('tasks/assignment/direct.html',
                                    {'attributes': attributes, 'typesLogicalData': types_logical_attr})
        elif request.GET.get('type') == 'Pivot Assignment':
            attributes = [
                ['physicalName1', 'string', 'logicalName1', 'categorical'],
                ['physicalName2', 'integer', 'logicalName2', 'numerical'],
                ['physicalName3', 'double', 'logicalName3', 'numerical'],
                ['physicalName4', 'string', 'logicalName4', 'categorical'],
                ['physicalName5', 'integer', 'logicalName5', 'numerical'],
                ['physicalName6', 'double', 'logicalName6', 'numerical'],
                ['physicalName7', 'boolean', 'logicalName7', 'categorical']
            ]

            html = render_to_string('tasks/assignment/pivot.html', {'attributes': attributes})
        elif request.GET.get('type') == 'Set Assignment':
            attributes = [
                ['physicalName1'],
                ['physicalName2'],
                ['physicalName3'],
                ['physicalName4'],
                ['physicalName5'],
                ['physicalName6'],
                ['physicalName7']
            ]

            types = ["numerical", "categorical", "ordinal", "notSpecified"]

            result = {
                'attributes': attributes,
                'types': types
            }

            html = render_to_string('tasks/assignment/set.html', result)
        elif request.GET.get('type') == 'Reverse Pivot Assignment':
            # получить данные
            attributes = [
                ['physicalName1'],
                ['physicalName2'],
                ['physicalName3'],
                ['physicalName4'],
                ['physicalName5'],
                ['physicalName6'],
                ['physicalName7']
            ]

            functions_select_attribute = ["isNotNull", "isNull", "isOne", "isZero", "isTrue", "isFalse"]

            functions_select_value = ["value", "attribute"]

            result = {'attributes': attributes,
                      'functions_select_attribute': functions_select_attribute,
                      'functions_select_value': functions_select_value}

            html = render_to_string('tasks/assignment/reversepivot.html', result)
        else:
            # получить данные
            attributes = [
                ['physicalName1', 'string', 'logicalName1', 'categorical'],
                ['physicalName2', 'integer', 'logicalName2', 'numerical'],
                ['physicalName3', 'double', 'logicalName3', 'numerical'],
                ['physicalName4', 'string', 'logicalName4', 'categorical'],
                ['physicalName5', 'integer', 'logicalName5', 'numerical'],
                ['physicalName6', 'double', 'logicalName6', 'numerical'],
                ['physicalName7', 'boolean', 'logicalName7', 'categorical']
            ]

            types_logical_attr = ["numerical", "categorical", "ordinal", "notSpecified"]

            result = {
                'attributes': attributes,
                'typesLogicalData': types_logical_attr
            }

            html = render_to_string('tasks/assignment/direct.html', result)

        return HttpResponse(html)
    else:
        return JsonResponse({'result': 'error'})


# Models -----------------------------------------------------------------------------------


@custom_login_required
def models(request, project):
    user_name = request.session['user']
    project_name = project

    return render(request, 'models/models.html', {'user': user_name, 'project_name': project_name})


# LOG -------------------------------------------------------------------------------------


@custom_login_required
def history(request, project):
    user_name = request.session['user']
    project_name = project

    return render(request, 'history/history.html', {'user': user_name, 'project_name': project_name})
