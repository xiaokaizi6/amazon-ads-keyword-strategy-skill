from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

src = Path("tmp/pdf_source/pages")
out = Path("tmp/pdf_source/contacts")
out.mkdir(parents=True, exist_ok=True)
pages = sorted(src.glob("page-*.png"))
font = ImageFont.load_default()
per_sheet = 4
for start in range(0, len(pages), per_sheet):
    group = pages[start:start + per_sheet]
    thumbs = []
    for page in group:
        image = Image.open(page).convert("RGB")
        image.thumbnail((520, 735))
        canvas = Image.new("RGB", (540, 775), "white")
        canvas.paste(image, ((540 - image.width) // 2, 28))
        ImageDraw.Draw(canvas).text((12, 8), page.stem.replace("page-", "Page "), fill="black", font=font)
        thumbs.append(canvas)
    sheet = Image.new("RGB", (1080, 1550), "#dddddd")
    for index, image in enumerate(thumbs):
        x = (index % 2) * 540
        y = (index // 2) * 775
        sheet.paste(image, (x, y))
    sheet.save(out / f"contact-{start + 1:03d}-{start + len(group):03d}.jpg", quality=92)
