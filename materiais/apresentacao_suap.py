from pathlib import Path
import textwrap


W, H = 960, 540  # 16:9
OUT = Path(__file__).with_name("conexao-suap.pdf")

NAVY = (0.05, 0.12, 0.22)
BLUE = (0.12, 0.42, 0.76)
CYAN = (0.10, 0.68, 0.78)
GREEN = (0.12, 0.58, 0.42)
ORANGE = (0.95, 0.53, 0.18)
RED = (0.78, 0.22, 0.25)
INK = (0.10, 0.14, 0.20)
MUTED = (0.36, 0.41, 0.48)
LIGHT = (0.94, 0.96, 0.98)
PALE_BLUE = (0.88, 0.94, 1.0)
PALE_GREEN = (0.88, 0.97, 0.93)
WHITE = (1, 1, 1)


def esc(s: str) -> str:
    s = s.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
    return s.encode("latin-1", "replace").decode("latin-1")


class Page:
    def __init__(self, num, title, kicker="GUIA DE INTEGRAÇÃO"):
        self.a = []
        self.num = num
        self.bg(WHITE)
        self.rect(0, 0, W, 10, NAVY, fill=True)
        self.text(48, 505, kicker, 9, BLUE, bold=True)
        self.text(48, 466, title, 27, NAVY, bold=True)
        self.text(900, 24, f"{num:02d}", 9, MUTED, bold=True, align="right")

    def bg(self, color):
        self.rect(0, 0, W, H, color, fill=True)

    def color(self, c):
        return f"{c[0]:.3f} {c[1]:.3f} {c[2]:.3f}"

    def rect(self, x, y, w, h, c, fill=True, stroke=None, radius=0):
        if radius:
            k = 0.5522848
            r = min(radius, w/2, h/2)
            p = [
                f"{x+r} {y} m", f"{x+w-r} {y} l", f"{x+w-r+k*r} {y} {x+w} {y+r-k*r} {x+w} {y+r} c",
                f"{x+w} {y+h-r} l", f"{x+w} {y+h-r+k*r} {x+w-r+k*r} {y+h} {x+w-r} {y+h} c",
                f"{x+r} {y+h} l", f"{x+r-k*r} {y+h} {x} {y+h-r+k*r} {x} {y+h-r} c",
                f"{x} {y+r} l", f"{x} {y+r-k*r} {x+r-k*r} {y} {x+r} {y} c", "h"
            ]
            self.a.append(" ".join(p))
        else:
            self.a.append(f"{x} {y} {w} {h} re")
        if fill:
            self.a.append(f"{self.color(c)} rg f")
        if stroke:
            self.a.append(f"{self.color(stroke)} RG S")

    def line(self, x1, y1, x2, y2, c=INK, width=1.5):
        self.a.append(f"{self.color(c)} RG {width} w {x1} {y1} m {x2} {y2} l S")

    def arrow(self, x1, y1, x2, y2, c=BLUE, width=2):
        self.line(x1, y1, x2, y2, c, width)
        if abs(x2-x1) >= abs(y2-y1):
            sign = 1 if x2 > x1 else -1
            self.a.append(f"{self.color(c)} rg {x2} {y2} m {x2-sign*10} {y2+5} l {x2-sign*10} {y2-5} l h f")
        else:
            sign = 1 if y2 > y1 else -1
            self.a.append(f"{self.color(c)} rg {x2} {y2} m {x2-5} {y2-sign*10} l {x2+5} {y2-sign*10} l h f")

    def text(self, x, y, s, size=14, c=INK, bold=False, align="left", font=None):
        font = font or ("F2" if bold else "F1")
        # Approximate width keeps alignment simple with standard fonts.
        width = len(s) * size * (0.56 if font == "F1" else 0.58)
        if align == "right": x -= width
        elif align == "center": x -= width / 2
        self.a.append(f"BT /{font} {size} Tf {self.color(c)} rg 1 0 0 1 {x:.1f} {y:.1f} Tm ({esc(s)}) Tj ET")

    def paragraph(self, x, y, s, width_chars, size=14, leading=20, c=INK, bold=False):
        lines = []
        for para in s.split("\n"):
            lines.extend(textwrap.wrap(para, width=width_chars) or [""])
        for i, line in enumerate(lines):
            self.text(x, y - i*leading, line, size, c, bold)
        return y - len(lines)*leading

    def pill(self, x, y, label, color=BLUE, width=None):
        width = width or (len(label)*7.2 + 24)
        self.rect(x, y, width, 24, color, fill=True, radius=12)
        self.text(x+width/2, y+7, label, 10, WHITE, bold=True, align="center")

    def browser(self, x, y, w, h, title, accent=BLUE):
        self.rect(x, y, w, h, WHITE, fill=True, stroke=(0.78,0.83,0.89), radius=10)
        self.rect(x, y+h-26, w, 26, (0.90,0.93,0.96), fill=True, radius=10)
        self.rect(x, y+h-26, w, 13, (0.90,0.93,0.96), fill=True)
        for i, col in enumerate([RED, ORANGE, GREEN]): self.rect(x+13+i*13, y+h-17, 7, 7, col, fill=True, radius=3.5)
        self.text(x+48, y+h-18, title, 9, MUTED)
        self.rect(x+18, y+h-56, w-36, 20, LIGHT, fill=True, radius=5)
        self.text(x+28, y+h-50, "http://127.0.0.1:5000/login", 8, MUTED)
        self.rect(x+25, y+25, w-50, h-95, (0.98,0.99,1), fill=True, radius=5)
        self.rect(x+w/2-78, y+h/2-5, 156, 32, accent, fill=True, radius=6)
        self.text(x+w/2, y+h/2+5, "Entrar com SUAP", 12, WHITE, bold=True, align="center")

    def finish(self):
        return "\n".join(self.a)


def slide1():
    p = Page(1, "Conectando uma aplicação ao SUAP")
    p.text(50, 420, "Um passo a passo de OAuth2", 18, BLUE, bold=True)
    p.paragraph(50, 375, "Como o usuário sai da nossa aplicação, autoriza o acesso no SUAP e volta com seus dados de forma segura.", 43, 17, 25, MUTED)
    p.browser(570, 185, 300, 235, "Nossa aplicação")
    p.rect(120, 165, 230, 135, PALE_BLUE, fill=True, radius=18)
    p.text(235, 260, "SUAP", 34, NAVY, bold=True, align="center")
    p.text(235, 225, "identidade do estudante", 12, BLUE, align="center")
    p.arrow(350, 235, 570, 290, CYAN, 3)
    p.text(458, 323, "autoriza", 11, CYAN, bold=True, align="center")
    p.pill(50, 90, "Flask + OAuth2", NAVY, 125)
    p.pill(185, 90, "Para ensino médio", GREEN, 145)
    return p


def slide2():
    p = Page(2, "A ideia em uma frase")
    p.text(480, 412, "A aplicação não recebe a senha do aluno.", 22, NAVY, bold=True, align="center")
    p.text(480, 375, "Ela recebe uma autorização temporária e usa essa autorização para consultar o SUAP.", 14, MUTED, align="center")
    boxes = [(70, 180, 190, 115, "1", "Aluno", "clica no botão", BLUE), (385, 180, 190, 115, "2", "SUAP", "confirma a identidade", CYAN), (700, 180, 190, 115, "3", "Aplicação", "consulta os dados", GREEN)]
    for x,y,w,h,n,t,sub,col in boxes:
        p.rect(x,y,w,h,WHITE,fill=True,stroke=(0.82,0.86,0.90),radius=15)
        p.rect(x+18,y+h-42,30,30,col,fill=True,radius=15)
        p.text(x+33,y+h-33,n,15,WHITE,bold=True,align="center")
        p.text(x+65,y+h-34,t,17,NAVY,bold=True)
        p.text(x+20,y+43,sub,12,MUTED)
    p.arrow(265, 238, 375, 238, BLUE, 3); p.arrow(580, 238, 690, 238, BLUE, 3)
    p.rect(185, 88, 590, 38, PALE_GREEN, fill=True, radius=19)
    p.text(480, 102, "Senha fica no SUAP • token fica na sessão da aplicação", 12, GREEN, bold=True, align="center")
    return p


def slide3():
    p = Page(3, "Passo 1 — cadastrar a aplicação no SUAP")
    p.text(60, 418, "Antes de programar, o SUAP precisa conhecer o nosso projeto.", 17, NAVY, bold=True)
    items = [("Nome", "Projeto INFO3M"), ("Tipo", "OAuth2 / Authorization Code"), ("Callback", "http://127.0.0.1:5000/suap/callback")]
    y=350
    for label,val in items:
        p.text(70,y,label,11,BLUE,bold=True); p.rect(180,y-8,520,28,LIGHT,fill=True,radius=5); p.text(195,y,val,12,INK); y-=54
    p.rect(740, 195, 145, 170, PALE_BLUE, fill=True, radius=18)
    p.text(812, 315, "SUAP", 25, NAVY, bold=True, align="center")
    p.rect(768, 275, 88, 22, BLUE, fill=True, radius=4); p.text(812,282,"Nova aplicação",8,WHITE,align="center")
    p.rect(768, 240, 88, 22, (0.75,0.83,0.92), fill=True, radius=4); p.text(812,247,"Client ID",8,NAVY,align="center")
    p.rect(768, 205, 88, 22, (0.75,0.83,0.92), fill=True, radius=4); p.text(812,212,"Secret",8,NAVY,align="center")
    p.arrow(700, 288, 735, 288, CYAN, 2)
    p.rect(60, 100, 640, 45, (1.0,0.95,0.88), fill=True, radius=8)
    p.text(82, 118, "Atenção: o callback precisa ser idêntico nos dois lugares.", 13, ORANGE, bold=True)
    return p


def slide4():
    p = Page(4, "Passo 2 — guardar as credenciais")
    p.text(60, 418, "O projeto lê as credenciais pelas variáveis de ambiente.", 17, NAVY, bold=True)
    p.rect(60, 215, 500, 145, NAVY, fill=True, radius=12)
    code = ["export SUAP_CLIENT_ID=seu_client_id", "export SUAP_CLIENT_SECRET=seu_client_secret", "flask run --debug"]
    for i,line in enumerate(code): p.text(85, 325-i*34, line, 14, WHITE, font="F3")
    p.rect(620, 215, 260, 145, PALE_GREEN, fill=True, radius=12)
    p.text(750, 326, "Por que?", 16, GREEN, bold=True, align="center")
    p.paragraph(650, 295, "Credenciais não devem ficar no GitHub nem dentro do código.", 24, 12, 18, INK)
    p.rect(60, 125, 820, 47, (1.0,0.93,0.93), fill=True, radius=8)
    p.text(82, 143, "Nunca compartilhe o CLIENT_SECRET. Se vazar, gere outro no SUAP.", 13, RED, bold=True)
    return p


def slide5():
    p = Page(5, "Passo 3 — o botão inicia o fluxo")
    p.browser(55, 170, 270, 230, "Login da aplicação", BLUE)
    p.rect(390, 210, 195, 150, PALE_BLUE, fill=True, radius=16)
    p.text(488, 323, "routes.py", 16, NAVY, bold=True, align="center")
    p.text(488, 294, "/login-suap", 15, BLUE, bold=True, align="center")
    p.text(488, 257, "gera state", 12, MUTED, align="center")
    p.text(488, 235, "e redireciona", 12, MUTED, align="center")
    p.rect(650, 210, 235, 150, PALE_GREEN, fill=True, radius=16)
    p.text(768, 323, "SUAP", 22, GREEN, bold=True, align="center")
    p.text(768, 292, "/o/authorize/", 13, GREEN, bold=True, align="center")
    p.text(768, 257, "mostra a tela de login", 11, MUTED, align="center")
    p.arrow(325, 285, 380, 285, BLUE, 3); p.arrow(585, 285, 640, 285, BLUE, 3)
    p.paragraph(70, 120, "O state é uma “etiqueta” aleatória. Quando o SUAP devolve a resposta, a aplicação confere se a etiqueta é a mesma.", 100, 13, 19, MUTED)
    return p


def slide6():
    p = Page(6, "Passo 4 — o SUAP devolve um código")
    p.text(60, 418, "Depois do login, o navegador volta para o callback.", 17, NAVY, bold=True)
    p.rect(60, 205, 820, 145, LIGHT, fill=True, radius=12)
    p.text(82, 315, "http://127.0.0.1:5000/suap/callback", 14, MUTED, font="F3")
    p.text(82, 277, "?code=ABC123&state=mesma-etiqueta", 17, BLUE, bold=True, font="F3")
    p.rect(60, 120, 390, 45, PALE_GREEN, fill=True, radius=8)
    p.text(80, 138, "code = autorização de uso único", 13, GREEN, bold=True)
    p.rect(480, 120, 400, 45, (1.0,0.95,0.88), fill=True, radius=8)
    p.text(500, 138, "state = proteção contra respostas falsas", 13, ORANGE, bold=True)
    return p


def slide7():
    p = Page(7, "Passo 5 — trocar o código por um token")
    p.rect(50, 185, 245, 175, PALE_BLUE, fill=True, radius=16)
    p.text(172, 322, "Nossa aplicação", 17, NAVY, bold=True, align="center")
    p.text(172, 280, "envia: code + client_secret", 12, BLUE, align="center")
    p.text(172, 250, "para /o/token/", 12, BLUE, align="center")
    p.rect(360, 185, 245, 175, PALE_GREEN, fill=True, radius=16)
    p.text(482, 322, "SUAP", 22, GREEN, bold=True, align="center")
    p.text(482, 278, "confere o pedido", 12, MUTED, align="center")
    p.text(482, 248, "devolve access_token", 12, GREEN, bold=True, align="center")
    p.rect(670, 185, 240, 175, NAVY, fill=True, radius=16)
    p.text(790, 322, "Sessão", 17, WHITE, bold=True, align="center")
    p.text(790, 278, "guarda o token", 12, WHITE, align="center")
    p.text(790, 248, "sem mostrar na tela", 12, WHITE, align="center")
    p.arrow(295, 272, 350, 272, BLUE, 3); p.arrow(605, 272, 660, 272, GREEN, 3)
    p.text(480, 115, "No código: SuapAuthenticationService.exchange_code(code, redirect_uri)", 12, MUTED, font="F3", align="center")
    return p


def slide8():
    p = Page(8, "Passo 6 — consultar os dados do usuário")
    p.text(60, 418, "Com o token, a aplicação pode chamar a API do SUAP.", 17, NAVY, bold=True)
    p.rect(60, 230, 820, 125, NAVY, fill=True, radius=12)
    p.text(85, 320, "GET https://suap.ifrn.edu.br/api/rh/meus-dados/", 14, WHITE, font="F3")
    p.text(85, 280, "Authorization: Bearer <access_token>", 14, CYAN, font="F3")
    p.rect(60, 135, 820, 56, PALE_GREEN, fill=True, radius=10)
    p.text(85, 160, "Resposta JSON → nome, matrícula, e-mail, vínculo e foto", 15, GREEN, bold=True)
    p.text(60, 95, "Regra de ouro: token é a chave; endpoint é a porta; JSON é a informação.", 13, MUTED)
    return p


def slide9():
    p = Page(9, "O fluxo completo, olhando para o código")
    steps = [
        ("1", "/login-suap", "cria state + URL"),
        ("2", "SUAP /authorize", "usuário autoriza"),
        ("3", "/suap/callback", "recebe code"),
        ("4", "SUAP /token", "troca code por token"),
        ("5", "/api/rh/meus-dados/", "lê o perfil"),
    ]
    x0=65
    for i,(n,path,sub) in enumerate(steps):
        x=x0+i*175
        p.rect(x, 250, 145, 95, WHITE, fill=True, stroke=(0.80,0.86,0.91), radius=12)
        p.rect(x+12, 306, 24, 24, BLUE if i<3 else GREEN, fill=True, radius=12)
        p.text(x+24, 313, n, 11, WHITE, bold=True, align="center")
        p.text(x+48, 315, path, 9, NAVY, bold=True)
        p.text(x+14, 270, sub, 10, MUTED)
        if i < 4: p.arrow(x+145, 297, x+168, 297, CYAN, 2)
    p.rect(145, 145, 670, 42, PALE_BLUE, fill=True, radius=21)
    p.text(480, 160, "routes.py coordena • SuapAuthenticationService conversa com o SUAP", 12, BLUE, bold=True, align="center")
    return p


def slide10():
    p = Page(10, "Checklist para testar com a turma")
    checks = [
        "☐ aplicação cadastrada no SUAP",
        "☐ callback idêntico ao cadastrado",
        "☐ SUAP_CLIENT_ID e SECRET definidos",
        "☐ servidor rodando em 127.0.0.1:5000",
        "☐ botão redireciona para o SUAP",
        "☐ perfil aparece depois do retorno",
    ]
    y=382
    for i, item in enumerate(checks):
        col = GREEN if i < 4 else BLUE
        p.rect(70, y-8, 28, 28, col, fill=True, radius=6)
        p.text(84, y, "✓", 15, WHITE, bold=True, align="center")
        p.text(120, y+1, item[2:], 16, NAVY)
        y -= 43
    p.rect(580, 180, 290, 220, PALE_GREEN, fill=True, radius=18)
    p.text(725, 360, "Se der erro…", 20, GREEN, bold=True, align="center")
    p.paragraph(620, 320, "Leia a URL, confira o callback, veja o terminal do Flask e procure se code, state e token chegaram na ordem certa.", 29, 13, 20, INK)
    p.text(480, 72, "Pergunta para a turma: em qual passo a senha deixa de estar na nossa aplicação?", 13, BLUE, bold=True, align="center")
    return p


def make_pdf():
    pages = [slide1(), slide2(), slide3(), slide4(), slide5(), slide6(), slide7(), slide8(), slide9(), slide10()]
    objects = []
    def obj(body):
        objects.append(body)
        return len(objects)
    f1 = obj("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>")
    f2 = obj("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>")
    f3 = obj("<< /Type /Font /Subtype /Type1 /BaseFont /Courier /Encoding /WinAnsiEncoding >>")
    page_ids=[]
    for page in pages:
        stream = page.finish().encode("latin-1", "replace")
        sid = obj(f"<< /Length {len(stream)} >>\nstream\n".encode()+stream+b"\nendstream")
        pid = obj(f"<< /Type /Page /Parent 0 0 R /MediaBox [0 0 {W} {H}] /Resources << /Font << /F1 {f1} 0 R /F2 {f2} 0 R /F3 {f3} 0 R >> >> /Contents {sid} 0 R >>")
        page_ids.append(pid)
    kids = " ".join(f"{i} 0 R" for i in page_ids)
    pages_id = obj(f"<< /Type /Pages /Kids [{kids}] /Count {len(page_ids)} >>")
    # Patch parent references now that Pages object exists.
    for pid in page_ids:
        body = objects[pid-1].replace("/Parent 0 0 R", f"/Parent {pages_id} 0 R")
        objects[pid-1] = body
    catalog_id = obj(f"<< /Type /Catalog /Pages {pages_id} 0 R >>")
    out = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets=[0]
    for i, body in enumerate(objects, 1):
        offsets.append(len(out)); out += f"{i} 0 obj\n".encode()
        out += body if isinstance(body, bytes) else body.encode("latin-1")
        out += b"\nendobj\n"
    xref=len(out); out += f"xref\n0 {len(objects)+1}\n0000000000 65535 f \n".encode()
    for off in offsets[1:]: out += f"{off:010d} 00000 n \n".encode()
    out += f"trailer\n<< /Size {len(objects)+1} /Root {catalog_id} 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes(out)
    print(OUT)


if __name__ == "__main__":
    make_pdf()
