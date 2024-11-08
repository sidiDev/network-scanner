import subprocess
import re
import datetime
import platform

def get_active_wifi_interface():
    """Get the active WiFi interface name based on OS type."""
    try:
        if platform.system() == "Darwin":  # macOS
            output = subprocess.check_output(['networksetup', '-listallhardwareports']).decode()
            wifi_info = re.findall(r'Hardware Port: Wi-Fi\nDevice: (.*?)\n', output)
            return wifi_info[0] if wifi_info else 'en0'
        elif platform.system() == "Linux":
            output = subprocess.check_output(['nmcli', '-t', '-f', 'DEVICE,TYPE', 'device', 'status']).decode()
            wifi_info = [line.split(":")[0] for line in output.splitlines() if "wifi" in line]
            return wifi_info[0] if wifi_info else 'wlan0'
    except Exception as e:
        print(f"Error finding Wi-Fi interface: {e}")
        return 'en0'  # Default if not found

def get_connected_devices(interface):
    """Get a list of currently connected devices using arp-scan if available."""
    try:
        # Prefer using arp-scan for live results if installed
        try:
            scan_output = subprocess.check_output(['sudo', 'arp-scan', '-l', '-I', interface]).decode()
            devices = re.findall(r'(\d+\.\d+\.\d+\.\d+)\s+([0-9a-fA-F:]{17})', scan_output)
            return devices
        except FileNotFoundError:
            print("arp-scan not found, falling back to arp command.")
        
        # Fall back to arp if arp-scan isn't installed
        arp_output = subprocess.check_output(['arp', '-a', '-i', interface]).decode()
        devices = re.findall(r'\((\d+\.\d+\.\d+\.\d+)\) at ([0-9a-fA-F:]+)', arp_output)
        return devices
    except Exception as e:
        print(f"Error scanning network: {e}")
        return []

if __name__ == "__main__":
    print("Real-Time Network Scanner Started")
    print(f"Time: {datetime.datetime.now()}")
    print("-" * 50)

    # Detect active network interface
    interface = get_active_wifi_interface()
    print(f"Using Wi-Fi Interface: {interface}")

    # Get current IP address
    try:
        if platform.system() == "Darwin":
            my_ip = subprocess.check_output(['ipconfig', 'getifaddr', interface]).decode().strip()
        elif platform.system() == "Linux":
            my_ip = subprocess.check_output(['hostname', '-I']).decode().split()[0]
        print(f"Your IP address: {my_ip}")
    except Exception as e:
        print(f"Error fetching IP address: {e}")
        my_ip = "Unknown"

    # Scan network for connected devices
    connected_devices = get_connected_devices(interface)
    print(f"\nCurrently Connected Devices: {len(connected_devices)}")
    print("-" * 50)

    for ip, mac in connected_devices:
        print(f"IP Address: {ip}")
        print(f"MAC Address: {mac}")
        print("-" * 30)
