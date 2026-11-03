on setText(theShape, theText, fontSize, fontColor, isBold)
 tell application "Microsoft PowerPoint"
  set content of text range of text frame of theShape to theText
 end tell
end setText

on addTwoColumn(thePres, slideTitle, leftText, rightText)
 tell application "Microsoft PowerPoint"
  set s to make new slide at end of thePres
  set titleShape to shape 1 of s
  set leftShape to shape 2 of s
  set rightShape to shape 3 of s
  my setText(titleShape, slideTitle, 26, {13, 31, 60}, true)
  my setText(leftShape, leftText, 20, {31, 111, 235}, false)
  my setText(rightShape, rightText, 20, {29, 155, 89}, false)
 end tell
end addTwoColumn

tell application "Microsoft PowerPoint"
 activate
 set thePres to make new presentation
 set firstSlide to make new slide at end of thePres
 set firstTitle to shape 1 of firstSlide
 set firstBody to shape 2 of firstSlide
 my setText(firstTitle, "Conectando uma aplicação Flask ao SUAP", 30, {13, 31, 60}, true)
 my setText(firstBody, "Passo a passo visual de OAuth 2.0\n\nAPLICAÇÃO  →  SUAP  →  PERFIL", 22, {31, 111, 235}, false)
 my addTwoColumn(thePres, "Passo 1 — cadastrar a aplicação", "SUAP / painel de aplicações\n\nNome: Projeto INFO3M\nTipo: OAuth2 / Authorization Code", "Callback cadastrado\n\nhttp://127.0.0.1:5000/suap/callback\n\nA URL deve ser idêntica nos dois lugares.")
 my addTwoColumn(thePres, "Passo 2 — guardar as credenciais", "CLIENT_ID\n\nexport SUAP_CLIENT_ID=seu_client_id\n\nIdentifica a aplicação.", "CLIENT_SECRET\n\nexport SUAP_CLIENT_SECRET=seu_client_secret\n\nÉ segredo: não compartilhe.")
 my addTwoColumn(thePres, "Passo 3 — colocar o botão na tela", "Na tela\n\nEntrar com SUAP\n\nO aluno clica e sai da aplicação.", "No código\n\n<a href=/login-suap>\n  Entrar com SUAP\n</a>")
 my addTwoColumn(thePres, "Passo 4 — iniciar o fluxo", "/login-suap\n\n1. cria state\n2. monta redirect_uri\n3. redireciona ao SUAP", "Serviço\n\nauthorization_url(state, redirect_uri)\n\nSuapAuthenticationService")
 my addTwoColumn(thePres, "Passo 5 — gerar o state", "Antes de sair\n\nstate = 8fJ2...xP9\n\nGuarda na sessão.", "Quando voltar\n\nstate enviado = state recebido\n\nSe não bater: interromper.")
 my addTwoColumn(thePres, "Passo 6 — o aluno autoriza", "SUAP\n\nAluno informa usuário e senha\n\nO SUAP confirma a identidade.", "Ação\n\nAutorizar\n\nDepois, o navegador volta.")
 my addTwoColumn(thePres, "Passo 7 — receber o callback", "URL de retorno\n\n/suap/callback?code=ABC123&state=8fJ2...xP9", "A aplicação recebe\n\ncode = autorização de uso único\nstate = etiqueta de segurança")
 my addTwoColumn(thePres, "Passo 8 — validar o state", "Se for igual\n\nA resposta parece ser do fluxo que iniciamos.", "Se for diferente\n\nMostre erro e volte ao login.\n\nNão prossiga.")
 my addTwoColumn(thePres, "Passo 9 — trocar o code por token", "Pedido ao SUAP\n\nPOST /o/token/\n\ncode + client_id + client_secret", "Resposta\n\naccess_token\n\nUm crachá temporário para a API.")
 my addTwoColumn(thePres, "Passo 10 — guardar o token", "No Flask\n\nsession['suap_access_token'] = token", "Cuidado\n\nNão imprimir no terminal.\nNão colocar no HTML.\nNão enviar ao GitHub.")
 my addTwoColumn(thePres, "Passo 11 — chamar a API", "Endpoint\n\nGET https://suap.ifrn.edu.br/api/rh/meus-dados/", "Cabeçalho\n\nAuthorization: Bearer <access_token>\n\nO token vai no servidor.")
 my addTwoColumn(thePres, "Passo 12 — receber o JSON", "Resposta\n\n{ nome, matrícula, email, vínculo }", "Ideia\n\nJSON é texto organizado\nque o Flask consegue ler.")
 my addTwoColumn(thePres, "Passo 13 — mostrar o perfil", "Dados\n\nnome\nmatrícula\ne-mail\ntipo de vínculo", "Tela\n\nOlá, Ana!\n\nPerfil SUAP\nMatrícula: 20260001")
 my addTwoColumn(thePres, "Passo 14 — entender o routes.py", "Rotas principais\n\n/login-suap\n/suap/callback\n/suap/meus_dados", "Responsabilidade\n\nReceber a requisição, chamar o serviço e escolher a tela.")
 my addTwoColumn(thePres, "Passo 15 — entender o serviço", "SuapAuthenticationService\n\nauthorization_url()\nexchange_code()\nmeus_dados()", "Responsabilidade\n\nMontar pedidos HTTP e devolver JSON ao Flask.")
 my addTwoColumn(thePres, "Passo 16 — tratar erros", "Exemplos\n\nstate inválido\ncode ausente\nsem access_token", "Boa resposta\n\nMensagem clara + retorno ao login\n+ nada de segredo exposto.")
 my addTwoColumn(thePres, "Passo 17 — testar o fluxo", "Checklist\n\n1 servidor rodando\n2 callback correto\n3 botão abre o SUAP\n4 aluno autoriza", "Resultado esperado\n\n5 retorno funciona\n6 perfil aparece\n7 erros são compreensíveis")
 my addTwoColumn(thePres, "Passo 18 — segurança em linguagem simples", "Faça\n\nuse HTTPS em produção\nvalide o state\nproteja o secret", "Evite\n\nsenha na sua aplicação\ntoken no GitHub\ntoken na tela")
 my addTwoColumn(thePres, "Passo 19 — desafio final", "Pergunta para a turma\n\nEm qual etapa a senha deixa de estar na nossa aplicação?", "Resposta esperada\n\nAssim que o aluno é redirecionado para o SUAP.\n\nA aplicação trabalha com token.")
 set outFile to (POSIX file "/Users/leosilva/development/ifrn/20261/3ano/prog_int/app_flask/materiais/conexao-suap-editavel.pptx") as alias
 save thePres in outFile
 close thePres
end tell
