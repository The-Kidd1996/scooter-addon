print("Booting...")
import webrepl
import machine
import network
import uasyncio
import pins 
import scooter

print("[Boot]: Starting AP")

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid="ScooterAddon", password="password")

print("[Boot]: Waiting for AP")
while ap.active() == False:
  pass

print("[Boot]: AP started")

webrepl.start()
print("[Boot]: webrepl started")

LED = machine.Pin(pins.LED_PIN, machine.Pin.OUT)
LED.value(1)

async def main():
    print("[Main]: Starting scooter task")
    await scooter.initialize()
    LED.value(0)
    await uasyncio.create_task(scooter.task())
    LED.value(1)

print("[Boot]: Running main()")
loop = uasyncio.get_event_loop()
loop.run_forever()
uasyncio.run(main())
