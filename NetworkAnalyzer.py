import pyshark

capture = pyshark.LiveCapture(interface='vEthernet (nat)')

for packet in capture.sniff_continuously(packet_count=None):

    try:
        print(packet['ip'].dst)
        print(packet['ip'].src)
        print(packet['ip'].len)
        print(packet['ip'])


    except (RuntimeError, TypeError, NameError, Exception):
        pass