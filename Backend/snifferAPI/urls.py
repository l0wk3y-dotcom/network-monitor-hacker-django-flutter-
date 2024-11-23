from django.urls import path
from . import views

urlpatterns = [
    path("start",views.StartSessionView.as_view(),name="start-sniffing"),
    path("stop/<str:session_id>",views.stop_session,name="stop-sniffing"),
    path("<str:session_id>", views.view_session ,name="retrieve-sniffing"),
    path("",views.ViewAllSessions.as_view(),name="view-all-session"),
    path("delete/<str:session_id>" , views.delete_session.as_view(), name="delete-session"),
]


# http://127.0.0.1:8000/sniffer/ : List Sniffer session
# http://127.0.0.1:8000/sniffer/start Create Sniffer session
# http://127.0.0.1:8000/sniffer/stop/4d5c06a6-a2a0-4d9f-bdfa-d5994573c724 : Stop Sniffing Session
# http://127.0.0.1:8000/sniffer/94c0bdd4-4b12-454d-b6b1-a337014e49a1 : Retrieve a single session
# http://127.0.0.1:8000/sniffer/delete/94c0bdd4-4b12-454d-b6b1-a337014e49a1 : delete a single session

