#!/bin/bash
# rendert alle Folien (auch ausgeblendete) als PNG
cd /home/user/bbig && python3 - <<'P'
from pptx import Presentation
p=Presentation('output/v3/praesentation_unterricht_v3.pptx')
for s in p.slides:
    if s._element.get('show')=='0': del s._element.attrib['show']
p.save('/tmp/v4_alle.pptx')
P
D=/tmp/claude-0/-home-user-bbig/039a734c-67c7-5163-9323-eb0bfa939268/scratchpad; rm -rf $D/v4 && mkdir -p $D/v4 && cd $D/v4 && timeout 600 soffice --headless --convert-to pdf --outdir $D/v4 /tmp/v4_alle.pptx >/dev/null 2>&1
python3 -c "
import pymupdf
d=pymupdf.open('v4_alle.pdf');print(len(d),'Folien gerendert')
for i,p in enumerate(d): p.get_pixmap(dpi=40).save(f'p{i+1:02d}.png')
"
