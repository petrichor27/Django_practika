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
        a = Rule.objects.get(id = rule_id)
        t = Task.objects.filter(rule = a)
        for i in t:
            print(i.value)
        # t1 = Task.objects.get.all()
        
    except:
        raise Http404("Правило не найдено")
    return render(request, 'polls/detail.html', {'rule': a.name, 'task': t, 'Dictionaries': Dictionaries})

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
            print(rule_del )
            for i in rule_del:
                Rule.objects.filter(id=i).delete()
        return HttpResponseRedirect("/polls/")
    except Rule.DoesNotExist:
        return Http404("Rule not found")

