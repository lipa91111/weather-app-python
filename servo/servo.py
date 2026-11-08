from gpiozero import AngularServo
from time import sleep


servo = AngularServo(24, min_angle=-90, max_angle=90)
servo.angle = None

print("Sterowanie serwem na GPIO24")
print("Podaj kąt od -90 do 90 stopni; Enter kończy program.")

try:
    while True:
        angle_input = input("Kąt (-90–90°): ")
        if not angle_input:
            break

        try:
            angle = float(angle_input)
        except ValueError:
            print("Wpisz kąt w stopniach od -90 do 90.")
            continue

        if not -90 <= angle <= 90:
            print("Kąt musi być w zakresie od -90 do 90 stopni.")
            continue

        servo.angle = angle
        sleep(0.1)
        servo.angle = None
finally:
    servo.close()
