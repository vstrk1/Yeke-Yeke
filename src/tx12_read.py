import hid
import time

VID = 0x1209
PID = 0x4F54

devices = hid.enumerate(VID, PID)

# Унікальні HID-шляхи
paths = list({d["path"] for d in devices})

print("Unique HID interfaces:", len(paths))

for index, path in enumerate(paths):
    print(f"\nOpening interface {index}...")

    dev = hid.device()

    try:
        dev.open_path(path)
        dev.set_nonblocking(1)

        print("Connected:", dev.get_product_string())
        print("Move sticks and press A / D.")
        print("Reading for 20 seconds...")

        start = time.time()
        last_data = None

        while time.time() - start < 20:
            data = dev.read(64)

            if data:
                current = bytes(data)

                if current != last_data:
                    print("HID DATA:", current.hex(" "))
                    last_data = current

            time.sleep(0.01)

        dev.close()

    except Exception as e:
        print("ERROR:", repr(e))
