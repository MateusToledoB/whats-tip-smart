from django.contrib import admin
from django.urls import path, include
from pages.views import login_view, index_view, historico_view, logout_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('index/', index_view, name='index'),
    path('historico/', historico_view, name='historico'),
    path('login/', include('users.urls')),
    path('instancias/', include('instancias.urls')),
    path('instancias_utils/', include('instancias_utils.urls')),
]
