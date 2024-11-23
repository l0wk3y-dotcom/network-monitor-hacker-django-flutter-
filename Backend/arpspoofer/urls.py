from django.urls import path
from . import views

urlpatterns = [
    path("start/",views.StartSpoofer.as_view(), name = "start-spoofer"),
    path("stop/<int:pk>",views.stop_spoofing, name = "stop-spoofer")
]