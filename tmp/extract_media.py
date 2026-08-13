from pathlib import Path
import zipfile
from PIL import Image, ImageDraw

root = Path(r"C:\Users\liuya\Downloads")
docs = [root / "2025亚马逊划线价运营玩法.docx", root / "亚马逊广告报告高效分析和优化-Word版 (1).docx"]
out = Path("tmp/media")
out.mkdir(parents=True, exist_ok=True)
for doc in docs:
    folder = out / doc.stem.replace(" ", "_")
    folder.mkdir(parents=True, exist_ok=True)
    imgs = []
    with zipfile.ZipFile(doc) as z:
        for name in z.namelist():
            if name.startswith("word/media/"):
                dest = folder / Path(name).name
                dest.write_bytes(z.read(name))
                try:
                    im = Image.open(dest).convert("RGB")
                    imgs.append((dest, im.size))
                except Exception:
                    pass
    print(doc.name, imgs)
    thumbs=[]
    for dest,size in imgs:
        im=Image.open(dest).convert("RGB")
        im.thumbnail((500, 700))
        canvas=Image.new("RGB",(520,760),"white")
        canvas.paste(im,((520-im.width)//2,30))
        d=ImageDraw.Draw(canvas)
        d.text((10,5),f"{dest.name} {size}",fill="black")
        thumbs.append(canvas)
    cols=2
    rows=(len(thumbs)+cols-1)//cols
    montage=Image.new("RGB",(cols*520,rows*760),(235,235,235))
    for i,im in enumerate(thumbs): montage.paste(im,((i%cols)*520,(i//cols)*760))
    montage.save(folder.parent/(folder.name+"_montage.jpg"),quality=90)
