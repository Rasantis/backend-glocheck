# #testes
# def test_login_form(client):
#     response = client.get('/login')
#     assert response.status_code == 200
#     assert b'Username' in response.data
#     assert b'Password' in response.data


# def test_login_submit(client):
#     # Teste com usuário e senha válidos
#     response = client.post('/login', data={"username": "admin", "password": "1234"})
#     assert response.status_code == 200
#     assert b'Voce foi autorizado' in response.data

#     # Teste com usuário e senha inválidos
#     response = client.post('/login', data={"username": "admin", "password": "12345"})
#     assert response.status_code == 200
#     assert b'Error' in response.data


# def test_upload(client):
#     # Enviar um arquivo para o servidor
#     response = client.post('/repositorio', data={"Nome": "John", "email": "john@example.com"},
#                            files={"imagem": ("test.png", b"test content", "image/png")})
#     assert response.status_code == 200
#     assert b'Repositorio' in response.data

#     # Verificar se o arquivo foi salvo na pasta repositorio
#     file_path = os.path.join(UPLOAD_FOLDER, "test.png")
#     assert os.path.exists(file_path)
#     assert open(file_path, "rb").read() == b"test content"

#     # Remover o arquivo da pasta repositorio
#     os.remove(file_path)
