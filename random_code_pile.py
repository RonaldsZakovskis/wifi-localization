# a = pd.read_csv("/home/ronaldsz/Repositories/wifi-localization/data/university_training.csv")  # All good
# a = pd.read_csv("/home/ronaldsz/Repositories/wifi-localization/data/university_testing.csv")  # All good
# a = pd.read_csv("/home/ronaldsz/Repositories/wifi-localization/data/house_training.csv")  # All good
# a = pd.read_csv("/home/ronaldsz/Repositories/wifi-localization/data/house_testing.csv")
from visualize import count_non_nans
# print(count_non_nans(list(a[c.STICK])))
# print(count_non_nans(list(a[c.IPHONE])))
# print(count_non_nans(list(a["72:CD:48:8B:11:82 (RosaMaria \\xF0\\x9F\\x92\\x95)"])))
# print(count_non_nans(list(a[c.ROUTER_HOUSE])))
# print(count_non_nans(list(a[c.ATOM])))
# a = pd.read_csv("/home/ronaldsz/Repositories/wifi-localization/data/apartment_training.csv")  # All good
# a = pd.read_csv("/home/ronaldsz/Repositories/wifi-localization/data/apartment_testing_1h.csv")  # All good
# a = pd.read_csv("/home/ronaldsz/Repositories/wifi-localization/data/apartment_testing_1d.csv")  # All good
# a = pd.read_csv("/home/ronaldsz/Repositories/wifi-localization/data/apartment_testing_1w.csv")  # All good
# print(count_non_nans(list(a[c.STICK])))
# print(count_non_nans(list(a[c.IPHONE])))
# print(count_non_nans(list(a[c.ROUTER_APARTMENT[0]])))
# print(count_non_nans(list(a[c.ROUTER_APARTMENT[1]])))
# print(count_non_nans(list(a[c.XIAOMI])))
# print(count_non_nans(list(a[c.ATOM])))
# print(a.shape)
# a = input("Temporary pause:")

# rssi/cooridnates
""" Unused:
for _ in range(10):
    # TODO: Get all known AP RSSI levels
    rssi_values = [-66, -49, -76]
    position = rssi_localizer.getNodePosition(rssi_values)
    print(f"Position (x, y) is ({position[0][0]:.2f}, {position[1][0]:.2f})")
    time.sleep(1)
"""


