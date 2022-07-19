from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import Rule, Task, Dictionaries

def index(request):
    search = request.GET.get('search', None)
    if search and ',' in search:
        search, value = search.split(',')

        if search == 'name':
            rule = Rule.objects.filter(name = value)
        elif search == 'queue':
            rule = Rule.objects.filter(queue = value)
            rule |= Rule.objects.filter(queue = 'Очередь '+str(value))
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
        # else:
        #     task = Task.objects.all()

        new_t = request.GET.get('new', None)
        new_attr = None
        new_op = None
        new_t_op = None
        if new_t:
            new_t = new_t[:-1]
            
            if ',' in new_t:
                new_t_op = new_t.split(',')
                if len(new_t_op)>1:
                    new_attr = new_t_op[1]
                if len(new_t_op)>2:
                    new_op = new_t_op[2]
                new_t_op = new_t_op[0]
            else:
                new_t_op = new_t
        type1_attribute = None
        type2_attribute = None
        for i in task:
            if i.attribute == 'Тип задания 1':
                type1_attribute = i.value
            elif i.attribute == 'Тип задания 2':
                type2_attribute = i.value
        
        # for i in task:
        #     if i.value[0] == '[':
        #         i.value = i.value.replace('[','')
        #         i.value = i.value.replace(']','')
        #         i.value = i.value.replace("'",'')

    except:
        raise Http404("Правило не найдено")
    return render(request, 'polls/detail.html', {'rule': rule.name, 'task': task, 'Dictionaries': Dictionaries, 
                                                'attribute_temp': new_attr, 'type1': type1_attribute, 
                                                'type2':type2_attribute, 'new_op': new_op, 'new_t_op': new_t_op})

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

def add2(request, rule_id):
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

def update2(request, rule_id, task_id):
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
    # print()
    return render(request,'polls/detail_upd.html', {'rule': rule.name, 'task': task, 'Dictionaries': Dictionaries, 'attribute_temp': attribute2, 
                                                'type1': type1_attribute, 'type2': type2_attribute, 'id_to_update': task_id})
    
def save_update2(request, rule_id, task_id):  
    task = Task.objects.get(id = task_id)
    if request.method == "POST":
        task.operation_type = request.POST.get("operation")
        task.attribute = request.POST.get("attribute")
        task.operator = request.POST.get("operator")
        task.value =  str(request.POST.getlist("value"))
        task.save()
    # rule_list = Rule.objects.order_by('name')
    return HttpResponseRedirect("/polls/"+str(rule_id)+"/")


def delete(request):
    try:
        if request.method == "POST":
            rule_del = request.POST.getlist('checks')
            for i in rule_del:
                Rule.objects.filter(id=i).delete()
        return HttpResponseRedirect("/polls/")
    except Rule.DoesNotExist:
        return Http404("Rule not found")

def delete2(request,rule_id):
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

def back2(request,rule_id,task_id):
    return HttpResponseRedirect("/polls/"+str(rule_id)+"/")