from django.shortcuts import render , get_object_or_404
from django.http import response
from .models import Session
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .helpers import start_sniffing_in_background
from django.core.cache import cache
from .serializers import SessionSerializer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import generics

class ViewAllSessions(generics.ListAPIView):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    
class StartSessionView(generics.CreateAPIView):
    serializer_class = SessionSerializer
    queryset = Session.objects.all()
    def post(self, request):  # sourcery skip: extract-method
        serializer = SessionSerializer(data=request.data)
        if serializer.is_valid():
            # Save the session
            session = serializer.save()
            session.running = True
            session.save(update_fields = ["running"])            
            # Cache data related to the session
            cache.set(f"stop_{session.session_id}", False, timeout=None)
            print(cache.get(f"stop_{session.session_id}"))
            start_sniffing_in_background(session_id=session.session_id)
            cache.set(f"task_{session.session_id}", session.session_id, timeout=None)

            # Return a success response
            return Response({
                "status": 200,
                "message": "Sniffing has been started",
                "session_id": session.session_id,
                "session": serializer.data
            }, status=status.HTTP_201_CREATED)

        # Return error response if serializer is not valid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def stop_session(request, session_id):
    session = Session.objects.filter(session_id=session_id).first()
    if not session:
        return Response({"status" : 404, "message" : f"{session_id} does not exist"})
    cache.set(f"stop_{session_id}", True , timeout=None)
    print(cache.get(f"stop_{session_id}"))
    session.running = False
    session.save(update_fields = ["running"])
    return Response({"status" : 200, "message" : f"{session_id} was stopped succesfully"})


@api_view(["GET"])
def view_session(request, session_id):
    try:
        session = Session.objects.get(session_id = session_id)
        if packets := session.packets:
            return Response({"session_id": session_id, "packets": packets})
        else:
            return Response({"error": "Session not found or has no data"}, status=404)
    except:
        return Response({"error": "Session not found or has no data"}, status=404)
    
class delete_session(generics.DestroyAPIView):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    lookup_field = "session_id"

    def delete(self, *args, **kwargs):
        session_id = kwargs.get("session_id")
        try:
            session = self.get_object()  # Fetch the object to be deleted
            session_name = session.name
            session.delete()  # Delete the session
            return Response({"status": 200, "message": f"Session | {session_name}-{session_id} | deleted successfully."}, status=status.HTTP_200_OK)
        except Session.DoesNotExist:
            return Response({"status": 404, "message": "Session not found."}, status=status.HTTP_404_NOT_FOUND)
        

def homepage(request):
    return response(request, "This is my homepage")
