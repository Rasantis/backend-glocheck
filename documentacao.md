Documentação:

Este código cria uma aplicação web usando o framework Flask, que é usado para criar aplicativos web em Python. O código inclui as seguintes funcionalidades:

1. Autenticação de usuário: o código define uma lista de usuários e senhas válidos e usa essa lista para verificar se um usuário forneceu credenciais válidas ao fazer login.

* Rota "/login" com método "GET": Exibe o formulário de login na página inicial do aplicativo.
* Rota "/login" com método "POST": Verifica as credenciais do usuário fornecidas no formulário de login e, se válidas, redireciona o usuário para a página de repositório. Se as credenciais não forem válidas, exibe uma página de erro.

2. Upload de arquivos: o código permite que os usuários façam upload de arquivos para uma pasta específica no servidor. Ele também cria uma pasta para cada usuário, onde os arquivos são salvos.

* Rota "/repositorio" com método "POST": Recebe o arquivo enviado pelo usuário, salva-o na pasta de repositório e na pasta do usuário, e também salva as informações de Nome, Email, Destino e data de envio em um arquivo de texto.

3. Envio de e-mail: O código configura uma conta de email para enviar email a um determinado endereço quando o arquivo é enviado.
4. Gravação de dados: o código grava os dados de nome, email, destino e data de envio em um arquivo de texto.
5. Download de arquivos: o código permite que os usuários baixem os arquivos que eles fizeram upload.

* Rota "/get-file/`<filename>`" : permite que os usuários baixem os arquivos que eles fizeram upload

6. Gerenciamento de sessão: o código usa o gerenciamento de sessão do Flask para manter o usuário logado enquanto ele usa a aplicação.

Para usar essa aplicação, é necessário ter o Flask e outras dependências instaladas. Além disso, as configurações de e-mail devem ser ajustadas de acordo com as configurações do seu provedor de e-mail.
