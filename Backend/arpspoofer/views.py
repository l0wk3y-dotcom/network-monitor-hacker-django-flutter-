from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import SpooferSerializer
from .spoofer import ARPSpoofer
from .models import Spoofer
from rest_framework import generics
active_spoofer = {}

class StartSpoofer(generics.CreateAPIView):
    serializer_class = SpooferSerializer
    queryset = Spoofer.objects.all()

    def post(self, request):
        data = request.data
        serializer = SpooferSerializer(data=data)
        
        # Check if data is valid
        if not serializer.is_valid():
            return Response({"message": "Data is not valid"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Save the Spoofer request data
        spoofrequest = serializer.save(is_running = True)
        arpspoofer = ARPSpoofer(target_ip=spoofrequest.target_ip, gateway_ip=spoofrequest.gateway_ip)
        
        # Retrieve MAC addresses and handle errors if they occur
        try:
            target_mac = arpspoofer.get_mac(spoofrequest.target_ip)
            gateway_mac = arpspoofer.get_mac(spoofrequest.gateway_ip)
        except Exception as e:
            return Response({"message": f"Error retrieving MAC addresses: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Save the MAC addresses to spoofrequest
        spoofrequest.target_mac = target_mac
        spoofrequest.gateway_mac = gateway_mac
        spoofrequest.save(update_fields=["target_mac", "gateway_mac"])
        
        # Start spoofing and check if it started successfully
        arpspoofer.start_spoofing()
        
        if arpspoofer.is_running():
            active_spoofer[spoofrequest.id] = arpspoofer
            return Response(
                {
                    "message": "Spoofing started successfully",
                    "payload": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {
                    "message": "Spoofing could not be started",
                    "payload": None,
                },
                status=status.HTTP_304_NOT_MODIFIED,
            )
@api_view(["GET"])
def stop_spoofing(request, pk):
    running_spoofer = get_object_or_404(Spoofer, id = pk)
    if running_spoofer.is_running == False:
        return Response({"message" : "Spoofer is not active"})
    
    try:
        spoofer_obj = active_spoofer[running_spoofer.id]
        if not spoofer_obj:
            return Response({"message" : "couldn't stop the spoofing"})
        if not spoofer_obj.is_running():
            return Response({"message" : "Spoofer is not active"})
        spoofer_obj.stop_spoofing()
        if not spoofer_obj.is_running():
            running_spoofer.is_running = False
            running_spoofer.save(update_fields = ["is_running"])
            return Response({"message" : "spoofing has been stopped"})
    except Exception as e:
        return Response({"message" : "Spoofer is not active", "error" : str(e)})