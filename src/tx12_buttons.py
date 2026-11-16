import hid
import time

VID = 0x1209
PID = 0x4F54

devices = hid.enumerate(VID, PID)
paths = list({d["path"] for d in devices})

if not paths:
    print("TX12 not found")
    raise SystemExit

dev = hid.device()
dev.open_path(paths[0])
dev.set_nonblocking(True)

print("TX12 connected")
print("Press A, release it, then press D.")
print("Watching button bytes...\n")

previous = None

try:
    while True:
        data = dev.read(64)

        if data:
            buttons = tuple(data[:3])

            if buttons != previous:
                print("BUTTON BYTES:", " ".join(f"{b:02X}" for b in buttons))
                previous = buttons

        time.sleep(0.005)

except KeyboardInterrupt:
    print("\nStopped")
finally:
    dev.close()
