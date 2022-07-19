from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index'),
    path('back/', views.index, name='index'),
    path('<int:rule_id>/', views.detail, name='detail'),
    # path('sort/<slug:sort_type>/', views.search, name='search'),
    path('delete/', views.delete),
    path('<int:rule_id>/delete/', views.delete2),
    path('add/', views.add),
    path('<int:rule_id>/add/', views.add2),
    path('<int:rule_id>/back/', views.back),
    path('update/<int:rule_id>/', views.update, name='list_upd'),
    path('update/<int:rule_id>/back/', views.back),
    path('update/<int:rule_id>/save/', views.save_update),
    path('<int:rule_id>/update/<int:task_id>/', views.update2, name='detail_upd'),
    path('<int:rule_id>/update/<int:task_id>/save/', views.save_update2),
    path('<int:rule_id>/update/<int:task_id>/back/', views.back2)
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)