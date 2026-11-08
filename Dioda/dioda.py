from gpiozero import PWMLED

# Wskazujemy GPIO23, co odpowiada fizycznemu pinowi 16 na złączu Raspberry Pi
dioda = PWMLED(23)
dioda.pulse(fade_in_time=1, fade_out_time=1)
