from django.db import models
import csv

class Value_for_type123(models.Model):
    def __init__(self):
        self.values_list = []

    def read_types(self,file):  
        with open(file, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=';', quotechar='|')
            for row in reader:
                self.values_list.append(row)
        self.values_list.pop(0)
        
    def get_type1_list(self):
        self.read_types('Типы заданий.csv')
        type1 = []
        for i in self.values_list:
            if not i[0] in type1:
                type1.append(i[0])
        return type1

    def get_type2_list(self, type1):
        type2 = []
        for i in self.values_list:
            if i[0] == type1:
                type2.append(i[1])
        return type2

    def get_type3_list(self, type1, type2):
        type3 = []
        for i in self.values_list:
            if i[0] == type1 and i[1] == type2:
                type3.append(i[2])
        return type3


class Dictionaries(models.Model):
    all_queues = ['Очередь 1','Очередь 2','Очередь 3','Очередь 4']
    all_operations = ['AND','OR']
    all_attributes = {'Тип задания 1': 'Справочник','Тип задания 2':'Справочник','Тип задания 3': 'Справочник','Тип клиента': 'Справочник',
                    'Признак запроса ОГВ': 'Логический','Признак соответствия суммы критериям НС': 'Логический','Статус': 'Справочник',
                    'Предпочитаемый способ связи': 'Справочник','Тип действия': 'Справочник','Результат действия': 'Строка'}
    all_operators = ['=','!=','in','not in','like','not like']
    all_values = {'Тип клиента': ('Юридическое лицо', 'Физическое лицо'),
                    'Статус': ('Открыто', 'В работе', 'Создан наряд во внешней системе', 'Отклонен', 'Завершен'),
                    'Предпочитаемый способ связи': ('SMS', 'Звонок', 'Email', 'Письмо', 'Информирование не требуется'),
                    'Тип действия': ('Update','Delete','Create')}

    def get_operators(attribute):
        print("a:")
        print(attribute)
        if Dictionaries.all_attributes[attribute] == 'Логический':
            print("a")
            return ['=','!=']
        elif Dictionaries.all_attributes[attribute] == 'Справочник':
            print("a3")
            return ['=','!=','in','not in']
        else:
            print("a4") 
            return Dictionaries.all_operators

    def get_values(attribute): 
        if attribute == 'Тип задания 1':
            return Value_for_type123.get_type1_list()
        elif attribute in Dictionaries.all_values.keys():
                return list(Dictionaries.all_values[attribute])
        elif Dictionaries.all_attributes[attribute] == 'Логический':
            return ['Да','Нет']
        else: return None

    def get_values(attribute_name,attribute1):
        if attribute_name == 'Тип задания 2':
            return Value_for_type123.get_type2_list(attribute1)

    def get_values(attribute_name,attribute1,attribute2):
        if attribute_name == 'Тип задания 3':
            return Value_for_type123.get_type3_list(attribute1,attribute2)


class Rule(models.Model):
    name = models.CharField('Название', max_length = 200)
    queue = models.CharField('Очередь', max_length = 200, choices = [(i,i) for i in Dictionaries.all_queues], default = '-')
    rule_range = models.IntegerField('Ранг',unique=True)
    creator = models.CharField('Пользователь, который создал правило', max_length = 20)
    updator = models.CharField('Пользователь, который последним изменил правило', max_length = 20)
    create_date = models.DateTimeField('Дата создания правила', auto_now=False, auto_now_add=True)
    update_date = models.DateTimeField('Дата последнего изменения правила',auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Правило"
        verbose_name_plural = "Список правил"



class Task(models.Model):
    rule = models.ForeignKey(Rule, on_delete = models.CASCADE, verbose_name="Правило")
    operation_type = models.CharField('Тип', max_length = 5, choices = [(i,i) for i in Dictionaries.all_operations], default = '-')
    attribute = models.CharField('Атрибут', max_length = 200, choices = [(i[0],i[0]) for i in list(Dictionaries.all_attributes.items())], default = '-')
    operator = models.CharField('Оператор', max_length = 200, choices = [(i,i) for i in Dictionaries.all_operators], default = '-')
    value = models.CharField('Значение', max_length = 200)

    def __str__(self):
        return self.operation_type + " " + self.attribute + " " + self.operator + " " + self.value

    class Meta:
        verbose_name = "Правило маршрутизации заданий"
        verbose_name_plural = "Правила маршрутизации заданий"
