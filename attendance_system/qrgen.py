import qrcode
import os

students = [
    {'id': '002', 'name': 'Sakhile Sibanda'},
    {'id': '001', 'name': 'Mthandazo Moyo'},
    # Add more students here
]

for student in students:
    qr = qrcode.make(student['id'])  # or use a unique identifier
    qr.save(os.path.join('static', 'qr_codes', f"{student['id']}.png"))
    print(f"Generated QR code for {student['name']} (ID: {student['id']})")

