from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:rule_id>/', views.detail, name='detail'),
    path('delete/', views.delete)
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)