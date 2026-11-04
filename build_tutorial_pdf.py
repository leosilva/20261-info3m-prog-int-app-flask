import html
import os
import re
import struct
import zlib
from html.parser import HTMLParser


ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "tutorial_login_suap.pdf")


class Parser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.blocks = []
        self.stack = []
        self.buf = []
        self.kind = "p"
        self.ignore = 0
        self.in_table = False
        self.in_row = False
        self.cell = None
        self.cells = []

    def flush(self):
        raw = "".join(self.buf)
        text = raw if self.kind == "pre" else raw.strip()
        if text:
            self.blocks.append((self.kind, text))
        self.buf = []

    def handle_starttag(self, tag, attrs):
        if tag in ("head", "style", "title"):
            self.ignore += 1
            return
        if self.ignore:
            return
        attrs = dict(attrs)
        if tag == "table":
            self.flush(); self.in_table = True; return
        if self.in_table and tag == "tr":
            self.in_row = True; self.cells = []; return
        if self.in_table and tag in ("td", "th"):
            self.cell = []; return
        if self.in_table:
            return
        if tag == "div" and attrs.get("class") in ("lead", "warning", "success"):
            self.flush(); self.kind = attrs["class"]; return
        if tag == "section":
            self.flush()
            if "cover" in attrs.get("class", ""):
                self.blocks.append(("cover", ""))
            elif "page" in attrs.get("class", ""):
                self.blocks.append(("page", ""))
        elif tag == "img":
            self.flush()
            src = attrs.get("src", "")
            self.blocks.append(("image", src.replace("file://", "")))
        elif tag in ("h1", "h2", "h3"):
            self.flush(); self.kind = tag
        elif tag == "pre":
            self.flush(); self.kind = "pre"
        elif tag in ("p", "li", "td", "th"):
            self.flush(); self.kind = "p"
            if tag == "li": self.buf.append("• ")
        elif tag == "br":
            self.buf.append("\n")

    def handle_endtag(self, tag):
        if tag in ("head", "style", "title"):
            self.ignore = max(0, self.ignore - 1)
            return
        if self.ignore:
            return
        if self.in_table and tag in ("td", "th"):
            self.cells.append("".join(self.cell or []).strip()); self.cell = None; return
        if self.in_table and tag == "tr":
            self.blocks.append(("table_row", self.cells)); self.in_row = False; return
        if self.in_table and tag == "table":
            self.in_table = False; return
        if tag == "div" and self.kind in ("lead", "warning", "success"):
            self.flush(); self.kind = "p"; return
        if tag in ("h1", "h2", "h3", "pre", "p", "li", "td", "th"):
            self.flush(); self.kind = "p"

    def handle_data(self, data):
        if self.ignore:
            return
        if self.in_table and self.cell is not None:
            self.cell.append(data); return
        self.buf.append(data)


def png_rgb(path):
    data = open(path, "rb").read()
    assert data[:8] == b"\x89PNG\r\n\x1a\n"
    pos = 8; raw = b""; width = height = color = None
    while pos < len(data):
        n = struct.unpack(">I", data[pos:pos+4])[0]
        typ = data[pos+4:pos+8]
        body = data[pos+8:pos+8+n]
        pos += 12+n
        if typ == b"IHDR": width, height, depth, color, comp, filt, inter = struct.unpack(">IIBBBBB", body); assert depth == 8 and inter == 0
        elif typ == b"IDAT": raw += body
        elif typ == b"IEND": break
    decoded = zlib.decompress(raw)
    channels = {2: 3, 6: 4, 0: 1, 4: 2}[color]
    stride = width * channels; rows = []; i = 0; prev = bytearray(stride)
    for _ in range(height):
        f = decoded[i]; i += 1; cur = bytearray(decoded[i:i+stride]); i += stride
        for x in range(stride):
            left = cur[x-channels] if x >= channels else 0
            up = prev[x]
            ul = prev[x-channels] if x >= channels else 0
            if f == 1: cur[x] = (cur[x] + left) & 255
            elif f == 2: cur[x] = (cur[x] + up) & 255
            elif f == 3: cur[x] = (cur[x] + ((left + up)//2)) & 255
            elif f == 4:
                p = left + up - ul; pa = abs(p-left); pb = abs(p-up); pc = abs(p-ul)
                q = left if pa <= pb and pa <= pc else (up if pb <= pc else ul)
                cur[x] = (cur[x] + q) & 255
        rows.append(cur); prev = cur
    if color == 2: rgb = b"".join(rows)
    elif color == 6: rgb = b"".join(bytes(row[x] for x in range(0, len(row), 4) for _ in (0,)) + b"" for row in [])
    else: raise ValueError("PNG deve ser RGB ou RGBA")
    if color == 6:
        rgb = b"".join(bytes(row[x:x+3]) for row in rows for x in range(0, len(row), 4))
    return width, height, zlib.compress(rgb, 6)


def cp(text):
    text = text.replace("→", "->").replace("✓", "[ok]")
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)").encode("cp1252", "replace")


def wrap(text, width):
    out = []
    for part in text.splitlines() or [""]:
        words = part.split()
        line = ""
        for word in words:
            if len(word) > width:
                if line:
                    out.append(line); line = ""
                while len(word) > width:
                    out.append(word[:width]); word = word[width:]
            if len(line) + len(word) + 1 > width and line:
                out.append(line); line = word
            else: line = (line + " " + word).strip()
        out.append(line)
    return out


def build():
    parser = Parser(); parser.feed(open(os.path.join(ROOT, "tutorial_login_suap.html"), encoding="utf-8").read())
    pages = [[]]
    for kind, value in parser.blocks:
        if kind in ("cover", "page") and pages[-1]: pages.append([])
        pages[-1].append((kind, value))
    images = {}
    for kind, value in parser.blocks:
        if kind == "image" and os.path.exists(value) and value not in images:
            images[value] = png_rgb(value)

    objects = [None]
    def obj(data): objects.append(data); return len(objects)-1
    font = obj(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>")
    bold = obj(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>")
    mono = obj(b"<< /Type /Font /Subtype /Type1 /BaseFont /Courier /Encoding /WinAnsiEncoding >>")
    img_ids = {path: obj(f"<< /Type /XObject /Subtype /Image /Width {w} /Height {h} /ColorSpace /DeviceRGB /BitsPerComponent 8 /Filter /FlateDecode /Length {len(raw)} >>\nstream\n".encode()+raw+b"\nendstream") for path,(w,h,raw) in images.items()}
    page_ids=[]; page_contents=[]; skipped=0
    W,H=595,842; margin=54
    for page in pages:
        y=H-72; content=[]; title=False
        cover_mode=False
        if page and page[0][0] != "cover":
            content += [("color", (0.95,0.97,0.99)), ("rect", (0,0,W,H)), ("color", (0.07,0.23,0.41)), ("rect", (0,H-48,W,48)), ("color", (1,1,1)), ("text", (margin, H-30, 8.2, "GUIA DE IMPLEMENTAÇÃO  ·  FLASK + SUAP", "F2"))]
        for kind,value in page:
            if kind == "cover":
                cover_mode=True
                content += [("color", (0.07,0.23,0.41)), ("rect", (0,0,W,H)), ("color", (0.98,0.83,0.38)), ("rect", (45,H-112,125,5)), ("color", (1,1,1)), ("text", (45,H-175,25,"Como adicionar login", "F2")), ("text", (45,H-205,25,"com SUAP a uma aplicação Flask", "F2")), ("text", (45,H-242,13,"OAuth 2.0  ·  Authorization Code  ·  Flask-Login", "F2"))]; y=H-275; continue
            if kind == "page":
                cover_mode=False
                continue
            if kind == "image" and value in img_ids:
                iw,ih,_=images[value]; maxw=W-2*margin-12; maxh=112; scale=min(maxw/iw,maxh/ih); ww=iw*scale; hh=ih*scale; x=(W-ww)/2; y-=hh+14
                content += [("color", (0.84,0.88,0.92)), ("rect", (x-5,y-5,ww+10,hh+10)), ("image",(x,y,ww,hh,img_ids[value]))]; y-=20; continue
            if kind in ("h1","h2","h3"):
                if cover_mode:
                    continue
                if kind == "h2":
                    y-=6; lines=wrap(value, 53); box_h=len(lines)*20+18
                    content += [("color", (0.12,0.42,0.72)), ("rect", (margin-8,y-box_h+8,W-2*margin+16,box_h))]
                    for line in lines: content += [("color",(1,1,1)),("text",(margin,y,16,line,"F2"))]; y-=20
                    y-=15
                else:
                    size=20 if kind == "h1" else 12.5; color=(0.07,0.23,0.41) if kind == "h1" else (0.09,0.42,0.27)
                    for line in wrap(value, 60): content += [("color",color),("text",(margin,y,size,line,"F2"))]; y-=size+5
                    content += [("color",(0.72,0.82,0.88)),("rect",(margin,y+2,W-2*margin,1))]; y-=10
                continue
            if kind in ("lead", "warning", "success"):
                lines=wrap(value, 82); leading=12; text_y=y-8; top=text_y+8; bottom=text_y-(len(lines)-1)*leading-9; box_h=top-bottom
                palette={"lead":((0.91,0.96,1.0),(0.12,0.42,0.72)),"warning":((1.0,0.96,0.82),(0.82,0.55,0.02)),"success":((0.91,0.98,0.93),(0.10,0.49,0.28))}[kind]
                content += [("color",palette[0]),("rect",(margin-4,bottom,W-2*margin+8,box_h)),("color",palette[1]),("rect",(margin-4,bottom,5,box_h))]
                for line in lines:
                    content += [("color",(0.10,0.17,0.23)),("text",(margin+10,text_y,8.9,line,"F1"))]; text_y-=leading
                y=bottom-12; continue
            size=8.2 if kind == "pre" else 9.2; width=88 if kind == "pre" else 92; leading=9.6 if kind == "pre" else 12; lines=wrap(value, width)
            if kind == "pre":
                text_y=y-8; top=text_y+8; bottom=text_y-(len(lines)-1)*leading-8; box_h=top-bottom; content += [("color", (0.88,0.93,0.97)), ("rect", (margin-5, bottom, W-2*margin+10, box_h)), ("color",(0.12,0.42,0.66)), ("rect",(margin-5,bottom,4,box_h))]
            else:
                text_y=y
            for line in lines:
                if y < 34:
                    skipped += 1
                    continue
                content += [("color",(0.10,0.15,0.22)),("text",(margin+8 if kind == "pre" else margin,text_y,size,line,"F3" if kind == "pre" else "F1"))]; text_y-=leading
            y=text_y
            y-=7
        if page and page[0][0] != "cover":
            content += [("color", (0.60,0.66,0.72)), ("rect", (margin,38,W-2*margin,1)), ("text", (margin,25,7.5,"Integração de login com SUAP", "F1")), ("text", (W-70,25,7.5,"Página %d" % (len(page_contents)+1), "F1"))]
        page_contents.append(content)
    pages_obj = obj(b"")
    for content in page_contents:
        stream=bytearray(); stream += b"q\n"
        for typ,data in content:
            if typ == "color": stream += (f"{data[0]} {data[1]} {data[2]} rg\n").encode()
            elif typ == "rect": stream += (f"{data[0]} {data[1]} {data[2]} {data[3]} re f\n").encode()
            elif typ == "text":
                if len(data) == 4: x,y,size,text = data; font_name = "F1"
                else: x,y,size,text,font_name = data
                stream += f"BT /{font_name} {size} Tf {x} {y} Td (".encode()+cp(text)+b") Tj ET\n"
            elif typ == "image":
                x,y,w,h,i=data; stream += f"q {w} 0 0 {h} {x} {y} cm /Im{i} Do Q\n".encode()
        stream += b"Q\n"; c=obj(f"<< /Length {len(stream)} >>\nstream\n".encode()+stream+b"endstream")
        resources=f"<< /Font << /F1 {font} 0 R /F2 {bold} 0 R /F3 {mono} 0 R >> /XObject << {' '.join('/Im%d %d 0 R'%(i,img_ids[p]) for p,i in img_ids.items())} >> >>"
        page_ids.append(obj(f"<< /Type /Page /Parent {pages_obj} 0 R /MediaBox [0 0 {W} {H}] /Resources {resources} /Contents {c} 0 R >>".encode()))
    kids=" ".join(f"{p} 0 R" for p in page_ids); objects[pages_obj]=f"<< /Type /Pages /Kids [{kids}] /Count {len(page_ids)} >>".encode()
    catalog=obj(f"<< /Type /Catalog /Pages {pages_obj} 0 R >>".encode())
    out=bytearray(b"%PDF-1.4\n%\xff\xff\xff\xff\n"); offsets=[0]
    for n,data in enumerate(objects[1:],1): offsets.append(len(out)); out += f"{n} 0 obj\n".encode()+data+b"\nendobj\n"
    xref=len(out); out += f"xref\n0 {len(objects)}\n0000000000 65535 f \n".encode(); out += b"".join(f"{o:010d} 00000 n \n".encode() for o in offsets[1:]); out += f"trailer\n<< /Size {len(objects)} /Root {catalog} 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode()
    open(OUT,"wb").write(out)
    if skipped:
        print("WARNING: skipped lines", skipped)


if __name__ == "__main__": build()
