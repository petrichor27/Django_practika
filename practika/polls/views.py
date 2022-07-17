from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import Rule, Task, Dictionaries

def index(request):
    sort_type = request.GET.get('sort', None)
    if sort_type:
        rule_list = Rule.objects.order_by(sort_type)
    else:
        rule_list = Rule.objects.all()
    return render(request,'polls/list.html', {'rule_list': rule_list, 'Dictionaries': Dictionaries})

def detail(request, rule_id):
    try:
        rule = Rule.objects.get(id = rule_id)
        task = Task.objects.filter(rule = rule)
        attribute =  request.GET.get('attribute', None)
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
                                                'attribute_temp':attribute, 'type1': type1_attribute, 'type2':type2_attribute})

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
        task.value = request.POST.get("value_new")
        task.save()
    return HttpResponseRedirect("/polls/"+str(rule_id)+"/")

def update(request, rule_id):
    rule_list = Rule.objects.order_by('name')
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