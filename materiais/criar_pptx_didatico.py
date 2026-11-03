import sys
from pathlib import Path

sys.path.insert(0, "/tmp/python_pptx_lib")
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Inches, Pt

ROOT = Path(__file__).parent
OUT = ROOT / "conexao-suap-editavel.pptx"
IMG_LOGIN = ROOT / "suap-aluno-login.png"
IMG_FLOW = ROOT / "suap-fluxo-referencia.png"
IMG_TOKEN = ROOT / "suap-code-token.png"

W, H = 13.333, 7.5
INK = RGBColor(25, 33, 48)
MUTED = RGBColor(92, 106, 128)
WHITE = RGBColor(255, 255, 255)
BG = RGBColor(248, 250, 253)
BLUE = RGBColor(47, 112, 224)
BLUE_LIGHT = RGBColor(229, 239, 255)
TEAL = RGBColor(0, 157, 150)
TEAL_LIGHT = RGBColor(224, 248, 245)
YELLOW = RGBColor(248, 184, 52)
YELLOW_LIGHT = RGBColor(255, 246, 220)
CORAL = RGBColor(226, 91, 87)
CORAL_LIGHT = RGBColor(255, 234, 233)
PURPLE = RGBColor(106, 78, 176)
NAVY = RGBColor(22, 39, 70)
CODE_BG = RGBColor(30, 40, 58)


def fmt(tf, size=18, color=INK, bold=False, font="Aptos", align=PP_ALIGN.LEFT):
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    for p in tf.paragraphs:
        p.alignment = align
        p.space_after = Pt(2)
        for r in p.runs:
            r.font.name = font
            r.font.size = Pt(size)
            r.font.bold = bold
            r.font.color.rgb = color


def text(slide, x, y, w, h, value, size=18, color=INK, bold=False, align=PP_ALIGN.LEFT, font="Aptos"):
    sh = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    sh.text_frame.clear(); sh.text_frame.text = value
    fmt(sh.text_frame, size, color, bold, font, align)
    return sh


def shape(slide, kind, x, y, w, h, fill, line=None, radius=False):
    sh = slide.shapes.add_shape(kind, Inches(x), Inches(y), Inches(w), Inches(h))
    sh.fill.solid(); sh.fill.fore_color.rgb = fill
    sh.line.color.rgb = line or fill
    return sh


def card(slide, x, y, w, h, title, body, fill=WHITE, accent=BLUE, body_size=16):
    sh = shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h, fill, fill)
    sh.text_frame.clear(); sh.text_frame.margin_left = Inches(.20); sh.text_frame.margin_right = Inches(.16)
    sh.text_frame.margin_top = Inches(.12); sh.text_frame.margin_bottom = Inches(.08)
    p = sh.text_frame.paragraphs[0]; p.text = title
    for r in p.runs:
        r.font.name="Aptos Display"; r.font.size=Pt(16); r.font.bold=True; r.font.color.rgb=accent
    for line in body.split("\n"):
        p=sh.text_frame.add_paragraph(); p.text=line; p.space_after=Pt(3)
        for r in p.runs:
            r.font.name="Aptos"; r.font.size=Pt(body_size); r.font.color.rgb=INK
    return sh


def code(slide, x, y, w, h, label, snippet):
    sh = shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h, CODE_BG, CODE_BG)
    tf=sh.text_frame; tf.clear(); tf.margin_left=Inches(.18); tf.margin_right=Inches(.12); tf.margin_top=Inches(.09)
    p=tf.paragraphs[0]; p.text=label.upper()
    for r in p.runs: r.font.name="Aptos"; r.font.size=Pt(8); r.font.bold=True; r.font.color.rgb=RGBColor(132, 220, 214)
    for line in snippet.split("\n"):
        p=tf.add_paragraph(); p.text=line; p.space_after=Pt(0)
        for r in p.runs: r.font.name="Courier New"; r.font.size=Pt(10.5); r.font.color.rgb=WHITE
    return sh


def line(slide, x1, y1, x2, y2, color=BLUE, width=2.5, arrow=True):
    ln=slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
    ln.line.color.rgb=color; ln.line.width=Pt(width)
    if arrow: ln.line.end_arrowhead=True
    return ln


def circle(slide, x, y, d, label, fill=BLUE, size=20):
    sh=shape(slide, MSO_SHAPE.OVAL, x, y, d, d, fill, fill)
    sh.text_frame.text=label; fmt(sh.text_frame, size, WHITE, True, "Aptos Display", PP_ALIGN.CENTER)
    return sh


def header(slide, n, title, eyebrow="CONEXÃO COM O SUAP"):
    slide.background.fill.solid(); slide.background.fill.fore_color.rgb=BG
    shape(slide, MSO_SHAPE.RECTANGLE, 0, 0, W, .10, NAVY, NAVY)
    text(slide, .55, .27, 5.0, .22, eyebrow, 9, BLUE, True)
    text(slide, .55, .58, 11.7, .52, title, 27, NAVY, True, font="Aptos Display")
    text(slide, 12.15, .34, .65, .22, f"{n:02d}/20", 9, MUTED, True, PP_ALIGN.RIGHT)


def add_slide(prs, n, title, eyebrow="CONEXÃO COM O SUAP"):
    s=prs.slides.add_slide(prs.slide_layouts[6]); header(s,n,title,eyebrow); return s


def person(slide, x, y, label, fill=YELLOW):
    circle(slide,x+.36,y,.50,"",fill)
    shape(slide,MSO_SHAPE.ROUNDED_RECTANGLE,x,y+.52,1.22,.75,fill,fill)
    text(slide,x-.10,y+1.35,1.45,.30,label,13,NAVY,True,PP_ALIGN.CENTER)


def server(slide, x, y, label, fill=TEAL):
    for i in range(3):
        shape(slide,MSO_SHAPE.ROUNDED_RECTANGLE,x,y+i*.42,1.85,.31,fill,fill)
        circle(slide,x+.12,y+.10+i*.42,.10,"",WHITE,8)
        circle(slide,x+.32,y+.10+i*.42,.10,"",WHITE,8)
    text(slide,x-.15,y+1.35,2.15,.30,label,13,NAVY,True,PP_ALIGN.CENTER)


def build():
    prs=Presentation(); prs.slide_width=Inches(W); prs.slide_height=Inches(H)
    while prs.slides._sldIdLst:
        rid=prs.slides._sldIdLst[0].rId; prs.part.drop_rel(rid); del prs.slides._sldIdLst[0]

    # 1 — cover
    s=add_slide(prs,1,"Como uma aplicação conversa com o SUAP","GUIA VISUAL • FLASK + OAUTH 2.0")
    text(s,.65,1.55,5.3,1.05,"Do clique no botão\naté o perfil do aluno",30,NAVY,True,font="Aptos Display")
    text(s,.68,3.00,4.8,.62,"Uma história em 18 passos, com código real do projeto.",17,MUTED)
    s.shapes.add_picture(str(IMG_LOGIN), Inches(6.0), Inches(1.15), width=Inches(6.7))
    card(s,.7,5.25,3.35,.82,"ALUNO","clica no botão",YELLOW_LIGHT,YELLOW,15)
    card(s,4.98,5.25,3.35,.82,"APLICAÇÃO","organiza o fluxo",BLUE_LIGHT,BLUE,15)
    card(s,9.25,5.25,3.35,.82,"SUAP","autoriza e responde",TEAL_LIGHT,TEAL,15)

    # 2 — objectives
    s=add_slide(prs,2,"O que vamos aprender?","ANTES DE CODAR")
    text(s,.7,1.35,11.5,.55,"Ao final, você conseguirá explicar o caminho completo.",21,NAVY,True)
    card(s,.7,2.25,3.75,2.35,"1 • IDENTIDADE","Como o SUAP sabe qual aplicação está pedindo acesso?",BLUE_LIGHT,BLUE,18)
    card(s,4.78,2.25,3.75,2.35,"2 • CAMINHO","Como o aluno sai e volta para a aplicação?",YELLOW_LIGHT,YELLOW,18)
    card(s,8.86,2.25,3.75,2.35,"3 • DADOS","Como o perfil chega à tela sem passar senha?",TEAL_LIGHT,TEAL,18)
    text(s,.8,5.45,11.8,.55,"Regra da aula: primeiro entendemos a história; depois lemos o código.",17,MUTED,False,PP_ALIGN.CENTER)

    # 3 — big idea
    s=add_slide(prs,3,"A ideia mais importante","COMECE POR AQUI")
    text(s,.72,1.35,5.0,.50,"A senha fica no SUAP.",26,CORAL,True,font="Aptos Display")
    text(s,.72,1.95,4.7,.72,"A aplicação recebe uma autorização temporária — o token.",18,INK)
    person(s,1.05,3.35,"ALUNO")
    server(s,9.95,3.35,"SUAP",TEAL)
    card(s,5.0,3.45,3.25,1.15,"O que viaja?","code → token",BLUE_LIGHT,BLUE,20)
    line(s,2.55,4.05,4.8,4.05,YELLOW); line(s,8.35,4.05,9.7,4.05,TEAL)
    text(s,4.8,5.35,3.6,.45,"Nunca: aluno → senha → nossa aplicação",15,CORAL,True,PP_ALIGN.CENTER)

    # 4 — map
    s=add_slide(prs,4,"O mapa da viagem","VISÃO GERAL")
    text(s,.7,1.30,11.8,.40,"Guarde estes cinco cartões. Eles voltam durante toda a aula.",17,MUTED)
    steps=[("1","Clique",YELLOW), ("2","Autorize",TEAL), ("3","Volte com code",BLUE), ("4","Troque por token",PURPLE), ("5","Consulte API",CORAL)]
    xs=[.65,3.15,5.65,8.15,10.65]
    for i,(num,lab,col) in enumerate(steps):
        circle(s,xs[i],2.35,.62,num,col,18); text(s,xs[i]-0.25,3.12,1.15,.35,lab,14,NAVY,True,PP_ALIGN.CENTER)
        if i<4: line(s,xs[i]+.75,2.66,xs[i+1]-.15,2.66,MUTED,1.8)
    s.shapes.add_picture(str(IMG_FLOW), Inches(.75), Inches(4.15), width=Inches(11.85), height=Inches(1.95))

    # 5 — register
    s=add_slide(prs,5,"Passo 1 — cadastrar a aplicação","PREPARAÇÃO")
    circle(s,.75,1.45,.70,"1",BLUE,22); text(s,1.65,1.48,4.2,.45,"O SUAP precisa reconhecer o projeto.",23,NAVY,True)
    card(s,.75,2.55,5.2,2.25,"NO PAINEL DO SUAP","Nome: Projeto INFO3M\nTipo: Authorization Code\nCallback: /suap/callback",WHITE,BLUE,18)
    card(s,6.55,2.55,5.95,2.25,"POR QUE ISSO IMPORTA?","O SUAP só devolve respostas para uma URL previamente cadastrada.",BLUE_LIGHT,BLUE,20)
    text(s,.85,5.55,11.8,.52,"A callback precisa ser exatamente igual nos dois lugares.",18,CORAL,True,PP_ALIGN.CENTER)

    # 6 — env
    s=add_slide(prs,6,"Passo 2 — guardar as credenciais","CONFIGURAÇÃO")
    circle(s,.75,1.45,.70,"2",BLUE,22); text(s,1.65,1.48,5.2,.45,"Identificador não é a mesma coisa que segredo.",23,NAVY,True)
    code(s,.75,2.35,6.0,1.85,"README.md", "export SUAP_CLIENT_ID=seu_client_id\nexport SUAP_CLIENT_SECRET=seu_client_secret")
    card(s,7.15,2.35,5.35,1.85,"PENSE ASSIM","CLIENT_ID = crachá\nCLIENT_SECRET = senha do servidor",YELLOW_LIGHT,YELLOW,20)
    text(s,.85,5.05,11.7,.55,"Nunca coloque o CLIENT_SECRET no GitHub ou em um slide com valor real.",18,CORAL,True,PP_ALIGN.CENTER)

    # 7 — button
    s=add_slide(prs,7,"Passo 3 — criar o botão","NA TELA DO ALUNO")
    circle(s,.75,1.45,.70,"3",BLUE,22); text(s,1.65,1.48,5.4,.45,"O clique chama uma rota Flask.",23,NAVY,True)
    code(s,.75,2.30,6.1,2.0,"login.html", "<a href=\"{{ url_for('login_suap') }}\">\n  Entrar com SUAP\n</a>")
    card(s,7.20,2.30,5.25,2.0,"O NAVEGADOR FAZ","1. aluno clica\n2. abre /login-suap\n3. Flask prepara a viagem",BLUE_LIGHT,BLUE,18)
    line(s,3.8,4.8,9.5,4.8,BLUE,2.5)
    text(s,4.5,5.05,4.4,.35,"clique → rota → SUAP",16,BLUE,True,PP_ALIGN.CENTER)

    # 8 — start
    s=add_slide(prs,8,"Passo 4 — iniciar o fluxo","ROUTES.PY")
    circle(s,.75,1.45,.70,"4",BLUE,22); text(s,1.65,1.48,6.0,.45,"A rota prepara duas coisas: state e callback.",23,NAVY,True)
    code(s,.75,2.25,7.15,2.15,"/login-suap", "state = token_urlsafe(32)\nredirect_uri = request.host_url.rstrip('/') + url_for('suap_callback')\nsession['suap_oauth_state'] = state")
    card(s,8.25,2.25,4.15,2.15,"TRADUÇÃO","state = etiqueta\nredirect_uri = endereço de volta\nsession = memória da sessão",TEAL_LIGHT,TEAL,17)
    text(s,.85,5.35,11.8,.45,"Depois disso, o navegador é redirecionado para o SUAP.",18,TEAL,True,PP_ALIGN.CENTER)

    # 9 — state
    s=add_slide(prs,9,"Passo 5 — entender o state","A ETIQUETA DE SEGURANÇA")
    circle(s,.75,1.45,.70,"5",BLUE,22); text(s,1.65,1.48,6.5,.45,"É como colocar uma etiqueta na encomenda.",23,NAVY,True)
    card(s,.75,2.35,3.25,1.65,"ANTES","state guardado\nna sessão",YELLOW_LIGHT,YELLOW,20)
    card(s,5.05,2.35,3.25,1.65,"DURANTE","SUAP devolve\no mesmo state",TEAL_LIGHT,TEAL,20)
    card(s,9.35,2.35,3.25,1.65,"DEPOIS","Flask compara\nos dois",BLUE_LIGHT,BLUE,20)
    line(s,4.1,3.18,4.9,3.18,MUTED); line(s,8.4,3.18,9.2,3.18,MUTED)
    text(s,1.0,5.05,11.2,.55,"Se a etiqueta não bater, a aplicação para o fluxo.",20,CORAL,True,PP_ALIGN.CENTER)

    # 10 — authorize
    s=add_slide(prs,10,"Passo 6 — o aluno autoriza","NO SUAP")
    circle(s,.75,1.45,.70,"6",TEAL,22); text(s,1.65,1.48,6.2,.45,"A senha é digitada aqui — no SUAP.",23,NAVY,True)
    person(s,1.25,2.65,"ALUNO")
    card(s,3.15,2.55,3.25,1.85,"1. LOGIN","Usuário e senha\nficam no SUAP.",YELLOW_LIGHT,YELLOW,19)
    card(s,7.05,2.55,3.25,1.85,"2. AUTORIZAR","O aluno permite\no acesso.",TEAL_LIGHT,TEAL,19)
    server(s,10.8,2.55,"SUAP",TEAL)
    line(s,2.65,3.45,3.0,3.45,YELLOW); line(s,6.5,3.45,6.9,3.45,TEAL); line(s,10.3,3.45,10.65,3.45,TEAL)
    text(s,.9,5.3,11.5,.5,"A nossa aplicação nunca vê a senha.",21,CORAL,True,PP_ALIGN.CENTER)

    # 11 — callback
    s=add_slide(prs,11,"Passo 7 — voltar com um code","CALLBACK")
    circle(s,.75,1.45,.70,"7",BLUE,22); text(s,1.65,1.48,6.5,.45,"O SUAP devolve uma autorização curta.",23,NAVY,True)
    card(s,.75,2.3,5.65,1.9,"URL DE RETORNO","/suap/callback?code=ABC123\n&state=8fJ2...xP9",BLUE_LIGHT,BLUE,19)
    card(s,6.75,2.3,5.65,1.9,"O QUE CHEGOU?","code = autorização de uso único\nstate = etiqueta para conferir",TEAL_LIGHT,TEAL,18)
    text(s,.9,5.25,11.5,.5,"O code ainda não é o perfil do aluno.",21,PURPLE,True,PP_ALIGN.CENTER)

    # 12 — validate
    s=add_slide(prs,12,"Passo 8 — conferir antes de continuar","PROTEÇÃO")
    circle(s,.75,1.45,.70,"8",CORAL,22); text(s,1.65,1.48,7.0,.45,"Primeiro: compare o state.",23,NAVY,True)
    code(s,.75,2.25,7.4,1.95,"routes.py — callback", "state = session.pop('suap_oauth_state', None)\nif state != request.args.get('state', ''):\n    return redirect(url_for('login'))")
    card(s,8.55,2.25,3.85,1.95,"PERGUNTA","A etiqueta voltou igual?",YELLOW_LIGHT,YELLOW,20)
    text(s,2.0,5.05,9.2,.55,"SIM → continua        NÃO → interrompe",21,TEAL,True,PP_ALIGN.CENTER)

    # 13 — exchange
    s=add_slide(prs,13,"Passo 9 — trocar code por token","SERVIÇO HTTP")
    circle(s,.75,1.45,.70,"9",PURPLE,22); text(s,1.65,1.48,7.3,.45,"O servidor faz uma troca segura.",23,NAVY,True)
    s.shapes.add_picture(str(IMG_TOKEN), Inches(.75), Inches(2.25), width=Inches(5.65), height=Inches(1.88))
    code(s,6.75,2.25,5.75,1.88,"POST /o/token/", "grant_type = authorization_code\ncode + client_id + client_secret\n→ access_token")
    text(s,.9,5.15,11.5,.5,"code = cupom de troca • token = crachá para a API",19,BLUE,True,PP_ALIGN.CENTER)

    # 14 — session
    s=add_slide(prs,14,"Passo 10 — guardar o token","SESSÃO FLASK")
    circle(s,.75,1.45,.70,"10",BLUE,20); text(s,1.65,1.48,7.5,.45,"Agora a aplicação consegue consultar o SUAP.",23,NAVY,True)
    code(s,.75,2.35,7.15,1.9,"routes.py", "session['suap_access_token'] = tokens['access_token']\n# o token fica no servidor, não no HTML")
    card(s,8.25,2.35,4.1,1.9,"REGRA DE OURO","Token é informação sensível.\nNão imprimir.\nNão publicar.",CORAL_LIGHT,CORAL,18)
    text(s,.9,5.25,11.5,.5,"Senha não. Token sim — e com cuidado.",21,CORAL,True,PP_ALIGN.CENTER)

    # 15 — API
    s=add_slide(prs,15,"Passo 11 — consultar a API","DADOS DO PERFIL")
    circle(s,.75,1.45,.70,"11",TEAL,20); text(s,1.65,1.48,7.2,.45,"O token acompanha o pedido HTTP.",23,NAVY,True)
    code(s,.75,2.25,7.1,2.0,"SuapAuthenticationService.py", "headers = {'Authorization': f'Bearer {access_token}'}\nGET /api/rh/meus-dados/")
    server(s,10.1,2.45,"API DO SUAP",TEAL)
    line(s,7.95,3.35,9.85,3.35,TEAL)
    text(s,1.0,5.25,11.2,.5,"Bearer significa: “quem tem este token pode pedir dados permitidos”.",17,MUTED,False,PP_ALIGN.CENTER)

    # 16 — JSON/profile
    s=add_slide(prs,16,"Passo 12 — transformar JSON em tela","RESULTADO")
    circle(s,.75,1.45,.70,"12",TEAL,20); text(s,1.65,1.48,7.0,.45,"A API responde; o Flask organiza.",23,NAVY,True)
    code(s,.75,2.25,5.3,2.0,"resposta da API", '{"nome_usual": "Ana",\n "matricula": "20260001"}')
    card(s,6.55,2.25,2.55,2.0,"FLASK","dados.get(...)\n→ template",BLUE_LIGHT,BLUE,18)
    card(s,9.55,2.25,2.75,2.0,"TELA","Olá, Ana!\nMatrícula: 20260001",TEAL_LIGHT,TEAL,18)
    line(s,6.15,3.25,6.45,3.25,BLUE); line(s,9.2,3.25,9.45,3.25,TEAL)

    # 17 — architecture
    s=add_slide(prs,17,"Passo 13 — quem faz o quê?","ORGANIZAÇÃO DO CÓDIGO")
    circle(s,.75,1.45,.70,"13",PURPLE,20); text(s,1.65,1.48,7.2,.45,"Separar responsabilidades deixa o projeto mais fácil de entender.",21,NAVY,True)
    card(s,.75,2.35,3.55,2.0,"routes.py","coordena\nrecebe requisição\nchama serviço\nrenderiza tela",BLUE_LIGHT,BLUE,17)
    card(s,4.9,2.35,3.55,2.0,"SuapAuthenticationService.py","monta URL\ntroca code\nconsulta API",TEAL_LIGHT,TEAL,17)
    card(s,9.05,2.35,3.55,2.0,"templates","mostra\nos dados\nao aluno",YELLOW_LIGHT,YELLOW,17)
    line(s,4.35,3.35,4.75,3.35,BLUE); line(s,8.5,3.35,8.9,3.35,TEAL)
    text(s,.9,5.25,11.5,.5,"Uma função, uma responsabilidade.",21,PURPLE,True,PP_ALIGN.CENTER)

    # 18 — errors
    s=add_slide(prs,18,"Passo 14 — testar e tratar erros","CHECKLIST")
    circle(s,.75,1.45,.70,"14",CORAL,20); text(s,1.65,1.48,7.2,.45,"Um bom programa também sabe dizer “não deu certo”.",21,NAVY,True)
    card(s,.75,2.3,3.5,2.0,"TESTE 1","callback errado\n→ não conecta",CORAL_LIGHT,CORAL,18)
    card(s,4.9,2.3,3.5,2.0,"TESTE 2","state diferente\n→ interrompe",YELLOW_LIGHT,YELLOW,18)
    card(s,9.05,2.3,3.5,2.0,"TESTE 3","API sem resposta\n→ mensagem clara",BLUE_LIGHT,BLUE,18)
    text(s,.9,5.25,11.5,.5,"Não mostre segredos no erro. Mostre o próximo passo.",20,CORAL,True,PP_ALIGN.CENTER)

    # 19 — security/research
    s=add_slide(prs,19,"Passo 15 — segurança: o que a pesquisa recomenda","PESQUISA + CÓDIGO")
    circle(s,.75,1.45,.70,"15",CORAL,20); text(s,1.65,1.48,7.5,.45,"O branch já usa state. A próxima melhoria é PKCE.",21,NAVY,True)
    card(s,.75,2.3,5.25,2.0,"JÁ EXISTE NO BRANCH","state aleatório\ncallback validado\nclient_secret no servidor",TEAL_LIGHT,TEAL,18)
    card(s,6.55,2.3,5.75,2.0,"RECOMENDAÇÃO ATUAL","PKCE adiciona:\ncode_challenge + code_verifier",YELLOW_LIGHT,YELLOW,18)
    code(s,.75,4.85,11.55,1.05,"ideia do PKCE", "autorização: code_challenge   |   token: code_verifier")
    text(s,.8,6.18,11.7,.25,"Base: RFC 6749 e RFC 9700 — boas práticas atuais de OAuth 2.0.",8,MUTED,False,PP_ALIGN.CENTER)

    # 20 — recap/challenge
    s=add_slide(prs,20,"Desafio final: conte a história","FECHAMENTO")
    text(s,.7,1.35,11.8,.55,"Explique o fluxo usando estas cinco palavras:",23,NAVY,True,PP_ALIGN.CENTER)
    words=[("clique",YELLOW),("autorize",TEAL),("code",BLUE),("token",PURPLE),("perfil",CORAL)]
    for i,(word,col) in enumerate(words):
        x=.75+i*2.52; circle(s,x,2.45,.75,str(i+1),col,20); text(s,x-.25,3.38,1.25,.35,word,18,NAVY,True,PP_ALIGN.CENTER)
        if i<4: line(s,x+.9,2.82,x+2.32,2.82,MUTED,2)
    card(s,1.25,4.45,10.85,1.05,"PERGUNTA","Em qual momento a senha deixa de estar na nossa aplicação?",BLUE_LIGHT,BLUE,21)
    text(s,.9,6.15,11.5,.35,"Resposta: ela fica no SUAP; nossa aplicação trabalha com code e token.",15,TEAL,True,PP_ALIGN.CENTER)

    prs.save(OUT)
    print(OUT)


if __name__ == "__main__":
    build()
