from PIL import Image, ImageDraw
from pathlib import Path

assets = Path(__file__).with_name('assets')
assets.mkdir(exist_ok=True)

ico_out = assets / 'icon.ico'
png_out = assets / 'icon.png'
size = (64, 64)
img = Image.new('RGBA', size, (0, 0, 0, 0))
d = ImageDraw.Draw(img)
# draw rounded rectangle background for a clean notebook badge
n = 6
r = 12
d.rounded_rectangle([(n, n), (size[0] - n, size[1] - n)], radius=r, fill=(255, 255, 255, 255), outline=(0, 0, 0, 255), width=2)
# draw black notebook cover edge
cover_x = 14
d.rectangle([(cover_x, 12), (cover_x + 4, 52)], fill=(0, 0, 0, 255))
# draw black page lines
line_x1 = 22
line_x2 = 50
for y in (20, 28, 36, 44):
    d.rectangle([(line_x1, y), (line_x2, y + 2)], fill=(0, 0, 0, 255))
# draw a simple black border around the page
for offset in range(0, 2):
    d.rounded_rectangle([(n + offset, n + offset), (size[0] - n - offset, size[1] - n - offset)], radius=r, outline=(0, 0, 0, 255))
# save as ico with multiple sizes and as png for title bar image
img.save(ico_out, format='ICO', sizes=[(64, 64), (32, 32), (16, 16)])
img.save(png_out, format='PNG')
print('Wrote', ico_out)
print('Wrote', png_out)
