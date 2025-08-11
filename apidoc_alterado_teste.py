import requests
from requests.exceptions import RequestException

BASE_URL = "http://localhost:5000"  # ajuste se necessário

USER = {"nome": "User App", "email": "user_app@example.com", "senha": "senha123"}
ADMIN = {"nome": "Admin App", "email": "admin_app@example.com", "senha": "senha123", "perfil": "ADMIN"}

def safe_call(method, url, **kwargs):
    try:
        return method(url, timeout=8, **kwargs)
    except RequestException as e:
        print(f"❌ ERRO DE REDE em {url}: {e}")
        return None

def create_user(user):
    return safe_call(requests.post, f"{BASE_URL}/usuarios", json=user)

def login(email, senha):
    resp = safe_call(requests.post, f"{BASE_URL}/auth/login", json={"email": email, "senha": senha})
    if resp is not None and resp.status_code == 200:
        return resp.json().get("access_token")
    return None

def main():
    nota = 0
    print("=== TESTE: ALTERAÇÕES (titulo obrigatório, admin não edita, editado em comentário) ===\n")

    # 1) Cria USER e ADMIN
    print("1) Criando usuários USER e ADMIN ...")
    r1 = create_user(USER)
    r2 = create_user(ADMIN)
    if r1 is not None and r1.status_code == 201:
        print("   ✅ USER criado (201).")
        nota += 3
    else:
        print(f"   ❌ Falha ao criar USER (esperado 201). Recebido: {r1.status_code if r1 else 'N/A'}")

    if r2 is not None and r2.status_code == 201:
        print("   ✅ ADMIN criado (201).")
        nota += 3
    else:
        print(f"   ❌ Falha ao criar ADMIN (esperado 201). Recebido: {r2.status_code if r2 else 'N/A'}")

    # 2) Autentica USER e ADMIN
    print("\n2) Autenticando USER e ADMIN ...")
    token_user = login(USER["email"], USER["senha"])
    token_admin = login(ADMIN["email"], ADMIN["senha"])
    if token_user:
        print("   ✅ USER autenticado (200).")
        nota += 2
    else:
        print("   ❌ Falha no login do USER.")
    if token_admin:
        print("   ✅ ADMIN autenticado (200).")
        nota += 2
    else:
        print("   ❌ Falha no login do ADMIN.")

    headers_user = {"Authorization": f"Bearer {token_user}"} if token_user else {}
    headers_admin = {"Authorization": f"Bearer {token_admin}"} if token_admin else {}

    # 3) USER cria mensagem sem titulo (422)
    print("\n3) USER criando mensagem sem 'titulo' (deve falhar 422) ...")
    r3 = safe_call(requests.post, f"{BASE_URL}/mensagens", json={
        "conteudo": "Mensagem sem título"
    }, headers=headers_user)
    if r3 is not None and r3.status_code == 422:
        print("   ✅ Validação correta: 422 sem 'titulo'.")
        nota += 4
    else:
        print(f"   ❌ Esperado 422, recebido: {r3.status_code if r3 else 'N/A'}")

    # 4) USER cria mensagem válida (201)
    print("\n4) USER criando mensagem válida (201) ...")
    mensagem_id = None
    r4 = safe_call(requests.post, f"{BASE_URL}/mensagens", json={
        "titulo": "Titulo OK",
        "conteudo": "Conteudo OK"
    }, headers=headers_user)
    if r4 is not None and r4.status_code == 201:
        body = r4.json()
        mensagem_id = body.get("id")
        if mensagem_id and "data_criacao" in body:
            print(f"   ✅ Mensagem criada id={mensagem_id} com data_criacao.")
            nota += 4
        else:
            print("   ❌ Corpo da mensagem sem id ou data_criacao.")
    else:
        print(f"   ❌ Esperado 201, recebido: {r4.status_code if r4 else 'N/A'}")

    # 5) ADMIN tenta editar mensagem (403)
    print("\n5) ADMIN tentando editar mensagem do USER (esperado 403) ...")
    if mensagem_id and token_admin:
        r5 = safe_call(requests.put, f"{BASE_URL}/mensagens/{mensagem_id}", json={
            "titulo": "Admin não pode",
            "conteudo": "Admin não deve editar"
        }, headers=headers_admin)
        if r5 is not None and r5.status_code == 403:
            print("   ✅ Bloqueio correto: ADMIN não pode editar mensagem (403).")
            nota += 4
        else:
            print(f"   ❌ Esperado 403, recebido: {r5.status_code if r5 else 'N/A'}")
    else:
        print("   ⚠️ Sem mensagem_id ou token_admin; teste 403 de mensagem não executado.")

    # 6) USER cria comentário (201) e verifica editado == false
    print("\n6) USER criando comentário (201) e checando 'editado == false' ...")
    comentario_id = None
    if mensagem_id and token_user:
        r6 = safe_call(requests.post, f"{BASE_URL}/mensagens/{mensagem_id}/comentarios", json={
            "conteudo": "Primeiro comentário"
        }, headers=headers_user)
        if r6 is not None and r6.status_code == 201:
            body = r6.json()
            comentario_id = body.get("id")
            editado = body.get("editado")
            if comentario_id and "data_criacao" in body and editado is False:
                print(f"   ✅ Comentário criado id={comentario_id}, editado=False.")
                nota += 4
            else:
                print(f"   ❌ Comentário sem id/data_criacao ou 'editado' != False. editado={editado}")
        else:
            print(f"   ❌ Esperado 201, recebido: {r6.status_code if r6 else 'N/A'}")
    else:
        print("   ⚠️ Sem mensagem_id ou token_user; não foi possível criar comentário.")

    # 7) ADMIN tenta editar comentário (403)
    print("\n7) ADMIN tentando editar comentário do USER (esperado 403) ...")
    if mensagem_id and comentario_id and token_admin:
        r7 = safe_call(requests.put, f"{BASE_URL}/mensagens/{mensagem_id}/comentarios/{comentario_id}", json={
            "conteudo": "Admin tentando editar"
        }, headers=headers_admin)
        if r7 is not None and r7.status_code == 403:
            print("   ✅ Bloqueio correto: ADMIN não pode editar comentário (403).")
            nota += 3
        else:
            print(f"   ❌ Esperado 403, recebido: {r7.status_code if r7 else 'N/A'}")
    else:
        print("   ⚠️ Dados insuficientes para testar edição por ADMIN.")

    # 8) USER edita o próprio comentário (200) e editado deve ficar true
    print("\n8) USER editando o próprio comentário (200) e checando 'editado == true' ...")
    if mensagem_id and comentario_id and token_user:
        r8 = safe_call(requests.put, f"{BASE_URL}/mensagens/{mensagem_id}/comentarios/{comentario_id}", json={
            "conteudo": "Comentário editado pelo autor"  # sem enviar 'editado' no payload
        }, headers=headers_user)
        print(r8, r8.status_code)
        if r8 is not None and r8.status_code == 200:
            body8 = r8.json()
            if body8.get("editado") is True:
                print("   ✅ 'editado' atualizado automaticamente para true após edição.")
                nota += 4
            else:
                print(f"   ❌ Esperado editado=True após PUT. Recebido: {body8.get('editado')}")
        else:
            print(f"   ❌ Esperado 200, recebido: {r8.status_code if r8 else 'N/A'}")
    else:
        print("   ⚠️ Dados insuficientes para editar o comentário como USER.")

    # 9) USER tenta forçar 'editado=false' (servidor deve ignorar e manter true)
    print("\n9) USER tentando forçar 'editado=false' (servidor deve ignorar) ...")
    if mensagem_id and comentario_id and token_user:
        r9 = safe_call(requests.put, f"{BASE_URL}/mensagens/{mensagem_id}/comentarios/{comentario_id}", json={
            "conteudo": "Tentando forçar editado falso",
            "editado": False  # deve ser ignorado pelo servidor
        }, headers=headers_user)
        if r9 is not None and r9.status_code == 200:
            body9 = r9.json()
            if body9.get("editado") is True:
                print("   ✅ Campo 'editado' ignorado no payload e permaneceu true.")
                nota += 4
            else:
                print(f"   ❌ Servidor aceitou alteração manual de 'editado'. Valor: {body9.get('editado')}")
        else:
            print(f"   ❌ Esperado 200, recebido: {r9.status_code if r9 else 'N/A'}")
    else:
        print("   ⚠️ Dados insuficientes para testar ignorar 'editado' no payload.")

    # Resultado final
    print("\n🎯 NOTA FINAL:", nota, "/ 30")
    if nota == 30:
        print("✅ TODOS OS CRITÉRIOS ATENDIDOS CONFORME ESPECIFICAÇÃO.")
    elif nota == 0:
        print("❌ Nenhum critério atendido — verifique disponibilidade e aderência da API.")
    else:
        print("⚠️ Parcial: alguns critérios falharam. Revise os logs acima.")

if __name__ == "__main__":
    main()
