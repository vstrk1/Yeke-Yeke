import hid
import time
import subprocess
import sys

VID = 0x1209
PID = 0x4F54

HOLD_THRESHOLD = 0.45
SEEK_INTERVAL = 0.5
SEEK_SECONDS = 5

# AppleScript: шукаємо вкладку YouTube у Google Chrome
# та виконуємо JavaScript без перемикання на цю вкладку.
APPLESCRIPT = r'''
on run argv
    set jsCode to item 1 of argv

    tell application "Google Chrome"
        repeat with w in windows
            repeat with t in tabs of w
                if (URL of t) contains "youtube.com" then
                    return execute t javascript jsCode
                end if
            end repeat
        end repeat
    end tell

    return "YOUTUBE_TAB_NOT_FOUND"
end run
'''

def run_js(js):
    try:
        result = subprocess.run(
            ["osascript", "-e", APPLESCRIPT, js],
            capture_output=True,
            text=True,
            timeout=3
        )

        if result.returncode != 0:
            print("Chrome error:", result.stderr.strip())
            return None

        return result.stdout.strip()

    except subprocess.TimeoutExpired:
        print("Chrome command timeout")
        return None


def previous_track():
    js = """
    (() => {
        const b = document.querySelector('.ytp-prev-button');
        if (!b || b.disabled) return 'PREVIOUS_UNAVAILABLE';
        b.click();
        return 'PREVIOUS';
    })()
    """
    print("Previous:", run_js(js))


def next_track():
    js = """
    (() => {
        const b = document.querySelector('.ytp-next-button');
        if (!b || b.disabled) return 'NEXT_UNAVAILABLE';
        b.click();
        return 'NEXT';
    })()
    """
    print("Next:", run_js(js))


def seek(seconds):
    js = f"""
    (() => {{
        const v = document.querySelector('video');
        if (!v) return 'VIDEO_NOT_FOUND';

        v.currentTime = Math.max(
            0,
            Math.min(v.duration || Infinity, v.currentTime + ({seconds}))
        );

        return Math.round(v.currentTime);
    }})()
    """
    run_js(js)


def main():
    devices = hid.enumerate(VID, PID)
    paths = list({d["path"] for d in devices})

    if not paths:
        print("TX12 not found")
        sys.exit(1)

    dev = hid.device()
    dev.open_path(paths[0])
    dev.set_nonblocking(True)

    print("TX12 connected")
    print("YouTube controller started")
    print("A: previous / hold: rewind")
    print("D: next / hold: forward")
    print("Press Ctrl+C to stop\n")

    previous_mask = 0
    pressed_at = {}
    last_seek_at = {}

    try:
        while True:
            data = dev.read(64)

            if data:
                mask = data[0] & 0x03
                now = time.monotonic()

                # Одночасне натискання A + D ігноруємо.
                if mask == 3:
                    previous_mask = mask
                    pressed_at.clear()
                    last_seek_at.clear()
                    time.sleep(0.005)
                    continue

                for bit in (1, 2):
                    was_pressed = bool(previous_mask & bit)
                    is_pressed = bool(mask & bit)

                    # Натискання
                    if is_pressed and not was_pressed:
                        pressed_at[bit] = now
                        last_seek_at[bit] = now

                    # Утримання
                    if is_pressed and bit in pressed_at:
                        held = now - pressed_at[bit]

                        if held >= HOLD_THRESHOLD:
                            if now - last_seek_at[bit] >= SEEK_INTERVAL:
                                if bit == 1:
                                    seek(-SEEK_SECONDS)
                                    print("Rewind")
                                else:
                                    seek(SEEK_SECONDS)
                                    print("Forward")

                                last_seek_at[bit] = now

                    # Відпускання
                    if was_pressed and not is_pressed:
                        start = pressed_at.pop(bit, now)
                        duration = now - start

                        if duration < HOLD_THRESHOLD:
                            if bit == 1:
                                previous_track()
                            else:
                                next_track()

                        last_seek_at.pop(bit, None)

                previous_mask = mask

            time.sleep(0.005)

    except KeyboardInterrupt:
        print("\nController stopped")

    finally:
        dev.close()


if __name__ == "__main__":
    main()
