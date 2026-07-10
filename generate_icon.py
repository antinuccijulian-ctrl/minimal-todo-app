from PIL import Image, ImageDraw
from pathlib import Path

out = Path(__file__).with_name('assets').joinpath('icon.ico')
size = (64, 64)
img = Image.new('RGBA', size, (0, 0, 0, 0))
d = ImageDraw.Draw(img)
# draw rounded rectangle background
d.rounded_rectangle([(4,4),(60,60)], radius=10, fill=(30,30,30,255))
# draw white notepad-like lines
d.rectangle([(12,14),(52,20)], fill=(255,255,255,255))
d.rectangle([(12,26),(52,32)], fill=(255,255,255,255))
d.rectangle([(12,38),(52,44)], fill=(255,255,255,255))
# draw small star dot (important)
d.polygon([(46,10),(49,18),(58,18),(51,23),(54,32),(46,26),(38,32),(41,23),(34,18),(43,18)], fill=(255,200,0,255))
# save as ico with multiple sizes
img.save(out, format='ICO', sizes=[(64,64),(32,32),(16,16)])
print('Wrote', out)
