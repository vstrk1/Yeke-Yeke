import pygame

pygame.init()
pygame.joystick.init()

count = pygame.joystick.get_count()
print("Joysticks found:", count)

if count == 0:
    print("TX12 not detected by pygame")
    raise SystemExit

joy = pygame.joystick.Joystick(0)
joy.init()

print("Device:", joy.get_name())
print("Axes:", joy.get_numaxes())
print("Buttons:", joy.get_numbuttons())
print("Hats:", joy.get_numhats())
print("\nMove controls and press A / D. CTRL+C to exit.")

try:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN:
                print("BUTTON PRESSED:", event.button)

            elif event.type == pygame.JOYBUTTONUP:
                print("BUTTON RELEASED:", event.button)

            elif event.type == pygame.JOYAXISMOTION:
                print("AXIS:", event.axis, "VALUE:", round(event.value, 3))

            elif event.type == pygame.JOYHATMOTION:
                print("HAT:", event.value)

        pygame.time.wait(10)

except KeyboardInterrupt:
    print("\nTest stopped.")

pygame.quit()
