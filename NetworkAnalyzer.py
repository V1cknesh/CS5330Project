import pyshark

capture = pyshark.LiveCapture(interface='Wi-Fi')

for packet in capture.sniff_continuously(packet_count=None):

    try:
        print(packet['ip'].dst)
        print(packet['ip'].src)

    except (RuntimeError, TypeError, NameError, Exception):
        pass