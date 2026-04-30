# ============================================================
#  FEItv - Plataforma de Informações de Vídeos
#  Projeto 1º Semestre - FEI
# ============================================================

import os

# ---------- Arquivos ----------
ARQ_USUARIOS  = "usuarios.txt"
ARQ_VIDEOS    = "videos.txt"
ARQ_LIKES     = "likes.txt"
ARQ_PLAYLISTS = "playlists.txt"

# ---------- Usuário logado (variável global) ----------
usuario_logado = None


# ============================================================
#  FUNÇÕES AUXILIARES DE ARQUIVO
# ============================================================

def ler_linhas(arquivo):
    """Lê todas as linhas de um arquivo e retorna como lista."""
    if not os.path.exists(arquivo):
        return []
    with open(arquivo, "r", encoding="utf-8") as f:
        linhas = f.readlines()
    return [l.strip() for l in linhas if l.strip() != ""]


def escrever_linhas(arquivo, linhas):
    """Sobrescreve o arquivo com a lista de linhas fornecida."""
    with open(arquivo, "w", encoding="utf-8") as f:
        for linha in linhas:
            f.write(linha + "\n")


def adicionar_linha(arquivo, linha):
    """Acrescenta uma linha ao final do arquivo."""
    with open(arquivo, "a", encoding="utf-8") as f:
        f.write(linha + "\n")


# ============================================================
#  USUÁRIOS
#  Formato no arquivo: usuario|senha
# ============================================================

def cadastrar_usuario():
    print("\n=== CADASTRAR USUÁRIO ===")
    nome = input("Nome de usuário: ").strip()
    if nome == "":
        print("[ERRO] Nome não pode ser vazio.")
        return

    # Verifica se já existe
    linhas = ler_linhas(ARQ_USUARIOS)
    for linha in linhas:
        partes = linha.split("|")
        if partes[0] == nome:
            print("[ERRO] Usuário já existe.")
            return

    senha = input("Senha: ").strip()
    if senha == "":
        print("[ERRO] Senha não pode ser vazia.")
        return

    adicionar_linha(ARQ_USUARIOS, nome + "|" + senha)
    print("[OK] Usuário '" + nome + "' cadastrado com sucesso!")


def login():
    global usuario_logado
    print("\n=== LOGIN ===")
    nome = input("Usuário: ").strip()
    senha = input("Senha: ").strip()

    linhas = ler_linhas(ARQ_USUARIOS)
    for linha in linhas:
        partes = linha.split("|")
        if partes[0] == nome and partes[1] == senha:
            usuario_logado = nome
            print("[OK] Bem-vindo, " + nome + "!")
            return

    print("[ERRO] Usuário ou senha incorretos.")


def logout():
    global usuario_logado
    print("\n[OK] Saindo da conta de " + usuario_logado + ".")
    usuario_logado = None


# ============================================================
#  VÍDEOS
#  Formato: id|titulo|tipo|genero|ano|sinopse
#  tipo: Filme ou Serie
# ============================================================

def carregar_videos():
    """Retorna lista de dicionários com os vídeos."""
    videos = []
    linhas = ler_linhas(ARQ_VIDEOS)
    for linha in linhas:
        partes = linha.split("|")
        if len(partes) == 6:
            v = {
                "id":      partes[0],
                "titulo":  partes[1],
                "tipo":    partes[2],
                "genero":  partes[3],
                "ano":     partes[4],
                "sinopse": partes[5]
            }
            videos.append(v)
    return videos


def exibir_video(v):
    """Imprime as informações de um vídeo formatado."""
    print("  ID      : " + v["id"])
    print("  Título  : " + v["titulo"])
    print("  Tipo    : " + v["tipo"])
    print("  Gênero  : " + v["genero"])
    print("  Ano     : " + v["ano"])
    print("  Sinopse : " + v["sinopse"])
    print("  Curtidas: " + str(contar_curtidas(v["id"])))
    print("  " + "-" * 40)


def buscar_video():
    print("\n=== BUSCAR VÍDEO ===")
    termo = input("Digite o nome (ou parte do nome): ").strip().lower()
    if termo == "":
        print("[AVISO] Nenhum termo informado.")
        return

    videos = carregar_videos()
    encontrados = []
    for v in videos:
        if termo in v["titulo"].lower():
            encontrados.append(v)

    if len(encontrados) == 0:
        print("[AVISO] Nenhum vídeo encontrado para '" + termo + "'.")
    else:
        print("\n" + str(len(encontrados)) + " resultado(s):\n")
        for v in encontrados:
            exibir_video(v)


def listar_todos_videos():
    print("\n=== TODOS OS VÍDEOS ===")
    videos = carregar_videos()
    if len(videos) == 0:
        print("[AVISO] Nenhum vídeo no catálogo.")
        return
    for v in videos:
        exibir_video(v)


# ============================================================
#  LIKES
#  Formato: usuario|id_video
# ============================================================

def contar_curtidas(id_video):
    linhas = ler_linhas(ARQ_LIKES)
    contagem = 0
    for linha in linhas:
        partes = linha.split("|")
        if partes[1] == id_video:
            contagem += 1
    return contagem


def ja_curtiu(usuario, id_video):
    linhas = ler_linhas(ARQ_LIKES)
    for linha in linhas:
        partes = linha.split("|")
        if partes[0] == usuario and partes[1] == id_video:
            return True
    return False


def curtir_descurtir():
    print("\n=== CURTIR / DESCURTIR ===")
    id_video = input("ID do vídeo: ").strip()

    # Verifica se o vídeo existe
    videos = carregar_videos()
    video_existe = False
    for v in videos:
        if v["id"] == id_video:
            video_existe = True
            break

    if not video_existe:
        print("[ERRO] Vídeo não encontrado.")
        return

    if ja_curtiu(usuario_logado, id_video):
        # Remove o like (descurtir)
        linhas = ler_linhas(ARQ_LIKES)
        novas = []
        for linha in linhas:
            partes = linha.split("|")
            if not (partes[0] == usuario_logado and partes[1] == id_video):
                novas.append(linha)
        escrever_linhas(ARQ_LIKES, novas)
        print("[OK] Você descurtiu o vídeo " + id_video + ".")
    else:
        adicionar_linha(ARQ_LIKES, usuario_logado + "|" + id_video)
        print("[OK] Você curtiu o vídeo " + id_video + "!")


# ============================================================
#  PLAYLISTS
#  Formato no arquivo: usuario|nome_playlist|id1,id2,id3
#  Se não tiver vídeos: usuario|nome_playlist|
# ============================================================

def carregar_playlists_usuario(usuario):
    """Retorna lista de dicts das playlists do usuário logado."""
    playlists = []
    linhas = ler_linhas(ARQ_PLAYLISTS)
    for linha in linhas:
        partes = linha.split("|")
        if len(partes) == 3 and partes[0] == usuario:
            ids = []
            if partes[2] != "":
                ids = partes[2].split(",")
            playlists.append({"nome": partes[1], "ids": ids})
    return playlists


def salvar_playlists_usuario(usuario, playlists):
    """Salva todas as playlists (mantendo as de outros usuários)."""
    linhas = ler_linhas(ARQ_PLAYLISTS)
    # Remove linhas do usuário atual
    outras = []
    for linha in linhas:
        partes = linha.split("|")
        if partes[0] != usuario:
            outras.append(linha)
    # Adiciona as novas
    for p in playlists:
        linha = usuario + "|" + p["nome"] + "|" + ",".join(p["ids"])
        outras.append(linha)
    escrever_linhas(ARQ_PLAYLISTS, outras)


def listar_playlists():
    playlists = carregar_playlists_usuario(usuario_logado)
    if len(playlists) == 0:
        print("  Você não tem playlists ainda.")
        return
    for i in range(len(playlists)):
        p = playlists[i]
        print("  [" + str(i + 1) + "] " + p["nome"] + " (" + str(len(p["ids"])) + " vídeo(s))")


def criar_playlist():
    print("\n=== CRIAR PLAYLIST ===")
    nome = input("Nome da playlist: ").strip()
    if nome == "":
        print("[ERRO] Nome não pode ser vazio.")
        return

    playlists = carregar_playlists_usuario(usuario_logado)
    for p in playlists:
        if p["nome"].lower() == nome.lower():
            print("[ERRO] Já existe uma playlist com esse nome.")
            return

    playlists.append({"nome": nome, "ids": []})
    salvar_playlists_usuario(usuario_logado, playlists)
    print("[OK] Playlist '" + nome + "' criada!")


def editar_playlist():
    print("\n=== EDITAR NOME DA PLAYLIST ===")
    playlists = carregar_playlists_usuario(usuario_logado)
    if len(playlists) == 0:
        print("[AVISO] Você não tem playlists.")
        return

    listar_playlists()
    escolha = input("Número da playlist: ").strip()

    if not escolha.isdigit():
        print("[ERRO] Entrada inválida.")
        return

    idx = int(escolha) - 1
    if idx < 0 or idx >= len(playlists):
        print("[ERRO] Número inválido.")
        return

    novo_nome = input("Novo nome: ").strip()
    if novo_nome == "":
        print("[ERRO] Nome não pode ser vazio.")
        return

    playlists[idx]["nome"] = novo_nome
    salvar_playlists_usuario(usuario_logado, playlists)
    print("[OK] Playlist renomeada para '" + novo_nome + "'.")


def excluir_playlist():
    print("\n=== EXCLUIR PLAYLIST ===")
    playlists = carregar_playlists_usuario(usuario_logado)
    if len(playlists) == 0:
        print("[AVISO] Você não tem playlists.")
        return

    listar_playlists()
    escolha = input("Número da playlist para excluir: ").strip()

    if not escolha.isdigit():
        print("[ERRO] Entrada inválida.")
        return

    idx = int(escolha) - 1
    if idx < 0 or idx >= len(playlists):
        print("[ERRO] Número inválido.")
        return

    nome = playlists[idx]["nome"]
    confirma = input("Confirma exclusão de '" + nome + "'? (s/n): ").strip().lower()
    if confirma == "s":
        playlists.pop(idx)
        salvar_playlists_usuario(usuario_logado, playlists)
        print("[OK] Playlist '" + nome + "' excluída.")
    else:
        print("[AVISO] Operação cancelada.")


def adicionar_video_playlist():
    print("\n=== ADICIONAR VÍDEO À PLAYLIST ===")
    playlists = carregar_playlists_usuario(usuario_logado)
    if len(playlists) == 0:
        print("[AVISO] Você não tem playlists. Crie uma primeiro.")
        return

    listar_playlists()
    escolha = input("Número da playlist: ").strip()

    if not escolha.isdigit():
        print("[ERRO] Entrada inválida.")
        return

    idx = int(escolha) - 1
    if idx < 0 or idx >= len(playlists):
        print("[ERRO] Número inválido.")
        return

    id_video = input("ID do vídeo a adicionar: ").strip()

    # Verifica se vídeo existe
    videos = carregar_videos()
    existe = False
    for v in videos:
        if v["id"] == id_video:
            existe = True
            break
    if not existe:
        print("[ERRO] Vídeo não encontrado no catálogo.")
        return

    if id_video in playlists[idx]["ids"]:
        print("[AVISO] Vídeo já está nessa playlist.")
        return

    playlists[idx]["ids"].append(id_video)
    salvar_playlists_usuario(usuario_logado, playlists)
    print("[OK] Vídeo " + id_video + " adicionado à playlist '" + playlists[idx]["nome"] + "'.")


def remover_video_playlist():
    print("\n=== REMOVER VÍDEO DA PLAYLIST ===")
    playlists = carregar_playlists_usuario(usuario_logado)
    if len(playlists) == 0:
        print("[AVISO] Você não tem playlists.")
        return

    listar_playlists()
    escolha = input("Número da playlist: ").strip()

    if not escolha.isdigit():
        print("[ERRO] Entrada inválida.")
        return

    idx = int(escolha) - 1
    if idx < 0 or idx >= len(playlists):
        print("[ERRO] Número inválido.")
        return

    p = playlists[idx]
    if len(p["ids"]) == 0:
        print("[AVISO] Essa playlist está vazia.")
        return

    print("Vídeos na playlist:")
    for vid_id in p["ids"]:
        print("  - " + vid_id)

    id_video = input("ID do vídeo a remover: ").strip()
    if id_video not in p["ids"]:
        print("[ERRO] Vídeo não encontrado nessa playlist.")
        return

    p["ids"].remove(id_video)
    salvar_playlists_usuario(usuario_logado, playlists)
    print("[OK] Vídeo " + id_video + " removido da playlist.")


def ver_playlist():
    print("\n=== VER PLAYLIST ===")
    playlists = carregar_playlists_usuario(usuario_logado)
    if len(playlists) == 0:
        print("[AVISO] Você não tem playlists.")
        return

    listar_playlists()
    escolha = input("Número da playlist: ").strip()

    if not escolha.isdigit():
        print("[ERRO] Entrada inválida.")
        return

    idx = int(escolha) - 1
    if idx < 0 or idx >= len(playlists):
        print("[ERRO] Número inválido.")
        return

    p = playlists[idx]
    print("\nPlaylist: " + p["nome"])
    if len(p["ids"]) == 0:
        print("  (vazia)")
        return

    videos = carregar_videos()
    for vid_id in p["ids"]:
        for v in videos:
            if v["id"] == vid_id:
                exibir_video(v)
                break


# ============================================================
#  DADOS INICIAIS (seed)
#  Popula o catálogo de vídeos se estiver vazio
# ============================================================

def criar_dados_iniciais():
    if not os.path.exists(ARQ_VIDEOS) or os.path.getsize(ARQ_VIDEOS) == 0:
        videos_iniciais = [
            "V001|Interestelar|Filme|Ficção Científica|2014|Astronautas viajam por um buraco de minhoca em busca de um novo lar para a humanidade.",
            "V002|Breaking Bad|Serie|Drama/Crime|2008|Um professor de química se torna um fabricante de metanfetamina após ser diagnosticado com câncer.",
            "V003|Parasita|Filme|Suspense|2019|Uma família pobre se infiltra na vida de uma família rica com consequências imprevisíveis.",
            "V004|Dark|Serie|Ficção Científica|2017|Quatro famílias de uma cidade alemã são conectadas por um mistério de viagem no tempo.",
            "V005|O Poderoso Chefão|Filme|Drama/Crime|1972|A história da família Corleone e sua ascensão no crime organizado americano.",
            "V006|Stranger Things|Serie|Terror/Ficção|2016|Um grupo de crianças enfrenta forças sobrenaturais em uma pequena cidade dos anos 80.",
            "V007|Oppenheimer|Filme|Drama Histórico|2023|A história do físico que liderou o projeto que criou a primeira bomba atômica.",
            "V008|La Casa de Papel|Serie|Ação/Crime|2017|Um grupo de ladrões executa um roubo milionário à Casa da Moeda da Espanha."
        ]
        escrever_linhas(ARQ_VIDEOS, videos_iniciais)
        print("[INFO] Catálogo de vídeos criado com 8 títulos.")


# ============================================================
#  MENUS
# ============================================================

def menu_playlists():
    while True:
        print("\n--- GERENCIAR PLAYLISTS ---")
        print("1. Ver minhas playlists")
        print("2. Criar playlist")
        print("3. Editar nome da playlist")
        print("4. Excluir playlist")
        print("5. Adicionar vídeo à playlist")
        print("6. Remover vídeo da playlist")
        print("0. Voltar")
        opcao = input("Escolha: ").strip()

        if opcao == "1":
            ver_playlist()
        elif opcao == "2":
            criar_playlist()
        elif opcao == "3":
            editar_playlist()
        elif opcao == "4":
            excluir_playlist()
        elif opcao == "5":
            adicionar_video_playlist()
        elif opcao == "6":
            remover_video_playlist()
        elif opcao == "0":
            break
        else:
            print("[ERRO] Opção inválida.")


def menu_logado():
    while True:
        print("\n========== FEItv ==========")
        print("Usuário: " + usuario_logado)
        print("1. Buscar vídeo por nome")
        print("2. Listar todos os vídeos")
        print("3. Curtir / Descurtir vídeo")
        print("4. Gerenciar playlists")
        print("0. Sair da conta")
        opcao = input("Escolha: ").strip()

        if opcao == "1":
            buscar_video()
        elif opcao == "2":
            listar_todos_videos()
        elif opcao == "3":
            curtir_descurtir()
        elif opcao == "4":
            menu_playlists()
        elif opcao == "0":
            logout()
            break
        else:
            print("[ERRO] Opção inválida.")


def menu_principal():
    while True:
        print("\n========== FEItv ==========")
        print("1. Cadastrar usuário")
        print("2. Login")
        print("0. Sair do programa")
        opcao = input("Escolha: ").strip()

        if opcao == "1":
            cadastrar_usuario()
        elif opcao == "2":
            login()
            if usuario_logado is not None:
                menu_logado()
        elif opcao == "0":
            print("\nAté logo!")
            break
        else:
            print("[ERRO] Opção inválida.")


# ============================================================
#  INÍCIO DO PROGRAMA
# ============================================================

criar_dados_iniciais()
menu_principal()
