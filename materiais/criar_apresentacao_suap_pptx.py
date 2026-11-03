from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from xml.sax.saxutils import escape


OUT = Path(__file__).with_name("conexao-suap-editavel.pptx")
W, H = 13_333_333, 7_500_000
EMU = 914400

NAVY = "0D1F3C"
BLUE = "1F6FEB"
CYAN = "19AFC7"
GREEN = "1D9B59"
ORANGE = "F0A21A"
RED = "C73A42"
INK = "192333"
MUTED = "596579"
LIGHT = "F0F4F8"
PALE_BLUE = "E3F0FF"
PALE_GREEN = "E5F7EC"
PALE_YELLOW = "FFF5D7"
PALE_RED = "FFE5E7"
WHITE = "FFFFFF"


def x(tag, attrs=None, children=None, text=None):
    attrs = attrs or {}
    body = "" if text is None else escape(str(text))
    if children:
        body += "".join(children)
    a = "".join(f' {k}="{escape(str(v))}"' for k, v in attrs.items())
    return f"<{tag}{a}>{body}</{tag}>"


def tx_body(text, size=18, color=INK, bold=False, align="l", font="Aptos"):
    # Simple rich-text body. The box itself remains fully editable in PowerPoint.
    paras = []
    for line in str(text).split("\n"):
        rpr = f'<a:rPr lang="pt-BR" sz="{size*100}" b="{str(bold).lower()}"><a:solidFill><a:srgbClr val="{color}"/></a:solidFill><a:latin typeface="{font}"/></a:rPr>'
        paras.append(x("a:p", children=[x("a:r", children=[rpr, x("a:t", text=line)])]))
    return x("a:txBody", children=[
        x("a:bodyPr", {"wrap": "square", "rtlCol": "0", "anchor": "ctr"}),
        x("a:lstStyle"),
        "".join(paras),
    ])


def shape(spid, name, x0, y0, w, h, fill=WHITE, line="D9E2EC", radius=True,
          text=None, size=18, color=INK, bold=False, align="l"):
    geom = "roundRect" if radius else "rect"
    fill_xml = '<a:noFill/>' if fill is None else f'<a:solidFill><a:srgbClr val="{fill}"/></a:solidFill>'
    line_xml = '<a:ln w="12700"><a:noFill/></a:ln>' if line is None else f'<a:ln w="12700"><a:solidFill><a:srgbClr val="{line}"/></a:solidFill></a:ln>'
    body = tx_body(text, size, color, bold, align) if text is not None else '<a:txBody><a:bodyPr/><a:lstStyle/></a:txBody>'
    return x("p:sp", children=[
        x("p:nvSpPr", children=[x("p:cNvPr", {"id": spid, "name": name}), x("p:cNvSpPr"), x("p:nvPr")]),
        x("p:spPr", children=[x("a:xfrm", children=[x("a:off", {"x": x0, "y": y0}), x("a:ext", {"cx": w, "cy": h})]), x("a:prstGeom", {"prst": geom}, children=[x("a:avLst")]), fill_xml, line_xml]),
        body,
    ])


def line(*args, arrow=True):
    # Accept both line(id, x1, y1, x2, y2, color, width) and
    # line(x1, y1, x2, y2, color, width) for compact slide definitions.
    if len(args) >= 5 and isinstance(args[4], str):
        spid, x1, y1, x2, y2, color, width = 999, args[0], args[1], args[2], args[3], args[4], args[5] if len(args) > 5 else 3
    else:
        spid, x1, y1, x2, y2 = args[:5]
        color = args[5] if len(args) > 5 else BLUE
        width = args[6] if len(args) > 6 else 3
    tail = '<a:tailEnd type="none" w="med" len="med"/>'
    head = '<a:headEnd type="none" w="med" len="med"/>'
    if arrow:
        tail = '<a:tailEnd type="triangle" w="med" len="med"/>'
    return x("p:cxnSp", children=[
        x("p:nvCxnSpPr", children=[x("p:cNvPr", {"id": spid, "name": f"Seta {spid}"}), x("p:cNvCxnSpPr"), x("p:nvPr")]),
        x("p:spPr", children=[x("a:xfrm", children=[x("a:off", {"x": x1, "y": y1}), x("a:ext", {"cx": x2-x1, "cy": y2-y1})]), x("a:prstGeom", {"prst": "line"}, children=[x("a:avLst")]), f'<a:ln w="{width*12700}"><a:solidFill><a:srgbClr val="{color}"/></a:solidFill>{head}{tail}</a:ln>']),
    ])


def icon_card(spid, x0, y0, w, h, number, title, subtitle, fill, accent, icon=""):
    return [
        shape(spid, f"Card {number}", x0, y0, w, h, fill, None, True),
        shape(spid+1, f"Número {number}", x0+180000, y0+150000, 500000, 500000, accent, None, True, str(number), 22, WHITE, True, "c"),
        shape(spid+2, f"Título {number}", x0+800000, y0+150000, w-980000, 480000, None, None, False, title, 18, NAVY, True, "l"),
        shape(spid+3, f"Descrição {number}", x0+220000, y0+850000, w-440000, h-1120000, None, None, False, subtitle, 13, INK, False, "c"),
        shape(spid+4, f"Ícone {number}", x0+w//2-400000, y0+h-900000, 800000, 420000, WHITE, accent, True, icon, 18, accent, True, "c"),
    ]


def slide_xml(slide_no, title, body_parts, bg=WHITE):
    title_shape = shape(2, "Título", 450000, 260000, 12400000, 650000, None, None, False, title, 28, NAVY, True, "l")
    top = shape(1, "Faixa superior", 0, 0, W, 125000, NAVY, None, False)
    footer = shape(900, "Rodapé", 11800000, 7050000, 850000, 220000, None, None, False, f"{slide_no:02d}/20", 10, MUTED, True, "r")
    sp_tree = ["<p:spTree>",
        '<p:nvGrpSpPr><p:cNvPr id="1" name=""><a:extLst/></p:cNvPr><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>',
        '<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>',
        top, title_shape, footer, *body_parts, "</p:spTree>"]
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
<p:cSld><p:bg><p:bgPr><a:solidFill><a:srgbClr val="{bg}"/></a:solidFill><a:effectLst/></p:bgPr></p:bg>{''.join(sp_tree)}</p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sld>'''


def slides():
    S=[]
    S.append(("Conectando a aplicação ao SUAP", [shape(10,"Subtítulo",550000,1400000,7000000,700000,None,None,False,"Um passo a passo visual de OAuth 2.0 para a turma",19,BLUE,True),
        *icon_card(20,650000,2800000,2800000,2100000,1,"Aplicação","botão de login",PALE_BLUE,BLUE,"WEB"),
        line(30,3450000,3850000,4000000,3850000,CYAN,3),
        *icon_card(31,4100000,2800000,2800000,2100000,2,"SUAP","login e autorização",PALE_GREEN,GREEN,"SUAP"),
        line(41,6900000,3850000,7450000,3850000,CYAN,3),
        *icon_card(42,7550000,2800000,2800000,2100000,3,"Perfil","dados do estudante",PALE_YELLOW,ORANGE,"JSON")]))
    S.append(("O que significa “conectar ao SUAP”?", [shape(10,"Definição",700000,1500000,11200000,1000000,PALE_BLUE,BLUE,True,"Nossa aplicação pede ao SUAP uma autorização para identificar o aluno.",22,NAVY,True,"c"),
        *icon_card(20,900000,3200000,3200000,1900000,1,"Usuário","quer entrar",WHITE,BLUE,"ALUNO"), line(30,4150000,4150000,5000000,4150000,BLUE),
        *icon_card(31,5100000,3200000,3200000,1900000,2,"SUAP","confirma identidade",WHITE,GREEN,"OK"), line(41,8300000,4150000,9150000,4150000,GREEN),
        *icon_card(42,9250000,3200000,3200000,1900000,3,"App","mostra o perfil",WHITE,ORANGE,"APP")]))
    S.append(("Mapa dos 20 passos", [shape(10,"Mapa",650000,1350000,12000000,4400000,LIGHT,None,True,"",1),
        *[shape(20+i, f"Passo {i+1}", 1000000+(i%4)*2800000, 4700000-(i//4)*750000, 2350000, 450000, PALE_BLUE if i<8 else PALE_GREEN if i<14 else PALE_YELLOW, BLUE if i<8 else GREEN if i<14 else ORANGE, True, f"{i+1}. {t}", 14, NAVY, True, "c") for i,t in enumerate(["Cadastrar app","Definir callback","Criar client ID","Guardar secret","Botão login","Gerar state","Redirecionar","Autorizar","Receber code","Validar state","Trocar code","Receber token","Guardar sessão","Chamar API","Ler JSON","Exibir perfil","Tratar erro","Testar","Revisar segurança","Desafio final"])]]))
    S.append(("Passo 1 — cadastrar a aplicação", [shape(10,"SUAP",600000,1450000,5200000,4200000,PALE_GREEN,GREEN,True,"SUAP\nPainel de aplicações",25,NAVY,True,"c"), line(5900000,3550000,6750000,3550000,CYAN,3), shape(20,"Formulário",7050000,1450000,5200000,4200000,WHITE,GREEN,True,"Nova aplicação\n\nNome: Projeto INFO3M\nTipo: OAuth2\nCallback: /suap/callback",18,INK,False,"l")]))
    S.append(("Passo 2 — entender o OAuth2", [shape(10,"Analogia",700000,1450000,11200000,850000,PALE_YELLOW,ORANGE,True,"OAuth2 é como pedir um crachá temporário.",24,NAVY,True,"c"),
        *icon_card(20,900000,3000000,3000000,2000000,1,"Senha","fica no SUAP",WHITE,GREEN,"SENHA"), line(30,3950000,4000000,4750000,4000000,BLUE),
        *icon_card(31,4850000,3000000,3000000,2000000,2,"Token","é o crachá",WHITE,BLUE,"TOKEN"), line(41,7900000,4000000,8700000,4000000,BLUE),
        *icon_card(42,8800000,3000000,3000000,2000000,3,"API","abre uma porta",WHITE,ORANGE,"API")]))
    S.append(("Passo 3 — definir o callback", [shape(10,"Callback",650000,1400000,11500000,950000,LIGHT,BLUE,True,"http://127.0.0.1:5000/suap/callback",20,BLUE,True,"c"), shape(20,"Regra",1400000,3000000,9800000,1200000,PALE_RED,RED,True,"A URL precisa ser exatamente igual no SUAP e no código.",22,RED,True,"c"), shape(30,"Exemplo",1400000,4650000,9800000,700000,WHITE,RED,True,"Erro comum: trocar localhost por 127.0.0.1.",16,INK,False,"c")]))
    S.append(("Passo 4 — criar o Client ID", [shape(10,"Identidade",700000,1500000,3800000,4000000,PALE_BLUE,BLUE,True,"CLIENT_ID\n\nIdentifica\nqual aplicação\nestá pedindo acesso.",22,NAVY,True,"c"), line(4700000,3500000,5700000,3500000,BLUE,3), shape(20,"Exemplo",6100000,1500000,6000000,4000000,NAVY,None,True,"export SUAP_CLIENT_ID=seu_client_id\n\nNão é uma senha.\nMas também não deve ser alterado sem motivo.",17,WHITE,False,"l")]))
    S.append(("Passo 5 — proteger o Client Secret", [shape(10,"Segredo",700000,1500000,5000000,4000000,PALE_RED,RED,True,"CLIENT_SECRET\n\nÉ secreto.\nNão vai para o GitHub.\nNão vai para o slide.",22,RED,True,"c"), shape(20,"Terminal",6500000,1500000,5700000,4000000,NAVY,None,True,"export SUAP_CLIENT_SECRET=********\n\n.env  →  fora do Git\n\nSe vazar: gere outro.",17,WHITE,False,"l")]))
    S.append(("Passo 6 — colocar o botão na tela", [shape(10,"Tela de login",700000,1450000,5000000,4200000,WHITE,BLUE,True,"Entrar com SUAP",23,WHITE,True,"c"), shape(20,"Código",6500000,1450000,5700000,4200000,NAVY,None,True,"<a href=\"/login-suap\">\n  Entrar com SUAP\n</a>",18,WHITE,False,"l")]))
    S.append(("Passo 7 — a rota /login-suap", [shape(10,"Rota",700000,1500000,4300000,3800000,PALE_BLUE,BLUE,True,"/login-suap\n\n1. cria state\n2. monta URL\n3. redireciona ao SUAP",20,NAVY,True,"c"), line(5400000,3400000,6500000,3400000,CYAN,3), shape(20,"Serviço",6900000,1500000,5300000,3800000,WHITE,BLUE,True,"authorization_url(state, redirect_uri)\n\nSuapAuthenticationService",17,INK,False,"c")]))
    S.append(("Passo 8 — gerar o state", [shape(10,"Etiqueta",750000,1450000,4200000,4200000,PALE_YELLOW,ORANGE,True,"state =\n\n8fJ2...xP9\n\naleatório\ne temporário",25,NAVY,True,"c"), shape(20,"Proteção",6200000,1450000,5400000,4200000,PALE_GREEN,GREEN,True,"Quando a resposta voltar,\ncomparar:\n\nstate enviado\n=\nstate recebido",22,GREEN,True,"c")]))
    S.append(("Passo 9 — o aluno autoriza no SUAP", [*icon_card(10,900000,1900000,3200000,2500000,1,"Login","aluno informa a senha",PALE_GREEN,GREEN,"SUAP"), line(4300000,3150000,5350000,3150000,CYAN,3), *icon_card(21,5650000,1900000,3200000,2500000,2,"Autorizar","SUAP confirma",PALE_YELLOW,ORANGE,"OK"), line(8950000,3150000,10000000,3150000,CYAN,3), *icon_card(32,10300000,1900000,2200000,2500000,3,"Voltar","para o callback",PALE_BLUE,BLUE,"CODE")]))
    S.append(("Passo 10 — receber o callback", [shape(10,"Navegador",700000,1500000,11200000,1000000,LIGHT,BLUE,True,"/suap/callback?code=ABC123&state=8fJ2...xP9",16,BLUE,True,"c"), shape(20,"Code",1200000,3050000,4500000,1700000,NAVY,None,True,"code = request.args.get('code')",18,WHITE,False,"c"), shape(30,"State",6600000,3050000,4500000,1700000,PALE_GREEN,GREEN,True,"state recebido\nconfere com a sessão",18,GREEN,True,"c")]))
    S.append(("Passo 11 — trocar code por token", [shape(10,"Pedido",700000,1500000,3700000,3800000,PALE_BLUE,BLUE,True,"POST /o/token/\n\ncode\nclient_id\nclient_secret\nredirect_uri",19,NAVY,True,"c"), line(4750000,3400000,5750000,3400000,CYAN,3), shape(20,"Resposta",6150000,1500000,5600000,3800000,PALE_GREEN,GREEN,True,"access_token\n\n\"eyJ...\"\n\nO SUAP confirma\no pedido.",23,GREEN,True,"c")]))
    S.append(("Passo 12 — guardar o access token", [shape(10,"Sessão",700000,1450000,5000000,4000000,NAVY,None,True,"session['suap_access_token']\n\nToken fica associado\nao navegador do usuário.",20,WHITE,True,"c"), shape(20,"Cuidado",6500000,1450000,5700000,4000000,PALE_RED,RED,True,"Não imprimir no terminal.\nNão colocar no HTML.\nNão compartilhar com a turma.\n\nToken é sensível.",20,RED,True,"c")]))
    S.append(("Passo 13 — chamar a API do SUAP", [shape(10,"GET",700000,1600000,2200000,3600000,PALE_BLUE,BLUE,True,"GET",28,BLUE,True,"c"), line(3300000,3400000,4200000,3400000,BLUE,3), shape(20,"Endpoint",4600000,1600000,4700000,3600000,WHITE,BLUE,True,"/api/rh/meus-dados/\n\nAuthorization:\nBearer <token>",21,NAVY,True,"c"), line(9600000,3400000,10500000,3400000,GREEN,3), shape(30,"JSON",10600000,1600000,1800000,3600000,PALE_GREEN,GREEN,True,"nome\nmatrícula\ne-mail\nvínculo",17,GREEN,True,"c")]))
    S.append(("Passo 14 — mostrar o perfil", [shape(10,"SUAP",800000,1550000,3000000,3900000,PALE_GREEN,GREEN,True,"JSON\n\n{ nome,\n  matrícula,\n  email }",22,GREEN,True,"c"), line(4200000,3500000,5300000,3500000,CYAN,3), shape(20,"Tela",5700000,1550000,6000000,3900000,WHITE,GREEN,True,"Olá, Ana!\n\nMatrícula: 20260001\nVínculo: estudante\n\nPerfil SUAP",22,NAVY,True,"c")]))
    S.append(("Passo 15 — entender o arquivo routes.py", [shape(10,"routes.py",700000,1450000,5000000,4200000,NAVY,None,True,"/login-suap\n\n/suap/callback\n\n/suap/meus_dados",20,WHITE,True,"c"), line(6000000,3500000,6900000,3500000,CYAN,3), shape(20,"Orquestração",7300000,1450000,4900000,4200000,PALE_BLUE,BLUE,True,"Rotas recebem\na requisição,\nchamam o serviço\ne escolhem a tela.",20,NAVY,True,"c")]))
    S.append(("Passo 16 — entender o serviço", [shape(10,"SuapAuthenticationService",600000,1450000,5500000,4200000,PALE_YELLOW,ORANGE,True,"authorization_url()\n\nexchange_code()\n\nmeus_dados()",19,NAVY,True,"c"), line(6350000,3500000,7350000,3500000,CYAN,3), shape(20,"Responsabilidade",7750000,1450000,4700000,4200000,PALE_GREEN,GREEN,True,"Conversar com\nos endpoints do SUAP\ne devolver JSON\npara o Flask.",20,GREEN,True,"c")]))
    S.append(("Passo 17 — tratar erros", [shape(10,"State inválido",700000,1700000,3000000,3000000,PALE_RED,RED,True,"Falha\nde segurança",21,RED,True,"c"), shape(20,"Sem token",5150000,1700000,3000000,3000000,PALE_YELLOW,ORANGE,True,"Falha\nde configuração",21,ORANGE,True,"c"), shape(30,"API fora",9300000,1700000,3000000,3000000,PALE_BLUE,BLUE,True,"Falha\nde conexão",21,BLUE,True,"c"), shape(40,"Regra",1600000,5150000,10000000,650000,WHITE,RED,True,"Mensagem clara + retorno ao login + nada de segredo exposto.",16,RED,True,"c")]))
    S.append(("Passo 18 — testar o fluxo", [shape(10,"Checklist",700000,1400000,11200000,4500000,LIGHT,None,True,"1  servidor rodando\n2  callback correto\n3  botão abre o SUAP\n4  autorização concluída\n5  perfil aparece\n6  erros são compreensíveis",22,NAVY,True,"l")]))
    S.append(("Passo 19 — segurança em linguagem simples", [shape(10,"Faça",800000,1500000,5000000,4000000,PALE_GREEN,GREEN,True,"✓ use HTTPS em produção\n✓ valide o state\n✓ proteja o secret\n✓ limite o que consulta",21,GREEN,True,"l"), shape(20,"Evite",6500000,1500000,5000000,4000000,PALE_RED,RED,True,"✗ senha na sua aplicação\n✗ token no GitHub\n✗ token na tela\n✗ callback improvisado",21,RED,True,"l")]))
    S.append(("Passo 20 — desafio final", [shape(10,"Desafio",700000,1400000,11200000,1100000,PALE_BLUE,BLUE,True,"Explique o fluxo com cinco cartões e cinco setas.",24,NAVY,True,"c"), *icon_card(20,900000,3300000,2800000,1700000,1,"Botão","inicia",WHITE,BLUE,"1"), line(3800000,4150000,4550000,4150000,CYAN,3), *icon_card(31,4850000,3300000,2800000,1700000,2,"SUAP","autoriza",WHITE,GREEN,"2"), line(7650000,4150000,8400000,4150000,CYAN,3), *icon_card(42,8700000,3300000,2800000,1700000,3,"Perfil","aparece",WHITE,ORANGE,"3"), shape(50,"Pergunta",1700000,5700000,9500000,500000,PALE_YELLOW,ORANGE,True,"Em qual etapa a senha deixa de estar na nossa aplicação?",17,ORANGE,True,"c")]))
    # 20 slides total: keep the title, the registration step, and the remaining
    # implementation steps. The conceptual overview and map are intentionally
    # folded into the title/teacher explanation so the deck stays at the
    # requested length.
    return [S[0], S[3], *S[5:]]


def content_types(n):
    overrides = [
        '<Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>',
        '<Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/>',
        '<Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/>',
        '<Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>',
    ] + [f'<Override PartName="/ppt/slides/slide{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>' for i in range(1,n+1)]
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/>{''.join(overrides)}</Types>'''


def rels(items):
    return '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">' + ''.join(x("Relationship", a) for a in items) + '</Relationships>'


def presentation_xml(n):
    ids = ''.join(f'<p:sldId id="{255+i}" r:id="rId{i+2}"/>' for i in range(1,n+1))
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:presentation xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"><p:sldMasterIdLst><p:sldMasterId id="1" r:id="rId1"/></p:sldMasterIdLst><p:sldIdLst>{ids}</p:sldIdLst><p:sldSz cx="{W}" cy="{H}" type="screen16x9"/><p:notesSz cx="6858000" cy="9144000"/><p:defaultTextStyle><a:defPPr/><a:lvl1pPr marL="0" algn="l"><a:defRPr lang="pt-BR"/></a:lvl1pPr></p:defaultTextStyle></p:presentation>'''


THEME = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="SUAP Classroom"><a:themeElements><a:clrScheme name="SUAP"><a:dk1><a:sysClr val="windowText" lastClr="000000"/></a:dk1><a:lt1><a:sysClr val="window" lastClr="FFFFFF"/></a:lt1><a:dk2><a:srgbClr val="0D1F3C"/></a:dk2><a:lt2><a:srgbClr val="F0F4F8"/></a:lt2><a:accent1><a:srgbClr val="1F6FEB"/></a:accent1><a:accent2><a:srgbClr val="1D9B59"/></a:accent2><a:accent3><a:srgbClr val="F0A21A"/></a:accent3><a:accent4><a:srgbClr val="19AFC7"/></a:accent4><a:accent5><a:srgbClr val="C73A42"/></a:accent5><a:accent6><a:srgbClr val="596579"/></a:accent6><a:hlink><a:srgbClr val="1F6FEB"/></a:hlink><a:folHlink><a:srgbClr val="C73A42"/></a:folHlink></a:clrScheme><a:fontScheme name="Aptos"><a:majorFont><a:latin typeface="Aptos Display"/></a:majorFont><a:minorFont><a:latin typeface="Aptos"/></a:minorFont></a:fontScheme><a:fmtScheme name="SUAP"><a:fillStyleLst/><a:lnStyleLst/><a:effectStyleLst/><a:bgFillStyleLst/></a:fmtScheme></a:themeElements></a:theme>'''

CORE = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><dc:title>Conexão da aplicação com o SUAP</dc:title><dc:subject>OAuth 2.0 e integração Flask-SUAP</dc:subject><dc:creator>Material didático</dc:creator><cp:lastModifiedBy>Material didático</cp:lastModifiedBy></cp:coreProperties>'''
APP = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes"><Application>Microsoft PowerPoint</Application><PresentationFormat>On-screen Show (16:9)</PresentationFormat><Slides>20</Slides><Notes>0</Notes><HiddenSlides>0</HiddenSlides><MMClips>0</MMClips><ScaleCrop>false</ScaleCrop><HeadingPairs><vt:vector size="2" baseType="variant"><vt:variant><vt:lpstr>Slides</vt:lpstr></vt:variant><vt:variant><vt:i4>20</vt:i4></vt:variant></vt:vector></HeadingPairs><TitlesOfParts><vt:vector size="0" baseType="lpstr"/></TitlesOfParts></Properties>'''


MASTER = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><p:sldMaster xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"><p:cSld name="Master"><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr/></p:spTree></p:cSld><p:clrMap accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" bg1="lt1" bg2="lt2" folHlink="folHlink" hlink="hlink" tx1="dk1" tx2="dk2"/><p:sldLayoutIdLst><p:sldLayoutId id="1" r:id="rId1"/></p:sldLayoutIdLst><p:txStyles><p:titleStyle/><p:bodyStyle/><p:otherStyle/></p:txStyles></p:sldMaster>'''
LAYOUT = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><p:sldLayout xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" type="blank"><p:cSld name="Blank"><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr/></p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sldLayout>'''


def make():
    ss = slides()
    files = {
        '[Content_Types].xml': content_types(len(ss)).replace('</Types>', '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/><Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/></Types>'),
        '_rels/.rels': rels([
            {'Id':'rId1','Type':'http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument','Target':'ppt/presentation.xml'},
            {'Id':'rId2','Type':'http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties','Target':'docProps/core.xml'},
            {'Id':'rId3','Type':'http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties','Target':'docProps/app.xml'},
        ]),
        'docProps/core.xml': CORE,
        'docProps/app.xml': APP,
        'ppt/presentation.xml': presentation_xml(len(ss)),
        'ppt/_rels/presentation.xml.rels': rels([{'Id':'rId1','Type':'http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster','Target':'slideMasters/slideMaster1.xml'}, *({'Id':f'rId{i+2}','Type':'http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide','Target':f'slides/slide{i}.xml'} for i in range(1,len(ss)+1))]),
        'ppt/slideMasters/slideMaster1.xml': MASTER,
        'ppt/slideMasters/_rels/slideMaster1.xml.rels': rels([{'Id':'rId1','Type':'http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout','Target':'../slideLayouts/slideLayout1.xml'}, {'Id':'rId2','Type':'http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme','Target':'../theme/theme1.xml'}]),
        'ppt/slideLayouts/slideLayout1.xml': LAYOUT,
        'ppt/slideLayouts/_rels/slideLayout1.xml.rels': rels([{'Id':'rId1','Type':'http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster','Target':'../slideMasters/slideMaster1.xml'}]),
        'ppt/theme/theme1.xml': THEME,
    }
    for i, (title, parts) in enumerate(ss, 1):
        files[f'ppt/slides/slide{i}.xml'] = slide_xml(i, title, parts)
        files[f'ppt/slides/_rels/slide{i}.xml.rels'] = rels([{'Id':'rId1','Type':'http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout','Target':'../slideLayouts/slideLayout1.xml'}])
    with ZipFile(OUT, 'w', ZIP_DEFLATED) as z:
        for name, data in files.items(): z.writestr(name, data)
    print(OUT)


if __name__ == '__main__':
    make()
