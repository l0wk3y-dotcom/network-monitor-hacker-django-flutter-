from celery import shared_task
from scapy.all import sniff, Packet
from django.core.cache import cache
from .models import Session
import threading
@shared_task(bind=True)
def start_sniffing(self, session_id, packets_count = None):
    packets = []
    session = Session.objects.get(session_id = session_id)
    num = 0
    print(cache.get(f"stop_{session_id}"))
    def process_packets(packet):
        nonlocal num
        print(f"{num}")
        packet_detail = packet_to_dict(packet=packet)
        packets.append(packet_detail)
        session.packets = packets
        session.save(update_fields=["packets"])
        num+=1

    def packet_to_dict(packet: Packet) -> dict:
        # Use Scapy's built-in 'show' method with 'dump=True' to get a dictionary representation
        packet_dict = packet.show(dump=True)
        return packet_dict

    sniff(prn=process_packets, stop_filter=lambda _:cache.get(f"stop_{session_id}"), count=packets_count or 0)
    print("sniffing has been stopped")

    session.packets = packets
    session.save(update_fields=["packets"])

    return packets

def start_sniffing_in_background(session_id, packets_count=None):
    thread = threading.Thread(target=start_sniffing, args=(session_id,packets_count,))
    thread.daemon = True  # Thread will exit when main program exits
    thread.start()