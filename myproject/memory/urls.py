from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.memory_list, name='memory_list'),  # メインページのURL
    path('add/', views.memory_add, name='memory_add'),  # 追加ページ
    path('memory/<int:year>/<int:month>/<int:day>/', views.memory_check, name='memory_check'),
]

if settings.DEBUG:  # 開発時のみ有効
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)