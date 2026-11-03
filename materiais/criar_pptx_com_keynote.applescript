property W : 1920
property H : 1080
property navy : {2570, 8000, 15400}
property blue : {8000, 28000, 56000}
property green : {7000, 39000, 22000}
property orange : {58000, 32000, 5000}
property red : {50000, 14000, 17000}
property paleBlue : {57000, 61000, 65000}
property paleGreen : {59000, 65000, 60000}
property paleYellow : {65000, 62000, 45000}
property ink : {8000, 11000, 18000}

on addText(theSlide, theText, x, y, w, h, fontSize, theColor, isBold)
	 tell theSlide
		 set t to make new text item with properties {position:{x, y}, width:w, height:h}
		 set object text of t to theText
		 tell t's object text
			 set font to "Aptos"
			 set size to fontSize
			 set color to theColor
		 end tell
		 if isBold then
			 tell t's object text to set font to "Aptos Bold"
		 end if
	 end tell
end addText

on addBox(theSlide, theText, x, y, w, h, fillColor, textColor, fontSize)
	 tell theSlide
		 set b to make new shape with properties {position:{x, y}, width:w, height:h}
		 set object text of b to theText
		 tell b's object text
			 set font to "Aptos"
			 set size to fontSize
			 set color to textColor
		 end tell
	 end tell
end addBox

on addSlide(theDoc, slideTitle, kicker, leftLabel, leftBody, rightLabel, rightBody, accent)
	 tell application "Keynote"
		 set s to make new slide at end of slides of theDoc with properties {base layout:master slide "Blank" of theDoc}
		 my addText(s, "GUIA DE INTEGRAÇÃO", 50, 24, 600, 30, 16, blue, true)
		 my addText(s, slideTitle, 50, 70, 1800, 75, 31, navy, true)
		 my addBox(s, leftLabel & return & return & leftBody, 70, 220, 820, 600, paleBlue, ink, 23)
		 my addBox(s, rightLabel & return & return & rightBody, 1030, 220, 820, 600, paleGreen, ink, 23)
		 my addText(s, kicker, 70, 870, 1780, 75, 19, accent, true)
	 end tell
end addSlide

tell application "Keynote"
	 activate
	 set theDoc to make new document
	 set theDoc's width to W
	 set theDoc's height to H
	 set title showing of first slide of theDoc to false
	 set body showing of first slide of theDoc to false
	 -- Reuse the first slide as the title slide.
	 set s to first slide of theDoc
	 my addText(s, "GUIA DE INTEGRAÇÃO", 50, 24, 600, 30, 16, blue, true)
	 my addText(s, "Conectando uma aplicação Flask ao SUAP", 50, 80, 1800, 90, 36, navy, true)
	 my addText(s, "Passo a passo visual de OAuth 2.0 para a turma", 55, 180, 1500, 55, 23, blue, true)
	 my addBox(s, "1  Aplicação Flask\n\nBotão Entrar com SUAP", 80, 360, 500, 300, paleBlue, ink, 24)
	 my addBox(s, "2  SUAP\n\nLogin e autorização", 710, 360, 500, 300, paleGreen, ink, 24)
	 my addBox(s, "3  Perfil\n\nDados do estudante", 1340, 360, 500, 300, paleYellow, ink, 24)
	 my addText(s, "Senha fica no SUAP • a aplicação recebe uma autorização temporária", 80, 790, 1760, 60, 22, green, true)

	 my addSlide(theDoc, "Passo 1 — cadastrar a aplicação", "O projeto precisa ser conhecido pelo SUAP antes de programar.", "SUAP / painel de aplicações", "Nome: Projeto INFO3M\nTipo: OAuth2 / Authorization Code", "Callback cadastrado", "http://127.0.0.1:5000/suap/callback\n\nA URL deve ser idêntica nos dois lugares.", green)
	 my addSlide(theDoc, "Passo 2 — guardar as credenciais", "Credenciais ficam em variáveis de ambiente, fora do GitHub.", "Client ID", "export SUAP_CLIENT_ID=seu_client_id\n\nIdentifica a aplicação.", "Client Secret", "export SUAP_CLIENT_SECRET=seu_client_secret\n\nÉ segredo: não compartilhe.", blue)
	 my addSlide(theDoc, "Passo 3 — colocar o botão na tela", "O botão chama a rota /login-suap.", "Na tela", "Entrar com SUAP\n\nO aluno clica e sai da aplicação.", "No código", "<a href=/login-suap>\n  Entrar com SUAP\n</a>", blue)
	 my addSlide(theDoc, "Passo 4 — iniciar o fluxo", "A rota monta a URL de autorização e redireciona o navegador.", "/login-suap", "1. cria state\n2. monta redirect_uri\n3. redireciona ao SUAP", "Serviço", "authorization_url(state, redirect_uri)\n\nSuapAuthenticationService", blue)
	 my addSlide(theDoc, "Passo 5 — gerar o state", "State é uma etiqueta aleatória para conferir a resposta depois.", "Antes de sair", "state = 8fJ2...xP9\n\nGuarda na sessão.", "Quando voltar", "state enviado = state recebido\n\nSe não bater: interromper.", orange)
	 my addSlide(theDoc, "Passo 6 — o aluno autoriza", "A senha é digitada no SUAP, não na nossa aplicação.", "SUAP", "Aluno informa usuário e senha\n\nO SUAP confirma a identidade.", "Ação", "Autorizar\n\nDepois, o SUAP devolve o navegador.", green)
	 my addSlide(theDoc, "Passo 7 — receber o callback", "O navegador volta para a rota cadastrada.", "URL de retorno", "/suap/callback?code=ABC123&state=8fJ2...xP9", "A aplicação recebe", "code = autorização de uso único\nstate = etiqueta de segurança", blue)
	 my addSlide(theDoc, "Passo 8 — validar o state", "Antes de usar o code, compare o state.", "Se for igual", "A resposta parece ser do fluxo que iniciamos.", "Se for diferente", "Mostre erro e volte ao login.\n\nNão prossiga.", orange)
	 my addSlide(theDoc, "Passo 9 — trocar o code por token", "O servidor troca o code usando também o client_secret.", "Pedido ao SUAP", "POST /o/token/\n\ncode + client_id + client_secret", "Resposta", "access_token\n\nUm crachá temporário para a API.", green)
	 my addSlide(theDoc, "Passo 10 — guardar o token", "O token fica associado à sessão do usuário.", "No Flask", "session['suap_access_token'] = token", "Cuidado", "Não imprimir no terminal.\nNão colocar no HTML.\nNão enviar ao GitHub.", red)
	 my addSlide(theDoc, "Passo 11 — chamar a API", "Com o token, a aplicação consulta os dados autorizados.", "Endpoint", "GET https://suap.ifrn.edu.br/api/rh/meus-dados/", "Cabeçalho", "Authorization: Bearer <access_token>\n\nO token vai no servidor.", blue)
	 my addSlide(theDoc, "Passo 12 — receber o JSON", "A API responde com dados estruturados.", "Resposta", "{ nome, matrícula, email, vínculo }", "Ideia", "JSON é texto organizado\nque o Flask consegue ler.", green)
	 my addSlide(theDoc, "Passo 13 — mostrar o perfil", "A aplicação usa o JSON para montar uma tela.", "Dados", "nome\nmatrícula\ne-mail\ntipo de vínculo", "Tela", "Olá, Ana!\n\nPerfil SUAP\nMatrícula: 20260001", green)
	 my addSlide(theDoc, "Passo 14 — entender o routes.py", "As rotas coordenam a viagem do navegador.", "Rotas principais", "/login-suap\n/suap/callback\n/suap/meus_dados", "Responsabilidade", "Receber a requisição, chamar o serviço e escolher a tela.", blue)
	 my addSlide(theDoc, "Passo 15 — entender o serviço", "O serviço concentra a conversa com o SUAP.", "SuapAuthenticationService", "authorization_url()\nexchange_code()\nmeus_dados()", "Responsabilidade", "Montar pedidos HTTP e devolver JSON ao Flask.", orange)
	 my addSlide(theDoc, "Passo 16 — tratar erros", "Todo fluxo externo pode falhar.", "Exemplos", "state inválido\ncode ausente\nsem access_token", "Boa resposta", "Mensagem clara + retorno ao login\n+ nada de segredo exposto.", red)
	 my addSlide(theDoc, "Passo 17 — testar o fluxo", "Teste cada etapa, sem pular direto para o final.", "Checklist", "1 servidor rodando\n2 callback correto\n3 botão abre o SUAP\n4 aluno autoriza", "Resultado esperado", "5 retorno funciona\n6 perfil aparece\n7 erros são compreensíveis", blue)
	 my addSlide(theDoc, "Passo 18 — segurança em linguagem simples", "Token é uma chave: trate como informação sensível.", "Faça", "Use HTTPS em produção\nValide o state\nProteja o secret", "Evite", "Senha na sua aplicação\nToken no GitHub\nToken na tela", green)
	 my addSlide(theDoc, "Passo 19 — fluxo completo", "Botão → SUAP → callback → token → API → perfil.", "Aplicação", "Gera state\nRedireciona\nRecebe code", "SUAP + API", "Autoriza\nEntrega token\nDevolve dados", blue)
	 my addSlide(theDoc, "Passo 20 — desafio final", "Explique o fluxo com cinco cartões e cinco setas.", "Pergunta para a turma", "Em qual etapa a senha deixa de estar na nossa aplicação?", "Resposta esperada", "Assim que o aluno é redirecionado para o SUAP.\n\nA nossa aplicação trabalha com token.", orange)

	 set outFile to POSIX file "/Users/leosilva/development/ifrn/20261/3ano/prog_int/app_flask/materiais/conexao-suap-editavel.pptx" as alias
	 -- export front document to outFile as Microsoft PowerPoint
	 -- close theDoc
end tell
