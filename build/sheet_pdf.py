import sys, pymupdf
from PIL import Image
pdf, out, cols = sys.argv[1], sys.argv[2], int(sys.argv[3]); per = int(sys.argv[4]) if len(sys.argv) > 4 else cols*2
d = pymupdf.open(pdf); ims = []
for p in d:
    pm = p.get_pixmap(dpi=60); ims.append(Image.frombytes("RGB", (pm.width, pm.height), pm.samples))
w, h = ims[0].size
for k in range(0, len(ims), per):
    ch = ims[k:k+per]; rows = (len(ch)+cols-1)//cols
    S = Image.new("RGB", (w*cols, h*rows), "white")
    for i, im in enumerate(ch): S.paste(im, ((i % cols)*w, (i//cols)*h))
    S.save(f"{out}_{k//per+1}.png")
print(len(ims), "pages")
