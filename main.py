import bluetooth
import time
import pyb

# Initialisation du BLE
ble = bluetooth.BLE()
ble.active(True)

# Nom du périphérique BLE
DEVICE_NAME = "Nucleo_WB55_Noe"

# UUID du service BLE
UART_SERVICE_UUID = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
TX_CHAR_UUID = bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E")  # TX (STM32 ? App)

# Création du service BLE avec NOTIFY
UART_SERVICE = (
    UART_SERVICE_UUID,
    (
        # Ajout du descripteur CCCD pour que App Inventor puisse s’abonner proprement
        (TX_CHAR_UUID, bluetooth.FLAG_READ | bluetooth.FLAG_NOTIFY),
    ),
)

# Enregistrement du service BLE
handles = ble.gatts_register_services([UART_SERVICE])
tx_handle = handles[0][0]

# Publicité BLE
ADV_DATA = (
    b"\x02\x01\x06" +
    bytearray((len(DEVICE_NAME) + 1, 0x09)) +
    DEVICE_NAME.encode()
)

ble.gap_advertise(100_000, ADV_DATA)
print(f"? BLE actif, connectez-vous à '{DEVICE_NAME}'")

# Capteur ultrason sur broche D7
SIG = pyb.Pin('D7', pyb.Pin.OUT_PP)
conn_handle = None

def get_distance():
    """Mesure la distance avec le capteur ultrason."""
    SIG.init(pyb.Pin.OUT_PP)
    SIG.low()
    time.sleep_us(2)
    SIG.high()
    time.sleep_us(10)
    SIG.low()

    SIG.init(pyb.Pin.IN)
    start = time.ticks_us()

    while SIG.value() == 0:
        start = time.ticks_us()

    while SIG.value() == 1:
        end = time.ticks_us()

    duration = end - start
    return (duration * 0.0343) / 2  # Distance en cm

def bt_callback(event, data):
    global conn_handle
    if event == 1:
        conn_handle = data[0]
        print("?? Appareil connecté")
    elif event == 2:
        conn_handle = None
        print("? Appareil déconnecté")

ble.irq(bt_callback)

# Boucle principale
try:
    while True:
        if conn_handle is not None:
            dist = get_distance()
            message = f"{dist:.1f} cm".encode()

            try:
                ble.gatts_write(tx_handle, message)
                print("?? Distance envoyée :", message.decode())
            except OSError as e:
                print("?? Erreur BLE :", e)

        time.sleep(5)

except KeyboardInterrupt:
    ble.active(False)
    print("? Arrêt du programme")
