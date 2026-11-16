import hid

VENDOR_ID = 0x1209
PRODUCT_ID = 0x4F54

devices = hid.enumerate(VENDOR_ID, PRODUCT_ID)

print("Matching devices:", len(devices))

for device in devices:
    print("Product:", device.get("product_string"))
    print("Manufacturer:", device.get("manufacturer_string"))
    print("Vendor ID:", hex(device["vendor_id"]))
    print("Product ID:", hex(device["product_id"]))
    print("Path:", device["path"])
    print("---")
