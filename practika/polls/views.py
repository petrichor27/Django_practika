from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import Rule, Task, Dictionaries

def index(request):
    search = request.GET.get('search', None)
    search_text = request.GET.get('text', None)
    if search and search_text:
        if search == 'name':
            rule = Rule.objects.filter(name = search_text)
        elif search == 'queue':
            rule = Rule.objects.filter(queue = search_text)
            rule |= Rule.objects.filter(queue = 'Очередь '+str(search_text))
        return render(request,'polls/list.html', {'rule_list': rule, 'Dictionaries': Dictionaries, 'search': True})
  
    sort_type = request.GET.get('sort', None)
    if sort_type:
        rule_list = Rule.objects.order_by(sort_type)
    else:
        rule_list = Rule.objects.all()
    return render(request,'polls/list.html', {'rule_list': rule_list, 'Dictionaries': Dictionaries, 'search': False})

def detail(request, rule_id):
    try:
        rule = Rule.objects.get(id = rule_id)
        task = Task.objects.filter(rule = rule)

        sort_type = request.GET.get('sort', None)
        if sort_type:
            task = task.order_by(sort_type)
        
        new_operation = request.GET.get('operation', None)
        new_attribute = request.GET.get('attribute', None)
        new_operator = request.GET.get('operator', None)
        
        type1_attribute = None
        type2_attribute = None
        for i in task:
            if i.attribute == 'Тип задания 1':
                type1_attribute = i.value
            elif i.attribute == 'Тип задания 2':
                type2_attribute = i.value
    except:
        raise Http404("Правило не найдено")
    return render(request, 'polls/detail.html', {'rule': rule.name, 'task': task, 'Dictionaries': Dictionaries, 
                                                'attribute_temp': new_attribute, 'type1': type1_attribute, 
                                                'type2':type2_attribute, 'new_operation': new_operation, 'new_operator': new_operator})

def add(request):
    if request.method == "POST":
        rule = Rule()
        rule.name = request.POST.get("name_new")
        rule.queue = request.POST.get("queue_new")
        rule.rule_range = request.POST.get("rule_range_new")
        rule.creator = 'admin'
        rule.updator = 'admin'
        rule.save()
    return HttpResponseRedirect("/polls/")

def add_for_task_table(request, rule_id):
    if request.method == "POST":
        task = Task()
        task.rule = Rule.objects.get(id = rule_id)
        task.operation_type = request.POST.get("operation_new")
        task.attribute = request.POST.get("attribute_new")
        task.operator = request.POST.get("operator_new")
        task.value = request.POST.getlist("value_new")
        task.save()
    return HttpResponseRedirect("/polls/"+str(rule_id)+"/")

def update(request, rule_id):
    rule_list = Rule.objects.all()
    return render(request,'polls/list_upd.html', {'rule_list': rule_list, 'Dictionaries': Dictionaries, 'id_to_update': rule_id})
    
def save_update(request, rule_id):  
    rule = Rule.objects.get(id = rule_id)
    if request.method == "POST":
        rule.name = request.POST.get("name")
        rule.queue = request.POST.get("queue")
        rule.rule_range = request.POST.get("rule_range")
        rule.creator = 'admin'
        rule.updator = 'admin'
        rule.save()
    rule_list = Rule.objects.order_by('name')
    return HttpResponseRedirect("/polls/")

def update_for_task_table(request, rule_id, task_id):
    rule = Rule.objects.get(id = rule_id)
    task = Task.objects.filter(rule = rule)
    upd_task = Task.objects.filter(id = task_id)
    type1_attribute = None
    type2_attribute = None
    for i in task:
        if i.attribute == 'Тип задания 1':
            type1_attribute = i.value
        elif i.attribute == 'Тип задания 2':
            type2_attribute = i.value
    attribute2 = request.GET.get('attribute', upd_task[0].attribute)
    return render(request,'polls/detail_upd.html', {'rule': rule.name, 'task': task, 'Dictionaries': Dictionaries, 'attribute_temp': attribute2, 
                                                'type1': type1_attribute, 'type2': type2_attribute, 'id_to_update': task_id})
    
def save_update_for_task_table(request, rule_id, task_id):  
    task = Task.objects.get(id = task_id)
    if request.method == "POST":
        task.operation_type = request.POST.get("operation")
        task.attribute = request.POST.get("attribute")
        task.operator = request.POST.get("operator")
        task.value =  str(request.POST.getlist("value"))
        task.save()
    return HttpResponseRedirect("/polls/"+str(rule_id)+"/")

def delete(request):
    print(request)
    try:
        if request.method == "POST":
            rule_del = request.POST.getlist('checks')

            for i in rule_del:

                Rule.objects.filter(id=i).delete()
        return HttpResponseRedirect("/polls/")
    except Rule.DoesNotExist:
        return Http404("Rule not found")

def delete_for_task_table(request,rule_id):
    try:
        if request.method == "POST":
            task_del = request.POST.getlist('checks')
            for i in task_del:
                Task.objects.filter(id=i).delete()
        return HttpResponseRedirect("/polls/"+str(rule_id)+"/")
    except Rule.DoesNotExist:
        return Http404("Rule not found")

def back(request,rule_id):
    return HttpResponseRedirect("/polls/")

def back_for_task_table(request,rule_id,task_id):
    return HttpResponseRedirect("/polls/"+str(rule_id)+"/")