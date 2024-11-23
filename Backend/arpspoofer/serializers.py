from rest_framework import serializers
from .models import Spoofer

class SpooferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spoofer
        exclude = ["is_running", "spoofer_id","target_mac","gateway_mac","total_count","time_ran",]