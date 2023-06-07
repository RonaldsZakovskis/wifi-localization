NETWORK_INTERFACE = "wlp0s20f3"

""" Data column names """
X_COLUMN = "x"
Y_COLUMN = "y"
Z_COLUMN = "z"
ROOM_INDEX_COLUMN = "room_index"
MEASUREMENT_INDEX_COLUMN = "measurement_index"
BATCH_INDEX_COLUMN = "batch_index"
UNNAMED_COLUMN = "Unnamed"

""" Access point MAC and SSID combinations """
# Important! When there are many MAC and SSID combinations originating from the
#   same router, they are combined in a list, to have more data about the
#   specific AP
# Mixed
XIAOMI = "9A:62:AB:67:28:4B (PhPhPhone)"
ATOM = "94:B9:7E:A9:10:15 (M5Atom)"
STICK = "4C:75:25:CD:DD:E9 (M5Stick)"
# iPhone actually has a dynamical MAC address, but we change it, so it is
#   always the same
IPHONE = "6A:51:48:7C:54:95 (RosaMaria \\xF0\\x9F\\x92\\x95)"
# University
# TODO: These could be objects with coordinates as well
# Note: Most of these routers (except 301 and 303), follow the same pattern,
#   we could create a code for generating these names and then it would be
#   approximately 8 times smaller, but I like being able to read them
ROUTER_UNIVERSITY_3 = [
    "18:8B:9D:13:85:D0 (eduroam)",
    "18:8B:9D:13:85:D1 (LU-WIFI)",
    "18:8B:9D:13:85:D2 (LU)",
    "18:8B:9D:13:85:D3 (\\x00)",
    "18:8B:9D:13:85:DC (\\x00)",
    "18:8B:9D:13:85:DD (LU)",
    "18:8B:9D:13:85:DE (LU-WIFI)",
    "18:8B:9D:13:85:DF (eduroam)"
]
ROUTER_UNIVERSITY_14_3 = [
    "18:8B:9D:13:AB:B0 (eduroam)",
    "18:8B:9D:13:AB:B1 (LU-WIFI)",
    "18:8B:9D:13:AB:B2 (LU)",
    "18:8B:9D:13:AB:B3 (\\x00)",
    "18:8B:9D:13:AB:BC (\\x00)",
    "18:8B:9D:13:AB:BD (LU)",
    "18:8B:9D:13:AB:BE (LU-WIFI)",
    "18:8B:9D:13:AB:BF (eduroam)"
]
ROUTER_UNIVERSITY_14_21 = [
    "18:8B:9D:13:B6:D0 (eduroam)",
    "18:8B:9D:13:B6:D1 (LU-WIFI)",
    "18:8B:9D:13:B6:D2 (LU)",
    "18:8B:9D:13:B6:D3 (\\x00)",
    "18:8B:9D:13:B6:DC (\\x00)",
    "18:8B:9D:13:B6:DE (LU-WIFI)",
    "18:8B:9D:13:B6:DF (eduroam)",
    "18:8B:9D:13:B6:DD (LU)"
]
ROUTER_UNIVERSITY_16_7 = [
    "18:8B:9D:35:85:20 (eduroam)",
    "18:8B:9D:35:85:21 (LU-WIFI)",
    "18:8B:9D:35:85:22 (LU)",
    "18:8B:9D:35:85:23 (\\x00)",
    "18:8B:9D:35:85:2C (\\x00)",
    "18:8B:9D:35:85:2D (LU)",
    "18:8B:9D:35:85:2E (LU-WIFI)",
    "18:8B:9D:35:85:2F (eduroam)"
]
ROUTER_UNIVERSITY_16_15 = [
    "80:E0:1D:F9:29:40 (eduroam)",
    "80:E0:1D:F9:29:41 (LU-WIFI)",
    "80:E0:1D:F9:29:42 (LU)",
    "80:E0:1D:F9:29:43 (\\x00)",
    "80:E0:1D:F9:29:4C (\\x00)",
    "80:E0:1D:F9:29:4D (LU)",
    "80:E0:1D:F9:29:4E (LU-WIFI)",
    "80:E0:1D:F9:29:4F (eduroam)"
]
ROUTER_UNIVERSITY_18_1 = [
    "18:8B:9D:03:94:10 (eduroam)",
    "18:8B:9D:03:94:11 (LU-WIFI)",
    "18:8B:9D:03:94:12 (LU)",
    "18:8B:9D:03:94:13 (\\x00)",
    "18:8B:9D:03:94:1C (\\x00)",
    "18:8B:9D:03:94:1D (LU)",
    "18:8B:9D:03:94:1E (LU-WIFI)",
    "18:8B:9D:03:94:1F (eduroam)"
]
ROUTER_UNIVERSITY_18_15 = [
    "18:8B:9D:35:7D:F0 (eduroam)",
    "18:8B:9D:35:7D:F1 (LU-WIFI)",
    "18:8B:9D:35:7D:F2 (LU)",
    "18:8B:9D:35:7D:F3 (\\x00)",
    "18:8B:9D:35:7D:FC (\\x00)",
    "18:8B:9D:35:7D:FD (LU)",
    "18:8B:9D:35:7D:FE (LU-WIFI)",
    "18:8B:9D:35:7D:FF (eduroam)"
]
ROUTER_UNIVERSITY_301 = [
    "B4:FB:E4:0B:07:75 (DF SP)",
    "B4:FB:E4:0B:07:76 (DF SP)",
    "B4:FB:E4:0B:07:77 (DF SP)",
    "BE:FB:E4:0B:07:76 ()",
    "C2:FB:E4:0B:07:76 ()"
]
ROUTER_UNIVERSITY_303 = "00:25:9C:92:47:95 (DFLAB_GUEST)"
ROUTER_UNIVERSITY_304 = [
    "18:8B:9D:13:84:D0 (eduroam)",
    "18:8B:9D:13:84:D1 (LU-WIFI)",
    "18:8B:9D:13:84:D2 (LU)",
    "18:8B:9D:13:84:D3 (\\x00)",
    "18:8B:9D:13:84:DC (\\x00)",
    "18:8B:9D:13:84:DD (LU)",
    "18:8B:9D:13:84:DE (LU-WIFI)",
    "18:8B:9D:13:84:DF (eduroam)"
]
ROUTER_UNIVERSITY_305 = [
    "18:8B:9D:2C:63:F0 (eduroam)",
    "18:8B:9D:2C:63:F1 (LU-WIFI)",
    "18:8B:9D:2C:63:F2 (LU)",
    "18:8B:9D:2C:63:F3 (\\x00)",
    "18:8B:9D:2C:63:FC (\\x00)",
    "18:8B:9D:2C:63:FD (LU)",
    "18:8B:9D:2C:63:FE (LU-WIFI)",
    "18:8B:9D:2C:63:FF (eduroam)"
]
ROUTER_UNIVERSITY_345_18 = [
    "18:8B:9D:03:6F:20 (eduroam)",
    "18:8B:9D:03:6F:21 (LU-WIFI)",
    "18:8B:9D:03:6F:22 (LU)",
    "18:8B:9D:03:6F:23 (\\x00)",
    "18:8B:9D:03:6F:2C (\\x00)",
    "18:8B:9D:03:6F:2D (LU)",
    "18:8B:9D:03:6F:2E (LU-WIFI)",
    "18:8B:9D:03:6F:2F (eduroam)"
]
ROUTER_UNIVERSITY_345_24 = [
    "18:8B:9D:03:65:A0 (eduroam)",
    "18:8B:9D:03:65:A2 (LU)",
    "18:8B:9D:03:65:A1 (LU-WIFI)",
    "18:8B:9D:03:65:A3 (\\x00)",
    "18:8B:9D:03:65:AC (\\x00)",
    "18:8B:9D:03:65:AD (LU)",
    "18:8B:9D:03:65:AE (LU-WIFI)",
    "18:8B:9D:03:65:AF (eduroam)"
]
ROUTERS_UNIVERSITY = [
    ROUTER_UNIVERSITY_3,
    ROUTER_UNIVERSITY_14_3,
    ROUTER_UNIVERSITY_14_21,
    ROUTER_UNIVERSITY_16_7,
    ROUTER_UNIVERSITY_16_15,
    ROUTER_UNIVERSITY_18_1,
    ROUTER_UNIVERSITY_18_15,
    ROUTER_UNIVERSITY_301,
    ROUTER_UNIVERSITY_303,
    ROUTER_UNIVERSITY_304,
    ROUTER_UNIVERSITY_305,
    ROUTER_UNIVERSITY_345_18,
    ROUTER_UNIVERSITY_345_24
]
# House
ROUTER_HOUSE = "C4:EA:1D:B9:49:5F (TNCAPB9495F)"
# Apartment
ROUTER_APARTMENT = ["A4:BD:C4:2E:D7:70 (Dignajas Rozes)", "A4:BD:C4:2E:D7:74 (Dignajas Rozes 5G)"]

""" Room index actual names for each of the locations """
ROOM_ID_TO_NAME_UNIVERSITY = {
    1: "Hallway 1",
    2: "Hallway 2",
    3: "Hallway 3",
    4: "Hallway 4",
    5: "Hallway 5",
    6: "Hallway 6",
    14: "Auditorium 14",
    16: "Auditorium 16",
    18: "Auditorium 17",
    301: "Students' Council",
    302: "DF LAB II",
    303: "DF LAB I",
    304: "Study Room",
    305: "Ping Pong",
    345: "Computer class 345",
    347: "Stairway 347",
}

ROOM_ID_TO_NAME_HOUSE = {
    0: "Outside, 1st floor",
    1: "Terrace, 1st floor",
    2: "Boiler room, 1st floor",
    3: "Living room, 1st floor",
    4: "Garage, 1st floor",
    5: "Toilet, 1st floor",
    6: "Wardrobe, 1st floor",
    7: "Kitchen, 1st floor",
    8: "Lower stairs, 1st floor",
    9: "Toilet, 2nd floor",
    10: "First bedroom, 2nd floor",
    11: "Office, 2nd floor",
    12: "Second bedroom, 2nd floor",
    13: "Hallway, 2nd floor",
    14: "Third bedroom, 2nd floor",
    15: "Upper stairs, 2nd floor",
    16: "Storage room, 2nd floor",
}

ROOM_ID_TO_NAME_APARTMENT = {
    0: "Bedroom",
    1: "Bathroom",
    2: "Living room",
    3: "Hallway"
}
