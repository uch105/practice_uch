import qrcode

website_url = "https://www.prescribemate.com"

qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data(website_url)
qr.make(fit=True)

img = qr.make_image(fill_color="white", back_color="#066f00")

img.save("prescribemate.png")
print("QR code saved as 'prescribemate.png'")