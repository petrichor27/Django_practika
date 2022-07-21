from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index'),
    path('back/', views.index, name='index'),
    path('<int:rule_id>/', views.detail, name='detail'),
    path('delete/', views.delete),
    path('<int:rule_id>/delete/', views.delete_for_task_table),
    path('add/', views.add),
    path('<int:rule_id>/add/', views.add_for_task_table),
    path('<int:rule_id>/back/', views.back),
    path('update/<int:rule_id>/', views.update, name='list_upd'),
    path('update/<int:rule_id>/back/', views.back),
    path('update/<int:rule_id>/save/', views.save_update),
    path('<int:rule_id>/update/<int:task_id>/', views.update_for_task_table, name='detail_upd'),
    path('<int:rule_id>/update/<int:task_id>/save/', views.save_update_for_task_table),
    path('<int:rule_id>/update/<int:task_id>/back/', views.back_for_task_table)
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)