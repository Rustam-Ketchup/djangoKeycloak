from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from auth import views


router = routers.DefaultRouter()

urlpatterns = [
    # path('', include(router.urls)),
    path('index/', views.Index.as_view(), name='index'),
    path('index/redir', views.Keycloak.as_view()),
    path('admin/', admin.site.urls),
    path('api/', include('rest_framework.urls', namespace='rest_framework'))
]
