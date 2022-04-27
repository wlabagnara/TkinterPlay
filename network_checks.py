"""
    Network interface checks and operations

    - using DOCTEST for unit testing
"""

""" Check if valid ipv4 address """

def is_valid_IP_addr(sample_str):
    """ TEST CASES - valid ip address return True
    >>> is_valid_IP_addr("1000.10.10.1")
    False
    >>> is_valid_IP_addr("10.10.10.1")
    True
    >>> is_valid_IP_addr("192.168.1.1")
    True
    >>> is_valid_IP_addr("a.1.1.1")
    False
    """            
    import re
    result = True
    match_obj = re.search( r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$", sample_str)
    if  match_obj is None:
        result = False
    else:
        for value in match_obj.groups():
            if int(value) > 255:
                result = False
                break
    return result
    
def get_ip_address(ifname):
    """ TEST CASES - valid ip address return True
    >>> get_ip_address("Wireless LAN adapter Wi-Fi")
    "192.168.0.193"
    """            
    import socket
    import fcntl
    import struct

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])


import doctest # enable doctest
doctest.testmod()
    