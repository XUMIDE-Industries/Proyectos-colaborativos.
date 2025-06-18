from machine import Pin
import sys

# Diccionario de LEDs por caja
leds = {
    "C1": {"verde": Pin(15, Pin.OUT), "rojo": Pin(2, Pin.OUT)},
    "C2": {"verde": Pin(18, Pin.OUT), "rojo": Pin(19, Pin.OUT)},
    "C3": {"verde": Pin(22, Pin.OUT), "rojo": Pin(23, Pin.OUT)},
    "C4": {"verde": Pin(32, Pin.OUT), "rojo": Pin(33, Pin.OUT)},
    "C5": {"verde": Pin(14, Pin.OUT), "rojo": Pin(12, Pin.OUT)},
}

for caja in leds.values():
    caja["verde"].value(1)
    caja["rojo"].value(0)

print("ESP32 listo. Esperando comandos C1R/C1V...")

while True:
    try:
        linea = sys.stdin.readline().strip()
        if len(linea) == 3 and linea[:2] in leds and linea[2] in ("R", "V"):
            caja_id = linea[:2]
            ocupado = (linea[2] == "R")
            leds[caja_id]["verde"].value(0 if ocupado else 1)
            leds[caja_id]["rojo"].value(1 if ocupado else 0)
            print(f"{caja_id} {'ocupada' if ocupado else 'libre'}")
        else:
            print("Comando desconocido:", linea)
    except Exception as e:
        print("Error:", e)