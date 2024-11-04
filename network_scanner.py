import subprocess
import re
import datetime
import json

def get_active_wifi_interface():
    """Get the active WiFi interface name"""
    try:
        output = subprocess.check_output(['networksetup', '-listallhardwareports']).decode()
        wifi_info = re.findall(r'Hardware Port: Wi-Fi\nDevice: (.*?)\n', output)
        return wifi_info[0] if wifi_info else 'en0'
    except:
        return 'en0'  # Default to en0 if we can't find it

def get_network_info():
    """Get current network information"""
    try:
        interface = get_active_wifi_interface()
        output = subprocess.check_output(['ipconfig', 'getifaddr', interface]).decode().strip()
        return output
    except:
        return None

def scan_network():
    """
    Enhanced network scanner for MacOS
    """
    print("Starting enhanced network scan...")
    devices = []
    
    # Method 1: Use arp-scan (more thorough than regular arp)
    try:
        print("\nScanning using arp-scan...")
        arp_output = subprocess.check_output(['sudo', 'arp', '-a']).decode()
        devices_arp = re.findall(r'\((\d+\.\d+\.\d+\.\d+)\) at ([0-9a-fA-F:]+)', arp_output)
        
        for ip, mac in devices_arp:
            try:
                # Try to get hostname
                hostname_output = subprocess.check_output(['host', ip]).decode()
                hostname = re.search(r'domain name pointer (.+?)\.', hostname_output)
                hostname = hostname.group(1) if hostname else "Unknown"
            except:
                hostname = "Unknown"
            
            devices.append({
                'ip': ip,
                'mac': mac,
                'hostname': hostname,
                'source': 'arp'
            })
    except Exception as e:
        print(f"Error with arp scan: {e}")

    # Method 2: Use networksetup to get additional information
    try:
        print("\nGetting additional network information...")
        network_output = subprocess.check_output(['networksetup', '-listallhardwareports']).decode()
        # Process and add any additional devices found
    except Exception as e:
        print(f"Error getting network info: {e}")

    # Method 3: Use lsof to find active network connections
    try:
        print("\nChecking active network connections...")
        lsof_output = subprocess.check_output(['sudo', 'lsof', '-i']).decode()
        connections = re.findall(r'(\d+\.\d+\.\d+\.\d+)', lsof_output)
        
        for ip in connections:
            if ip not in [d['ip'] for d in devices]:
                try:
                    hostname_output = subprocess.check_output(['host', ip]).decode()
                    hostname = re.search(r'domain name pointer (.+?)\.', hostname_output)
                    hostname = hostname.group(1) if hostname else "Unknown"
                except:
                    hostname = "Unknown"
                
                devices.append({
                    'ip': ip,
                    'mac': "Unknown",
                    'hostname': hostname,
                    'source': 'lsof'
                })
    except Exception as e:
        print(f"Error checking connections: {e}")

    return devices

if __name__ == "__main__":
    print("Enhanced Network Scanner Started")
    print(f"Time: {datetime.datetime.now()}")
    print("-" * 50)
    
    # Get current network info
    my_ip = get_network_info()
    if my_ip:
        print(f"Your IP address: {my_ip}")
    
    devices = scan_network()
    
    print("\nScan Complete")
    print(f"Found {len(devices)} devices")
    print("-" * 50)
    
    # Print results in a more readable format
    for device in devices:
        print(f"\nDevice Details:")
        print(f"IP Address: {device['ip']}")
        print(f"MAC Address: {device['mac']}")
        print(f"Hostname: {device['hostname']}")
        print(f"Detection Method: {device['source']}")
        print("-" * 30)
    
    # Save results to a file
    with open('network_scan_results.txt', 'w') as f:
        json.dump(devices, f, indent=2)
    print("\nResults have been saved to 'network_scan_results.txt'")