from typing import Dict, List
from pprint import pprint

import wifi


def scan_access_points(interface: str) -> List[Dict]:
    """ Scans nearby access points from the given interface and returns
        information about each of the access points detected.

    Args:
        interface: Name of the network interface, for example, "wlan0". If you
            are not sure about your necessary network interface name, enter the
            "iwconfig" in the terminal.

    Returns:
        parsed_access_points: Access points which the "wifi" package detected
            parsed into a more useful format.
    """
    # Scanning for access points and transforming the returned map object to
    #   list
    access_points = None
    while access_points is None:
        try:
            access_points = list(wifi.Cell.all(interface))
        except Exception as e:
            print(e)
            print("An error occured!")

    parsed_access_points = []

    for i in access_points:
        # Note: Cell type has an attribute "encryption_type", which is None if
        #   encrypted is False, or one of "wep", "wpa" or "wpa2" if encrypted
        #   is True, but the problem is that an access point can support both
        #   WPA and WPA2, but this library will only show one of them, and you
        #   don't know which one it will show..., so probably this value
        #   shouldn't be used, but if needed, I can just quickly write code
        #   that eliminates the need for the wifi package.
        parsed_access_points.append({
            "ssid": i.ssid,
            "signal": i.signal,
            "quality": i.quality,
            "frequency": i.frequency,
            "bitrates": i.bitrates,
            "encrypted": i.encrypted,
            "channel": i.channel,
            "address": i.address,
            "mode": i.mode,
            "encryption_type": i.encryption_type
        })
    return parsed_access_points


if __name__ == "__main__":  # If file is run directly
    my_access_points = scan_access_points(interface="wlp0s20f3")
    pprint(my_access_points)
    print(len(my_access_points))
