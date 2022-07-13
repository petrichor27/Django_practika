from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from .models import Rule, Task, Dictionaries

def index(request):
    rule_list = Rule.objects.order_by('name')
    return render(request,'polls/list.html', {'rule_list': rule_list, 'Dictionaries': Dictionaries})

def detail(request, rule_id):
    try:
        a = Rule.objects.get(id = rule_id)
    except:
        raise Http404("Правило не найдено")

    return render(request, 'polls/detail.html', {'rule': a})

#????
# сохранение данных в бд
def create(request):
    if request.method == "POST":
        rule = Rule()
        rule.name = request.POST.get("name")
        rule.queue = request.POST.get("queue")
        rule.rule_range = request.POST.get("rule_range")
        rule.creator = 'admin'
        rule.updator = 'admin'
        # rule.create_date = request.POST.get("create_date")
        # rule.update_date = request.POST.get("update_date")
        rule.save()
    return HttpResponseRedirect("polls/list.html")

# изменение данных в бд
def edit(request, id):
    try:
        rule_list = Rule.objects.get(id = rule_id)
 
        if request.method == "POST":
            rule_list.name = request.POST.get("name")
            rule_list.queue = request.POST.get("queue")
            rule_list.rule_range = request.POST.get("rule_range")
            rule_list.creator = request.POST.get("creator")
            rule_list.updator = request.POST.get("updator")
            rule_list.create_date = request.POST.get("create_date")
            rule_list.update_date = request.POST.get("update_date")
            rule_list.save()
            return HttpResponseRedirect("/polls/")
        else:
            return render(request, "list.html", {"rule_list": rule_list})
    except Person.DoesNotExist:
        return Http404("Rule not found")
     
# удаление данных из бд
def delete(request):
    try:
        rule_del  = request.POST.getlist('checks')
        print(rule_del)
        for i in rule_del:
            Rule.objects.filter(id=i).delete()
        return HttpResponseRedirect("/polls/")
    except Rule.DoesNotExist:
        return Http404("Rule not found")
