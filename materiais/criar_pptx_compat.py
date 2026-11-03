import sys
from pathlib import Path

sys.path.insert(0, "/tmp/python_pptx_lib")
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Inches, Pt


OUT = Path(__file__).with_name("conexao-suap-editavel.pptx")
IMG_LOGIN = Path(__file__).with_name("suap-aluno-login.png")
IMG_FLOW = Path(__file__).with_name("suap-fluxo-referencia.png")
IMG_TOKEN = Path(__file__).with_name("suap-code-token.png")

NAVY = RGBColor(13, 31, 60)
BLUE = RGBColor(31, 111, 235)
GREEN = RGBColor(29, 155, 89)
ORANGE = RGBColor(240, 162, 26)
RED = RGBColor(199, 58, 66)
PALE_BLUE = RGBColor(227, 240, 255)
PALE_GREEN = RGBColor(229, 247, 236)
PALE_YELLOW = RGBColor(255, 245, 215)
PALE_RED = RGBColor(255, 229, 231)
INK = RGBColor(25, 35, 51)
MUTED = RGBColor(89, 101, 121)
WHITE = RGBColor(255, 255, 255)


def set_text(shape, text, size=18, color=INK, bold=False, align=PP_ALIGN.LEFT):
    tf = shape.text_frame
    tf.clear()
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    for i, line in enumerate(text.split("\n")):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = line
        p.alignment = align
        p.space_after = Pt(3)
        for r in p.runs:
            r.font.name = "Aptos"
            r.font.size = Pt(size)
            r.font.bold = bold
            r.font.color.rgb = color


def box(slide, x, y, w, h, fill, text="", size=18, color=INK, bold=False, align=PP_ALIGN.LEFT):
    sh = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    sh.fill.solid(); sh.fill.fore_color.rgb = fill
    sh.line.color.rgb = fill
    sh.text_frame.margin_left = Inches(0.16)
    sh.text_frame.margin_right = Inches(0.16)
    sh.text_frame.margin_top = Inches(0.08)
    sh.text_frame.margin_bottom = Inches(0.08)
    if text: set_text(sh, text, size, color, bold, align)
    return sh


def text(slide, x, y, w, h, value, size=18, color=INK, bold=False, align=PP_ALIGN.LEFT):
    sh = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    set_text(sh, value, size, color, bold, align)
    return sh


def arrow(slide, x1, y1, x2, y2, color=BLUE):
    ln = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
    ln.line.color.rgb = color
    ln.line.width = Pt(2.5)
    ln.line.end_arrowhead = True
    return ln


def code_box(slide, x, y, w, h, label, code):
    """Small editable code card for classroom examples."""
    sh = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    sh.fill.solid(); sh.fill.fore_color.rgb = NAVY
    sh.line.color.rgb = NAVY
    tf = sh.text_frame
    tf.clear(); tf.word_wrap = True
    tf.margin_left = Inches(0.16); tf.margin_right = Inches(0.12)
    tf.margin_top = Inches(0.08); tf.margin_bottom = Inches(0.05)
    p = tf.paragraphs[0]
    p.text = label.upper()
    for r in p.runs:
        r.font.name = "Aptos"; r.font.size = Pt(8); r.font.bold = True; r.font.color.rgb = RGBColor(126, 211, 255)
    for line in code.split("\n"):
        p = tf.add_paragraph(); p.text = line; p.space_after = Pt(0)
        for r in p.runs:
            r.font.name = "Courier New"; r.font.size = Pt(10.5); r.font.color.rgb = WHITE
    return sh


def header(slide, title, n):
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(0.11))
    bar.fill.solid(); bar.fill.fore_color.rgb = NAVY; bar.line.fill.background()
    text(slide, 0.48, 0.22, 2.4, 0.25, "GUIA DE INTEGRAÇÃO", 9, BLUE, True)
    text(slide, 0.48, 0.58, 12.0, 0.52, title, 25, NAVY, True)
    text(slide, 12.2, 7.18, 0.55, 0.18, f"{n:02d}/20", 9, MUTED, True, PP_ALIGN.RIGHT)


def add_standard_slide(prs, n, title, kicker, left_title, left_body, right_title, right_body, accent=BLUE):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    header(slide, title, n)
    text(slide, 0.50, 1.18, 12.2, 0.30, kicker, 12, accent, True)
    box(slide, 0.58, 1.65, 5.75, 3.65, PALE_BLUE, f"{left_title}\n\n{left_body}", 17, INK, False)
    box(slide, 7.00, 1.65, 5.75, 3.65, PALE_GREEN, f"{right_title}\n\n{right_body}", 17, INK, False)
    arrow(slide, 6.42, 3.85, 6.90, 3.85, accent)
    if title.startswith("Passo 9"):
        slide.shapes.add_picture(str(IMG_TOKEN), Inches(2.75), Inches(5.45), width=Inches(7.8), height=Inches(1.45))
    elif title.startswith("Passo 17"):
        code_box(slide, 0.70, 5.55, 12.00, 1.08, "pesquisa — OAuth 2.0 Security BCP", "PKCE: code_challenge + code_verifier\nEste branch já valida state; PKCE é uma melhoria para a próxima etapa.")
        text(slide, 0.80, 6.70, 11.8, 0.22, "Base: RFC 6749 (Authorization Code) e RFC 9700 (boas práticas de segurança).", 8, MUTED, False, PP_ALIGN.CENTER)
    elif title.startswith("Passo 18"):
        code_box(slide, 0.70, 5.55, 12.00, 1.08, "desafio de leitura", "navegador → SUAP → code → token → API → perfil")
    elif title.startswith("Passo 2"):
        code_box(slide, 0.70, 5.55, 12.00, 1.08, "README.md — configuração", "export SUAP_CLIENT_ID=seu_client_id\nexport SUAP_CLIENT_SECRET=seu_client_secret")
    elif title.startswith("Passo 3"):
        code_box(slide, 0.70, 5.55, 12.00, 1.08, "login.html — botão", "<a href=\"{{ url_for('login_suap') }}\">\n  Entrar com SUAP\n</a>")
    elif title.startswith("Passo 4"):
        code_box(slide, 0.70, 5.55, 12.00, 1.08, "routes.py — início", "state = token_urlsafe(32)\nredirect_uri = request.host_url.rstrip('/') + url_for('suap_callback')")
    elif title.startswith("Passo 7"):
        code_box(slide, 0.70, 5.55, 12.00, 1.08, "callback — dados recebidos", "code = request.args.get('code')\nstate = request.args.get('state', '')")
    elif title.startswith("Passo 8"):
        code_box(slide, 0.70, 5.55, 12.00, 1.08, "routes.py — proteção", "state = session.pop('suap_oauth_state', None)\nif state != request.args.get('state', ''): return redirect(...) ")
    elif title.startswith("Passo 10"):
        code_box(slide, 0.70, 5.55, 12.00, 1.08, "routes.py — sessão", "session['suap_access_token'] = tokens['access_token']\n# token fica no servidor, não no HTML")
    elif title.startswith("Passo 11"):
        code_box(slide, 0.70, 5.55, 12.00, 1.08, "SuapAuthenticationService.py — API", "headers = {'Authorization': f'Bearer {access_token}'}\nGET /api/rh/meus-dados/")
    elif title.startswith("Passo 13"):
        code_box(slide, 0.70, 5.55, 12.00, 1.08, "routes.py — perfil", "dados = SuapAuthenticationService.meus_dados(access_token)\nAuthenticationService.login_suap(dados)")
    elif title.startswith("Passo 14"):
        code_box(slide, 0.70, 5.55, 12.00, 1.08, "separação de responsabilidades", "routes.py  →  coordena o fluxo\nSuapAuthenticationService.py  →  conversa com o SUAP")
    else:
        # A compact visual memory aid: three roles in the flow.
        box(slide, 1.50, 5.72, 2.55, 0.62, PALE_YELLOW, "ALUNO", 16, NAVY, True, PP_ALIGN.CENTER)
        box(slide, 5.40, 5.72, 2.55, 0.62, PALE_BLUE, "APLICAÇÃO", 16, NAVY, True, PP_ALIGN.CENTER)
        box(slide, 9.30, 5.72, 2.55, 0.62, PALE_GREEN, "SUAP / API", 16, NAVY, True, PP_ALIGN.CENTER)
        arrow(slide, 4.12, 6.03, 5.30, 6.03, accent)
        arrow(slide, 8.02, 6.03, 9.20, 6.03, accent)
    return slide


def make_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    # Remove the default slide; we add all slides explicitly.
    while prs.slides._sldIdLst:
        rId = prs.slides._sldIdLst[0].rId
        prs.part.drop_rel(rId)
        del prs.slides._sldIdLst[0]

    slide = prs.slides.add_slide(prs.slide_layouts[6])
    header(slide, "Conectando uma aplicação Flask ao SUAP", 1)
    text(slide, 0.55, 1.32, 5.6, 0.40, "Passo a passo visual de OAuth 2.0 para a turma", 17, BLUE, True)
    text(slide, 0.60, 2.00, 5.3, 1.10, "A ideia central:\nA aplicação não recebe a senha do aluno.", 23, NAVY, True)
    text(slide, 0.60, 3.30, 5.2, 0.80, "Ela recebe uma autorização temporária e consulta os dados permitidos.", 17, MUTED, False)
    slide.shapes.add_picture(str(IMG_LOGIN), Inches(6.30), Inches(1.20), width=Inches(6.45))
    box(slide, 0.70, 5.15, 3.55, 0.82, PALE_BLUE, "1  APLICAÇÃO\nBotão de login", 16, NAVY, True, PP_ALIGN.CENTER)
    box(slide, 4.88, 5.15, 3.55, 0.82, PALE_GREEN, "2  SUAP\nAutoriza", 16, NAVY, True, PP_ALIGN.CENTER)
    box(slide, 9.06, 5.15, 3.55, 0.82, PALE_YELLOW, "3  PERFIL\nDados", 16, NAVY, True, PP_ALIGN.CENTER)
    arrow(slide, 4.30, 5.56, 4.80, 5.56, BLUE); arrow(slide, 8.48, 5.56, 8.98, 5.56, GREEN)

    overview = prs.slides.add_slide(prs.slide_layouts[6])
    header(overview, "Visão geral — veja a história inteira primeiro", 2)
    text(overview, 0.55, 1.18, 12.2, 0.30, "Depois vamos desmontar este fluxo em etapas menores.", 12, BLUE, True)
    overview.shapes.add_picture(str(IMG_FLOW), Inches(0.55), Inches(1.65), width=Inches(12.25))
    box(overview, 2.0, 6.25, 9.35, 0.55, PALE_GREEN, "Clique → autorize → volte → troque code por token → consulte o perfil", 15, GREEN, True, PP_ALIGN.CENTER)

    slides = [
        ("Passo 1 — cadastrar a aplicação", "O SUAP precisa conhecer o projeto antes do código funcionar.", "SUAP / painel de aplicações", "Nome: Projeto INFO3M\nTipo: OAuth2 / Authorization Code", "Callback cadastrado", "http://127.0.0.1:5000/suap/callback\n\nA URL deve ser idêntica nos dois lugares.", GREEN),
        ("Passo 2 — guardar as credenciais", "Credenciais ficam em variáveis de ambiente, fora do GitHub.", "CLIENT_ID", "export SUAP_CLIENT_ID=seu_client_id\n\nIdentifica a aplicação.", "CLIENT_SECRET", "export SUAP_CLIENT_SECRET=seu_client_secret\n\nÉ segredo: não compartilhe.", BLUE),
        ("Passo 3 — colocar o botão na tela", "O botão chama a rota /login-suap.", "Na tela", "Entrar com SUAP\n\nO aluno clica e sai da aplicação.", "No código", "<a href=/login-suap>\n  Entrar com SUAP\n</a>", BLUE),
        ("Passo 4 — iniciar o fluxo", "A rota monta a URL de autorização e redireciona o navegador.", "/login-suap", "1. cria state\n2. monta redirect_uri\n3. redireciona ao SUAP", "Serviço", "authorization_url(state, redirect_uri)\n\nSuapAuthenticationService", BLUE),
        ("Passo 5 — gerar o state", "State é uma etiqueta aleatória para conferir a resposta depois.", "Antes de sair", "state = 8fJ2...xP9\n\nGuarda na sessão.", "Quando voltar", "state enviado = state recebido\n\nSe não bater: interromper.", ORANGE),
        ("Passo 6 — o aluno autoriza", "A senha é digitada no SUAP, não na nossa aplicação.", "SUAP", "Aluno informa usuário e senha\n\nO SUAP confirma a identidade.", "Ação", "Autorizar\n\nDepois, o navegador volta.", GREEN),
        ("Passo 7 — receber o callback", "O navegador volta para a rota cadastrada.", "URL de retorno", "/suap/callback?code=ABC123&state=8fJ2...xP9", "A aplicação recebe", "code = autorização de uso único\nstate = etiqueta de segurança", BLUE),
        ("Passo 8 — validar o state", "Antes de usar o code, compare o state.", "Se for igual", "A resposta parece ser do fluxo que iniciamos.", "Se for diferente", "Mostre erro e volte ao login.\n\nNão prossiga.", ORANGE),
        ("Passo 9 — trocar o code por token", "O servidor troca o code usando também o client_secret.", "Pedido ao SUAP", "POST /o/token/\n\ncode + client_id + client_secret", "Resposta", "access_token\n\nUm crachá temporário para a API.", GREEN),
        ("Passo 10 — guardar o token", "O token fica associado à sessão do usuário.", "No Flask", "session['suap_access_token'] = token", "Cuidado", "Não imprimir no terminal.\nNão colocar no HTML.\nNão enviar ao GitHub.", RED),
        ("Passo 11 — chamar a API", "Com o token, a aplicação consulta os dados autorizados.", "Endpoint", "GET https://suap.ifrn.edu.br/api/rh/meus-dados/", "Cabeçalho", "Authorization: Bearer <access_token>\n\nO token vai no servidor.", BLUE),
        ("Passo 12 — receber o JSON", "A API responde com dados estruturados.", "Resposta", "{ nome, matrícula, email, vínculo }", "Ideia", "JSON é texto organizado\nque o Flask consegue ler.", GREEN),
        ("Passo 13 — mostrar o perfil", "A aplicação usa o JSON para montar uma tela.", "Dados", "nome\nmatrícula\ne-mail\ntipo de vínculo", "Tela", "Olá, Ana!\n\nPerfil SUAP\nMatrícula: 20260001", GREEN),
        ("Passo 14 — routes.py + serviço", "As rotas coordenam; o serviço conversa com o SUAP.", "routes.py", "/login-suap\n/suap/callback\n/suap/meus_dados", "SuapAuthenticationService", "authorization_url()\nexchange_code()\nmeus_dados()", BLUE),
        ("Passo 15 — tratar erros", "Todo fluxo externo pode falhar.", "Exemplos", "state inválido\ncode ausente\nsem access_token", "Boa resposta", "Mensagem clara + retorno ao login\n+ nada de segredo exposto.", RED),
        ("Passo 16 — testar o fluxo", "Teste cada etapa, sem pular direto para o final.", "Checklist", "1 servidor rodando\n2 callback correto\n3 botão abre o SUAP\n4 aluno autoriza", "Resultado esperado", "5 retorno funciona\n6 perfil aparece\n7 erros são compreensíveis", BLUE),
        ("Passo 17 — segurança em linguagem simples", "Token é uma chave: trate como informação sensível.", "Faça", "Use HTTPS em produção\nValide o state\nProteja o secret", "Evite", "Senha na sua aplicação\nToken no GitHub\nToken na tela", GREEN),
        ("Passo 18 — desafio final", "Explique o fluxo com cinco cartões e cinco setas.", "Pergunta para a turma", "Em qual etapa a senha deixa de estar na nossa aplicação?", "Resposta esperada", "Assim que o aluno é redirecionado para o SUAP.\n\nA aplicação trabalha com token.", ORANGE),
    ]
    # The service layer is explained alongside routes.py to keep the narrative
    # at exactly 20 slides while preserving the complete flow.
    for n, data in enumerate(slides, 3):
        add_standard_slide(prs, n, *data)
    prs.save(OUT)
    print(OUT)


if __name__ == "__main__":
    make_deck()
