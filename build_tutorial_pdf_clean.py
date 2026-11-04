import os
from build_tutorial_pdf import Parser, png_rgb, cp, wrap

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "tutorial_login_suap.pdf")
W, H, M = 595, 842, 58


def code_lines(text, width):
    result = []
    for raw in text.splitlines():
        line = raw.expandtabs(4).rstrip()
        if not line:
            result.append("")
            continue
        while len(line) > width:
            result.append(line[:width])
            line = line[width:]
        result.append(line)
    return result or [""]


def make_pdf():
    p = Parser(); p.feed(open(os.path.join(ROOT, "tutorial_login_suap.html"), encoding="utf-8").read())
    sections, current = [], []
    for item in p.blocks:
        if item[0] in ("cover", "page") and current:
            sections.append(current); current = []
        current.append(item)
    if current: sections.append(current)

    images = {}
    for kind, path in p.blocks:
        if kind == "image" and os.path.exists(path) and path not in images:
            images[path] = png_rgb(path)

    objects = [None]
    def obj(data): objects.append(data); return len(objects) - 1
    fonts = {
        "F1": obj(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>"),
        "F2": obj(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>"),
        "F3": obj(b"<< /Type /Font /Subtype /Type1 /BaseFont /Courier /Encoding /WinAnsiEncoding >>"),
    }
    img_ids = {}
    for path, (w, h, raw) in images.items():
        img_ids[path] = obj(f"<< /Type /XObject /Subtype /Image /Width {w} /Height {h} /ColorSpace /DeviceRGB /BitsPerComponent 8 /Filter /FlateDecode /Length {len(raw)} >>\nstream\n".encode() + raw + b"\nendstream")

    pages = []
    def new_page(title=None):
        page = [("color", (1, 1, 1)), ("rect", (0, 0, W, H))]
        if title:
            page += [("color", (0.12, 0.42, 0.35)), ("rect", (M, H-61, 28, 3)),
                     ("color", (0.08, 0.11, 0.15)), ("text", (M, H-88, 19, title, "F2")),
                     ("color", (0.80, 0.83, 0.85)), ("rect", (M, H-101, W-2*M, 1))]
        pages.append(page)
        return page, H-125 if title else H-70

    def add_text(page, x, y, text, size=9.2, font="F1", color=(0.12, 0.16, 0.22)):
        page += [("color", color), ("text", (x, y, size, text, font))]

    def add_footer(page, number):
        page += [("color", (0.82, 0.84, 0.86)), ("rect", (M, 38, W-2*M, 1)),
                 ("text", (M, 25, 7.5, "Tutorial de login com SUAP", "F1")),
                 ("text", (W-78, 25, 7.5, "Página %d" % number, "F1"))]

    # Cover
    cover, _ = new_page()
    cover += [("color", (0.12, 0.42, 0.35)), ("rect", (M, H-130, 72, 4)),
              ("color", (0.08, 0.11, 0.15)), ("text", (M, H-190, 25, "Como adicionar login", "F2")),
              ("text", (M, H-222, 25, "com SUAP a uma aplicação Flask", "F2")),
              ("color", (0.35, 0.39, 0.43)), ("text", (M, H-258, 12, "OAuth 2.0  ·  Authorization Code  ·  Flask-Login", "F1"))]
    cover_img = next((v for k, v in sections[0] if k == "image" and v in img_ids), None)
    if cover_img:
        iw, ih, _ = images[cover_img]; maxw=W-2*M; maxh=125; s=min(maxw/iw,maxh/ih); ww=iw*s; hh=ih*s; x=(W-ww)/2; y=H-455
        cover += [("color", (0.88,0.89,0.90)), ("rect", (x-3,y-3,ww+6,hh+6)), ("image", (x,y,ww,hh,img_ids[cover_img]))]
    add_text(cover, M, H-500, "Guia técnico de configuração e implementação", 11, "F1", (0.35,0.39,0.43))

    for section in sections[1:]:
        title = next((v for k, v in section if k == "h2"), "Integração com SUAP")
        page, y = new_page(title)
        for kind, value in section:
            if kind in ("page", "h2"): continue
            if kind == "table_row":
                left, right = value if len(value) >= 2 else ("", "")
                left_lines, right_lines = wrap(left, 28), wrap(right, 61)
                leading=11; row_h=max(len(left_lines),len(right_lines))*leading+12
                if y-row_h < 62:
                    add_footer(page, len(pages)); page, y = new_page(title + " (continuação)")
                header = left == "Arquivo"
                if header:
                    page += [("color",(0.93,0.95,0.95)),("rect",(M-2,y-row_h,W-2*M+4,row_h))]
                    color=(0.08,0.11,0.15); font="F2"
                else:
                    page += [("color",(1,1,1)),("rect",(M-2,y-row_h,W-2*M+4,row_h)),("color",(0.82,0.84,0.86)),("rect",(M-2,y-row_h,W-2*M+4,1))]
                    color=(0.10,0.16,0.22); font="F1"
                page += [("color",(0.82,0.84,0.86)),("rect",(M+145,y-row_h,1,row_h))]
                ty=y-9
                for line in left_lines: add_text(page,M+6,ty,line,8.2,font,color); ty-=leading
                ty=y-9
                for line in right_lines: add_text(page,M+153,ty,line,8.2,font,color); ty-=leading
                y-=row_h+2; continue
            if kind in ("h1", "h3"):
                lines = wrap(value, 64); needed = len(lines)*17 + 18
                if y-needed < 62: add_footer(page, len(pages)); page, y = new_page(title + " (continuação)")
                for line in lines:
                    add_text(page, M, y, line, 12 if kind == "h3" else 18, "F2", (0.09,0.42,0.27) if kind == "h3" else (0.07,0.23,0.41)); y -= 17 if kind == "h3" else 22
                    page += [("color", (0.80,0.82,0.84)), ("rect", (M, y+4, W-2*M, 1))]; y -= 14; continue
            if kind == "image" and value in img_ids:
                iw, ih, _ = images[value]; maxw=W-2*M-12; maxh=180 if title.startswith("2.") else 125; s=min(maxw/iw,maxh/ih); ww=iw*s; hh=ih*s; needed=hh+28
                if y-needed < 62: add_footer(page, len(pages)); page, y = new_page(title + " (continuação)")
                x=(W-ww)/2; y-=hh+10; page += [("color", (0.88,0.89,0.90)), ("rect", (x-3,y-3,ww+6,hh+6)), ("image",(x,y,ww,hh,img_ids[value]))]; y-=18; continue
            if kind in ("lead", "warning", "success"):
                lines=wrap(value, 82); leading=12; needed=len(lines)*leading+24
                if y-needed < 62: add_footer(page, len(pages)); page, y = new_page(title + " (continuação)")
                colors={"lead":((0.97,0.98,0.98),(0.12,0.42,0.35)),"warning":((0.98,0.98,0.97),(0.35,0.39,0.43)),"success":((0.97,0.98,0.98),(0.12,0.42,0.35))}[kind]
                bottom=y-needed+8; page += [("color",colors[0]),("rect",(M-5,bottom,W-2*M+10,needed)),("color",colors[1]),("rect",(M-5,bottom,3,needed))]
                ty=y-8
                for line in lines: add_text(page,M+10,ty,line,8.9); ty-=leading
                y=bottom-13; continue
            size=8.2 if kind == "pre" else 9.2; width=88 if kind == "pre" else 92; leading=9.6 if kind == "pre" else 12
            lines=code_lines(value,width) if kind == "pre" else wrap(value,width); needed=len(lines)*leading+18
            if y-needed < 62: add_footer(page, len(pages)); page, y = new_page(title + " (continuação)")
            if kind == "pre":
                bottom=y-needed+8; page += [("color",(0.97,0.97,0.97)),("rect",(M-5,bottom,W-2*M+10,needed)),("color",(0.12,0.42,0.35)),("rect",(M-5,bottom,3,needed))]; ty=y-8; x=M+8; font="F3"
            else: ty=y; x=M; font="F1"
            for line in lines: add_text(page,x,ty,line,size,font); ty-=leading
            y=ty-9
        add_footer(page, len(pages))

    page_tree = obj(b"")
    for page in pages:
        stream=bytearray(b"q\n")
        for typ, data in page:
            if typ == "color": stream += (f"{data[0]} {data[1]} {data[2]} rg\n").encode()
            elif typ == "rect": stream += (f"{data[0]} {data[1]} {data[2]} {data[3]} re f\n").encode()
            elif typ == "text":
                x,y,size,text,font=data; stream += f"BT /{font} {size} Tf {x} {y} Td (".encode()+cp(text)+b") Tj ET\n"
            elif typ == "image":
                x,y,w,h,i=data; stream += f"q {w} 0 0 {h} {x} {y} cm /Im{i} Do Q\n".encode()
        stream += b"Q\n"; c=obj(f"<< /Length {len(stream)} >>\nstream\n".encode()+stream+b"endstream")
        xobjs=" ".join('/Im%d %d 0 R'%(i,img_ids[p]) for p,i in img_ids.items())
        res=f"<< /Font << {' '.join('/%s %d 0 R'%(k,v) for k,v in fonts.items())} >> /XObject << {xobjs} >> >>"
        page_ids = globals().setdefault("_page_ids", [])
        page_ids.append(obj(f"<< /Type /Page /Parent {page_tree} 0 R /MediaBox [0 0 {W} {H}] /Resources {res} /Contents {c} 0 R >>".encode()))
    page_ids=globals().pop("_page_ids")
    objects[page_tree]=f"<< /Type /Pages /Kids [{' '.join('%d 0 R'%x for x in page_ids)}] /Count {len(page_ids)} >>".encode()
    catalog=obj(f"<< /Type /Catalog /Pages {page_tree} 0 R >>".encode())
    out=bytearray(b"%PDF-1.4\n%\xff\xff\xff\xff\n"); offsets=[0]
    for n,data in enumerate(objects[1:],1): offsets.append(len(out)); out += f"{n} 0 obj\n".encode()+data+b"\nendobj\n"
    xref=len(out); out += f"xref\n0 {len(objects)}\n0000000000 65535 f \n".encode(); out += b"".join(f"{x:010d} 00000 n \n".encode() for x in offsets[1:]); out += f"trailer\n<< /Size {len(objects)} /Root {catalog} 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode()
    open(OUT,"wb").write(out)
    print("generated", len(pages), "pages")


if __name__ == "__main__": make_pdf()
