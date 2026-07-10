from PIL import Image, ImageDraw
from pathlib import Path

assets = Path(__file__).with_name('assets')
assets.mkdir(exist_ok=True)

ico_out = assets / 'icon.ico'
png_out = assets / 'icon.png'
size = (64, 64)
img = Image.new('RGBA', size, (0, 0, 0, 0))
d = ImageDraw.Draw(img)
# draw rounded rectangle background
n = 6
r = 12
d.rounded_rectangle([(n, n), (size[0] - n, size[1] - n)], radius=r, fill=(30, 30, 30, 255))
# draw white notepad-like lines
line_x1 = 16
line_x2 = 48
d.rectangle([(line_x1, 16), (line_x2, 22)], fill=(255, 255, 255, 255))
d.rectangle([(line_x1, 28), (line_x2, 34)], fill=(255, 255, 255, 255))
d.rectangle([(line_x1, 40), (line_x2, 46)], fill=(255, 255, 255, 255))
# draw small star dot (important)
star = [(46, 8), (50, 20), (62, 20), (52, 26), (56, 38), (46, 30), (36, 38), (40, 26), (30, 20), (42, 20)]
d.polygon(star, fill=(255, 200, 0, 255))
# save as ico with multiple sizes and as png for title bar image
img.save(ico_out, format='ICO', sizes=[(64, 64), (32, 32), (16, 16)])
img.save(png_out, format='PNG')
print('Wrote', ico_out)
print('Wrote', png_out)
