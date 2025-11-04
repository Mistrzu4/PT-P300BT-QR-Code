import sys
import qrcode
from PIL import Image
import printlabel
import serial.tools.list_ports
from PIL import Image

if len(sys.argv) < 2:
    print("Use: python justprint.py <part_nr> [-COM COMx]")
    sys.exit(1)

qr_value = sys.argv[1]  # np. "1"

qr_data = f'{{"part": {qr_value}}}'
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=1,
)
qr.add_data(qr_data)
qr.make(fit=True)

qr_img = qr.make_image(fill_color="black", back_color="white")
qr_filename = "qr_print.png"
qr_img.save(qr_filename)



# 1️⃣ Wczytanie obrazów
qr_img = Image.open("qr_print.png")       # 50x50
other_img = Image.open("right.png")       # 50x50

# 2️⃣ Sprawdzenie wysokości obu obrazów
if qr_img.height != other_img.height:
    # Jeśli różne, skalujemy drugi obraz do wysokości QR
    other_img = other_img.resize((other_img.width, qr_img.height))

# 3️⃣ Stworzenie nowego obrazu
combined_width = qr_img.width + other_img.width
combined_height = qr_img.height
combined_img = Image.new("RGB", (combined_width, combined_height), "white")

# 4️⃣ Wklejenie obrazów
combined_img.paste(qr_img, (0, 0))                    # po lewej
combined_img.paste(other_img, (qr_img.width, 0))      # po prawej

# 5️⃣ Zapis finalnego obrazu
combined_img.save("qr_print.png")
combined_img.show()




user_com = None
if "-COM" in sys.argv:
    idx = sys.argv.index("-COM")
    if idx + 1 < len(sys.argv):
        user_com = sys.argv[idx + 1]

if not user_com:
    ports = serial.tools.list_ports.comports()
    bt_ports = [p for p in ports if 'Bluetooth' in (p.description or '')]
    outgoing_bt_ports = [p.device for p in bt_ports if 'Incoming' not in (p.description or '')]

    if outgoing_bt_ports:
        user_com = outgoing_bt_ports[0]
        print(f"No outgoing Bluetooth port found. Automatically selected: {user_com}")
    else:
        print(".")
        sys.exit(1)

sys.argv = ["printlabel.py", user_com, "-M", qr_filename]

printlabel.main()
