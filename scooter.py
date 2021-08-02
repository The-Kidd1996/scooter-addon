import uasyncio
import ubluetooth
import scooterble

ble = ubluetooth.BLE()

async def initialize():
    print("[Scooter]: Init")

    ble.active(True)

    while ble.active() == False:
      pass

    print("[Scooter]: Init Bluetooth done")

async def task():
    print("[Scooter]: Scooter task start")
    central = scooterble.BLESimpleCentral(ble)
    not_found = True

    def on_scan(addr_type, addr, name):
        if addr_type is not None:
            print("[Scooter](on_scan): Found peripheral:", addr_type, addr, name)
            central.connect()
            print("[Scooter](on_scan): Connected")
            nonlocal not_found
            not_found = False
        else:
            print("[Scooter](on_scan): No peripheral found.")

    central.scan(callback=on_scan)

    while not central.is_connected():
        await uasyncio.sleep_ms(5000)
        if not_found:
            central.scan(callback=on_scan)

    print("Connected")

    def on_rx(v):
        print("RX", v)

    central.on_notify(on_rx)

    connect_init_done = False

    while central.is_connected():
        if not connect_init_done:
            print("[Scooter]: Connected")
            connect_init_done = True
    
    print("Disconnected")