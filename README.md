# Network Scanner Guide

### This script allows you to capture the IP and MAC addresses of devices currently connected to your Wi-Fi network.

## To install

1. You should have Python installed on your machine

2. Run these commends to install tools required

```bash
brew install arp-scan
```

```bash
brew install lsof
```

3. Use this commend to run the script

```bash
sudo python3 network_scanner.py
```

## Expected Output

When the script runs, you should see output similar to this:

Real-Time Network Scanner Started
Time: 2024-11-08 14:55:36.123456

---

Using Wi-Fi Interface: en0
Your IP address: 192.168.1.10

## Currently Connected Devices: 3

IP Address: 192.168.1.5
MAC Address: aa:bb:cc:dd:ee:ff

---

IP Address: 192.168.1.6
MAC Address: bb:cc:dd:ee:ff:gg

---

...
