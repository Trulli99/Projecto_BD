# =============================================================================================
# =============================================================================================

# Coimbra Run Club (CRC)
# Bases de Dados - LEEC/UC
# 2017246934 - Gonçalo Arsénio
# 2017261525 - Pedro Teixeira

# =============================================================================================
# =============================================================================================

from ast import While
import hashlib
from pickle import FALSE  # Encriptar
from re import X  
# from this import d
import psycopg2

# serve para esconder os inputs das passwords ( pip install maskpass )
import maskpass

import random

# from datetime
import datetime  # Permite trabalhar com datas
from datetime import timedelta
from dateutil.relativedelta import relativedelta
# trabalhar com datas (pip install python-dateutil)

# ( pip install names )
import names

import os  # Permite fazer clear à janela

# =============================================================================================
# =============================================================================================

semana = ("Segunda", 
          "Terça", 
          "Quarta", 
          "Quinta", 
          "Sexta", 
          "Sábado",
          "Domingo")  # Array com os dias da semana (Segunda = 0)

# =============================================================================================
# =============================================================================================

def clear():
    return os.system('cls')

# =============================================================================================
# =============================================================================================

def limparjanela(username):
    #def clear(): return os.system('cls')  # Estas duas linhas
    clear()  # Apagam a janela
    updatedates()
    updatetempos()
    print(" ")
    diadasemana = semana[datetime.datetime.now().weekday()]
    print(datetime.datetime.now().strftime('%Y-%m-%d ======== COIMBRA RUN CLUB ======== %H:%M:%S'))
    # Mostra a data e hora atuais
    print("@" + username + " - " + converteusernameparanome(username) + " " * (50 - (len(diadasemana) + len(username) + len(converteusernameparanome(username)))) + diadasemana)  # Imprimem o dia da semana atual
    print(" ")

# =============================================================================================
# =============================================================================================

def menuinicial():

    clear()  # Apagam a janela
    print(" ")
    print(datetime.datetime.now().strftime('%Y-%m-%d ======== COIMBRA RUN CLUB ======== %H:%M:%S'))
    print(" ")
    print("MENU INICIAL -----------------------------------------")
    print("[M] - Log in (MEMBRO)")
    print("[A] - Log in (ADMIN)")
    print("[R] - Registar")
    print("------------------------------------------------------")
    print(" ")

    OPCAO = input('Selecionar opcao: ')
    OPCAO = OPCAO.upper()
    clear()
    if OPCAO == 'M':

        membro = loginmembro()
        
        if(membro == 0):
            input("Pressione Enter para continuar...")
            menuinicial()
        else:
            membro = converteemailparausername(membro)
            menumembro(membro)
    
    elif OPCAO == 'A':
        admin = loginadmin()
            
        if(admin == 0):
            input("Pressione Enter para continuar...")
            menuinicial()
        else:
            admin = converteemailparausername(admin)
            menuadmin(admin)
        
    elif OPCAO == 'R':
        registarmembro()
        menuinicial()
    else:
        menuinicial()

# =============================================================================================
# =============================================================================================

def loginmembro():
    clear()
    print(" ")
    print(datetime.datetime.now().strftime('%Y-%m-%d ======== COIMBRA RUN CLUB ======== %H:%M:%S'))
    print(" ")
    print("LOG IN (MEMBRO) --------------------------------------\n")

    while True:
        EMAIL = input('E-mail: ')
        EMAIL = EMAIL.lower()
        if (EMAIL == '' or ' ' in EMAIL):
            print("Não insira um campo vazio!")
        else:
            break

    while True:
        PASSWORD = maskpass.askpass(prompt="Password: ", mask="*")
        if PASSWORD == '':
            print("Não insira um campo vazio!")
        else:
            PASSWORD = hashlib.md5(PASSWORD.encode())
            PASSWORD = PASSWORD.hexdigest()
            break

    if verifica_login_membro(EMAIL, PASSWORD) == 1:
        print("Login válido!")
        return EMAIL
    elif verifica_login_membro(EMAIL, PASSWORD) == 0:
        print("Login inválido")
    
        return 0
    
# =============================================================================================
# =============================================================================================

def menumembro(membro):

    limparjanela(membro)

    print("MENU MEMBRO ------------------------------------------")
    print("")
    print("[T] - Treinos")
    print("[P] - Provas")
    print("[I] - Inscrições")
    print("[C] - Classificações")
    print("[M] - Mensagens")
    print("[S] - Sair") 
    print(" ")
    print("------------------------------------------------------")
    print(" ")
    OPCAO = input('Selecionar opcao: ')
    OPCAO = OPCAO.upper()

    if OPCAO == 'T':
        menu_treino(membro)
    elif OPCAO == 'P':
        menu_provas(membro)
    elif OPCAO == 'I':
        menu_inscricoes(membro)
    elif OPCAO == 'C':
        menu_classificacoes(membro)
    elif OPCAO == 'M':
        limparjanela(membro)
        listarMensagensRecebidas(converteusernameparaid(membro))

        while True:
            print(" ")
            print("Quer abrir alguma mensagem?")
            print("[S] - Sim")
            print("[N] - Não")
            print(" ")
            RESPOSTA = input('Opção: ')
            RESPOSTA = RESPOSTA.upper()
            if (RESPOSTA != 'S' and RESPOSTA != 'N'):
                print("Insira uma opção válida!")
            else:
                break
        if RESPOSTA == 'S':
            while True:
                IDMENSAGEM = int(input("ID da Mensagem: "))
                EXISTE = verifica_mensagem(IDMENSAGEM, converteusernameparaid(membro))
                if (EXISTE != 1):
                    print("Insira uma opção válida!")
                else:
                    break
            limparjanela(membro)
            abrirMensagem(converteusernameparaid(membro), IDMENSAGEM)
            print(" ")
            input("Pressione Enter para continuar...")
            menumembro(membro)

        else:
            menumembro(membro)
    elif OPCAO == 'S':
        print("selecionou S")
        menuinicial()
    else:
        menumembro(membro)

# =============================================================================================
# =============================================================================================

def desinscreveProva(membro):
    idmembro = converteusernameparaid(membro)
    try:
        conn = psycopg2.connect(user="postgres",
                                password="postgres",
                                host="localhost",
                                port="5433",
                                database="CRC") 

        cur = conn.cursor()

        while True:
            valid = False
            while not valid: #loop until the user enters a valid int
                try:
                    idprova = int(input("\nIndique o id da prova da qual pretende desinscrever-se:"))
                    valid = True #if this point is reached, x is a valid int
                except ValueError:
                    print('Introduza apenas numero inteiros\n')

            cur.execute("SELECT DISTINCT corridas.id "
                        "FROM corridas, provas, inscricoes "
                        "WHERE corridas.id = provas.corridas_id AND inscricoes.corridas_id = corridas.id AND corridas.data_corrida > '{0}' "
                        "AND membros_utilizadores_id = (Select id from utilizadores where username = '{1}') AND provas.corridas_id = {2} ".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),membro,idprova))     
            conn.commit()

            i = 0
            for linha in cur.fetchall():
                i+=1 

            if i == 0:
                print("Introduza uma opção válida.")
            else:
                break

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
    finally:
        # closing database connection.
        if(conn):
            cur.close()
            conn.close()
    
    desinscreve(idmembro,idprova)

# =============================================================================================
# =============================================================================================

def desinscreveTreino(membro):
    idmembro = converteusernameparaid(membro)
    try:
        conn = psycopg2.connect(user="postgres",
                                password="postgres",
                                host="localhost",
                                port="5433",
                                database="CRC") 

        cur = conn.cursor()

        while True:
            valid = False
            while not valid: #loop until the user enters a valid int
                try:
                    idtreino = int(input("\nIndique o id do treino do qual pretende desinscrever-se:"))
                    valid = True #if this point is reached, x is a valid int
                except ValueError:
                    print('Introduza apenas numero inteiros\n')

            cur.execute("SELECT DISTINCT corridas.id "
                        "FROM corridas, treinos, inscricoes "
                        "WHERE corridas.id = treinos.corridas_id AND inscricoes.corridas_id = corridas.id AND corridas.data_corrida > '{0}' "
                        "AND membros_utilizadores_id = (Select id from utilizadores where username = '{1}') AND pago = true AND treinos.corridas_id = {2}".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),membro,idtreino))   
            conn.commit()

            i = 0
            for linha in cur.fetchall():
                i+=1 

            if i == 0:
                print("Introduza uma opção válida.")
            else:
                break

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
    finally:
        # closing database connection.
        if(conn):
            cur.close()
            conn.close()
    
    desinscreve(idmembro,idtreino)

# =============================================================================================
# =============================================================================================

def classificacoesPessoais(membro):
    try:
        conn = psycopg2.connect(user="postgres",
                                password="postgres",
                                host="localhost",
                                port="5433",
                                database="CRC") 

        cur = conn.cursor()

        limparjanela(membro)
        #inicio8
        cur.execute("SELECT tempo_seg, provas_corridas_id, corridas.sito, corridas.km "
                    "FROM hist_de_tempos, provas, corridas "
                    "WHERE provas_corridas_id = provas.corridas_id AND  corridas.id = provas_corridas_id "
                    "AND membros_utilizadores_id = (SELECT id FROM utilizadores WHERE username = '{0}')",format(membro))            
        conn.commit()


        for linha in cur.fetchall():
            x1 = linha[0] # tempo
            x2 = linha[1] # id prova
            x3 = linha[2] # local
            x4 = linha[3] # distancia

            print("Id da prova:",x1,"| Local:",x3,"| Distância:",x4," | Tempo:",x2,"segundos")
    
    #fim8
    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
    finally:
        # closing database connection.
        if(conn):
            cur.close()
            conn.close()

# =============================================================================================
# =============================================================================================

def menu_inscricoes(membro):
    limparjanela(membro)
    print("MENU INSCRIÇÕES --------------------------------------")
    print("")
    print("[P] - Provas")
    print("[T] - Treinos")
    print("[H] - Histórico")
    print("[S] - Sair")
    print(" ")

    OPCAO = input('Selecionar opcao: ')
    OPCAO = OPCAO.upper()

    if OPCAO == 'P':
        print("selecionou P")
        crit = pesquisa_ordenar(membro)
        pesq = asc_desc(membro)

        limparjanela(membro)
        provasInscrito(membro,crit,pesq)
        input("Pressione Enter para continuar...")
        while True:
            op = input('Pretende deinscrever-se de alguma prova? [S/N]: ')
            op = op.upper()
            if op == 'S':
                desinscreveProva(membro)
                input("Pressione Enter para continuar...")
                break
            if op == 'N':
                break
        menu_inscricoes(membro)
    elif OPCAO == 'T':
        print("selecionou T")
        treinosInscrito(membro)
        input("Pressione Enter para continuar...")

        #inicio9
        while True:
            op = input('Pretende deinscrever-se de algum treino? [S/N]: ')
            op = op.upper()
            if op == 'S':
                desinscreveTreino(membro)
                input("Pressione Enter para continuar...")
                break
            if op == 'N':
                break

        menu_inscricoes(membro)
    elif OPCAO == 'H':
        print("selecionou H")

        while True:
            print("\n[P] - Provas")
            print("[T] - Treinos\n")
            op = input('Selecionar opcao:')
            op = op.upper()

            if op == 'P':
                while True:
                    print("")
                    print("Distância:")
                    print("[A] - 1km")
                    print("[B] - 5km")
                    print("[C] - 10km")
                    print("[D] - 20km")
                    print("[E] - 40km (maratona)")
                    print(" ")

                    opdist = input('Selecionar opcao: ')
                    opdist = opdist.upper()

                    if opdist == 'A':
                        dist = '1'
                        break
                    elif opdist == 'B':
                        dist = '5'
                        break
                    elif opdist == 'C':
                        dist = '10'
                        break
                    elif opdist == 'D':
                        dist = '20'
                        break
                    elif opdist == 'E':
                        dist = '40'
                        break
                    else:
                        print("Opcao invalida")

                histProvas(membro,dist)
                input("Pressione Enter para continuar...")
                menu_inscricoes(membro)
            elif op == 'T':
                histTreinos(membro)
                input("Pressione Enter para continuar...")
                menu_inscricoes(membro)
    elif OPCAO == 'S':
        print("selecionou S")
        menumembro(membro)
    else:
        menu_inscricoes(membro)

# =============================================================================================
# =============================================================================================

def histProvas(membro,dist):
    try:
        conn = psycopg2.connect(user="postgres",
                                password="postgres",
                                host="localhost",
                                port="5433",
                                database="CRC") 

        cur = conn.cursor()

        limparjanela(membro)
        print("\nHistórico de Provas:\n")

        cur.execute("SELECT DISTINCT corridas.id, corridas.sitio, corridas.km, corridas.lim_data, corridas.data_corrida, corridas.lim_inscritos, corridas.num_inscritos, provas.valor "
                    "FROM corridas, provas, inscricoes "
                    "WHERE corridas.id = provas.corridas_id AND inscricoes.corridas_id = corridas.id AND corridas.data_corrida < '{0}' "
                    "AND membros_utilizadores_id = (Select id from utilizadores where username = '{1}') AND pago = true "
                    "AND km = {2} ".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),membro,dist))            
        conn.commit()


        for linha in cur.fetchall():
            x1 = linha[0]  # id
            x2 = linha[1]  # local
            x3 = linha[2]  # distancia
            x4 = linha[3]  # data limite
            x5 = linha[4]  # data corrida
            x6 = linha[5]  # limite inscritos
            x7 = linha[6]  # numero inscritos
            x8 = linha[7]  # valor

            print("DISTANCIA:", x3, "km\n| Id:", x1, "| Local:", x2, "| Distancia:", x3, "km | Data:", x5,
                  "\n| Participantes:", x7, "| Pagou:", x8,"\n")
    

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
    finally:
        # closing database connection.
        if(conn):
            cur.close()
            conn.close()

# =============================================================================================
# =============================================================================================

def histTreinos(membro):
    try:
        conn = psycopg2.connect(user="postgres",
                                password="postgres",
                                host="localhost",
                                port="5433",
                                database="CRC") 

        cur = conn.cursor()

        limparjanela(membro)
        print("\nHistórico de Treinos:\n")

        cur.execute("SELECT DISTINCT corridas.id, corridas.sitio, corridas.km, corridas.lim_data, corridas.data_corrida, corridas.lim_inscritos, corridas.num_inscritos, treinos.rep, treinadores_id "
                    "FROM corridas, treinos, inscricoes "
                    "WHERE corridas.id = treinos.corridas_id AND inscricoes.corridas_id = corridas.id AND corridas.data_corrida > '{0}' "
                    "AND membros_utilizadores_id = (Select id from utilizadores where username = '{1}') AND pago = true".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),membro))   
            
        conn.commit()

        for linha in cur.fetchall():
            x1 = linha[0]  # id
            x2 = linha[1]  # local
            x3 = linha[2]  # distancia
            x4 = linha[3]  # data limite
            x5 = linha[4]  # data corrida
            x6 = linha[5]  # limite inscritos
            x7 = linha[6]  # numero inscritos
            x8 = linha[7]  # repetitivo
            x9 = linha[8]  #id treinador

            if x9 == None:
                treinador = "Sem treinador"
            
            else:
                cur.execute("SELECT nome FROM treinadores WHERE id = {0}".format(x9))
                for linha1 in cur.fetchall():
                    treinador = linha1[0]

            if x8 == "S":
                REPETE = "Semanalmente"
            elif x8 == "M":
                REPETE = "Mensalmente"
            elif x8 == "N":
                REPETE = "Não"

            print("ID:", x1, "\n| Local:", x2, "| Distancia:", x3, "km | Data:", x5,
                  "\n| Participantes:", x7, "\n| Repete:", REPETE,"| Treinador:",treinador,"\n")

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
    finally:
        # closing database connection.
        if(conn):
            cur.close()
            conn.close()

# =============================================================================================
# =============================================================================================

def provasInscrito(membro,pesq,crit):
    try:
        conn = psycopg2.connect(user="postgres",
                                password="postgres",
                                host="localhost",
                                port="5433",
                                database="CRC") 

        cur = conn.cursor()

        cur.execute("SELECT DISTINCT corridas.id, corridas.sitio, corridas.km, corridas.lim_data, corridas.data_corrida, corridas.lim_inscritos, corridas.num_inscritos, inscricoes.pago "
                    "FROM corridas, provas, inscricoes "
                    "WHERE corridas.id = provas.corridas_id AND inscricoes.corridas_id = corridas.id AND corridas.data_corrida > '{0}' "
                    "AND membros_utilizadores_id = (Select id from utilizadores where username = '{1}') "
                    "ORDER BY {2} {3} ;".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),membro,pesq,crit))            
        conn.commit()
        i = 0

        for linha in cur.fetchall():
            x1 = linha[0]  # id
            x2 = linha[1]  # local
            x3 = linha[2]  # distancia
            x4 = linha[3]  # data limite
            x5 = linha[4]  # data corrida
            x6 = linha[5]  # limite inscritos
            x7 = linha[6]  # numero inscritos
            x8 = linha[7]  # pago

            if x8 == False:
                x8 = "Não"
                i+=1
            else:
                x8 = "Sim"

            print("ID:", x1, "\n| Local:", x2, "| Distancia:", x3, "km | Data:", x5,
                  "\n| Inscritos:", x7, "| Pago:", x8,"\n")
        
        if(i>0):
            print("Tem inscricoes por pagar. Por favor faça-o, caso contrário a sua inscrição será cancelada.\n")

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
    finally:
        # closing database connection.
        if(conn):
            cur.close()
            conn.close()

# =============================================================================================
# =============================================================================================

def treinosInscrito(membro):
    limparjanela(membro)
    try:
        conn = psycopg2.connect(user="postgres",
                                password="postgres",
                                host="localhost",
                                port="5433",
                                database="CRC") 

        cur = conn.cursor()

        cur.execute("SELECT DISTINCT corridas.id, corridas.sitio, corridas.km, corridas.lim_data, corridas.data_corrida, corridas.lim_inscritos, corridas.num_inscritos, treinos.rep, treinadores_id "
                    "FROM corridas, treinos, inscricoes "
                    "WHERE corridas.id = treinos.corridas_id AND inscricoes.corridas_id = corridas.id AND corridas.data_corrida > '{0}' "
                    #inicio4
                    "AND membros_utilizadores_id = (Select id from utilizadores where username = '{1}') AND pago = true".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),membro))    
                    #fim4        
        conn.commit()

        for linha in cur.fetchall():
            x1 = linha[0]  # id
            x2 = linha[1]  # local
            x3 = linha[2]  # distancia
            x4 = linha[3]  # data limite
            x5 = linha[4]  # data corrida
            x6 = linha[5]  # limite inscritos
            x7 = linha[6]  # numero inscritos
            x8 = linha[7]  # repetitivo
            x9 = linha[8]  #id treinador

            if x9 == None:
                treinador = "Sem treinador"
            
            else:
                cur.execute("SELECT nome FROM treinadores WHERE id = {0}".format(x9))
                for linha1 in cur.fetchall():
                    treinador = linha1[0]

            if x8 == "S":
                REPETE = "Semanalmente"
            elif x8 == "M":
                REPETE = "Mensalmente"
            elif x8 == "N":
                REPETE = "Não"

            #inicio4
            print("ID:", x1, "\n| Local:", x2, "| Distancia:", x3, "km | Data:", x5,
                  "\n| Inscritos:", x7, "\n| Repete:", REPETE,"| Treinador:",treinador,"\n")
            #fim4

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
    finally:
        # closing database connection.
        if(conn):
            cur.close()
            conn.close()

# =============================================================================================
# =============================================================================================

def menu_provas(membro):

    limparjanela(membro)
    print("MENU PROVAS ------------------------------------------")
    print("")
    print("[L] - Listar Todos as Provas")
    print("[P] - Pesquisar Provas")
    print("[I] - Inscrições Abertas")
    print("[S] - Sair")
    print(" ")

    OPCAO = input('Selecionar opcao: ')
    OPCAO = OPCAO.upper()

    if OPCAO == 'L':
        print("selecionou L")
        crit = pesquisa_ordenar(membro)
        pesq = asc_desc(membro)
        limparjanela(membro)
        listarProvasMembro(pesq,crit)
        input("Pressione Enter para continuar...")
        
        while True:
            op = input('Pretende inscrever-se em alguma prova? [S/N]: ')
            op = op.upper()
            if op == 'S':
                inscreverProva(membro)
                break
            if op == 'N':
                break
            
        menu_provas(membro)

    elif OPCAO == 'P':
        print("selecionou P")
        menuPesquisaProvas(membro)
    elif OPCAO == 'I':
        print("selecionou I")
        listarProvasInscricoes(membro)
        input("Pressione Enter para continuar...")
        while True:
            op = input('Pretende inscrever-se em alguma prova? [S/N]: ')
            op = op.upper()
            if op == 'S':
                inscreverProva(membro)
                break
            if op == 'N':
                break
        menu_provas(membro)
    elif OPCAO == 'S':
        print("selecionou S")
        menumembro(membro)
    else:
        menu_provas(membro)

# =============================================================================================
# =============================================================================================

def inscreverProva(membro):

    id = input("\nIndique o id da prova em que se pretende inscrever: ")

    try:
        conn = psycopg2.connect(user="postgres",
                                password="postgres",
                                host="localhost",
                                port="5433",
                                database="CRC") 

        cur = conn.cursor()

        #verifica se é possivel inscrever na prova
        cur.execute("SELECT corridas.lim_inscritos, corridas.num_inscritos "
                    "FROM corridas, provas "
                    "WHERE corridas.id = provas.corridas_id AND corridas.lim_data > '{0}' AND corridas.id = {1}".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),id))     
        conn.commit()

        i = 0
        for linha in cur.fetchall():
            i = cur.rowcount
            x1 = linha[0]
            x2 = linha[1]
            
            vagas = x1-x2

            if vagas == 0:
                input("Não é possivel inscrever-se nessa prova")
                return 0
        
        if i == 0:
            input("Não é possivel inscrever-se nessa prova")
            return 0
        
        #verifica se já está inscrito na prova
        cur.execute("SELECT inscricoes.corridas_id, inscricoes.membros_utilizadores_id "
                    "FROM inscricoes, utilizadores, provas "
                    "WHERE provas.corridas_id = inscricoes.corridas_id AND membros_utilizadores_id = utilizadores.id AND username = '{0}' AND provas.corridas_id = {1}".format(membro,id))
        conn.commit()

        j = 0
        for linha1 in cur.fetchall():
            j = cur.rowcount
        
        if j == 1:
            input("Já está inscrito nesta prova")
            return 0

        # Se chegou até aqui vai então fazer a inscrição
        cur.execute("SELECT id FROM utilizadores WHERE username = '{0}';".format(membro))
        #membroID = cur.fetchone()
        for linha2 in cur.fetchall():
            membroID = linha2[0]
        conn.commit()
        
        # Confirma se pretende fazer a inscrição
        cur.execute("SELECT provas.valor, corridas.data_corrida "
                    "FROM corridas, provas "
                    "WHERE provas.corridas_id = corridas.id AND corridas.id = {0} ".format(id))
        conn.commit()
        
        for linha3 in cur.fetchall():
            x1 = linha3[0] # valor
            x2 = linha3[1] # data
        
        print("\nEsta prova tem um preço de",x1,"euros e decorre a",x2,"\n")

        while True:
            op = input("Tem a certeza que se pretende inscrever? [S/N]: ")
            op = op.upper()
            if op == 'S':
                break
            if op == 'N':
                return 0

        #Transação
        conn.autocommit = False
        cur.execute("INSERT INTO inscricoes (pago, corridas_id,membros_utilizadores_id) VALUES(FALSE,{0},{1})".format(id,membroID))
        cur.execute("UPDATE corridas SET num_inscritos = num_inscritos + 1 WHERE id = {0}".format(id))
        conn.commit()

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
        conn.rollback() #Transação
    finally:
        # closing database connection.
        if(conn):
            cur.close()
            conn.close()

# =============================================================================================
# =============================================================================================

def pesquisa_ordenar(membro):
    limparjanela(membro)
    print("Escolha o critério de ordenação: ")
    print(" ")
    print("[I] - ID")
    print("[D] - Distancia")
    print("[P] - Preço")
    print("[DT] - Data")
    print("[N] - Nome")
    print("[S] Sair")
    print(" ")

    OPCAO = input('Selecionar opcao: ')
    OPCAO = OPCAO.upper()

    if OPCAO == 'I':
        return 'id'
    elif OPCAO == 'D':
        return 'km'
    elif OPCAO == 'P':
        return 'valor'
    elif OPCAO == 'DT':
        return 'data_corrida'
    elif OPCAO == 'N':
        return 'sitio'
    else:
        menu_provas(membro)

# =============================================================================================
# =============================================================================================

def asc_desc(membro):
    limparjanela(membro)
    print("Escolha uma ordem:")
    print(" ")
    print("[A] - Ascendente")
    print("[D] - Descendente")
    print(" ")

    OPCAO = input('Selecionar opcao: ')
    OPCAO = OPCAO.upper()

    if OPCAO == 'A':
        return 'ASC'
    if OPCAO == 'D':
        return 'DESC'
    else:
        asc_desc(membro)

# =============================================================================================
# =============================================================================================

def listarProvasMembro(pesq,crit):

    try:
        conn = psycopg2.connect(user="postgres",
                                password="postgres",
                                host="localhost",
                                port="5433",
                                database="CRC") 

        cur = conn.cursor()

        #inicio2
        cur.execute("SELECT corridas.id, corridas.sitio, corridas.km, corridas.lim_data, corridas.data_corrida, corridas.lim_inscritos, corridas.num_inscritos, provas.valor "
                    "FROM corridas, provas "
                    "WHERE corridas.id = provas.corridas_id "
                    "ORDER BY {0} {1} ;".format(crit,pesq))
                
        conn.commit()


        for linha in cur.fetchall():
            x1 = linha[0]  # id
            x2 = linha[1]  # local
            x3 = linha[2]  # distancia
            x4 = linha[3]  # data limite
            x5 = linha[4]  # data corrida
            x6 = linha[5]  # limite inscritos
            x7 = linha[6]  # numero inscritos
            x8 = linha[7]  # preço da prova

            vagas = x6-x7

            print("ID:", x1, "\n| Local:", x2, "| Distancia:", x3, "km | Data:", x5,
                  "\n| Limite Inscricao:", x4, "| Vagas:", vagas, "| Valor:",x8,"\n")
        #fim2

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
    finally:
        # closing database connection.
        if(conn):
            cur.close()
            conn.close()

# =============================================================================================
# =============================================================================================

def menuPesquisaProvas(membro):

    limparjanela(membro)
    print("MENU DE PESQUISA -------------------------------------")
    print("\nPesquisar por:")
    print("")
    print("[T] - Titulo")
    print("[ID] - ID")
    print("[L] - Local")
    print("[D] - Distancia")
    print("[DT] - Data")
    print("[IDT] - Intervalo de Data")
    print("[S] - Sair")
    print(" ")

    OPCAO = input('Selecionar opcao: ')
    OPCAO = OPCAO.upper()

    if OPCAO == 'T':
        print("selecionou T")
        pesquisaProvaTitulo(membro)
        input("Pressione Enter para continuar...")

        while True:
            op = input('Pretende inscrever-se em alguma prova? [S/N]: ')
            op = op.upper()
            if op == 'S':
                inscreverProva(membro)
                break
            if op == 'N':
                break

        menuPesquisaProvas(membro)
    elif OPCAO == "ID":
        print("selecinou ID")
        pesquisaProvaID(membro)
        input("Pressione Enter para continuar...")

        while True:
            op = input('Pretende inscrever-se em alguma prova? [S/N]: ')
            op = op.upper()
            if op == 'S':
                inscreverProva(membro)
                break
            if op == 'N':
                break

        menuPesquisaProvas(membro)
    elif OPCAO == 'L':
        print("selecionou L")
        pesquisaProvaLocal(membro)
        input("Pressione Enter para continuar...")

        while True:
            op = input('Pretende inscrever-se em alguma prova? [S/N]: ')
            op = op.upper()
            if op == 'S':
                inscreverProva(membro)
                break
            if op == 'N':
                break

        menuPesquisaProvas(membro)
    elif OPCAO == 'D':
        print("selecionou D")
        pesquisaProvaDistancia(membro)
        input("Pressione Enter para continuar...")

        while True:
            op = input('Pretende inscrever-se em alguma prova? [S/N]: ')
            op = op.upper()
            if op == 'S':
                inscreverProva(membro)
                break
            if op == 'N':
                break

        menuPesquisaProvas(membro)
    elif OPCAO == 'DT':
        print("selecionou DT")
        pesquisaProvaData(membro)
        input("Pressione Enter para continuar...")

        while True:
            op = input('Pretende inscrever-se em alguma prova? [S/N]: ')
            op = op.upper()
            if op == 'S':
                inscreverProva(membro)
                break
            if op == 'N':
                break

        menuPesquisaProvas(membro)
    elif OPCAO == 'IDT':
        print("selecionou IDT")
        pesquisaProvaIntervaloData(membro)
        input("Pressione Enter para continuar...")

        while True:
            op = input('Pretende inscrever-se em alguma prova? [S/N]: ')
            op = op.upper()
            if op == 'S':
                inscreverProva(membro)
                break
            if op == 'N':
                break

        menuPesquisaProvas(membro)
    elif OPCAO == 'S':
        print("selecionou S")
        menu_provas(membro)
    else:
        menu_provas(membro)

# =============================================================================================
# =============================================================================================

def pesquisaProvaTitulo(membro):
    limparjanela(membro)
    try:
        conn = psycopg2.connect(user="postgres",
                                password="postgres",
                                host="localhost",
                                port="5433",
                                database="CRC")

        cur = conn.cursor()


        
        OP = input("Insira o titulo ou parte do titulo que pretende pesquisar: ")
        OP = OP.upper()

        
        cur.execute("SELECT corridas.id, corridas.sitio, corridas.km, corridas.lim_data, corridas.data_corrida, corridas.lim_inscritos, corridas.num_inscritos, provas.valor "
                    "FROM corridas, provas "
                    "WHERE corridas.id = provas.corridas_id AND UPPER(corridas.sitio) LIKE '%"+OP+"%' ")

        conn.commit()

        i = 0
        for linha in cur.fetchall():
            i = cur.rowcount
            x1 = linha[0]  # id
            x2 = linha[1]  # local
            x3 = linha[2]  # distancia
            x4 = linha[3]  # data limite
            x5 = linha[4]  # data corrida
            x6 = linha[5]  # limite inscritos
            x7 = linha[6]  # numero inscritos
            x8 = linha[7]  # valor

            vagas = x6-x7

            print("ID:", x1, "\n| Local:", x2, "| Distancia:", x3, "km | Data:", x5,
                  "\n| Limite Inscricao:", x4, "| Vagas:", vagas, "\n| Valor:", x8,"\n")

        if(i == 0):
            print("Não existe nenhuma prova com esse titulo")

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
    finally:
        # closing database connection.
        if(conn):
            cur.close()
            conn.close()

# =============================================================================================
# =============================================================================================

def pesquisaProvaID(membro):
    limparjanela(membro)

    try:
        conn = psycopg2.connect(user="postgres",
                                password="postgres",
                                host="localhost",
                                port="5433",
                                database="CRC") 

        cur = conn.cursor()

        OP = input("Insira o id da prova que pretende pesquisar: ")

        #inicio
        cur.execute("SELECT corridas.id, corridas.sitio, corridas.km, corridas.lim_data, corridas.data_corrida, corridas.lim_inscritos, corridas.num_inscritos, provas.valor "
                    "FROM corridas, provas "
                    "WHERE corridas.id = provas.corridas_id AND corridas.id = {0} ".format(OP))
        #fim
        conn.commit()

        i = 0
        for linha in cur.fetchall():
            i = cur.rowcount
            x1 = linha[0]  # id
            x2 = linha[1]  # local
            x3 = linha[2]  # distancia
            x4 = linha[3]  # data limite
            x5 = linha[4]  # data corrida
            x6 = linha[5]  # limite inscritos
            x7 = linha[6]  # numero inscritos
            x8 = linha[7]  # valor

            vagas = x6-x7

            print("ID:", x1, "\n| Local:", x2, "| Distancia:", x3, "km | Data:", x5,
                  "\n| Limite Inscricao:", x4, "| Vagas:", vagas, "\n| Valor:", x8,"\n")

        if(i == 0):
            print("Não existe nenhuma prova com esse id")

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
    finally:
        # closing database connection.
        if(conn):
            cur.close()
            conn.close()

# =============================================================================================
# =============================================================================================

def pesquisaProvaLocal(membro):
    limparjanela(membro)
    try:
        conn = psycopg2.connect(user="postgres",
                                password="postgres",
                                host="localhost",
                                port="5433",
                                database="CRC") 

        cur = conn.cursor()

        OP = input("Insira o local da prova que pretende pesquisar: ")
        OP = OP.upper()

        cur.execute("SELECT corridas.id, corridas.sitio, corridas.km, corridas.lim_data, corridas.data_corrida, corridas.lim_inscritos, corridas.num_inscritos, provas.valor "
                    "FROM corridas, provas "
                    "WHERE corridas.id = provas.corridas_id AND UPPER(corridas.sitio) LIKE '%"+OP+"'")
        
        conn.commit()

        i = 0
        for linha in cur.fetchall():
            i = cur.rowcount
            x1 = linha[0]  # id
            x2 = linha[1]  # local
            x3 = linha[2]  # distancia
            x4 = linha[3]  # data limite
            x5 = linha[4]  # data corrida
            x6 = linha[5]  # limite inscritos
            x7 = linha[6]  # numero inscritos
            x8 = linha[7]  # valor

            vagas = x6-x7

            print("ID:", x1, "\n| Local:", x2, "| Distancia:", x3, "km | Data:", x5,
                  "\n| Limite Inscricao:", x4, "| Vagas:", vagas, "\n| Valor:", x8,"\n")

        if(i == 0):
            print("Não existe nenhuma prova nesse local")

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
    finally:
        # closing database connection.
        if(conn):
            cur.close()
            conn.close()

# =============================================================================================
# =============================================================================================

def pesquisaProvaDistancia(membro):
    limparjanela(membro)
    try:
        conn = psycopg2.connect(user="postgres",
                                password="postgres",
                                host="localhost",
                                port="5433",
                                database="CRC") 

        cur = conn.cursor()

        while True:
            print("")
            print("Distância:")
            print("[A] - 1km")
            print("[B] - 5km")
            print("[C] - 10km")
            print("[D] - 20km")
            print("[E] - 40km (maratona)")
            print("------------------------------------------------------")
            print(" ")

            OPCAO = input('Selecionar opcao: ')
            OPCAO = OPCAO.upper()

            if OPCAO == 'A':
                DISTANCIA = '1'
                break
            elif OPCAO == 'B':
                DISTANCIA = '5'
                break
            elif OPCAO == 'C':
                DISTANCIA = '10'
                break
            elif OPCAO == 'D':
                DISTANCIA = '20'
                break
            elif OPCAO == 'E':
                DISTANCIA = '40'
                break
            else:
                print("Opcao invalida")

        cur.execute("SELECT corridas.id, corridas.sitio, corridas.km, corridas.lim_data, corridas.data_corrida, corridas.lim_inscritos, corridas.num_inscritos, provas.valor "
                    "FROM corridas, provas "
                    "WHERE corridas.id = provas.corridas_id AND corridas.km = {0} ".format(DISTANCIA))
        conn.commit()

        i = 0
        for linha in cur.fetchall():
            i = cur.rowcount
            x1 = linha[0]  # id
            x2 = linha[1]  # local
            x3 = linha[2]  # distancia
            x4 = linha[3]  # data limite
            x5 = linha[4]  # data corrida
            x6 = linha[5]  # limite inscritos
            x7 = linha[6]  # numero inscritos
            x8 = linha[7]  # valor

            vagas = x6-x7

            print("ID:", x1, "\n| Local:", x2, "| Distancia:", x3, "km | Data:", x5,
                  "\n| Limite Inscricao:", x4, "| Vagas:", vagas, "\n| Valor:", x8,"\n")

        if(i == 0):
            print("Não existe nenhuma prova com essa distancia")

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
    finally:
        # closing database connection.
        if(conn):
            cur.close()
            conn.close()

# =============================================================================================
# =============================================================================================

def pesquisaProvaDataOLD(membro):
    limparjanela(membro)
    try:
        conn = psycopg2.connect(user="postgres",
                                password="postgres",
                                host="localhost",
                                port="5433",
                                database="CRC")  

        cur = conn.cursor()

        while True:
            ANO = input("Ano: ")
            if (int(ANO) < int(datetime.datetime.now().strftime('%Y'))):
                print("Não pode escolher uma data do passado!")
            else:
                break

        while True:
            MES = input("Mes: ")
            if int(MES) <= 9: 
                MES = "0"+str(int(MES))
            if (int(MES) < 1 or int(str(ANO)+str(MES)) < int(datetime.datetime.now().strftime('%Y%m'))):
                print("Não pode escolher uma data do passado!")
            else:
                break

        while True:
            DIA = input("Dia: ")
            if int(DIA) <= 9: 
                DIA = "0"+str(int(DIA))
            if (int(DIA) < 1 or int(str(ANO)+str(MES)+str(DIA)) < int(datetime.datetime.now().strftime('%Y%m%d'))):
                print("Não pode escolher uma data do passado!")
            else:
                break

        if datavalida(int(ANO), int(MES), int(DIA)) == False:
            print("Introduza uma data válida!")
            pesquisaTreinoData()

  
        HORA1 = '00'
        MINUTO1 = '00'
        DATACORRIDAFORMATADA1 = ANO+"-"+MES+"-"+DIA+" "+HORA1+":"+MINUTO1
        HORA2 = '23'
        MINUTO2 = '59'
        DATACORRIDAFORMATADA2 = ANO+"-"+MES+"-"+DIA+" "+HORA2+":"+MINUTO2

        cur.execute("SELECT corridas.id, corridas.sitio, corridas.km, corridas.lim_data, corridas.data_corrida, corridas.lim_inscritos, corridas.num_inscritos, provas.valor "
                    "FROM corridas, provas "
                    "WHERE corridas.id = provas.corridas_id  AND corridas.data_corrida > '{0}' AND corridas.data_corrida < '{1}'".format(DATACORRIDAFORMATADA1, DATACORRIDAFORMATADA2))


        conn.commit()

        i = 0
        for linha in cur.fetchall():
            i = cur.rowcount
            x1 = linha[0]  # id
            x2 = linha[1]  # local
            x3 = linha[2]  # distancia
            x4 = linha[3]  # data limite
            x5 = linha[4]  # data corrida
            x6 = linha[5]  # limite inscritos
            x7 = linha[6]  # numero inscritos
            x8 = linha[7]  # valor

            vagas = x6-x7

            print("ID:", x1, "\n| Local:", x2, "| Distancia:", x3, "km | Data:", x5,
                  "\n| Limite Inscricao:", x4, "| Vagas:", vagas, "\n| Valor:", x8,"\n")

        if(i == 0):
            print("Não existe nenhum treino dentro desse intervalo")

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
    finally:
        # closing database connection.
        if(conn):
            cur.close()
            conn.close()

# =============================================================================================
# =============================================================================================

def pesquisaProvaData(membro):
    limparjanela(membro)
    try:
        conn = psycopg2.connect(user="postgres",
                                password="postgres",
                                host="localhost",
                                port="5433",
                                database="CRC")  

        cur = conn.cursor()


        ANO = input("Ano: ")


        while True:
            MES = input("Mes: ")
            if int(MES) <= 9: 
                MES = "0"+str(int(MES))
            if (int(MES) < 1 ):
                print("Não pode ser negativo!")
            else:
                break

        while True:
            DIA = input("Dia: ")
            if int(DIA) <= 9: 
                DIA = "0"+str(int(DIA))
            if (int(DIA) < 1 ):
                print("Não pode ser negativo!")
            else:
                break

        if datavalida(int(ANO), int(MES), int(DIA)) == False:
            print("Introduza uma data válida!")
            pesquisaProvaData(membro)

  
        HORA1 = '00'
        MINUTO1 = '00'
        DATACORRIDAFORMATADA1 = ANO+"-"+MES+"-"+DIA+" "+HORA1+":"+MINUTO1
        HORA2 = '23'
        MINUTO2 = '59'
        DATACORRIDAFORMATADA2 = ANO+"-"+MES+"-"+DIA+" "+HORA2+":"+MINUTO2

        cur.execute("SELECT corridas.id, corridas.sitio, corridas.km, corridas.lim_data, corridas.data_corrida, corridas.lim_inscritos, corridas.num_inscritos, provas.valor "
                    "FROM corridas, provas "
                    "WHERE corridas.id = provas.corridas_id  AND corridas.data_corrida > '{0}' AND corridas.data_corrida < '{1}'".format(DATACORRIDAFORMATADA1, DATACORRIDAFORMATADA2))


        conn.commit()

        i = 0
        for linha in cur.fetchall():
            i = cur.rowcount
            x1 = linha[0]  # id
            x2 = linha[1]  # local
            x3 = linha[2]  # distancia
            x4 = linha[3]  # data limite
            x5 = linha[4]  # data corrida
            x6 = linha[5]  # limite inscritos
            x7 = linha[6]  # numero inscritos
            x8 = linha[7]  # valor

            vagas = x6-x7

            print("ID:", x1, "\n| Local:", x2, "| Distancia:", x3, "km | Data:", x5,
                  "\n| Limite Inscricao:", x4, "| Vagas:", vagas, "\n| Valor:", x8,"\n")

        if(i == 0):
            print("Não existe nenhum treino dentro desse intervalo")

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
    finally:
        # closing database connection.
        if(conn):
            cur.close()
            conn.close()

# =============================================================================================
# =============================================================================================

def pesquisaProvaIntervaloData(membro):
    limparjanela(membro)
    try:
        conn = psycopg2.connect(user="postgres",
                                password="postgres",
                                host="localhost",
                                port="5433",
                                database="CRC")  

        cur = conn.cursor()
        
        print("Data menor: ")

        ANO1 = input("Ano: ")

        while True:
            MES1 = input("Mes: ")
            if int(MES1) <= 9:
                MES1 = "0"+str(int(MES1))
            if (int(MES1) < 1 ):
                print("Não pode ser negativo!")
            else:
                break

        while True:
            DIA1 = input("Dia: ")
            if int(DIA1) <= 9:
                DIA1 = "0"+str(int(DIA1))
            if (int(DIA1) < 1 ):
                print("Não pode ser negativo!")
            else:
                break

        if datavalida(int(ANO1), int(MES1), int(DIA1)) == False:
            print("Introduza uma data válida!")
            pesquisaProvaIntervaloData(membro)

        HORA1 = '00'
        MINUTO1 = '00'
        
        DATACORRIDAFORMATADA1 = ANO1+"-"+MES1+"-"+DIA1+" "+HORA1+":"+MINUTO1

        print("Data maior: ")

        ANO2 = input("Ano: ")

        while True:
            MES2 = input("Mes: ")
            if int(MES2) <= 9:
                MES2 = "0"+str(int(MES2))
            if (int(MES2) < 1 ):
                print("Não pode ser negativo!")
            else:
                break

        while True:
            DIA2 = input("Dia: ")
            if int(DIA2) <= 9:
                DIA2 = "0"+str(int(DIA2))


            if (int(DIA2) < 1 ):
                print("Não pode ser negativo!")
            else:
                break

        if datavalida(int(ANO2), int(MES2), int(DIA2)) == False:
            print("Introduza uma data válida!")
            pesquisaProvaIntervaloData(membro)

        HORA2 = '23'
        MINUTO2 = '59'
        DATACORRIDAFORMATADA2 = ANO2+"-"+MES2+"-"+DIA2+" "+HORA2+":"+MINUTO2
     
        cur.execute("SELECT corridas.id, corridas.sitio, corridas.km, corridas.lim_data, corridas.data_corrida, corridas.lim_inscritos, corridas.num_inscritos, provas.valor "
                    "FROM corridas, provas "
                    "WHERE corridas.id = provas.corridas_id AND corridas.data_corrida BETWEEN '{0}' AND '{1}'".format(DATACORRIDAFORMATADA1, DATACORRIDAFORMATADA2))
        conn.commit()

        i = 0
        for linha in cur.fetchall():
            i = cur.rowcount
            x1 = linha[0]  # id
            x2 = linha[1]  # local
            x3 = linha[2]  # distancia
            x4 = linha[3]  # data limite
            x5 = linha[4]  # data corrida
            x6 = linha[5]  # limite inscritos
            x7 = linha[6]  # numero inscritos
            x8 = linha[7]  # valor

            vagas = x6-x7

            print("ID:", x1, "\n| Local:", x2, "| Distancia:", x3, "km | Data:", x5,
                  "\n| Limite Inscricao:", x4, "| Vagas:", vagas, "\n| Valor:", x8,"\n")

        if(i == 0):
            print("Não existe nenhuma prova nesse intervalo")

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
    finally:
        # closing database connection.
        if(conn):
            cur.close()
            conn.close()

# =============================================================================================
# =============================================================================================

def pesquisaProvaIntervaloDataOLD(membro):
    limparjanela(membro)
    try:
        conn = psycopg2.connect(user="postgres",
                                password="postgres",
                                host="localhost",
                                port="5433",
                                database="CRC")  

        cur = conn.cursor()
        
        print("Data menor: ")
        while True:
            ANO1 = input("Ano: ")
            if (int(ANO1) < int(datetime.datetime.now().strftime('%Y'))):
                print("Não pode escolher uma data do passado!")
            else:
                break

        while True:
            MES1 = input("Mes: ")
            if int(MES1) <= 9:
                MES1 = "0"+str(int(MES1))
            if (int(MES1) < 1 or int(str(ANO1)+str(MES1)) < int(datetime.datetime.now().strftime('%Y%m'))):
                print("Não pode escolher uma data do passado!")
            else:
                break

        while True:
            DIA1 = input("Dia: ")
            if int(DIA1) <= 9:
                DIA1 = "0"+str(int(DIA1))
            if (int(DIA1) < 1 or int(str(ANO1)+str(MES1)+str(DIA1)) < int(datetime.datetime.now().strftime('%Y%m%d'))):
                print("Não pode escolher uma data do passado!")
            else:
                break

        if datavalida(int(ANO1), int(MES1), int(DIA1)) == False:
            print("Introduza uma data válida!")
            pesquisaTreinoData(membro)

        HORA1 = '00'
        MINUTO1 = '00'
        
        DATACORRIDAFORMATADA1 = ANO1+"-"+MES1+"-"+DIA1+" "+HORA1+":"+MINUTO1

        print("Data maior: ")
        while True:
            ANO2 = input("Ano: ")
            if (int(ANO2) < int(datetime.datetime.now().strftime('%Y'))):
                print("Não pode escolher uma data do passado!")
            else:
                break

        while True:
            MES2 = input("Mes: ")
            if int(MES2) <= 9:
                MES2 = "0"+str(int(MES2))
            if (int(MES2) < 1 or int(str(ANO2)+str(MES2)) < int(datetime.datetime.now().strftime('%Y%m'))):
                print("Não pode escolher uma data do passado!")
            else:
                break

        while True:
            DIA2 = input("Dia: ")
            if int(DIA2) <= 9:
                DIA2 = "0"+str(int(DIA2))
            if (int(DIA2) < 1 or int(str(ANO2)+str(MES2)+str(DIA2)) < int(datetime.datetime.now().strftime('%Y%m%d'))):
                print("Não pode escolher uma data do passado!")
            else:
                break

        if datavalida(int(ANO2), int(MES2), int(DIA2)) == False:
            print("Introduza uma data válida!")
            pesquisaTreinoData(membro)

        HORA2 = '23'
        MINUTO2 = '59'
        DATACORRIDAFORMATADA2 = ANO2+"-"+MES2+"-"+DIA2+" "+HORA2+":"+MINUTO2
     
        cur.execute("SELECT corridas.id, corridas.sitio, corridas.km, corridas.lim_data, corridas.data_corrida, corridas.lim_inscritos, corridas.num_inscritos, provas.valor "
                    "FROM corridas, provas "
                    "WHERE corridas.id = provas.corridas_id AND corridas.data_corrida BETWEEN '{0}' AND '{1}'".format(DATACORRIDAFORMATADA1, DATACORRIDAFORMATADA2))
        conn.commit()

        i = 0
        for linha in cur.fetchall():
            i = cur.rowcount
            x1 = linha[0]  # id
            x2 = linha[1]  # local
            x3 = linha[2]  # distancia
            x4 = linha[3]  # data limite
            x5 = linha[4]  # data corrida
            x6 = linha[5]  # limite inscritos
            x7 = linha[6]  # numero inscritos
            x8 = linha[7]  # valor

            vagas = x6-x7

            print("ID:", x1, "\n| Local:", x2, "| Distancia:", x3, "km | Data:", x5,
                  "\n| Limite Inscricao:", x4, "| Vagas:", vagas, "\n| Valor:", x8,"\n")

        if(i == 0):
            print("Não existe nenhuma prova nesse intervalo")

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
    finally:
        # closing database connection.
        if(conn):
            cur.close()
            conn.close()

# =============================================================================================
# =============================================================================================

def listarProvasInscricoes(membro):
    limparjanela(membro)

    try:
        conn = psycopg2.connect(user="postgres",
                                password="postgres",
                                host="localhost",
                                port="5433",
                                database="CRC") 

        cur = conn.cursor()

        
        cur.execute("SELECT corridas.id, corridas.sitio, corridas.km, corridas.lim_data, corridas.data_corrida, corridas.lim_inscritos, corridas.num_inscritos, provas.valor "
                    "FROM corridas, provas "
                    "WHERE corridas.id = provas.corridas_id AND corridas.lim_data > '{0}'".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                
        conn.commit()


        for linha in cur.fetchall():
            x1 = linha[0]  # id
            x2 = linha[1]  # local
            x3 = linha[2]  # distancia
            x4 = linha[3]  # data limite
            x5 = linha[4]  # data corrida
            x6 = linha[5]  # limite inscritos
            x7 = linha[6]  # numero inscritos
            x8 = linha[7]  # valor

            vagas = x6-x7

            if vagas > 0:
                print("ID:", x1, "\n| Local:", x2, "| Distancia:", x3, "km | Data:", x5,
                      "\n| Limite Inscricao:", x4, "| Vagas:", vagas, "\n| Valor:", x8,"\n")

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
    finally:
        # closing database connection.
        if(conn):
            cur.close()
            conn.close()

# =============================================================================================
# =============================================================================================

def menu_treino(membro):

    limparjanela(membro)
    print("MENU TREINO ------------------------------------------")
    print("")
    print("[L] - Listar Todos os Treinos")
    print("[P] - Pesquisar Treinos")
    print("[I] - Inscrições Abertas")
    print("[S] - Sair")
    print(" ")

    OPCAO = input('Selecionar opcao: ')
    OPCAO = OPCAO.upper()

    if OPCAO == 'L':
        print("selecionou L")
        limparjanela(membro)
        listarTreinos()
        input("Pressione Enter para continuar...")
        while True:
            op = input('Pretende inscrever-se em algum treino? [S/N]: ')
            op = op.upper()
            if op == 'S':
                inscreverTreino(membro)
                input("Pressione Enter para continuar...")
                break
            if op == 'N':
                break
        menu_treino(membro)
    elif OPCAO == 'P':
        print("selecionou P")
        menuPesquisaTreino(membro)
    elif OPCAO == 'I':
        print("selecionou I")
        listarTreinosInscricoes()
        input("Pressione Enter para continuar...")
        while True:
            op = input('Pretende inscrever-se em algum treino? [S/N]: ')
            op = op.upper()
            if op == 'S':
                inscreverTreino(membro)
                input("Pressione Enter para continuar...")
                break
            if op == 'N':
                break
        menu_treino(membro)
    elif OPCAO == 'S':
        print("selecionou S")
        menumembro(membro)
    else:
        menu_treino(membro)

# =============================================================================================
# =============================================================================================

def inscreverTreino(membro):

    id = input("\nIndique o id do treino em que se pretende inscrever: ")

    try:
        conn = psycopg2.connect(user="postgres",
                                password="postgres",
                                host="localhost",
                                port="5433",
                                database="CRC") 

        cur = conn.cursor()

        #verifica se é possivel inscrever na prova
        cur.execute("SELECT corridas.lim_inscritos, corridas.num_inscritos "
                    "FROM corridas, treinos "
                    "WHERE corridas.id = treinos.corridas_id AND corridas.lim_data > '{0}' AND corridas.id = {1}".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),id))     
        conn.commit()

        i = 0
        for linha in cur.fetchall():
            i = cur.rowcount
            x1 = linha[0]
            x2 = linha[1]
            
            vagas = x1-x2

            if vagas == 0:
                input("Não é possivel inscrever-se nessa prova")
                return 0
        
        if i == 0:
            input("Não é possivel inscrever-se nessa prova")
            return 0
        
        #verifica se já está inscrito na prova
        cur.execute("SELECT inscricoes.corridas_id, inscricoes.membros_utilizadores_id "
                    "FROM inscricoes, utilizadores, treinos "
                    "WHERE treinos.corridas_id = inscricoes.corridas_id AND membros_utilizadores_id = utilizadores.id AND username = '{0}' AND treinos.corridas_id = {1}".format(membro,id))
        conn.commit()

        j = 0
        for linha1 in cur.fetchall():
            j = cur.rowcount
        
        if j == 1:
            input("Já está inscrito nesta prova")
            return 0


        # Confirma se pretende fazer a inscrição
        cur.execute("SELECT corridas.num_inscritos, corridas.data_corrida "
                    "FROM corridas, treinos "
                    "WHERE treinos.corridas_id = corridas.id AND corridas.id = {0} ".format(id))
        conn.commit()
        
        for linha3 in cur.fetchall():
            x1 = linha3[0] # nº inscritos
            x2 = linha3[1] # data
        
        print("\nEste treinos tem",x1,"pessoas inscritas e decorre a",x2,"\n")

        while True:
            op = input("Tem a certeza que se pretende inscrever? [S/N]: ")
            op = op.upper()
            if op == 'S':
                break
            if op == 'N':
                return 0


        # Se chegou até aqui vai então fazer a inscrição
        cur.execute("SELECT id FROM utilizadores WHERE username = '{0}';".format(membro))
        for linha2 in cur.fetchall():
            membroID = linha2[0]
        conn.commit()
        
        #Transação
        conn.autocommit = False
        cur.execute("INSERT INTO inscricoes (pago, datapagamento, precopago, corridas_id,membros_utilizadores_id) VALUES(TRUE,'{0}',0,{1},{2})".format(datetime.datetime.now().strftime('%Y-%m-%d'),id,membroID))
        cur.execute("UPDATE corridas SET num_inscritos = num_inscritos + 1 WHERE id = {0}".format(id))
        conn.commit()


    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
        conn.rollback() #Transação
    finally:
        # closing database connection.
        if(conn):
            cur.close()
            conn.close()

# =============================================================================================
# =============================================================================================

def listarTreinosInscricoes():

    try:
        conn = psycopg2.connect(user="postgres",
                                password="postgres",
                                host="localhost",
                                port="5433",
                                database="CRC") 

        cur = conn.cursor()

        
        cur.execute("SELECT corridas.id, corridas.sitio, corridas.km, corridas.lim_data, corridas.data_corrida, corridas.lim_inscritos, corridas.num_inscritos, treinos.rep, treinadores_id "
                    "FROM corridas, treinos "
                    "WHERE corridas.id = treinos.corridas_id AND corridas.lim_data > '{0}'".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                
        conn.commit()


        for linha in cur.fetchall():
            x1 = linha[0]  # id
            x2 = linha[1]  # local
            x3 = linha[2]  # distancia
            x4 = linha[3]  # data limite
            x5 = linha[4]  # data corrida
            x6 = linha[5]  # limite inscritos
            x7 = linha[6]  # numero inscritos
            x8 = linha[7]  # repetitivo
            x9 = linha[8]  #id treinador

            if x9 == None:
                treinador = "Sem treinador"
            
            else:
                cur.execute("SELECT nome FROM treinadores WHERE id = {0}".format(x9))
                for linha1 in cur.fetchall():
                    treinador = linha1[0]

            if x8 == "S":
                REPETE = "Semanalmente"
            elif x8 == "M":
                REPETE = "Mensalmente"
            elif x8 == "N":
                REPETE = "Não"


            vagas = x6-x7

            if vagas > 0:
                print("ID:", x1, "\n| Local:", x2, "| Distancia:", x3, "km | Data:", x5,
                      "\n| Limite Inscricao:", x4, "| Vagas:", vagas, "\n| Repete:", REPETE,"| Treinador:",treinador,"\n")

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
    finally:
        # closing database connection.
        if(conn):
            cur.close()
            conn.close()

# =============================================================================================
# =============================================================================================

def listarTreinos():

    try:
        conn = psycopg2.connect(user="postgres",
                                password="postgres",
                                host="localhost",
                                port="5433",
                                database="CRC") 

        cur = conn.cursor()

        cur.execute("SELECT corridas.id, corridas.sitio, corridas.km, corridas.lim_data, corridas.data_corrida, corridas.lim_inscritos, corridas.num_inscritos, treinos.rep, treinadores_id "
                    "FROM corridas, treinos "
                    "WHERE corridas.id = treinos.corridas_id")            
        conn.commit()


        for linha in cur.fetchall():
            x1 = linha[0]  # id
            x2 = linha[1]  # local
            x3 = linha[2]  # distancia
            x4 = linha[3]  # data limite
            x5 = linha[4]  # data corrida
            x6 = linha[5]  # limite inscritos
            x7 = linha[6]  # numero inscritos
            x8 = linha[7]  # repetitivo
            x9 = linha[8]  # id treinadores

            if x9 == None:
                treinador = "Sem treinador"
            
            else:
                cur.execute("SELECT nome FROM treinadores WHERE id = {0}".format(x9))
                for linha1 in cur.fetchall():
                    treinador = linha1[0]

            if x8 == "S":
                REPETE = "Semanalmente"
            elif x8 == "M":
                REPETE = "Mensalmente"
            elif x8 == "N":
                REPETE = "Não"

            vagas = x6-x7

            print("ID:", x1, "\n| Local:", x2, "| Distancia:", x3, "km | Data:", x5,
                  "\n| Limite Inscricao:", x4, "| Vagas:", vagas, "\n| Repete:", REPETE,"| Treinador:", treinador,"\n")

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
    finally:
        # closing database connection.
        if(conn):
            cur.close()
            conn.close()

# =============================================================================================
# =============================================================================================

def menuPesquisaTreino(membro):

    limparjanela(membro)
    print("MENU DE PESQUISA -------------------------------------")
    print("\nPesquisar por:")
    print("")
    print("[T] - Titulo")
    print("[ID] - ID")
    print("[L] - Local")
    print("[D] - Distancia")
    print("[DT] - Data")
    print("[IDT] - Intervalo de Data")
    print("[S] - Sair")
    print(" ")

    OPCAO = input('Selecionar opcao: ')
    OPCAO = OPCAO.upper()

    if OPCAO == 'T':
        print("selecionou T")
        pesquisaTreinoTitulo(membro)
        input("Pressione Enter para continuar...")
        while True:
            op = input('Pretende inscrever-se em algum treino? [S/N]: ')
            op = op.upper()
            if op == 'S':
                inscreverTreino(membro)
                input("Pressione Enter para continuar...")
                break
            if op == 'N':
                break
        menuPesquisaTreino(membro)
    elif OPCAO == "ID":
        print("selecinou ID")
        pesquisaTreinoID(membro)
        input("Pressione Enter para continuar...")
        while True:
            op = input('Pretende inscrever-se em algum treino? [S/N]: ')
            op = op.upper()
            if op == 'S':
                inscreverTreino(membro)
                input("Pressione Enter para continuar...")

                break
            if op == 'N':
                break
        menuPesquisaTreino(membro)
    elif OPCAO == 'L':
        print("selecionou L")
        pesquisaTreinoLocal(membro)
        input("Pressione Enter para continuar...")
        while True:
            op = input('Pretende inscrever-se em algum treino? [S/N]: ')
            op = op.upper()
            if op == 'S':
                inscreverTreino(membro)
                input("Pressione Enter para continuar...")

                break
            if op == 'N':
                break
        menuPesquisaTreino(membro)
    elif OPCAO == 'D':
        print("selecionou D")
        pesquisaTreinoDistancia(membro)
        input("Pressione Enter para continuar...")
        while True:
            op = input('Pretende inscrever-se em algum treino? [S/N]: ')
            op = op.upper()
            if op == 'S':
                inscreverTreino(membro)
                input("Pressione Enter para continuar...")

                break
            if op == 'N':
                break
        menuPesquisaTreino(membro)
    elif OPCAO == 'DT':
        print("selecionou DT")
        pesquisaTreinoData(membro)
        input("Pressione Enter para continuar...")
        while True:
            op = input('Pretende inscrever-se em algum treino? [S/N]: ')
            op = op.upper()
            if op == 'S':
                inscreverTreino(membro)
                input("Pressione Enter para continuar...")

                break
            if op == 'N':
                break
        menuPesquisaTreino(membro)
    elif OPCAO == 'IDT':
        print("selecionou IDT")
        pesquisaTreinoIntervaloData(membro)
        input("Pressione Enter para continuar...")
        while True:
            op = input('Pretende inscrever-se em algum treino? [S/N]: ')
            op = op.upper()
            if op == 'S':
                inscreverTreino(membro)
                input("Pressione Enter para continuar...")

                break
            if op == 'N':
                break
        menuPesquisaTreino(membro)
    elif OPCAO == 'S':
        print("selecionou S")
        menu_treino(membro)
    else:
        menu_treino(membro)

# =============================================================================================
# =============================================================================================

def pesquisaTreinoTitulo(membro):
    limparjanela(membro)
    try:
        conn = psycopg2.connect(user="postgres",
                                password="postgres",
                                host="localhost",
                                port="5433",
                                database="CRC")

        cur = conn.cursor()


        
        OP = input("Insira o titulo ou parte do titulo que pretende pesquisar: ")
        OP = OP.upper()

        
        cur.execute("SELECT corridas.id, corridas.sitio, corridas.km, corridas.lim_data, corridas.data_corrida, corridas.lim_inscritos, corridas.num_inscritos, treinos.rep, treinadores_id "
                    "FROM corridas, treinos "
                    "WHERE corridas.id = treinos.corridas_id AND UPPER(corridas.sitio) LIKE '%"+OP+"%' ")

        conn.commit()

        i = 0
        for linha in cur.fetchall():
            i = cur.rowcount
            x1 = linha[0]  # id
            x2 = linha[1]  # local
            x3 = linha[2]  # distancia
            x4 = linha[3]  # data limite
            x5 = linha[4]  # data corrida
            x6 = linha[5]  # limite inscritos
            x7 = linha[6]  # numero inscritos
            x8 = linha[7]  # repetitivo
            x9 = linha[8]  # id treinadores

            if x9 == None:
                treinador = "Sem treinador"
            
            else:
                cur.execute("SELECT nome FROM treinadores WHERE id = {0}".format(x9))
                for linha1 in cur.fetchall():
                    treinador = linha1[0]

            if x8 == "S":
                REPETE = "Semanalmente"
            elif x8 == "M":
                REPETE = "Mensalmente"
            elif x8 == "N":
                REPETE = "Não"

            vagas = x6-x7

            print("ID:", x1, "\n| Local:", x2, "| Distancia:", x3, "km | Data:", x5,
                  "\n| Limite Inscricao:", x4, "| Vagas:", vagas, "\n| Repete:", REPETE,"| Treinador:",treinador,"\n")

        if(i == 0):
            print("Não existe nenhum treino com esse titulo")

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
    finally:
        # closing database connection.
        if(conn):
            cur.close()
            conn.close()

# =============================================================================================
# =============================================================================================

def pesquisaTreinoID(membro):
    limparjanela(membro)
    try:
        conn = psycopg2.connect(user="postgres",
                                password="postgres",
                                host="localhost",
                                port="5433",
                                database="CRC") 

        cur = conn.cursor()

        OP = input("Insira o id do treino que pretende pesquisar: ")

        cur.execute("SELECT corridas.id, corridas.sitio, corridas.km, corridas.lim_data, corridas.data_corrida, corridas.lim_inscritos, corridas.num_inscritos, treinos.rep, treinadores_id "
                    "FROM corridas, treinos "
                    "WHERE corridas.id = treinos.corridas_id AND corridas.id = {0} ".format(OP))
        conn.commit()

        i = 0
        for linha in cur.fetchall():
            i = cur.rowcount
            x1 = linha[0]  # id
            x2 = linha[1]  # local
            x3 = linha[2]  # distancia
            x4 = linha[3]  # data limite
            x5 = linha[4]  # data corrida
            x6 = linha[5]  # limite inscritos
            x7 = linha[6]  # numero inscritos
            x8 = linha[7]  # repetitivo
            x9 = linha[8]  # id treinador

            if x9 == None:
                treinador = "Sem treinador"
            
            else:
                cur.execute("SELECT nome FROM treinadores WHERE id = {0}".format(x9))
                for linha1 in cur.fetchall():
                    treinador = linha1[0]

            if x8 == "S":
                REPETE = "Semanalmente"
            elif x8 == "M":
                REPETE = "Mensalmente"
            elif x8 == "N":
                REPETE = "Não"

            vagas = x6-x7

            print("ID:", x1, "\n| Local:", x2, "| Distancia:", x3, "km | Data:", x5,
                  "\n| Limite Inscricao:", x4, "| Vagas:", vagas, "\n| Repete:", REPETE,"| Treinador:",treinador,"\n")

        if(i == 0):
            print("Não existe nenhum treino com esse id")

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
    finally:
        # closing database connection.
        if(conn):
            cur.close()
            conn.close()

# =============================================================================================
# =============================================================================================

def pesquisaTreinoLocal(membro):
    limparjanela(membro)
    try:
        conn = psycopg2.connect(user="postgres",
                                password="postgres",
                                host="localhost",
                                port="5433",
                                database="CRC") 

        cur = conn.cursor()

        OP = input("Insira o local do treino que pretende pesquisar: ")
        OP = OP.upper()

        cur.execute("SELECT corridas.id, corridas.sitio, corridas.km, corridas.lim_data, corridas.data_corrida, corridas.lim_inscritos, corridas.num_inscritos, treinos.rep, treinadores_id "
                    "FROM corridas, treinos "
                    "WHERE corridas.id = treinos.corridas_id AND UPPER(corridas.sitio) LIKE '%"+OP+"' ")
        
        conn.commit()

        i = 0
        for linha in cur.fetchall():
            i = cur.rowcount
            x1 = linha[0]  # id
            x2 = linha[1]  # local
            x3 = linha[2]  # distancia
            x4 = linha[3]  # data limite
            x5 = linha[4]  # data corrida
            x6 = linha[5]  # limite inscritos
            x7 = linha[6]  # numero inscritos
            x8 = linha[7]  # repetitivo
            x9 = linha[8]  # id treinador

            if x9 == None:
                treinador = "Sem treinador"
            
            else:
                cur.execute("SELECT nome FROM treinadores WHERE id = {0}".format(x9))
                for linha1 in cur.fetchall():
                    treinador = linha1[0]

            if x8 == "S":
                REPETE = "Semanalmente"
            elif x8 == "M":
                REPETE = "Mensalmente"
            elif x8 == "N":
                REPETE = "Não"

            vagas = x6-x7

            print("ID:", x1, "\n| Local:", x2, "| Distancia:", x3, "km | Data:", x5,
                  "\n| Limite Inscricao:", x4, "| Vagas:", vagas, "\n| Repete:", REPETE,"| Treinador:",treinador,"\n")

        if(i == 0):
            print("Não existe nenhum treino nesse local")

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
    finally:
        # closing database connection.
        if(conn):
            cur.close()
            conn.close()

# =============================================================================================
# =============================================================================================

def pesquisaTreinoDistancia(membro):
    limparjanela(membro)
    try:
        conn = psycopg2.connect(user="postgres",
                                password="postgres",
                                host="localhost",
                                port="5433",
                                database="CRC") 

        cur = conn.cursor()

        while True:
            print("")
            print("Distância:")
            print("[A] - 1km")
            print("[B] - 5km")
            print("[C] - 10km")
            print("[D] - 20km")
            print("[E] - 40km (maratona)")
            print("------------------------------------------------------")
            print(" ")

            OPCAO = input('Selecionar opcao: ')
            OPCAO = OPCAO.upper()

            if OPCAO == 'A':
                DISTANCIA = '1'
                break
            elif OPCAO == 'B':
                DISTANCIA = '5'
                break
            elif OPCAO == 'C':
                DISTANCIA = '10'
                break
            elif OPCAO == 'D':
                DISTANCIA = '20'
                break
            elif OPCAO == 'E':
                DISTANCIA = '40'
                break
            else:
                print("Opcao invalida")

        cur.execute("SELECT corridas.id, corridas.sitio, corridas.km, corridas.lim_data, corridas.data_corrida, corridas.lim_inscritos, corridas.num_inscritos, treinos.rep, treinadores_id "
                    "FROM corridas, treinos "
                    "WHERE corridas.id = treinos.corridas_id AND corridas.km = {0} ".format(DISTANCIA))
        conn.commit()

        i = 0
        for linha in cur.fetchall():
            i = cur.rowcount
            x1 = linha[0]  # id
            x2 = linha[1]  # local
            x3 = linha[2]  # distancia
            x4 = linha[3]  # data limite
            x5 = linha[4]  # data corrida
            x6 = linha[5]  # limite inscritos
            x7 = linha[6]  # numero inscritos
            x8 = linha[7]  # repetitivo
            x9 = linha[8]  #id treinador

            if x9 == None:
                treinador = "Sem treinador"
            
            else:
                cur.execute("SELECT nome FROM treinadores WHERE id = {0}".format(x9))
                for linha1 in cur.fetchall():
                    treinador = linha1[0]

            if x8 == "S":
                REPETE = "Semanalmente"
            elif x8 == "M":
                REPETE = "Mensalmente"
            elif x8 == "N":
                REPETE = "Não"

            vagas = x6-x7

            print("ID:", x1, "\n| Local:", x2, "| Distancia:", x3, "km | Data:", x5,
                  "\n| Limite Inscricao:", x4, "| Vagas:", vagas, "\n| Repete:", REPETE,"| Treinador:",treinador,"\n")

        if(i == 0):
            print("Não existe nenhum treino com essa distancia")

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
    finally:
        # closing database connection.
        if(conn):
            cur.close()
            conn.close()

# =============================================================================================
# =============================================================================================

def pesquisaTreinoData(membro):
    limparjanela(membro)
    try:
        conn = psycopg2.connect(user="postgres",
                                password="postgres",
                                host="localhost",
                                port="5433",
                                database="CRC")  

        cur = conn.cursor()

        ANO = input("Ano: ")

        while True:
            MES = input("Mes: ")
            if int(MES) <= 9: 
                MES = "0"+str(int(MES))
            if (int(MES) < 1 ):
                print("Não pode ser negativo!")
            else:
                break

        while True:
            DIA = input("Dia: ")
            if int(DIA) <= 9: 
                DIA = "0"+str(int(DIA))
            if (int(DIA) < 1 ):
                print("Não pode ser negativo!")
            else:
                break

        if datavalida(int(ANO), int(MES), int(DIA)) == False:
            print("Introduza uma data válida!")
            pesquisaTreinoData(membro)

        HORA1 = '00'
        MINUTO1 = '00'
        DATACORRIDAFORMATADA1 = ANO+"-"+MES+"-"+DIA+" "+HORA1+":"+MINUTO1
        HORA2 = '23'
        MINUTO2 = '59'
        DATACORRIDAFORMATADA2 = ANO+"-"+MES+"-"+DIA+" "+HORA2+":"+MINUTO2

        cur.execute("SELECT corridas.id, corridas.sitio, corridas.km, corridas.lim_data, corridas.data_corrida, corridas.lim_inscritos, corridas.num_inscritos, treinos.rep, treinadores_id "
                    "FROM corridas, treinos "
                    "WHERE corridas.id = treinos.corridas_id AND corridas.data_corrida > '{0}' AND corridas.data_corrida < '{1}' ".format(DATACORRIDAFORMATADA1, DATACORRIDAFORMATADA2))

        conn.commit()

        i = 0
        for linha in cur.fetchall():
            i = cur.rowcount
            x1 = linha[0]  # id
            x2 = linha[1]  # local
            x3 = linha[2]  # distancia
            x4 = linha[3]  # data limite
            x5 = linha[4]  # data corrida
            x6 = linha[5]  # limite inscritos
            x7 = linha[6]  # numero inscritos
            x8 = linha[7]  # repetitivo
            x9 = linha[8]  # id treinador
            if x9 == None:
                treinador = "Sem treinador"
            
            else:
                cur.execute("SELECT nome FROM treinadores WHERE id = {0}".format(x9))
                for linha1 in cur.fetchall():
                    treinador = linha1[0]

            if x8 == "S":
                REPETE = "Semanalmente"
            elif x8 == "M":
                REPETE = "Mensalmente"
            elif x8 == "N":
                REPETE = "Não"

            vagas = x6-x7

            print("ID:", x1, "\n| Local:", x2, "| Distancia:", x3, "km | Data:", x5,
                  "\n| Limite Inscricao:", x4, "| Vagas:", vagas, "\n| Repete:", REPETE,"| Treinador:",treinador,"\n")

        if(i == 0):
            print("Não existe nenhum treino nessa data")

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
    finally:
        # closing database connection.
        if(conn):
            cur.close()
            conn.close()

# =============================================================================================
# =============================================================================================

def pesquisaTreinoDataOLD(membro):
    limparjanela(membro)
    try:
        conn = psycopg2.connect(user="postgres",
                                password="postgres",
                                host="localhost",
                                port="5433",
                                database="CRC")  

        cur = conn.cursor()

        while True:
            ANO = input("Ano: ")
            if (int(ANO) < int(datetime.datetime.now().strftime('%Y'))):
                print("Não pode escolher uma data do passado!")
            else:
                break

        while True:
            MES = input("Mes: ")
            if int(MES) <= 9: 
                MES = "0"+str(int(MES))
            if (int(MES) < 1 or int(str(ANO)+str(MES)) < int(datetime.datetime.now().strftime('%Y%m'))):
                print("Não pode escolher uma data do passado!")
            else:
                break

        while True:
            DIA = input("Dia: ")
            if int(DIA) <= 9: 
                DIA = "0"+str(int(DIA))
            if (int(DIA) < 1 or int(str(ANO)+str(MES)+str(DIA)) < int(datetime.datetime.now().strftime('%Y%m%d'))):
                print("Não pode escolher uma data do passado!")
            else:
                break

        if datavalida(int(ANO), int(MES), int(DIA)) == False:
            print("Introduza uma data válida!")

        HORA1 = '00'
        MINUTO1 = '00'
        DATACORRIDAFORMATADA1 = ANO+"-"+MES+"-"+DIA+" "+HORA1+":"+MINUTO1
        HORA2 = '23'
        MINUTO2 = '59'
        DATACORRIDAFORMATADA2 = ANO+"-"+MES+"-"+DIA+" "+HORA2+":"+MINUTO2

        cur.execute("SELECT corridas.id, corridas.sitio, corridas.km, corridas.lim_data, corridas.data_corrida, corridas.lim_inscritos, corridas.num_inscritos, treinos.rep, treinadores_id "
                    "FROM corridas, treinos "
                    "WHERE corridas.id = treinos.corridas_id AND corridas.data_corrida > '{0}' AND corridas.data_corrida < '{1}' ".format(DATACORRIDAFORMATADA1, DATACORRIDAFORMATADA2))

        conn.commit()

        i = 0
        for linha in cur.fetchall():
            i = cur.rowcount
            x1 = linha[0]  # id
            x2 = linha[1]  # local
            x3 = linha[2]  # distancia
            x4 = linha[3]  # data limite
            x5 = linha[4]  # data corrida
            x6 = linha[5]  # limite inscritos
            x7 = linha[6]  # numero inscritos
            x8 = linha[7]  # repetitivo
            x9 = linha[8]  # id treinador
            if x9 == None:
                treinador = "Sem treinador"
            
            else:
                cur.execute("SELECT nome FROM treinadores WHERE id = {0}".format(x9))
                for linha1 in cur.fetchall():
                    treinador = linha1[0]

            if x8 == "S":
                REPETE = "Semanalmente"
            elif x8 == "M":
                REPETE = "Mensalmente"
            elif x8 == "N":
                REPETE = "Não"

            vagas = x6-x7

            print("ID:", x1, "\n| Local:", x2, "| Distancia:", x3, "km | Data:", x5,
                  "\n| Limite Inscricao:", x4, "| Vagas:", vagas, "\n| Repete:", REPETE,"| Treinador:",treinador,"\n")

        if(i == 0):
            print("Não existe nenhum treino nessa data")

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
    finally:
        # closing database connection.
        if(conn):
            cur.close()
            conn.close()

# =============================================================================================
# =============================================================================================

def pesquisaTreinoIntervaloData(membro):
    limparjanela(membro)
    try:
        conn = psycopg2.connect(user="postgres",
                                password="postgres",
                                host="localhost",
                                port="5433",
                                database="CRC")  

        cur = conn.cursor()
        
        print("Data menor: ")

        ANO1 = input("Ano: ")

        while True:
            MES1 = input("Mes: ")
            if int(MES1) <= 9:
                MES1 = "0"+str(int(MES1))
            if (int(MES1) < 1 ):
                print("Não pode ser negativo!")
            else:
                break

        while True:
            DIA1 = input("Dia: ")
            if int(DIA1) <= 9:
                DIA1 = "0"+str(int(DIA1))
            if (int(DIA1) < 1 ):
                print("Não pode ser negativo!")
            else:
                break

        if datavalida(int(ANO1), int(MES1), int(DIA1)) == False:
            print("Introduza uma data válida!")
            pesquisaTreinoIntervaloData(membro)
        HORA1 = "00"
        MINUTO1 = "00"
        
        DATACORRIDAFORMATADA1 = ANO1+"-"+MES1+"-"+DIA1+" "+HORA1+":"+MINUTO1

        print("Data maior: ")

        ANO2 = input("Ano: ")


        while True:
            MES2 = input("Mes: ")
            if int(MES2) <= 9:
                MES2 = "0"+str(int(MES2))
            if (int(MES2) < 1 ):
                print("Não pode ser negativo!")
            else:
                break

        while True:
            DIA2 = input("Dia: ")
            if int(DIA2) <= 9:
                DIA2 = "0"+str(int(DIA2))
            if (int(DIA2) < 1 ):
                print("Não pode ser negativo!")
            else:
                break

        if datavalida(int(ANO2), int(MES2), int(DIA2)) == False:
            print("Introduza uma data válida!")
            pesquisaTreinoIntervaloData(membro)

        HORA2 = "23"
        MINUTO2 = "59"
        
        DATACORRIDAFORMATADA2 = ANO2+"-"+MES2+"-"+DIA2+" "+HORA2+":"+MINUTO2
     
        cur.execute("SELECT corridas.id, corridas.sitio, corridas.km, corridas.lim_data, corridas.data_corrida, corridas.lim_inscritos, corridas.num_inscritos, treinos.rep, treinadores_id "
                    "FROM corridas, treinos "
                    "WHERE corridas.id = treinos.corridas_id AND corridas.data_corrida BETWEEN '{0}' AND '{1}' ".format(DATACORRIDAFORMATADA1, DATACORRIDAFORMATADA2))
        conn.commit()

        i = 0
        for linha in cur.fetchall():
            i = cur.rowcount
            x1 = linha[0]  # id
            x2 = linha[1]  # local
            x3 = linha[2]  # distancia
            x4 = linha[3]  # data limite
            x5 = linha[4]  # data corrida
            x6 = linha[5]  # limite inscritos
            x7 = linha[6]  # numero inscritos
            x8 = linha[7]  # repetitivo
            x9 = linha[8]  # id treinador

            if x9 == None:
                treinador = "Sem treinador"
            
            else:
                cur.execute("SELECT nome FROM treinadores WHERE id = {0}".format(x9))
                for linha1 in cur.fetchall():
                    treinador = linha1[0]

            if x8 == "S":
                REPETE = "Semanalmente"
            elif x8 == "M":
                REPETE = "Mensalmente"
            elif x8 == "N":
                REPETE = "Não"

            vagas = x6-x7

            print("ID:", x1, "\n| Local:", x2, "| Distancia:", x3, "km | Data:", x5,
                  "\n| Limite Inscricao:", x4, "| Vagas:", vagas, "\n| Repete:", REPETE,"| Treinador:",treinador,"\n")

        if(i == 0):
            print("Não existe nenhum treino nesse intervalo")

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
    finally:
        # closing database connection.
        if(conn):
            cur.close()
            conn.close()

# =============================================================================================
# =============================================================================================

def pesquisaTreinoIntervaloDataOLD(membro):
    limparjanela(membro)
    try:
        conn = psycopg2.connect(user="postgres",
                                password="postgres",
                                host="localhost",
                                port="5433",
                                database="CRC")  

        cur = conn.cursor()
        
        print("Data menor: ")
        while True:
            ANO1 = input("Ano: ")
            if (int(ANO1) < int(datetime.datetime.now().strftime('%Y'))):
                print("Não pode escolher uma data do passado!")
            else:
                break

        while True:
            MES1 = input("Mes: ")
            if int(MES1) <= 9:
                MES1 = "0"+str(int(MES1))
            if (int(MES1) < 1 or int(str(ANO1)+str(MES1)) < int(datetime.datetime.now().strftime('%Y%m'))):
                print("Não pode escolher uma data do passado!")
            else:
                break

        while True:
            DIA1 = input("Dia: ")
            if int(DIA1) <= 9:
                DIA1 = "0"+str(int(DIA1))
            if (int(DIA1) < 1 or int(str(ANO1)+str(MES1)+str(DIA1)) < int(datetime.datetime.now().strftime('%Y%m%d'))):
                print("Não pode escolher uma data do passado!")
            else:
                break

        if datavalida(int(ANO1), int(MES1), int(DIA1)) == False:
            print("Introduza uma data válida!")

        HORA1 = "00"
        MINUTO1 = "00"
        
        DATACORRIDAFORMATADA1 = ANO1+"-"+MES1+"-"+DIA1+" "+HORA1+":"+MINUTO1

        print("Data maior: ")
        while True:
            ANO2 = input("Ano: ")
            if (int(ANO2) < int(datetime.datetime.now().strftime('%Y'))):
                print("Não pode escolher uma data do passado!")
            else:
                break

        while True:
            MES2 = input("Mes: ")
            if int(MES2) <= 9:
                MES2 = "0"+str(int(MES2))
            if (int(MES2) < 1 or int(str(ANO2)+str(MES2)) < int(datetime.datetime.now().strftime('%Y%m'))):
                print("Não pode escolher uma data do passado!")
            else:
                break

        while True:
            DIA2 = input("Dia: ")
            if int(DIA2) <= 9:
                DIA2 = "0"+str(int(DIA2))
            if (int(DIA2) < 1 or int(str(ANO2)+str(MES2)+str(DIA2)) < int(datetime.datetime.now().strftime('%Y%m%d'))):
                print("Não pode escolher uma data do passado!")
            else:
                break

        if datavalida(int(ANO2), int(MES2), int(DIA2)) == False:
            print("Introduza uma data válida!")

        HORA2 = "23"
        MINUTO2 = "59"
        
        DATACORRIDAFORMATADA2 = ANO2+"-"+MES2+"-"+DIA2+" "+HORA2+":"+MINUTO2
     
        cur.execute("SELECT corridas.id, corridas.sitio, corridas.km, corridas.lim_data, corridas.data_corrida, corridas.lim_inscritos, corridas.num_inscritos, treinos.rep, treinadores_id "
                    "FROM corridas, treinos "
                    "WHERE corridas.id = treinos.corridas_id AND corridas.data_corrida BETWEEN '{0}' AND '{1}' ".format(DATACORRIDAFORMATADA1, DATACORRIDAFORMATADA2))
        conn.commit()

        i = 0
        for linha in cur.fetchall():
            i = cur.rowcount
            x1 = linha[0]  # id
            x2 = linha[1]  # local
            x3 = linha[2]  # distancia
            x4 = linha[3]  # data limite
            x5 = linha[4]  # data corrida
            x6 = linha[5]  # limite inscritos
            x7 = linha[6]  # numero inscritos
            x8 = linha[7]  # repetitivo
            x9 = linha[8]  # id treinador

            if x9 == None:
                treinador = "Sem treinador"
            
            else:
                cur.execute("SELECT nome FROM treinadores WHERE id = {0}".format(x9))
                for linha1 in cur.fetchall():
                    treinador = linha1[0]

            if x8 == "S":
                REPETE = "Semanalmente"
            elif x8 == "M":
                REPETE = "Mensalmente"
            elif x8 == "N":
                REPETE = "Não"

            vagas = x6-x7

            print("ID:", x1, "\n| Local:", x2, "| Distancia:", x3, "km | Data:", x5,
                  "\n| Limite Inscricao:", x4, "| Vagas:", vagas, "\n| Repete:", REPETE,"| Treinador:",treinador,"\n")

        if(i == 0):
            print("Não existe nenhum treino nesse intervalo")

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
    finally:
        # closing database connection.
        if(conn):
            cur.close()
            conn.close()

# =============================================================================================
# =============================================================================================

def loginadmin():
    clear()
    print(" ")
    print(datetime.datetime.now().strftime('%Y-%m-%d ======== COIMBRA RUN CLUB ======== %H:%M:%S'))
    print(" ")
    print("LOG IN (ADMIN) ---------------------------------------\n")

    while True:
        EMAIL = input('E-mail: ')
        EMAIL = EMAIL.lower()
        if (EMAIL == '' or ' ' in EMAIL):
            print("Não insira um campo vazio!")
        else:
            break

    while True:
        PASSWORD = maskpass.askpass(prompt="Password: ", mask="*")
        if PASSWORD == '':
            print("Não insira um campo vazio!")
        else:
            PASSWORD = hashlib.md5(PASSWORD.encode())
            PASSWORD = PASSWORD.hexdigest()
            break

    if verifica_login_admin(EMAIL, PASSWORD) == 1:
        print("Login válido!")
        return EMAIL
    elif verifica_login_admin(EMAIL, PASSWORD) == 0:
        print("Login inválido")
        return 0

# =============================================================================================
# =============================================================================================

def menuadmin(admin):

    limparjanela(admin)
    print("MENU ADMIN -------------------------------------------")
    print(" ")
    print("[NT] - Novo treino")
    print("[NP] - Nova prova")
    print(" ")
    print("[TT] - Todos os treinos")
    print("[TP] - Todas as provas")
    print(" ")
    print("[EM] - Enviar mensagem")
    print("[GI] - Gerir inscrições")
    print("[VE] - Ver estatísticas")
    print(" ")
    print("[S] - Log out")
    print(" ")
    print("------------------------------------------------------")
    print(" ")

    OPCAO = input('Selecionar opção: ')
    OPCAO = OPCAO.upper()

    if OPCAO == 'NT':
        addnovotreino(admin)

    elif OPCAO == 'NP':
        addnovaprova(admin)

    elif OPCAO == 'TT':
        
        while True:
            limparjanela(admin)
            listarTreinos()
            print("------------------------------------------------------")
            print(" ")
            print("[A] - Alterar informação de um treino")
            print("[S] - Sair")

            RESPOSTA = input('Opção: ')
            RESPOSTA = RESPOSTA.upper()
            if (RESPOSTA != 'A' and RESPOSTA != 'S'):
                print("Insira uma opção válida!")
            else:
                break

        if (RESPOSTA == 'A'):
            while True:
                limparjanela(admin)
                listarTreinos()
                print("------------------------------------------------------")
                print(" ")
                IDTREINO = int(input('ID do treino a alterar: '))

                # VER SE ID EXISTE
                EXISTE = verifica_treino(IDTREINO)


                if (EXISTE != 1):
                    print("Insira uma opção válida!")
                else:
                    break

            alterarTreino(IDTREINO, admin)

        else:
            menuadmin(admin)
            

    elif OPCAO == 'TP':
        while True:
            limparjanela(admin)
            listarProvas()
            print("------------------------------------------------------")
            print(" ")
            print("[A] - Alterar informação de uma prova")
            print("[R] - Remover prova")
            print("[H] - Histórico de preços")
            print("[S] - Sair")
            print(" ")
            RESPOSTA = input('Opção: ')
            RESPOSTA = RESPOSTA.upper()
            if (RESPOSTA != 'A' and RESPOSTA != 'R' and RESPOSTA != 'H' and RESPOSTA != 'S'):
                print("Insira uma opção válida!")
            else:
                break

        if (RESPOSTA == 'A'):
            while True:
                limparjanela(admin)
                listarProvas()
                print("------------------------------------------------------")
                print(" ")
                IDPROVA = int(input('ID da prova a alterar: '))

                # VER SE ID EXISTE
                EXISTE = verifica_prova(IDPROVA)


                if (EXISTE != 1):
                    print("Insira uma opção válida!")
                else:
                    break

            alterarProva(IDPROVA, admin)


        elif (RESPOSTA == 'R'):
            apagarprova(admin)
            input("Pressione Enter para voltar...")
            menuadmin(admin)

        elif (RESPOSTA == 'H'):
            while True:
                limparjanela(admin)
                listarProvas()
                print("------------------------------------------------------")
                print(" ")

                IDPROVA = int(input('ID da prova para ver histórico: '))

                # VER SE ID EXISTE
                EXISTE = verifica_prova(IDPROVA)


                if (EXISTE != 1):
                    print("Insira uma opção válida!")
                else:
                    break
            limparjanela(admin)
            historicoAltPrecos(IDPROVA)
            input("Pressione Enter para voltar...")
            menuadmin(admin)

        else:
            menuadmin(admin)

    elif OPCAO == 'EM':
        SelecionarDestinatario(admin)
        menuadmin(admin)

    elif OPCAO == 'GI':

        while True:
            limparjanela(admin)
            print("GERIR INSCRIÇÕES -------------------------------------")
            print(" ")
            print("[A] - Alterar inscrição de prova para pago")
            print("[D] - Desinscrever membro")
            print("[S] - Sair")

            RESPOSTA = input('Opção: ')
            RESPOSTA = RESPOSTA.upper()
            if (RESPOSTA != 'A' and RESPOSTA != 'D' and RESPOSTA != 'S'):
                print("Insira uma opção válida!")
            else:
                break
                
        if (RESPOSTA == 'A'):
            alterapago(admin)
            input("Pressione Enter para voltar...")
            menuadmin(admin)

        elif (RESPOSTA == 'D'):
            desinscreveMembro(admin)
            input("Pressione Enter para voltar...")
            menuadmin(admin)
        
        elif (RESPOSTA == 'S'):
            menuadmin(admin)

    elif OPCAO == 'VE':
        menuestatisticas(admin)

    elif OPCAO == 'S':
        menuinicial()
    else:
        menuadmin(admin)

# =============================================================================================
# =============================================================================================

def datavalida(ano, mes, dia):
    day_count_for_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if ano % 4 == 0 and (ano % 100 != 0 or ano % 400 == 0):
        day_count_for_month[2] = 29
    return (1 <= mes <= 12 and 1 <= dia <= day_count_for_month[mes])

# =============================================================================================
# =============================================================================================

def desinscreveMembro(admin):
    limparjanela(admin)
    try:
        conn = psycopg2.connect(user="postgres",
                                password="postgres",
                                host="localhost",
                                port="5433",
                                database="CRC")

        cur = conn.cursor()

        cur.execute("SELECT id, sitio, num_inscritos FROM corridas "
                    "WHERE num_inscritos > 0 AND data_corrida > '{0}' "
                    "ORDER BY id ASC".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        conn.commit()

        i = 0
        for linha in cur.fetchall():
            i+=1
            x1 = linha[0] # id corrida
            x2 = linha[1] # local
            x3 = linha[2] # inscritos

            print("Id da prova:",x1,"| Local:",x2,"| Inscritos:",x3)
        
        if i == 0:
            print("Não existem provas com inscritos")
            return 0
        
        while True:
            valid = False
            while not valid: #loop until the user enters a valid int
                try:
                    x = int(input("\nIndique o id da prova da qual pretende desinscrever um membro:"))
                    valid = True #if this point is reached, x is a valid int
                except ValueError:
                    print('Introduza apenas numero inteiros\n')

            cur.execute("SELECT id FROM corridas "
                        "WHERE num_inscritos > 0 AND data_corrida > '{0}' AND id = {1} ".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),x))
            conn.commit()

            i = 0
            for linha in cur.fetchall():
                i+=1 

            if i == 0:
                print("Introduza uma opção válida.")
            else:
                break
        
        input("Pressione enter para continuar...")
        limparjanela(admin)
        print("\nMembros inscritos nessa prova:\n")
        
        cur.execute("SELECT utilizadores.id, utilizadores.nome FROM inscricoes,utilizadores "
                    "WHERE membros_utilizadores_id = utilizadores.id "
                    "AND inscricoes.corridas_id = {0}".format(x))
        conn.commit()

        for linha in cur.fetchall():
            x1 = linha[0] # id
            x2 = linha[1] # nome

            print("ID: ",x1,"| Nome:",x2)

        while True:
            valid = False
            while not valid: #loop until the user enters a valid int
                try:
                    y = int(input("\nIndique o id do membro que pretende desinscrever:"))
                    valid = True #if this point is reached, x is a valid int
                except ValueError:
                    print('Introduza apenas numero inteiros\n')

            cur.execute("SELECT utilizadores.id FROM inscricoes,utilizadores "
                        "WHERE membros_utilizadores_id = utilizadores.id "
                        "AND inscricoes.corridas_id = {0} AND inscricoes.membros_utilizadores_id = {1}".format(x,y))
            conn.commit()

            i = 0
            for linha in cur.fetchall():
                i+=1 

            if i == 0:
                print("Introduza uma opção válida.")
            else:
                break
            
            desinscreve(y,x)

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
        conn.rollback() #Transação
    finally:
        # closing database connection.
        if(conn):
            cur.close()
            conn.close()

# =============================================================================================
# =============================================================================================

def desinscreve(idmembro,idcorrida):
    try:
        conn = psycopg2.connect(user="postgres",
                                password="postgres",
                                host="localhost",
                                port="5433",
                                database="CRC")

        cur = conn.cursor()

        cur.execute("DELETE FROM inscricoes WHERE corridas_id = {0} AND membros_utilizadores_id = {1};".format(idcorrida,idmembro))
        conn.commit()
        cur.execute("UPDATE corridas SET num_inscritos=num_inscritos-1 WHERE id = {0};".format(idcorrida))
        conn.commit()

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
        #conn.rollback() #Transação
    finally:
        # closing database connection.
        if(conn):
            cur.close()
            conn.close()

# =============================================================================================
# =============================================================================================

def apagarprova(admin):
    limparjanela(admin)
    try:
        conn = psycopg2.connect(user="postgres",
                                password="postgres",
                                host="localhost",
                                port="5433",
                                database="CRC")

        cur = conn.cursor()

        print("Provas sem inscrições --------------------------------")

        cur.execute("SELECT provas.corridas_id, corridas.sitio FROM provas,corridas WHERE provas.corridas_id = corridas.id AND "
                    "provas.corridas_id NOT IN (SELECT corridas_id FROM inscricoes)")
        conn.commit()

        i = 0
        for linha in cur.fetchall():
            i+=1
            x1 = linha[0] # id corrida
            x2 = linha[1] # local

            print("Id da prova:",x1,"| Local:",x2)
        
        if i == 0:
            print("Todas as provas contêm inscritos")
            return 0
        
        while True:
            valid = False
            while not valid: #loop until the user enters a valid int
                try:
                    x = int(input("\nIndique o id da prova que pretende apagar:"))
                    valid = True #if this point is reached, x is a valid int
                except ValueError:
                    print('Introduza apenas numero inteiros\n')

            cur.execute("SELECT provas.corridas_id, corridas.sitio FROM provas,corridas WHERE provas.corridas_id = corridas.id AND "
                        "provas.corridas_id NOT IN (SELECT corridas_id FROM inscricoes) AND provas.corridas_id = {0}".format(x))
            conn.commit()

            i = 0
            for linha in cur.fetchall():
                i+=1  
            if i == 0:
                print("Introduza uma opção válida.")
                    
            else:
                break

        cur.execute("DELETE FROM hist_de_alt_preco WHERE provas_corridas_id = {0};".format(x))
        conn.commit()
        cur.execute("DELETE FROM provas WHERE provas.corridas_id = {0};".format(x))
        conn.commit()
        cur.execute("DELETE FROM corridas WHERE corridas.id = {0};".format(x))
        conn.commit()

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
        conn.rollback() #Transação
    finally:
        # closing database connection.
        if(conn):
            cur.close()
            conn.close()

# =============================================================================================
# =============================================================================================

def alterapago(admin):
    limparjanela(admin)
    try:
        conn = psycopg2.connect(user="postgres",
                                password="postgres",
                                host="localhost",
                                port="5433",
                                database="CRC")

        cur = conn.cursor()

        cur.execute("SELECT corridas_id, membros_utilizadores_id FROM inscricoes WHERE pago = false ORDER BY corridas_id ASC")
        conn.commit()

        i = 0
        for linha in cur.fetchall():
            i+=1
            x1 = linha[0] # id corrida
            x2 = linha[1] # id membro

            print("Id da prova:",x1,"| Id do membro:",x2)
        
        if(i == 0):
            print("Todas as inscrições estão pagas!")
            return 0
        
        while True:
            valid = False
            while not valid: #loop until the user enters a valid int
                try:
                    x = int(input("\nIndique o id da prova que pretende fazer a alteração:"))
                    valid = True #if this point is reached, x is a valid int
                except ValueError:
                    print('Introduza apenas numero inteiros\n')

            cur.execute("SELECT corridas_id, membros_utilizadores_id FROM inscricoes "
                            "WHERE corridas_id = {0} AND pago = false".format(x))
            conn.commit()

            i = 0
            for linha in cur.fetchall():
                i+=1  
            if i == 0:
                print("Introduza uma opção válida.")
                    
            else:
                break

        while True:
            valid = False
            while not valid: #loop until the user enters a valid int
                try:
                    y = int(input("\nIndique o id do membro que pretende fazer a alteração:"))
                    valid = True #if this point is reached, x is a valid int
                except ValueError:
                    print('Introduza apenas numero inteiros\n')
        
            cur.execute("SELECT corridas_id, membros_utilizadores_id FROM inscricoes "
                            "WHERE corridas_id = {0} AND pago = false AND membros_utilizadores_id = {1}".format(x,y))
            i = 0
            for linha in cur.fetchall():
                i+=1
                
            if i == 0:
                print("Introduza uma opção válida.")
                    
            else:
                break
        
        updatePago(y,x)

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
    finally:
        # closing database connection.
        if(conn):
            cur.close()
            conn.close()
    
# =============================================================================================
# =============================================================================================

def addnovotreino(admin):
    limparjanela(admin)
    print("NOVO TREINO ------------------------------------------")
    print(" ")
    MENU = "NT"
    print("Distância:")
    print("[A] - 1km")
    print("[B] - 5km")
    print("[C] - 10km")
    print("[D] - 20km")
    print("[E] - 40km (maratona)")
    print(" ")
    OPCAO = input('Selecionar opcao: ')
    OPCAO = OPCAO.upper()
    if OPCAO == 'A':
        DISTANCIA = 1
    elif OPCAO == 'B':
        DISTANCIA = 5
    elif OPCAO == 'C':
        DISTANCIA = 10
    elif OPCAO == 'D':
        DISTANCIA = 20
    elif OPCAO == 'E':
        DISTANCIA = 40
    else:
        addnovotreino(admin)
    
    print(" ")
    while True:
        LOCAL = input("Local: ")
        if (LOCAL == ''):
            print("Não insira campos vazios!")
        else:
            break

    print(" ")
    while True:
        LIMITEINSCRITOS = int(input("Número MAX de inscritos: "))
        if (LIMITEINSCRITOS < 3):
            print("Insira dados válidos!")
        else:
            break

    print(" ")
    while True:
        REPETE = input("O treino repete? [S/N]: ")
        REPETE = REPETE.upper()
        if (REPETE != 'S' and REPETE != 'N'):
            print("Escolha uma resposta válida!")
        else:
            break

    if REPETE == 'S':
        while True:
            print("[S] - Semanalmente")
            print("[M] - Mensalmente")
            REPETE = input("Opção: ")
            REPETE = REPETE.upper()
            if (REPETE != 'S' and REPETE != 'M'):
                print("Escolha uma resposta válida!")
            else:
                break
    print(" ")
    print("DATA DO TREINO ---------------------------------------")
    print(" ")

    while True:
        ANO = input("Ano: ")
        if (int(ANO) < int(datetime.datetime.now().strftime('%Y'))):
            print("Não pode escolher uma data do passado!")
        else:
            break

    while True:
        MES = input("Mes: ")

        if int(MES) <= 9: # CORRIGIR
            MES = "0"+str(int(MES))

        if (int(MES) < 1 or int(str(ANO)+str(MES)) < int(datetime.datetime.now().strftime('%Y%m'))):
            print("Não pode escolher uma data do passado!")
        else:
            break

    while True:
        DIA = input("Dia: ")
        if int(DIA) <= 9:
            DIA = "0"+str(int(DIA))

        if (int(DIA) < 1 or int(str(ANO)+str(MES)+str(DIA)) < int(datetime.datetime.now().strftime('%Y%m%d'))):
            print("Não pode escolher uma data do passado!")
        else:
            break

    if datavalida(int(ANO), int(MES), int(DIA)) == False:
        print("Introduza uma data válida!")
        addnovotreino(admin)

    while True:
        HORA = input("Hora (h): ")
        if (int(HORA) < 0 or int(HORA) > 23 ):
            print("Introduza uma hora válida!")
        else:
            if int(HORA) <= 9:
                HORA = "0"+str(int(HORA))
            break

    while True:
        MINUTO = input("Minuto (m): ")
        if (int(MINUTO) < 0 or int(MINUTO) > 59 ):
            print("Introduza uma hora válida!")
        else:
            if int(MINUTO) <= 9:
                MINUTO = "0"+str(int(MINUTO))
            break

    print(" ")
    print("DATA LIMITE PARA INSCRIÇÃO ---------------------------")
    print(" ")

    while True:
        LIMITEANO = input("Ano: ")
        if (int(LIMITEANO) < int(datetime.datetime.now().strftime('%Y')) or int(LIMITEANO) > int(ANO)):
            print("Escolha uma data válida!")
        else:
            break

    while True:
        LIMITEMES = input("Mes: ")

        if int(LIMITEMES) <= 9:
            LIMITEMES = "0"+str(int(LIMITEMES))

        if (int(LIMITEMES) < 1 or int(str(LIMITEANO)+str(LIMITEMES)) < int(datetime.datetime.now().strftime('%Y%m')) or int(str(LIMITEANO)+str(LIMITEMES)) > int(str(ANO)+str(MES))):
            print("Escolha uma data válida!")
        else:
            break

    while True:
        LIMITEDIA = input("Dia: ")
        if int(LIMITEDIA) <= 9:
            LIMITEDIA = "0"+str(int(LIMITEDIA))

        if (int(LIMITEDIA) < 1 or int(str(LIMITEANO)+str(LIMITEMES)+str(LIMITEDIA)) < int(datetime.datetime.now().strftime('%Y%m%d')) or int(str(LIMITEANO)+str(LIMITEMES)+str(LIMITEDIA)) > int(str(ANO)+str(MES)+str(DIA))):
            print("Escolha uma data válida!")
        else:
            break

    if datavalida(int(LIMITEANO), int(LIMITEMES), int(LIMITEDIA)) == False:
        print("Introduza uma data válida!")
        addnovotreino(admin)

    print(" ")
    while True:
        TEMTREINADOR = input("Tem treinador? [S/N]: ")
        TEMTREINADOR = TEMTREINADOR.upper()
        if (TEMTREINADOR != 'S' and TEMTREINADOR != 'N'):
            print("Escolha uma resposta válida!")
        else:
            break

    if (TEMTREINADOR == 'S'):

        listarTreinadores()
        
        while True:
            print("[E] - Escolher treinador já existente")
            print("[N] - Adicionar novo treinador")
            OPCAO = input("Opção: ")
            OPCAO = OPCAO.upper()
            if (OPCAO != 'E' and OPCAO != 'N'):
                print("Escolha uma resposta válida!")
            else:
                break

        if (OPCAO == 'N'):
            
            while True:
                PRIMEIRONOME = input("Primeiro nome: ")
                if (PRIMEIRONOME == '' or ' ' in PRIMEIRONOME):
                    print("Não insira espaços ou campos vazios!")
                else:
                    break

            while True:
                APELIDO = input("Apelido: ")
                if (APELIDO == '' or ' ' in APELIDO):
                    print("Não insira espaços ou campos vazios!")
                else:
                    break

            NOMETREINADOR = PRIMEIRONOME+" "+APELIDO
            IDTREINADOR = insere_novo_treinador(NOMETREINADOR)
        else:
            while True:
                IDTREINADOR = input("Selecione o ID: ")
                EXISTE = verifica_treinador(IDTREINADOR)
                if (EXISTE != 1):     # ALTERAR PARA     SE NÃO EXISTIR UM TREINADOR COM ESSE ID
                    print("Escolha uma resposta válida!")
                else:
                    break

    DATACORRIDAFORMATADA = ANO+"-"+MES+"-"+DIA+" "+HORA+":"+MINUTO
    LIMITEDATAFORMATADA = LIMITEANO+"-"+LIMITEMES+"-"+LIMITEDIA

    if TEMTREINADOR == 'S':
        insere_novo_treinoCOMtreinador(REPETE, datetime.datetime(int(ANO), int(MES), int(DIA)).weekday(), IDTREINADOR, LOCAL, DISTANCIA, LIMITEINSCRITOS, LIMITEDATAFORMATADA, DATACORRIDAFORMATADA)
    else:
        insere_novo_treinoSEMtreinador(REPETE, datetime.datetime(int(ANO), int(MES), int(DIA)).weekday(), LOCAL, DISTANCIA, LIMITEINSCRITOS, LIMITEDATAFORMATADA, DATACORRIDAFORMATADA)

    menuadmin(admin)

# =============================================================================================
# =============================================================================================

def registarmembro():
    clear()
    print(" ")
    print(datetime.datetime.now().strftime('%Y-%m-%d ======== COIMBRA RUN CLUB ======== %H:%M:%S'))
    print(" ")
    print("REGISTAR (MEMBRO) ------------------------------------")
    print(" ")

    while True:
        EMAIL = input("E-mail: ")
        if (EMAIL == '' or ' ' in EMAIL):
            print("Não insira espaços ou campos vazios!")
        else:
            break
    EMAIL = EMAIL.lower()

    while True:
        USERNAME = input("Username: ")
        if (USERNAME == '' or ' ' in USERNAME):
            print("Não insira espaços ou campos vazios!")
        else:
            break
    USERNAME = USERNAME.lower()

    while True:
        PRIMEIRONOME = input("Primeiro nome: ")
        if (PRIMEIRONOME == '' or ' ' in PRIMEIRONOME):
            print("Não insira espaços ou campos vazios!")
        else:
            break

    while True:
        APELIDO = input("Apelido: ")
        if (APELIDO == '' or ' ' in APELIDO):
            print("Não insira espaços ou campos vazios!")
        else:
            break

    NOME = PRIMEIRONOME+" "+APELIDO
    PASSWORD = "PASSWORD"
    CONFIRMARPASSWORD = "CONFIRMARPASSWORD"

    while PASSWORD != CONFIRMARPASSWORD:
        print(" ")
        PASSWORD = maskpass.askpass(prompt="Password: ", mask="*")
        PASSWORD = hashlib.md5(PASSWORD.encode())
        PASSWORD = PASSWORD.hexdigest()
        CONFIRMARPASSWORD = maskpass.askpass(
            prompt="Confirmar password: ", mask="*")
        CONFIRMARPASSWORD = hashlib.md5(CONFIRMARPASSWORD.encode())
        CONFIRMARPASSWORD = CONFIRMARPASSWORD.hexdigest()
        if PASSWORD != CONFIRMARPASSWORD:
            print(" ")
            print("ERRO: As passwords não são identicas!")
            print("Tente novamente!")
            print(" ")

    SEXO = 'X'
    while SEXO != 'F' and SEXO != 'M':
        print(" ")
        SEXO = input('Sexo [F/M]: ')
        SEXO = SEXO.upper()

    insere_novo_membro(EMAIL, PASSWORD, NOME, USERNAME, SEXO)

# =============================================================================================
# =============================================================================================

def insere_novo_membro(email, password, nome, username, sexo):
    try:
        conn = psycopg2.connect(user="postgres",
                                password="postgres",
                                host="localhost",
                                port="5433",
                                database="CRC")

        cur = conn.cursor()

        cur.execute("CALL insere_membro('{0}','{1}','{2}','{3}','{4}')".format(nome,email,password,username,sexo))
        conn.commit()

    except (Exception, psycopg2.Error):
        if(conn):
            print(
                "Já existe uma conta com esse email e/ou username. Por favor tente outro!")

    finally:
        # closing database connection.
        if(conn):
            cur.close()
            conn.close()

# =============================================================================================
# =============================================================================================

def verifica_login_admin(input_email, input_password):
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="postgres",
                                      host="localhost",
                                      port="5433",
                                      database="CRC")

        cursor = connection.cursor()

        cursor.execute("SELECT email, password FROM utilizadores, administradores WHERE utilizadores.id = administradores.utilizadores_id AND email =%s AND password = %s;",
                       (input_email, input_password))

        if cursor.rowcount == 1:
            return 1  # Login válido
        else:
            return 0  # Login inválido

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
    finally:
        # closing database connection.
        if(connection):
            cursor.close()
            connection.close()

# =============================================================================================
# =============================================================================================

def verifica_login_membro(input_email, input_password):
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="postgres",
                                      host="localhost",
                                      port="5433",
                                      database="CRC")

        cursor = connection.cursor()

        cursor.execute("SELECT email, password FROM utilizadores,membros WHERE utilizadores.id = membros.utilizadores_id AND email =%s AND password = %s;",
                       (input_email, input_password))

        if cursor.rowcount == 1:
            return 1  # Login válido
        else:
            return 0  # Login inválido

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
    finally:
        # closing database connection.
        if(connection):
            cursor.close()
            connection.close()

# =============================================================================================
# =============================================================================================

def converteemailparausername(input_email):

    try:
        conn = psycopg2.connect(user="postgres",
                                password="postgres",
                                host="localhost",
                                port="5433",
                                database="CRC") 

        cur = conn.cursor()

        cur.execute("SELECT username FROM utilizadores WHERE email = '{0}';".format(input_email))
    
        conn.commit()
        
        i = 0
        for linha in cur.fetchall():
            i = cur.rowcount
            username = linha[0]  # username
            
        # row = cursor.fetchone()

        if(i == 0):
            print("erro a converter email para username")

        return username
        

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
    finally:
        # closing database connection.
        if(conn):
            cur.close()
            conn.close()

# =============================================================================================
# =============================================================================================

def converteidparausername(input_id):

    try:
        conn = psycopg2.connect(user="postgres",
                                password="postgres",
                                host="localhost",
                                port="5433",
                                database="CRC") 

        cur = conn.cursor()

        cur.execute("SELECT username FROM utilizadores WHERE id = {0};".format(input_id))
    
        conn.commit()
        
        i = 0
        for linha in cur.fetchall():
            i = cur.rowcount
            username = linha[0]  # username
            
        # row = cursor.fetchone()

        if(i == 0):
            print("erro a converter email para username")

        return username
        

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
    finally:
        # closing database connection.
        if(conn):
            cur.close()
            conn.close()

# =============================================================================================
# =============================================================================================

def insere_novo_treinoSEMtreinador(rep, dia_semana, sitio, km, lim_inscritos, lim_data, data_corrida):
    try:
        conn = psycopg2.connect(user="postgres",
                                password="postgres",
                                host="localhost",
                                port="5433",
                                database="CRC")

        cur = conn.cursor()

        cur.execute("INSERT INTO corridas VALUES (DEFAULT, %s, %s, %s, %s, %s, 0) RETURNING id;",
                    (sitio, km, lim_inscritos, lim_data, data_corrida))
        IDCORRIDA = cur.fetchone()
        conn.commit()

        cur.execute(
            "INSERT INTO treinos VALUES (%s, %s, NULL, %s);",
            (rep, dia_semana, IDCORRIDA))
        conn.commit()

    except (Exception, psycopg2.Error):
        if(conn):
            print(
                "erro!")

    finally:
        # closing database connection.
        if(conn):
            cur.close()
            conn.close()

# =============================================================================================
# =============================================================================================

def insere_novo_treinoCOMtreinador(rep, dia_semana, id_treinador, sitio, km, lim_inscritos, lim_data, data_corrida):
    try:
        conn = psycopg2.connect(user="postgres",
                                password="postgres",
                                host="localhost",
                                port="5433",
                                database="CRC")

        cur = conn.cursor()

        cur.execute("INSERT INTO corridas VALUES (DEFAULT, %s, %s, %s, %s, %s, 0) RETURNING id;",
                    (sitio, km, lim_inscritos, lim_data, data_corrida))
        IDCORRIDA = cur.fetchone()
        conn.commit()

        cur.execute(
            "INSERT INTO treinos VALUES (%s, %s, %s, %s);",
            (rep, dia_semana, id_treinador, IDCORRIDA))
        conn.commit()

    except (Exception, psycopg2.Error):
        if(conn):
            print(
                "Erro!")

    finally:
        # closing database connection.
        if(conn):
            cur.close()
            conn.close()

# =============================================================================================
# =============================================================================================

def insere_novo_treinador(nome):
    try:
        conn = psycopg2.connect(user="postgres",
                                password="postgres",
                                host="localhost",
                                port="5433",
                                database="CRC")

        cur = conn.cursor()
        cur.execute("INSERT INTO treinadores VALUES (DEFAULT, %s) RETURNING id;",  # DUVIDA
                    (nome,))
        TREINADOR = cur.fetchone()
        conn.commit()
        IDTREINADOR = int(TREINADOR[0])

        return IDTREINADOR

    except (Exception, psycopg2.Error):
        if(conn):
            print("ERRO!")

    finally:
        # closing database connection.
        if(conn):
            cur.close()
            conn.close()

# =============================================================================================
# =============================================================================================

def listarTreinadores():

    try:
        conn = psycopg2.connect(user="postgres",
                                password="postgres",
                                host="localhost",
                                port="5433",
                                database="CRC") 

        cur = conn.cursor()

        #inicio
        cur.execute("SELECT * FROM treinadores")
        #fim            
        conn.commit()
        print(" ")
        for linha in cur.fetchall():
            x1 = linha[0]  # id
            x2 = linha[1]  # nome

            print("ID:", x1, "-", x2)
        print(" ")
    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
    finally:
        # closing database connection.
        if(conn):
            cur.close()
            conn.close()

# =============================================================================================
# =============================================================================================

def verifica_treinador(input_id):
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="postgres",
                                      host="localhost",
                                      port="5433",
                                      database="CRC")

        cursor = connection.cursor()

        cursor.execute("SELECT nome FROM treinadores WHERE id = %s;",
                       (input_id,))

        if cursor.rowcount == 1:
            return 1  # Login válido
        else:
            return 0  # Login inválido

    except (Exception, psycopg2.Error) as error:
        print("Erro", error)
    finally:
        # closing database connection.
        if(connection):
            cursor.close()
            connection.close()

# =============================================================================================
# =============================================================================================

def addnovaprova(admin):
    limparjanela(admin)
    print("NOVA PROVA -------------------------------------------")
    print(" ")
    MENU = "NP"
    print("Distância:")
    print("[A] - 1km")
    print("[B] - 5km")
    print("[C] - 10km")
    print("[D] - 20km")
    print("[E] - 40km (maratona)")
    print(" ")
    OPCAO = input('Selecionar opcao: ')
    OPCAO = OPCAO.upper()
    if OPCAO == 'A':
        DISTANCIA = 1
    elif OPCAO == 'B':
        DISTANCIA = 5
    elif OPCAO == 'C':
        DISTANCIA = 10
    elif OPCAO == 'D':
        DISTANCIA = 20
    elif OPCAO == 'E':
        DISTANCIA = 40
    else:
        addnovaprova(admin)
    

    while True:
        LOCAL = input("Local: ")
        if (LOCAL == ''):
            print("Não insira campos vazios!")
        else:
            break


    while True:
        LIMITEINSCRITOS = int(input("Número MAX de inscritos: "))
        if (LIMITEINSCRITOS < 3):
            print("Insira dados válidos!")
        else:
            break


    print("DATA DA PROVA ----------------------------------------")
    print(" ")

    while True:
        ANO = input("Ano: ")
        if (int(ANO) < int(datetime.datetime.now().strftime('%Y'))):
            print("Não pode escolher uma data do passado!")
        else:
            break

    while True:
        MES = input("Mes: ")

        if int(MES) <= 9:
            MES = "0"+str(int(MES))

        if (int(MES) < 1 or int(str(ANO)+str(MES)) < int(datetime.datetime.now().strftime('%Y%m'))):
            print("Não pode escolher uma data do passado!")
        else:
            break

    while True:
        DIA = input("Dia: ")
        if int(DIA) <= 9:
            DIA = "0"+str(int(DIA))

        if (int(DIA) < 1 or int(str(ANO)+str(MES)+str(DIA)) < int(datetime.datetime.now().strftime('%Y%m%d'))):
            print("Não pode escolher uma data do passado!")
        else:
            break

    if datavalida(int(ANO), int(MES), int(DIA)) == False:
        print("Introduza uma data válida!")
        addnovaprova(admin)

    while True:
        HORA = input("Hora (h): ")
        if (int(HORA) < 0 or int(HORA) > 23 ):
            print("Introduza uma hora válida!")
        else:
            if int(HORA) <= 9:
                HORA = "0"+str(int(HORA))
            break

    while True:
        MINUTO = input("Minuto (m): ")
        if (int(MINUTO) < 0 or int(MINUTO) > 59 ):
            print("Introduza uma hora válida!")
        else:
            if int(MINUTO) <= 9:
                MINUTO = "0"+str(int(MINUTO))
            break

    print("Nova Prova inserida a "+DIA+"-"+MES+"-"+ANO+" "+HORA+":"+MINUTO)


    print("DATA LIMITE PARA INSCRIÇÃO ---------------------------")
    print(" ")

    while True:
        LIMITEANO = input("Ano: ")
        if (int(LIMITEANO) < int(datetime.datetime.now().strftime('%Y')) or int(LIMITEANO) > int(ANO)):
            print("Escolha uma data válida!")
        else:
            break

    while True:
        LIMITEMES = input("Mes: ")

        if int(LIMITEMES) <= 9:
            LIMITEMES = "0"+str(int(LIMITEMES))

        if (int(LIMITEMES) < 1 or int(str(LIMITEANO)+str(LIMITEMES)) < int(datetime.datetime.now().strftime('%Y%m')) or int(str(LIMITEANO)+str(LIMITEMES)) > int(str(ANO)+str(MES))):
            print("Escolha uma data válida!")
        else:
            break

    while True:
        LIMITEDIA = input("Dia: ")
        if int(LIMITEDIA) <= 9:
            LIMITEDIA = "0"+str(int(LIMITEDIA))

        if (int(LIMITEDIA) < 1 or int(str(LIMITEANO)+str(LIMITEMES)+str(LIMITEDIA)) < int(datetime.datetime.now().strftime('%Y%m%d')) or int(str(LIMITEANO)+str(LIMITEMES)+str(LIMITEDIA)) >= int(str(ANO)+str(MES)+str(DIA))):
            print("Escolha uma data válida e pelo menos 1 dia antes do treino!")
        else:
            break

    if datavalida(int(LIMITEANO), int(LIMITEMES), int(LIMITEDIA)) == False:
        print("Introduza uma data válida!")
        addnovotreino(admin)


    while True:
        PRECO = input("Preço (EUR): ")
        if (PRECO == '' or PRECO == ' '):
            print("Escolha uma resposta válida!")
        else:
            break

    DATACORRIDAFORMATADA = ANO+"-"+MES+"-"+DIA+" "+HORA+":"+MINUTO
    LIMITEDATAFORMATADA = LIMITEANO+"-"+LIMITEMES+"-"+LIMITEDIA
    USERNAMEADMIN = admin

    insere_nova_prova(PRECO, LOCAL, DISTANCIA, LIMITEINSCRITOS, LIMITEDATAFORMATADA, DATACORRIDAFORMATADA, USERNAMEADMIN)

    menuadmin(admin)

# =============================================================================================
# =============================================================================================

def insere_nova_prova(preco, sitio, km, lim_inscritos, lim_data, data_corrida, usernameadmin):
    try:
        conn = psycopg2.connect(user="postgres",
                                password="postgres",
                                host="localhost",
                                port="5433",
                                database="CRC")

        cur = conn.cursor()

        cur.execute("INSERT INTO corridas VALUES (DEFAULT, %s, %s, %s, %s, %s, 0) RETURNING id;",
                    (sitio, km, lim_inscritos, lim_data, data_corrida))
        IDCORRIDA = cur.fetchone()
        conn.commit()

        cur.execute(
            "INSERT INTO provas VALUES (%s, %s);",
            (preco, IDCORRIDA))
        conn.commit()

        cur.execute(
            "SELECT id FROM utilizadores WHERE username = '{0}';".format(usernameadmin))
        IDADMIN = cur.fetchone()
        conn.commit()

        cur.execute(
            "INSERT INTO hist_de_alt_preco VALUES (DEFAULT, %s, %s, %s, %s);",
            (preco, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), IDADMIN, IDCORRIDA))
        conn.commit()

    except (Exception, psycopg2.Error):
        if(conn):
            print(
                "erro!")

    finally:
        # closing database connection.
        if(conn):
            cur.close()
            conn.close()

# =============================================================================================
# =============================================================================================

def listarProvas():

    try:
        conn = psycopg2.connect(user="postgres",
                                password="postgres",
                                host="localhost",
                                port="5433",
                                database="CRC") 

        cur = conn.cursor()

        #inicio
        cur.execute("SELECT corridas.id, corridas.sitio, corridas.km, corridas.lim_data, corridas.data_corrida, corridas.lim_inscritos, corridas.num_inscritos, provas.valor "
                    "FROM corridas, provas "
                    "WHERE corridas.id = provas.corridas_id AND corridas.lim_data > '{0}'".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        #fim            
        conn.commit()


        for linha in cur.fetchall():
            x1 = linha[0]  # id
            x2 = linha[1]  # local
            x3 = linha[2]  # distancia
            x4 = linha[3]  # data limite
            x5 = linha[4]  # data corrida
            x6 = linha[5]  # limite inscritos
            x7 = linha[6]  # numero inscritos
            x8 = linha[7]  # valor

            vagas = x6-x7

            if vagas > 0:
                print("ID:", x1, "\n| Local:", x2, "| Distancia:", x3, "km | Data:", x5,
                      "\n| Limite Inscricao:", x4, "| Vagas:", vagas, "\n| Valor:", x8,"EUR\n")

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
    finally:
        # closing database connection.
        if(conn):
            cur.close()
            conn.close()

# =============================================================================================
# =============================================================================================

def SelecionarDestinatario(admin):
    limparjanela(admin)
    print("ENVIAR MENSAGEM --------------------------------------")
    print(" ")
    MENU = "NP"
    print("Destinatário:")
    print("[TM] - Todos os Membros")
    print("[ME] - Membro Específico")
    print("[GP] - Grupo de Prova")
    print("[GT] - Grupo de Treino")
    print("\n[S] - Sair")

    print(" ")
    OPCAO = input("Selecionar opcao: ")
    OPCAO = OPCAO.upper()
    print(" ")
    if OPCAO == "TM":

        while True:
            ASSUNTO = input("Assunto: ")
            if (ASSUNTO == '' or ASSUNTO == ' '):
                print("Escolha uma resposta válida!")
            else:
                break
        print(" ")
        while True:
            TEXTO = input("Texto: ")
            if (TEXTO == '' or TEXTO == ' '):
                print("Escolha uma resposta válida!")
            else:
                break

        enviarmensagemTM(admin, ASSUNTO, TEXTO)


    elif OPCAO == "ME":
        listarMembros()

        while True:
            USERNAMEMEMBRO = input("Username: @")
            IDMEMBRO = converteusernameparaid(USERNAMEMEMBRO)
            
            EXISTE = verifica_membro(IDMEMBRO)
            if (EXISTE != 1):
                print("Escolha uma resposta válida!")
            else:
                break
        print(" ")
        while True:
            ASSUNTO = input("Assunto: ")
            if (ASSUNTO == '' or ASSUNTO == ' '):
                print("Escolha uma resposta válida!")
            else:
                break
        print(" ")
        while True:
            TEXTO = input("Texto: ")
            if (TEXTO == '' or TEXTO == ' '):
                print("Escolha uma resposta válida!")
            else:
                break

        enviarmensagemME(admin, ASSUNTO, TEXTO, IDMEMBRO)


    elif OPCAO == "GP":

        listarProvasCOMinscritos(admin)


        while True:
            IDPROVA = input("ID da Prova: #")
            
            EXISTE = verifica_prova(IDPROVA)
            if (EXISTE != 1):
                print("Escolha uma resposta válida!")
            else:
                break
        print(" ")

        while True:
            print("Da prova #" + str(IDPROVA) + " enviar mensagem para:")
            print("[N] - Quem ainda não pagou")
            print("[P] - Quem já pagou")
            print("[T] - Todos")
            print(" ")


            OP = input("Opção: ")
            OP = OP.upper()
            if (OP != 'N' and OP != 'P' and OP != 'T'):
                print("Escolha uma resposta válida!")
            else:
                break

        print(" ")

        while True:
            ASSUNTO = input("Assunto: ")
            if (ASSUNTO == '' or ASSUNTO == ' '):
                print("Escolha uma resposta válida!")
            else:
                break
        print(" ")
        while True:
            TEXTO = input("Texto: ")
            if (TEXTO == '' or TEXTO == ' '):
                print("Escolha uma resposta válida!")
            else:
                break


        if OP == "N": 
            enviarmensagemGP_NAOPAGO(admin, ASSUNTO, TEXTO, IDPROVA)

        elif OP == "P": 
            enviarmensagemGP_PAGO(admin, ASSUNTO, TEXTO, IDPROVA)

        else: 
            enviarmensagemG_TODOS(admin, ASSUNTO, TEXTO, IDPROVA)


    elif OPCAO == "GT":

        listarTreinosCOMinscritos(admin)

        while True:
            IDTREINO = input("ID do Treino: #")
            
            EXISTE = verifica_treino(IDTREINO)
            if (EXISTE != 1):
                print("Escolha uma resposta válida!")
            else:
                break
        print(" ")
        while True:
            ASSUNTO = input("Assunto: ")
            if (ASSUNTO == '' or ASSUNTO == ' '):
                print("Escolha uma resposta válida!")
            else:
                break
        print(" ")
        while True:
            TEXTO = input("Texto: ")
            if (TEXTO == '' or TEXTO == ' '):
                print("Escolha uma resposta válida!")
            else:
                break

        enviarmensagemG_TODOS(admin, ASSUNTO, TEXTO, IDTREINO)


    elif OPCAO == "S":
        menuadmin(admin)
    else:
        SelecionarDestinatario(admin)
    
# =============================================================================================
# =============================================================================================

def enviarmensagemTM(admin, ASSUNTO, TEXTO):
    try:
        conn = psycopg2.connect(user="postgres",
                                password="postgres",
                                host="localhost",
                                port="5433",
                                database="CRC")

        cur = conn.cursor()
        IDADMIN = converteusernameparaid(admin)
        cur.execute("INSERT INTO mensagens VALUES (DEFAULT, '{0}', '{1}', '{2}', {3}) RETURNING id;".format(ASSUNTO, TEXTO, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), IDADMIN))

        IDMENSAGEM = cur.fetchone()
        conn.commit()

        cur.execute("SELECT utilizadores_id FROM membros;")          
        conn.commit()

        for linha in cur.fetchall():
            IDMEMBRO = linha[0]  # id
            
            cur.execute("INSERT INTO leituras VALUES (false, %s, %s);",(IDMEMBRO, IDMENSAGEM))
            conn.commit()

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
    finally:
        # closing database connection.
        if(conn):
            cur.close()
            conn.close()

# =============================================================================================
# =============================================================================================

def enviarmensagemME(admin, ASSUNTO, TEXTO, IDMEMBRO):
    try:
        conn = psycopg2.connect(user="postgres",
                                password="postgres",
                                host="localhost",
                                port="5433",
                                database="CRC")

        cur = conn.cursor()
        IDADMIN = converteusernameparaid(admin)
        cur.execute("INSERT INTO mensagens VALUES (DEFAULT, '{0}', '{1}', '{2}', {3}) RETURNING id;".format(ASSUNTO, TEXTO, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), IDADMIN))
        IDMENSAGEM = cur.fetchone()
        conn.commit()

        cur.execute("INSERT INTO leituras VALUES (false, %s, %s);",(IDMEMBRO, IDMENSAGEM))
        conn.commit()

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
    finally:
        # closing database connection.
        if(conn):
            cur.close()
            conn.close()

# =============================================================================================
# =============================================================================================

def verifica_treino(input_id):
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="postgres",
                                      host="localhost",
                                      port="5433",
                                      database="CRC")

        cursor = connection.cursor()

        cursor.execute("SELECT corridas_id FROM treinos WHERE corridas_id = %s;",
                       (input_id,))

        if cursor.rowcount == 1:
            return 1  # Login válido
        else:
            return 0  # Login inválido

    except (Exception, psycopg2.Error) as error:
        print("Erro", error)
    finally:
        # closing database connection.
        if(connection):
            cursor.close()
            connection.close()

# =============================================================================================
# =============================================================================================

def verifica_prova(input_id):
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="postgres",
                                      host="localhost",
                                      port="5433",
                                      database="CRC")

        cursor = connection.cursor()

        cursor.execute("SELECT corridas_id FROM provas WHERE corridas_id = %s;",
                       (input_id,))

        if cursor.rowcount == 1:
            return 1  # Login válido
        else:
            return 0  # Login inválido

    except (Exception, psycopg2.Error) as error:
        print("Erro", error)
    finally:
        # closing database connection.
        if(connection):
            cursor.close()
            connection.close()

# =============================================================================================
# =============================================================================================

def converteusernameparaid(input_username):

    try:
        conn = psycopg2.connect(user="postgres",
                                password="postgres",
                                host="localhost",
                                port="5433",
                                database="CRC") 

        cur = conn.cursor()

        cur.execute("SELECT id FROM utilizadores WHERE username = '{0}';".format(input_username))
    
        conn.commit()
        
        i = 0
        for linha in cur.fetchall():
            i = cur.rowcount
            id = linha[0]  # username
            
        # row = cursor.fetchone()

        if(i == 0):
            print("erro a converter email para username")

        return id
        

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
    finally:
        # closing database connection.
        if(conn):
            cur.close()
            conn.close()

# =============================================================================================
# =============================================================================================

def verifica_membro(input_id):
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="postgres",
                                      host="localhost",
                                      port="5433",
                                      database="CRC")

        cursor = connection.cursor()

        cursor.execute("SELECT utilizadores_id FROM membros WHERE utilizadores_id = %s;",
                       (input_id,))

        if cursor.rowcount == 1:
            return 1  # Login válido
        else:
            return 0  # Login inválido

    except (Exception, psycopg2.Error) as error:
        print("Erro", error)
    finally:
        # closing database connection.
        if(connection):
            cursor.close()
            connection.close()

# =============================================================================================
# =============================================================================================

def listarMembros():

    try:
        conn = psycopg2.connect(user="postgres",
                                password="postgres",
                                host="localhost",
                                port="5433",
                                database="CRC") 

        cur = conn.cursor()

        #inicio
        cur.execute("SELECT utilizadores.id, utilizadores.nome, utilizadores.email, utilizadores.username, membros.sexo FROM utilizadores, membros WHERE utilizadores.id = membros.utilizadores_id")
        #fim            
        conn.commit()
        print(" ")

        for linha in cur.fetchall():
            x1 = linha[0]  # id
            x2 = linha[1]  # nome
            x3 = linha[2]  # email
            x4 = linha[3]  # username
            x5 = linha[4]  # sexo

            print("@" + x4, "\n| ID:", x1, "| Nome:", x2, "| Sexo:", x5,
                "\n| Email:", x3,"\n")

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
    finally:
        # closing database connection.
        if(conn):
            cur.close()
            conn.close()

# =============================================================================================
# =============================================================================================

def alterarTreino(IDTREINO, admin): # TERMINAR ISTO
    limparjanela(admin)
    listarUMtreino(IDTREINO)
    
    try:
        conn = psycopg2.connect(user="postgres",
                                password="postgres",
                                host="localhost",
                                port="5433",
                                database="CRC") 

        cur = conn.cursor()

        while True:
            print("Alterar:")
            print(" ")
            print("[R] - Repetição") 
            print("[T] - Treinador")
            print("[L] - Local")
            print("[D] - Distância")
            print(" ")
            print("[LI] - Limite de Inscrições")
            print("[DI] - Data limite de Inscrição")
            print("[DT] - Data do Treino")
            print(" ")
            print("[S] - Sair")
            print(" ")

            ALTERACAO = input("Alterar: ")
            ALTERACAO = ALTERACAO.upper()


            if (ALTERACAO != "R" and ALTERACAO != "T" and ALTERACAO != "L" and ALTERACAO != "D" and ALTERACAO != "LI" and ALTERACAO != "DI" and ALTERACAO != "DT" and ALTERACAO != "S"):
                print("Insira dados válidos!")
            else:
                break

        if ALTERACAO == "R":

            while True:
                print("Quer que o Treino #" + str(IDTREINO) + " repita:")
                print("[S] - Semanalmente")
                print("[M] - Mensalmente")
                print("[N] - Não repetir")
                REPETIR = input("Opção: ")
                REPETIR = REPETIR.upper()


                if (REPETIR != "S" and REPETIR != "M" and REPETIR != "N"):
                    print("Insira dados válidos!")
                else:
                    break
                
            cur.execute("UPDATE treinos SET rep = '{0}' WHERE corridas_id = {1}".format(REPETIR, IDTREINO))
            conn.commit()

            alterarTreino(IDTREINO, admin)

        elif ALTERACAO == "T":
            print("Alterar Treinador:")

            while True:
                print("[E] - Escolher treinador já existente")
                print("[N] - Adicionar novo treinador")
                print("[R] - Remover treinador do treino")

                OPCAO = input("Opção: ")
                OPCAO = OPCAO.upper()
                if (OPCAO != 'E' and OPCAO != 'N' and OPCAO != 'R'):
                    print("Escolha uma resposta válida!")
                else:
                    break

            if (OPCAO == 'N'):
                print(" ")
                while True:
                    PRIMEIRONOME = input("Primeiro nome: ")
                    if (PRIMEIRONOME == '' or ' ' in PRIMEIRONOME):
                        print("Não insira espaços ou campos vazios!")
                    else:
                        break

                while True:
                    APELIDO = input("Apelido: ")
                    if (APELIDO == '' or ' ' in APELIDO):
                        print("Não insira espaços ou campos vazios!")
                    else:
                        break
                print(" ")
                NOMETREINADOR = PRIMEIRONOME+" "+APELIDO
                IDTREINADOR = insere_novo_treinador(NOMETREINADOR)

                cur.execute("UPDATE treinos SET treinadores_id = {0} WHERE corridas_id = {1}".format(IDTREINADOR, IDTREINO))       # AQUI TREIN
                conn.commit()

            elif (OPCAO == 'E'):
                while True:
                    limparjanela(admin)
                    listarTreinadores()
                    IDTREINADOR = input("Selecione o ID: ")
                    EXISTE = verifica_treinador(IDTREINADOR)
                    if (EXISTE != 1): 
                        print("Escolha uma resposta válida!")
                    else:
                        break
                cur.execute("UPDATE treinos SET treinadores_id = {0} WHERE corridas_id = {1}".format(IDTREINADOR, IDTREINO))
                conn.commit()

            else:
                cur.execute("UPDATE treinos SET treinadores_id = NULL WHERE corridas_id = {0}".format(IDTREINO))
                conn.commit()

            alterarTreino(IDTREINO, admin)


        elif ALTERACAO == "L":
            print(" ")

            while True:
                LOCAL = input("Local: ")
                if (LOCAL == ''):
                    print("Não insira campos vazios!")
                else:
                    break

            cur.execute("UPDATE corridas SET sitio = '{0}' WHERE id = {1}".format(LOCAL, IDTREINO))
            conn.commit()

            alterarTreino(IDTREINO, admin)


        elif ALTERACAO == "D":
            print(" ")
            print("Distância:")
            print("[A] - 1km")
            print("[B] - 5km")
            print("[C] - 10km")
            print("[D] - 20km")
            print("[E] - 40km (maratona)")
            print(" ")
            OPCAO = input('Selecionar opcao: ')
            OPCAO = OPCAO.upper()
            if OPCAO == 'A':
                DISTANCIA = 1
            elif OPCAO == 'B':
                DISTANCIA = 5
            elif OPCAO == 'C':
                DISTANCIA = 10
            elif OPCAO == 'D':
                DISTANCIA = 20
            elif OPCAO == 'E':
                DISTANCIA = 40
            else:
                alterarTreino(IDTREINO, admin)

            cur.execute("UPDATE corridas SET km = {0} WHERE id = {1}".format(DISTANCIA, IDTREINO))
            conn.commit()

            alterarTreino(IDTREINO, admin)


        elif ALTERACAO == "LI":
            print(" ")
            while True:
                LIMITEINSCRITOS = int(input("Número MAX de inscritos: "))


                cur.execute("SELECT num_inscritos FROM corridas WHERE corridas.id = {0}".format(IDTREINO))
                conn.commit()
                NUMINSCRITOS = cur.fetchone()[0]
                if (LIMITEINSCRITOS < 3):
                    print("Insira dados válidos!")
                elif(LIMITEINSCRITOS < NUMINSCRITOS):
                    print("O limite de inscritos não pode ser inferior ao numero de inscritos:",NUMINSCRITOS)
                else:
                    break
                #fim9
            cur.execute("UPDATE corridas SET lim_inscritos = {0} WHERE id = {1}".format(LIMITEINSCRITOS, IDTREINO))
            conn.commit()
            alterarTreino(IDTREINO, admin)



        elif ALTERACAO == "DI":

            print(" ")
            print("DATA LIMITE PARA INSCRIÇÃO ---------------------------")
            print(" ")




            cur.execute("SELECT lim_data, data_corrida FROM corridas WHERE id = {0};".format(IDTREINO))
    
            conn.commit()
        
            for linha in cur.fetchall():
                dataINSCoriginal = datetime.datetime.combine(linha[0], datetime.datetime.min.time()) # data de incr
                dataCORRoriginal = linha[1] # data da corrida


            while True:
                LIMITEANO = input("Ano: ")
                if (int(LIMITEANO) < int(datetime.datetime.now().strftime('%Y')) or int(LIMITEANO) > dataCORRoriginal.year):
                    print("Escolha uma data válida!")
                else:
                    break

            while True:
                LIMITEMES = input("Mes: ")

                if int(LIMITEMES) <= 9:
                    LIMITEMES = "0"+str(int(LIMITEMES))

                MESORIGINAL = dataCORRoriginal.month
                if int(MESORIGINAL) <= 9:
                    MESORIGINAL = "0"+str(int(MESORIGINAL))

                if (int(LIMITEMES) < 1 or int(str(LIMITEANO)+str(LIMITEMES)) < int(datetime.datetime.now().strftime('%Y%m')) or int(str(LIMITEANO)+str(LIMITEMES)) > int(str(dataCORRoriginal.year)+str(MESORIGINAL))):
                    print("Escolha uma data válida!")
                else:
                    break

            while True:
                LIMITEDIA = input("Dia: ")
                if int(LIMITEDIA) <= 9:
                    LIMITEDIA = "0"+str(int(LIMITEDIA))

                DIAORIGINAL = dataCORRoriginal.day
                if int(DIAORIGINAL) <= 9:
                    DIAORIGINAL = "0"+str(int(DIAORIGINAL))

                if (int(LIMITEDIA) < 1 or int(str(LIMITEANO)+str(LIMITEMES)+str(LIMITEDIA)) < int(datetime.datetime.now().strftime('%Y%m%d')) or int(str(LIMITEANO)+str(LIMITEMES)+str(LIMITEDIA)) > int(str(dataCORRoriginal.year)+str(MESORIGINAL)+str(DIAORIGINAL))):
                    print("Escolha uma data válida!")
                else:
                    break

            if datavalida(int(LIMITEANO), int(LIMITEMES), int(LIMITEDIA)) == False:
                print("Introduza uma data válida!")
                alterarTreino(IDTREINO, admin)


            LIMITEDATAFORMATADA = LIMITEANO+"-"+LIMITEMES+"-"+LIMITEDIA

            cur.execute("UPDATE corridas SET lim_data = '{0}' WHERE id = {1}".format(LIMITEDATAFORMATADA, IDTREINO))
            conn.commit()
            alterarTreino(IDTREINO, admin)



        elif ALTERACAO == "DT":

            print(" ")
            print("DATA DO TREINO ---------------------------------------")
            print(" ")

            cur.execute("SELECT lim_data, data_corrida FROM corridas WHERE id = {0};".format(IDTREINO))
    
            conn.commit()
        
            for linha in cur.fetchall():
                dataINSCoriginal = datetime.datetime.combine(linha[0], datetime.datetime.min.time()) # data de incr
                dataCORRoriginal = linha[1] # data da corrida

                DIFdias = (dataCORRoriginal - dataINSCoriginal).days

            while True:
                ANO = input("Ano: ")
                if (int(ANO) < int(datetime.datetime.now().strftime('%Y'))):
                    print("Escolha uma data válida!")
                else:
                    break

            while True:
                MES = input("Mes: ")

                if int(MES) <= 9:
                    MES = "0"+str(int(MES))

                if (int(MES) < 1 or int(str(ANO)+str(MES)) < int(datetime.datetime.now().strftime('%Y%m'))):
                    print("Escolha uma data válida!")
                else:
                    break

            while True:
                DIA = input("Dia: ")
                if int(DIA) <= 9:
                    DIA = "0"+str(int(DIA))

                if (int(DIA) < 1 or int(str(ANO)+str(MES)+str(DIA)) < int(datetime.datetime.now().strftime('%Y%m%d'))):
                    print("Escolha uma data válida!")
                else:
                    break

            if datavalida(int(ANO), int(MES), int(DIA)) == False:
                print("Introduza uma data válida!")
                alterarTreino(IDTREINO, admin)


            while True:
                HORA = input("Hora (h): ")
                if (int(HORA) < 0 or int(HORA) > 23 ):
                    print("Introduza uma hora válida!")
                else:
                    if int(HORA) <= 9:
                        HORA = "0"+str(int(HORA))
                    break

            while True:
                MINUTO = input("Minuto (m): ")
                if (int(MINUTO) < 0 or int(MINUTO) > 59 ):
                    print("Introduza uma hora válida!")
                else:
                    if int(MINUTO) <= 9:
                        MINUTO = "0"+str(int(MINUTO))
                    break


            DATACORRIDA = ANO+"-"+MES+"-"+DIA+" "+HORA+":"+MINUTO+":00"
            DATACORRIDAFORMATADA = datetime.datetime.strptime(DATACORRIDA, '%Y-%m-%d %H:%M:%S')
            LIMITEDATAFORMATADA = DATACORRIDAFORMATADA - datetime.timedelta(days=DIFdias)

            cur.execute("UPDATE corridas SET lim_data = '{0}', data_corrida = '{1}' WHERE id = {2}".format(LIMITEDATAFORMATADA, DATACORRIDAFORMATADA, IDTREINO))
            conn.commit()
            alterarTreino(IDTREINO, admin)
            
        else:
            menuadmin(admin)

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
    finally:
        # closing database connection.
        if(conn):
            cur.close()
            conn.close()

# =============================================================================================
# =============================================================================================

def updatedates():
    # Se for Semanal
        # ver a diferenca (DIF) de dias entre o limite e a corrida
        # somar +7 dias a data inicial ate dar um dia do futuro ou presente
        # subtrair DIF a essa data e obter a data de inscricao

    # Se for Mensal
        # ver a diferenca (DIF) de dias entre o limite e a corrida
        # somar +1 mes a data inicial ate dar um dia do futuro ou presente
        # subtrair DIF a essa data e obter a data de inscricao


    try:
        conn = psycopg2.connect(user="postgres",
                                password="postgres",
                                host="localhost",
                                port="5433",
                                database="CRC") 

        cur = conn.cursor()

        
        cur.execute("SELECT corridas.id, corridas.sitio, corridas.km, corridas.lim_data, corridas.data_corrida, corridas.lim_inscritos, corridas.num_inscritos, treinos.rep, treinadores_id "
                    "FROM corridas, treinos "
                    "WHERE corridas.id = treinos.corridas_id")
                
        conn.commit()


        for linha in cur.fetchall():
            x1 = linha[0]  # id
            x2 = linha[1]  # local
            x3 = linha[2]  # distancia

            x4 = linha[3]  # data limite
            x5 = linha[4]  # data corrida

            x6 = linha[5]  # limite inscritos
            x7 = linha[6]  # numero inscritos
            x8 = linha[7]  # repetitivo
            x9 = linha[8]  #id treinador

            DATAINSCRICAO = datetime.datetime.combine(x4, datetime.datetime.min.time())
            DATACORRIDA = x5

            if x8 == "S":

                INICIALmenosINSCRICAO = (DATACORRIDA - DATAINSCRICAO).days

                while DATACORRIDA < datetime.datetime.now():
                    DATACORRIDA = DATACORRIDA + datetime.timedelta(days=7)

                DATAINSCRICAO = DATACORRIDA - datetime.timedelta(days=INICIALmenosINSCRICAO)

                cur.execute("UPDATE treinos SET dia_semana = {0} WHERE corridas_id = {1}".format(DATACORRIDA.weekday(), x1))
                conn.commit()
                cur.execute("UPDATE corridas SET data_corrida = '{0}' WHERE id = {1}".format(DATACORRIDA, x1))
                conn.commit()
                cur.execute("UPDATE corridas SET lim_data = '{0}' WHERE id = {1}".format(DATAINSCRICAO, x1))
                conn.commit()

            elif x8 == "M":

                INICIALmenosINSCRICAO = (DATACORRIDA - DATAINSCRICAO).days

                while DATACORRIDA < datetime.datetime.now():
                    DATACORRIDA = DATACORRIDA + relativedelta(months=1)


                DATAINSCRICAO = DATACORRIDA - datetime.timedelta(days=INICIALmenosINSCRICAO)


                cur.execute("UPDATE treinos SET dia_semana = {0} WHERE corridas_id = {1}".format(DATACORRIDA.weekday(), x1))
                conn.commit()
                cur.execute("UPDATE corridas SET data_corrida = '{0}' WHERE id = {1}".format(DATACORRIDA, x1))
                conn.commit()
                cur.execute("UPDATE corridas SET lim_data = '{0}' WHERE id = {1}".format(DATAINSCRICAO, x1))
                conn.commit()

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
    finally:
        # closing database connection.
        if(conn):
            cur.close()
            conn.close()

# =============================================================================================
# =============================================================================================

def listarUMAprova(IDPROVA):

    try:
        conn = psycopg2.connect(user="postgres",
                                password="postgres",
                                host="localhost",
                                port="5433",
                                database="CRC") 

        cur = conn.cursor()

        cur.execute("SELECT corridas.id, corridas.sitio, corridas.km, corridas.lim_data, corridas.data_corrida, corridas.lim_inscritos, corridas.num_inscritos, provas.valor "
                    "FROM corridas, provas "
                    "WHERE corridas.id = provas.corridas_id AND corridas.id = {0}".format(IDPROVA))
        conn.commit()


        for linha in cur.fetchall():
            x1 = linha[0]  # id
            x2 = linha[1]  # local
            x3 = linha[2]  # distancia
            x4 = linha[3]  # data limite
            x5 = linha[4]  # data corrida
            x6 = linha[5]  # limite inscritos
            x7 = linha[6]  # numero inscritos
            x8 = linha[7]  # valor

            vagas = x6-x7

            if vagas > 0:
                print("ID:", x1, "\n| Local:", x2, "| Distancia:", x3, "km | Data:", x5,
                      "\n| Limite Inscricao:", x4, "| Vagas:", vagas, "\n| Valor:", x8,"EUR\n")

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
    finally:
        # closing database connection.
        if(conn):
            cur.close()
            conn.close()

# =============================================================================================
# =============================================================================================

def listarMensagensRecebidas(IDMEMBRO):

    try:
        conn = psycopg2.connect(user="postgres",
                                password="postgres",
                                host="localhost",
                                port="5433",
                                database="CRC") 

        cur = conn.cursor()

        cur.execute("SELECT leituras.vista, mensagens.id, mensagens.assunto, mensagens.texto, mensagens.data, mensagens.administradores_utilizadores_id, utilizadores.nome, utilizadores.username "
                    "FROM leituras, mensagens, utilizadores "
                    "WHERE utilizadores.id = {0} AND leituras.membros_utilizadores_id = {0} AND leituras.mensagens_id = mensagens.id".format(IDMEMBRO))            
        conn.commit()

        print("------------------------------------------------------")


        for linha in cur.fetchall():
            x1 = linha[0]  # vista
            x2 = linha[1]  # id da mensagem
            x3 = linha[2]  # assunto da mensagem
            x4 = linha[3]  # texto da mensagem
            x5 = linha[4]  # data da mensagem
            x6 = linha[5]  # id do administrador que enviou
            x7 = linha[6]  # nome do admin (ERRO ESTA A MOSTRAR O DO MEMBRO)
            x8 = linha[7]  # username do admin (ERRO ESTA A MOSTRAR O DO MEMBRO)

            cur.execute("SELECT username "
                "FROM utilizadores "
                "WHERE id = {0}".format(x6)) 
            ADMINUSERNAME = cur.fetchone()[0]
           
            conn.commit()


            if x1 == False:
                VISTA = "[X]"
            
            else:
                VISTA = "[ ]"


            print(VISTA, "#" + str(x2) + " Data:", x5, "\n    Enviado por: @" + str(ADMINUSERNAME),
                  "\n    Assunto:", x3.strip())
            print("------------------------------------------------------")

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
    finally:
        # closing database connection.
        if(conn):
            cur.close()
            conn.close()

# =============================================================================================
# =============================================================================================

def abrirMensagem(IDMEMBRO, IDMENSAGEM):
    try:
        conn = psycopg2.connect(user="postgres",
                                password="postgres",
                                host="localhost",
                                port="5433",
                                database="CRC") 

        cur = conn.cursor()

        cur.execute("SELECT leituras.vista, mensagens.id, mensagens.assunto, mensagens.texto, mensagens.data, mensagens.administradores_utilizadores_id, utilizadores.nome, utilizadores.username "
                    "FROM leituras, mensagens, utilizadores "
                    "WHERE utilizadores.id = {0} AND leituras.membros_utilizadores_id = {0} AND leituras.mensagens_id = mensagens.id AND mensagens.id = {1}".format(IDMEMBRO, IDMENSAGEM))            
        conn.commit()

        print("\n--------------------------------------------------")
        linha = cur.fetchone()
        x1 = linha[0]  # vista
        x2 = linha[1]  # id da mensagem
        x3 = linha[2]  # assunto da mensagem
        x4 = linha[3]  # texto da mensagem
        x5 = linha[4]  # data da mensagem
        x6 = linha[5]  # id do administrador que enviou
        x7 = linha[6]  # nome do admin (ERRO ESTA A MOSTRAR O DO MEMBRO)
        x8 = linha[7]  # username do admin (ERRO ESTA A MOSTRAR O DO MEMBRO)

        cur.execute("SELECT username "
                "FROM utilizadores "
                "WHERE id = {0}".format(x6)) 
        ADMINUSERNAME = cur.fetchone()[0]
           
        conn.commit()

        cur.execute("UPDATE leituras SET vista = TRUE WHERE membros_utilizadores_id = {0} AND mensagens_id = {1}".format(IDMEMBRO, IDMENSAGEM)) # AQUI
        conn.commit()
    

        print("#" + str(x2) + " Data:", x5, "\n    Enviado por: @" + str(ADMINUSERNAME),
            "\n    Assunto:", x3.strip(), "\n--------------------------------------------------",
            "\nTexto:")
        print(x4.strip(), "\n--------------------------------------------------")


    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
    finally:
        # closing database connection.
        if(conn):
            cur.close()
            conn.close()

# =============================================================================================
# =============================================================================================

def verifica_mensagem(IDMENSAGEM, IDMEMBRO):
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="postgres",
                                      host="localhost",
                                      port="5433",
                                      database="CRC")

        cursor = connection.cursor()
        cursor.execute("SELECT membros_utilizadores_id FROM leituras WHERE membros_utilizadores_id = %s AND mensagens_id = %s;",
                       (IDMEMBRO, IDMENSAGEM))
        if cursor.rowcount == 1:
            return 1  # Login válido
        else:
            return 0  # Login inválido

    except (Exception, psycopg2.Error) as error:
        print("Erro", error)
    finally:
        # closing database connection.
        if(connection):
            cursor.close()
            connection.close()

# =============================================================================================
# =============================================================================================

def alterarProva(IDPROVA, admin):
    limparjanela(admin)
    listarUMAprova(IDPROVA)
    
    try:
        conn = psycopg2.connect(user="postgres",
                                password="postgres",
                                host="localhost",
                                port="5433",
                                database="CRC") 

        cur = conn.cursor()

        while True:
            print("Alterar:")
            print(" ")
            print("[V] - Valor") 
            print("[L] - Local")
            print("[D] - Distância")
            print(" ")
            print("[LI] - Limite de Inscrições")
            print("[DI] - Data limite de Inscrição")
            print("[DP] - Data da Prova")
            print(" ")
            print("[S] - Sair")
            print(" ")

            ALTERACAO = input("Alterar: ")
            ALTERACAO = ALTERACAO.upper()


            if (ALTERACAO != "V" and ALTERACAO != "L" and ALTERACAO != "D" and ALTERACAO != "LI" and ALTERACAO != "DI" and ALTERACAO != "DP" and ALTERACAO != "S"):
                print("Insira dados válidos!")
            else:
                break

        if ALTERACAO == "V":

            while True:
                VALOR = float(input("Quer alterar o preço da Prova #" + str(IDPROVA) + " para quantos EUR: "))


                if (VALOR < 0):
                    print("Impossível inserir valores negativos!")
                else:
                    break
                
            cur.execute("UPDATE provas SET valor = {0} WHERE corridas_id = {1}".format(VALOR, IDPROVA))
            conn.commit()
            cur.execute(
            "INSERT INTO hist_de_alt_preco VALUES (DEFAULT, %s, %s, %s, %s);",
            (VALOR, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), converteusernameparaid(admin), IDPROVA))
            conn.commit()

            alterarProva(IDPROVA, admin)



        elif ALTERACAO == "L":
            print(" ")

            while True:
                LOCAL = input("Local: ")
                if (LOCAL == ''):
                    print("Não insira campos vazios!")
                else:
                    break

            cur.execute("UPDATE corridas SET sitio = '{0}' WHERE id = {1}".format(LOCAL, IDPROVA))
            conn.commit()

            alterarProva(IDPROVA, admin)


        elif ALTERACAO == "D":
            print(" ")
            print("Distância:")
            print("[A] - 1km")
            print("[B] - 5km")
            print("[C] - 10km")
            print("[D] - 20km")
            print("[E] - 40km (maratona)")
            print(" ")
            OPCAO = input('Selecionar opcao: ')
            OPCAO = OPCAO.upper()
            if OPCAO == 'A':
                DISTANCIA = 1
            elif OPCAO == 'B':
                DISTANCIA = 5
            elif OPCAO == 'C':
                DISTANCIA = 10
            elif OPCAO == 'D':
                DISTANCIA = 20
            elif OPCAO == 'E':
                DISTANCIA = 40
            else:
                alterarProva(IDPROVA, admin)

            cur.execute("UPDATE corridas SET km = {0} WHERE id = {1}".format(DISTANCIA, IDPROVA))
            conn.commit()

            alterarProva(IDPROVA, admin)


        elif ALTERACAO == "LI":
            while True:
                LIMITEINSCRITOS = int(input("Número MAX de inscritos: "))


                cur.execute("SELECT num_inscritos FROM corridas WHERE corridas.id = {0}".format(IDPROVA))
                conn.commit()
                NUMINSCRITOS = cur.fetchone()[0]
                if (LIMITEINSCRITOS < 3):
                    print("Insira dados válidos!")
                elif(LIMITEINSCRITOS < NUMINSCRITOS):
                    print("O limite de inscritos não pode ser inferior ao numero de inscritos:",NUMINSCRITOS)
                else:
                    break
            cur.execute("UPDATE corridas SET lim_inscritos = {0} WHERE id = {1}".format(LIMITEINSCRITOS, IDPROVA))
            conn.commit()
            alterarProva(IDPROVA, admin)



        elif ALTERACAO == "DI":

            print(" ")
            print("DATA LIMITE PARA INSCRIÇÃO ---------------------------")
            print(" ")




            cur.execute("SELECT lim_data, data_corrida FROM corridas WHERE id = {0};".format(IDPROVA))
    
            conn.commit()
        
            for linha in cur.fetchall():
                dataINSCoriginal = datetime.datetime.combine(linha[0], datetime.datetime.min.time()) # data de incr
                dataCORRoriginal = linha[1] # data da corrida


            while True:
                LIMITEANO = input("Ano: ")
                if (int(LIMITEANO) < int(datetime.datetime.now().strftime('%Y')) or int(LIMITEANO) > dataCORRoriginal.year):
                    print("Escolha uma data válida!")
                else:
                    break

            while True:
                LIMITEMES = input("Mes: ")

                if int(LIMITEMES) <= 9:
                    LIMITEMES = "0"+str(int(LIMITEMES))

                MESORIGINAL = dataCORRoriginal.month
                if int(MESORIGINAL) <= 9:
                    MESORIGINAL = "0"+str(int(MESORIGINAL))

                if (int(LIMITEMES) < 1 or int(str(LIMITEANO)+str(LIMITEMES)) < int(datetime.datetime.now().strftime('%Y%m')) or int(str(LIMITEANO)+str(LIMITEMES)) > int(str(dataCORRoriginal.year)+str(MESORIGINAL))):
                    print("Escolha uma data válida!")
                else:
                    break

            while True:
                LIMITEDIA = input("Dia: ")
                if int(LIMITEDIA) <= 9:
                    LIMITEDIA = "0"+str(int(LIMITEDIA))

                DIAORIGINAL = dataCORRoriginal.day
                if int(DIAORIGINAL) <= 9:
                    DIAORIGINAL = "0"+str(int(DIAORIGINAL))

                if (int(LIMITEDIA) < 1 or int(str(LIMITEANO)+str(LIMITEMES)+str(LIMITEDIA)) < int(datetime.datetime.now().strftime('%Y%m%d')) or int(str(LIMITEANO)+str(LIMITEMES)+str(LIMITEDIA)) > int(str(dataCORRoriginal.year)+str(MESORIGINAL)+str(DIAORIGINAL))):
                    print("Escolha uma data válida!")
                else:
                    break

            if datavalida(int(LIMITEANO), int(LIMITEMES), int(LIMITEDIA)) == False:
                print("Introduza uma data válida!")
                alterarProva(IDPROVA, admin)


            LIMITEDATAFORMATADA = LIMITEANO+"-"+LIMITEMES+"-"+LIMITEDIA

            cur.execute("UPDATE corridas SET lim_data = '{0}' WHERE id = {1}".format(LIMITEDATAFORMATADA, IDPROVA))
            conn.commit()
            alterarProva(IDPROVA, admin)




        elif ALTERACAO == "DP":

            print(" ")
            print("DATA DA PROVA ----------------------------------------")
            print(" ")

            cur.execute("SELECT lim_data, data_corrida FROM corridas WHERE id = {0};".format(IDPROVA))
    
            conn.commit()
        
            for linha in cur.fetchall():
                dataINSCoriginal = datetime.datetime.combine(linha[0], datetime.datetime.min.time()) # data de incr
                dataCORRoriginal = linha[1] # data da corrida

                DIFdias = (dataCORRoriginal - dataINSCoriginal).days

            while True:
                ANO = input("Ano: ")
                if (int(ANO) < int(datetime.datetime.now().strftime('%Y'))):
                    print("Escolha uma data válida!")
                else:
                    break

            while True:
                MES = input("Mes: ")

                if int(MES) <= 9:
                    MES = "0"+str(int(MES))

                if (int(MES) < 1 or int(str(ANO)+str(MES)) < int(datetime.datetime.now().strftime('%Y%m'))):
                    print("Escolha uma data válida!")
                else:
                    break

            while True:
                DIA = input("Dia: ")
                if int(DIA) <= 9:
                    DIA = "0"+str(int(DIA))

                if (int(DIA) < 1 or int(str(ANO)+str(MES)+str(DIA)) < int(datetime.datetime.now().strftime('%Y%m%d'))):
                    print("Escolha uma data válida!")
                else:
                    break

            if datavalida(int(ANO), int(MES), int(DIA)) == False:
                print("Introduza uma data válida!")
                alterarProva(IDPROVA, admin)


            while True:
                HORA = input("Hora (h): ")
                if (int(HORA) < 0 or int(HORA) > 23 ):
                    print("Introduza uma hora válida!")
                else:
                    if int(HORA) <= 9:
                        HORA = "0"+str(int(HORA))
                    break

            while True:
                MINUTO = input("Minuto (m): ")
                if (int(MINUTO) < 0 or int(MINUTO) > 59 ):
                    print("Introduza uma hora válida!")
                else:
                    if int(MINUTO) <= 9:
                        MINUTO = "0"+str(int(MINUTO))
                    break


            DATACORRIDA = ANO+"-"+MES+"-"+DIA+" "+HORA+":"+MINUTO+":00"
            DATACORRIDAFORMATADA = datetime.datetime.strptime(DATACORRIDA, '%Y-%m-%d %H:%M:%S')
            LIMITEDATAFORMATADA = DATACORRIDAFORMATADA - datetime.timedelta(days=DIFdias)

            cur.execute("UPDATE corridas SET lim_data = '{0}', data_corrida = '{1}' WHERE id = {2}".format(LIMITEDATAFORMATADA, DATACORRIDAFORMATADA, IDPROVA))
            conn.commit()
            alterarProva(IDPROVA, admin)

        else:
            menuadmin(admin)

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
    finally:
        # closing database connection.
        if(conn):
            cur.close()
            conn.close()

# =============================================================================================
# =============================================================================================

def historicoAltPrecos(IDPROVA):

    try:
        conn = psycopg2.connect(user="postgres",
                                password="postgres",
                                host="localhost",
                                port="5433",
                                database="CRC") 

        cur = conn.cursor()

        cur.execute("SELECT id, preco, dataalteracao, administradores_utilizadores_id "
                    "FROM hist_de_alt_preco "
                    "WHERE provas_corridas_id = {0} ORDER BY dataalteracao ASC".format(IDPROVA))            
        conn.commit()
        print("                                           MAIS ANTIGO")        
        print("------------------------------------------------------")
        for linha in cur.fetchall():
            x1 = linha[0]  # id
            x2 = linha[1]  # preco
            x3 = linha[2]  # data alteracao
            x4 = linha[3]  # admin id



            cur.execute("SELECT username "
                "FROM utilizadores "
                "WHERE id = {0}".format(x4)) 
            ADMINUSERNAME = cur.fetchone()[0]
           
            conn.commit()


            print("#" + str(x1) + " Data:", x3, "\n    Alterado por: @" + str(ADMINUSERNAME),
                  "\n    Preço (EUR):", x2)
            print("------------------------------------------------------")
        print("                                          MAIS RECENTE")        
        print(" ")
    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
    finally:
        # closing database connection.
        if(conn):
            cur.close()
            conn.close()

# =============================================================================================
# =============================================================================================

def listarUMtreino(IDTREINO):

    try:
        conn = psycopg2.connect(user="postgres",
                                password="postgres",
                                host="localhost",
                                port="5433",
                                database="CRC") 

        cur = conn.cursor()

        cur.execute("SELECT corridas.id, corridas.sitio, corridas.km, corridas.lim_data, corridas.data_corrida, corridas.lim_inscritos, corridas.num_inscritos, treinos.rep, treinadores_id "
                    "FROM corridas, treinos "
                    "WHERE corridas.id = treinos.corridas_id AND corridas.id = {0}".format(IDTREINO))         
        conn.commit()


        for linha in cur.fetchall():
            x1 = linha[0]  # id
            x2 = linha[1]  # local
            x3 = linha[2]  # distancia
            x4 = linha[3]  # data limite
            x5 = linha[4]  # data corrida
            x6 = linha[5]  # limite inscritos
            x7 = linha[6]  # numero inscritos
            x8 = linha[7]  # repetitivo
            x9 = linha[8]  # id treinadores

            if x9 == None:
                treinador = "Sem treinador"
            
            else:
                cur.execute("SELECT nome FROM treinadores WHERE id = {0}".format(x9))
                for linha1 in cur.fetchall():
                    treinador = linha1[0]

            if x8 == "S":
                REPETE = "Semanalmente"
            elif x8 == "M":
                REPETE = "Mensalmente"
            elif x8 == "N":
                REPETE = "Não"

            vagas = x6-x7

            print("ID:", x1, "\n| Local:", x2, "| Distancia:", x3, "km | Data:", x5,
                  "\n| Limite Inscricao:", x4, "| Vagas:", vagas, "\n| Repete:", REPETE,"| Treinador:", treinador,"\n")

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
    finally:
        # closing database connection.
        if(conn):
            cur.close()
            conn.close()

# =============================================================================================
# =============================================================================================

def converteusernameparanome(input_username):

    try:
        conn = psycopg2.connect(user="postgres",
                                password="postgres",
                                host="localhost",
                                port="5433",
                                database="CRC") 

        cur = conn.cursor()

        cur.execute("SELECT nome FROM utilizadores WHERE username = '{0}';".format(input_username))
    
        conn.commit()
        
        i = 0
        for linha in cur.fetchall():
            i = cur.rowcount
            nome = linha[0]  # username
            
        # row = cursor.fetchone()

        if(i == 0):
            print("erro a converter email para username")

        return nome
        

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
    finally:
        # closing database connection.
        if(conn):
            cur.close()
            conn.close()

# =============================================================================================
# =============================================================================================

def enviarmensagemG_TODOS(admin, ASSUNTO, TEXTO, IDCORRIDA):
    try:
        conn = psycopg2.connect(user="postgres",
                                password="postgres",
                                host="localhost",
                                port="5433",
                                database="CRC")

        cur = conn.cursor()
        IDADMIN = converteusernameparaid(admin)
        cur.execute("INSERT INTO mensagens VALUES (DEFAULT, '{0}', '{1}', '{2}', {3}) RETURNING id;".format(ASSUNTO, TEXTO, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), IDADMIN))

        IDMENSAGEM = cur.fetchone()
        conn.commit()

        cur.execute("SELECT membros_utilizadores_id FROM inscricoes WHERE corridas_id = {0} ;".format(IDCORRIDA))     
        conn.commit()

        for linha in cur.fetchall():
            IDMEMBRO = linha[0]  # id
            
            cur.execute("INSERT INTO leituras VALUES (false, %s, %s);",(IDMEMBRO, IDMENSAGEM))
            conn.commit()

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
    finally:
        # closing database connection.
        if(conn):
            cur.close()
            conn.close()

# =============================================================================================
# =============================================================================================

def enviarmensagemGP_PAGO(admin, ASSUNTO, TEXTO, IDCORRIDA):
    try:
        conn = psycopg2.connect(user="postgres",
                                password="postgres",
                                host="localhost",
                                port="5433",
                                database="CRC")

        cur = conn.cursor()
        IDADMIN = converteusernameparaid(admin)
        cur.execute("INSERT INTO mensagens VALUES (DEFAULT, '{0}', '{1}', '{2}', {3}) RETURNING id;".format(ASSUNTO, TEXTO, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), IDADMIN))

        IDMENSAGEM = cur.fetchone()
        conn.commit()

        cur.execute("SELECT membros_utilizadores_id FROM inscricoes WHERE corridas_id = {0} AND pago = true;".format(IDCORRIDA))      
        conn.commit()

        for linha in cur.fetchall():
            IDMEMBRO = linha[0]  # id
            
            cur.execute("INSERT INTO leituras VALUES (false, %s, %s);",(IDMEMBRO, IDMENSAGEM))
            conn.commit()

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
    finally:
        # closing database connection.
        if(conn):
            cur.close()
            conn.close()

# =============================================================================================
# =============================================================================================

def enviarmensagemGP_NAOPAGO(admin, ASSUNTO, TEXTO, IDCORRIDA):
    try:
        conn = psycopg2.connect(user="postgres",
                                password="postgres",
                                host="localhost",
                                port="5433",
                                database="CRC")

        cur = conn.cursor()
        IDADMIN = converteusernameparaid(admin)
        cur.execute("INSERT INTO mensagens VALUES (DEFAULT, '{0}', '{1}', '{2}', {3}) RETURNING id;".format(ASSUNTO, TEXTO, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), IDADMIN))

        IDMENSAGEM = cur.fetchone()
        conn.commit()

        cur.execute("SELECT membros_utilizadores_id FROM inscricoes WHERE corridas_id = {0} AND pago = false;".format(IDCORRIDA))      
        conn.commit()

        for linha in cur.fetchall():
            IDMEMBRO = linha[0]  # id
            
            cur.execute("INSERT INTO leituras VALUES (false, %s, %s);",(IDMEMBRO, IDMENSAGEM))
            conn.commit()

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
    finally:
        # closing database connection.
        if(conn):
            cur.close()
            conn.close()

# =============================================================================================
# =============================================================================================

def menuestatisticas(admin):
    limparjanela(admin)
    print("------------------ MENU ESTATÍSTICAS -----------------")
    print(" ")
    estPT(admin)
    print(" ")
    print("INSCRIÇÕES EM PROVAS ---------------------------------")
    print("AINDA A DECORRER")
    print(" ")
    print("   Por pagar:", inscricoesProvasPorPagar())
    print("   Pagas:", inscricoesProvasPagas())
    print("   Total:", inscricoesProvasTotal())
    print("   Valor (EUR):", inscricoesProvasVALOR())
    print(" ")
    print("TOTAL DE MEMBROS -------------------------------------")
    print(" ")
    print("   Sexo Masculino:", membrosM())
    print("   Sexo Feminino:", membrosF())
    print("   Total:", membrosTOTAL())
    print(" ")
    print("TREINADORES ------------------------------------------")
    print(" ")
    print("   Total:", treinadoresTOTAL())
    print(" ")
    print("ADMINISTRADORES ---------------------------------------")
    print(" ")
    print("   Total:", administradoresTOTAL())
    print(" ")
    print("MEMBROS QUE PARTICIPARAM -----------------------------")
    print("EM MAIS PROVAS")
    print(" ")
    TOP3membros()
    print(" ")
    print("------------------------------------------------------")
    print(" ")
    input("Pressione Enter para voltar...")
    menuadmin(admin)

# =============================================================================================
# =============================================================================================

def estPT(admin):
    try:
        conn = psycopg2.connect(user="postgres",
                                password="postgres",
                                host="localhost",
                                port="5433",
                                database="CRC") 

        cur = conn.cursor()

        print("PROVAS POR TIPO --------------------------------------")
        print(" ")
        TOTALPROVAS = 0
        QUANTIDADE = 0
        cur.execute("SELECT corridas.km, COUNT(*) "
                    "FROM corridas, provas "
                    "WHERE corridas.id = provas.corridas_id AND corridas.km = 1 "
                    "GROUP BY corridas.km "
                    "ORDER BY corridas.km ASC")
        conn.commit()

        for linha in cur.fetchall():
            DISTANCIA = linha[0] 
            QUANTIDADE = linha[1]
            TOTALPROVAS = TOTALPROVAS + QUANTIDADE
        if QUANTIDADE == 0:
            print("   Provas de 1km:  0")
        else:
            print("   Provas de 1km: ", QUANTIDADE)
        QUANTIDADE = 0

        cur.execute("SELECT corridas.km, COUNT(*) "
                    "FROM corridas, provas "
                    "WHERE corridas.id = provas.corridas_id AND corridas.km = 5 "
                    "GROUP BY corridas.km "
                    "ORDER BY corridas.km ASC")
        conn.commit()

        for linha in cur.fetchall():
            DISTANCIA = linha[0] 
            QUANTIDADE = linha[1]
            TOTALPROVAS = TOTALPROVAS + QUANTIDADE
        if QUANTIDADE == 0:
            print("   Provas de 5km:  0")
        else:
            print("   Provas de 5km: ", QUANTIDADE)
        
        QUANTIDADE = 0

        cur.execute("SELECT corridas.km, COUNT(*) "
                    "FROM corridas, provas "
                    "WHERE corridas.id = provas.corridas_id AND corridas.km = 10 "
                    "GROUP BY corridas.km "
                    "ORDER BY corridas.km ASC")
        conn.commit()

        for linha in cur.fetchall():
            DISTANCIA = linha[0] 
            QUANTIDADE = linha[1]
            TOTALPROVAS = TOTALPROVAS + QUANTIDADE
        if QUANTIDADE == 0:
            print("   Provas de 10km: 0")
        else:
            print("   Provas de 10km:", QUANTIDADE)
        QUANTIDADE = 0

        cur.execute("SELECT corridas.km, COUNT(*) "
                    "FROM corridas, provas "
                    "WHERE corridas.id = provas.corridas_id AND corridas.km = 20 "
                    "GROUP BY corridas.km "
                    "ORDER BY corridas.km ASC")
        conn.commit()

        for linha in cur.fetchall():
            DISTANCIA = linha[0] 
            QUANTIDADE = linha[1]
            TOTALPROVAS = TOTALPROVAS + QUANTIDADE

        if QUANTIDADE == 0:
            print("   Provas de 20km: 0")
        else:
            print("   Provas de 20km:", QUANTIDADE)

        QUANTIDADE = 0

        cur.execute("SELECT corridas.km, COUNT(*) "
                    "FROM corridas, provas "
                    "WHERE corridas.id = provas.corridas_id AND corridas.km = 40 "
                    "GROUP BY corridas.km "
                    "ORDER BY corridas.km ASC")
        conn.commit()

        for linha in cur.fetchall():
            DISTANCIA = linha[0] 
            QUANTIDADE = linha[1]
            TOTALPROVAS = TOTALPROVAS + QUANTIDADE
        if QUANTIDADE == 0:
            print("   Provas de 40km: 0")
        else:
            print("   Provas de 40km:", QUANTIDADE)

        
        print(" ")
        print("TOTAL DE PROVAS --------------------------------------")
        print(" ")
        print("   Total:", TOTALPROVAS)


    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
    finally:
        # closing database connection.
        if(conn):
            cur.close()
            conn.close()

# =============================================================================================
# =============================================================================================

def inscricoesProvasPagas():
    try:
        conn = psycopg2.connect(user="postgres",
                                password="postgres",
                                host="localhost",
                                port="5433",
                                database="CRC") 

        cur = conn.cursor()

        cur.execute("SELECT inscricoes.membros_utilizadores_id "
                    "FROM inscricoes, provas, corridas "
                    "WHERE inscricoes.corridas_id = provas.corridas_id "
                    "AND inscricoes.pago = true "
                    "AND corridas.id = provas.corridas_id "
                    "AND corridas.data_corrida >= '{0}'".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                
        conn.commit()

        return cur.rowcount

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
    finally:
        # closing database connection.
        if(conn):
            cur.close()
            conn.close()

# =============================================================================================
# =============================================================================================

def inscricoesProvasPorPagar():
    try:
        conn = psycopg2.connect(user="postgres",
                                password="postgres",
                                host="localhost",
                                port="5433",
                                database="CRC") 

        cur = conn.cursor()

        cur.execute("SELECT inscricoes.membros_utilizadores_id "
                    "FROM inscricoes, provas, corridas "
                    "WHERE inscricoes.corridas_id = provas.corridas_id "
                    "AND inscricoes.pago = false "
                    "AND corridas.id = provas.corridas_id "
                    "AND corridas.data_corrida >= '{0}'".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                
        conn.commit()

        return cur.rowcount

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
    finally:
        # closing database connection.
        if(conn):
            cur.close()
            conn.close()

# =============================================================================================
# =============================================================================================

def inscricoesProvasTotal():
    try:
        conn = psycopg2.connect(user="postgres",
                                password="postgres",
                                host="localhost",
                                port="5433",
                                database="CRC") 

        cur = conn.cursor()

        #inicio2
        cur.execute("SELECT inscricoes.membros_utilizadores_id "
                    "FROM inscricoes, provas, corridas "
                    "WHERE inscricoes.corridas_id = provas.corridas_id "
                    "AND corridas.id = provas.corridas_id "
                    "AND corridas.data_corrida >= '{0}'".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                
        conn.commit()

        return cur.rowcount

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
    finally:
        # closing database connection.
        if(conn):
            cur.close()
            conn.close()

# =============================================================================================
# =============================================================================================

def inscricoesProvasVALOR():
    try:
        conn = psycopg2.connect(user="postgres",
                                password="postgres",
                                host="localhost",
                                port="5433",
                                database="CRC") 

        cur = conn.cursor()

        #inicio2
        cur.execute("SELECT SUM(inscricoes.precopago) "
                    "FROM inscricoes, provas, corridas "
                    "WHERE inscricoes.corridas_id = provas.corridas_id "
                    "AND inscricoes.pago = true "
                    "AND corridas.id = provas.corridas_id "
                    "AND corridas.data_corrida >= '{0}'".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                
        conn.commit()
        for linha in cur.fetchall():
            VALOR = linha[0]  # id
        return VALOR

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
    finally:
        # closing database connection.
        if(conn):
            cur.close()
            conn.close()

# =============================================================================================
# =============================================================================================

def membrosF():
    try:
        conn = psycopg2.connect(user="postgres",
                                password="postgres",
                                host="localhost",
                                port="5433",
                                database="CRC") 

        cur = conn.cursor()

        #inicio2
        cur.execute("SELECT membros.utilizadores_id "
                    "FROM membros "
                    "WHERE membros.sexo = 'F'")
                
        conn.commit()

        return cur.rowcount

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
    finally:
        # closing database connection.
        if(conn):
            cur.close()
            conn.close()

# =============================================================================================
# =============================================================================================

def membrosM():
    try:
        conn = psycopg2.connect(user="postgres",
                                password="postgres",
                                host="localhost",
                                port="5433",
                                database="CRC") 

        cur = conn.cursor()

        #inicio2
        cur.execute("SELECT membros.utilizadores_id "
                    "FROM membros "
                    "WHERE membros.sexo = 'M'")
                
        conn.commit()

        return cur.rowcount

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
    finally:
        # closing database connection.
        if(conn):
            cur.close()
            conn.close()

# =============================================================================================
# =============================================================================================

def membrosTOTAL():
    try:
        conn = psycopg2.connect(user="postgres",
                                password="postgres",
                                host="localhost",
                                port="5433",
                                database="CRC") 

        cur = conn.cursor()

        #inicio2
        cur.execute("SELECT membros.utilizadores_id "
                    "FROM membros")
                
        conn.commit()

        return cur.rowcount

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
    finally:
        # closing database connection.
        if(conn):
            cur.close()
            conn.close()

# =============================================================================================
# =============================================================================================

def treinadoresTOTAL():
    try:
        conn = psycopg2.connect(user="postgres",
                                password="postgres",
                                host="localhost",
                                port="5433",
                                database="CRC") 

        cur = conn.cursor()

        cur.execute("SELECT id "
                    "FROM treinadores")
                
        conn.commit()

        return cur.rowcount

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
    finally:
        # closing database connection.
        if(conn):
            cur.close()
            conn.close()

# =============================================================================================
# =============================================================================================

def administradoresTOTAL():
    try:
        conn = psycopg2.connect(user="postgres",
                                password="postgres",
                                host="localhost",
                                port="5433",
                                database="CRC") 

        cur = conn.cursor()

        cur.execute("SELECT utilizadores_id "
                    "FROM administradores")
                
        conn.commit()

        return cur.rowcount

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
    finally:
        # closing database connection.
        if(conn):
            cur.close()
            conn.close()

# =============================================================================================
# =============================================================================================

def menu_classificacoes(membro):
    limparjanela(membro)
    print("MENU CLASSIFICAÇÕES ----------------------------------")
    print("")
    print("[P] - Pessoais")
    print("[G] - Gerais")
    print("[S] - Sair")
    print(" ")

    OPCAO = input('Selecionar opcao: ')
    OPCAO = OPCAO.upper()

    if OPCAO == 'P':
        print("selecionou P")
        classificacoesPessoais(membro)
        input("Pressione Enter para continuar...")
        menu_classificacoes(membro)
    elif OPCAO == 'G':
        print("selecionou G")
        print("\n[F] - Femininas")
        print("[M] - Masculinas")
        print("[MT] - Mistas")
        while True:
            s = input("\nIntroduza a opção:")
            s = s.upper()
            print("")
            if s == 'F':
                id = provasClassificacoes()
                if id == 0:
                    print("Id inválido")
                    input("Pressione Enter para continuar...")
                    menu_classificacoes(membro)

                limparjanela(membro)
                classificacoesSexo(s,id)
                break
            elif s == 'M':
                id = provasClassificacoes()
                if id == 0:
                    print("Id inválido")
                    input("Pressione Enter para continuar...")
                    menu_classificacoes(membro)

                limparjanela(membro)

                classificacoesSexo(s,id)
                break
            elif s == 'MT':
                id = provasClassificacoes()
                if id == 0:
                    print("Id inválido")
                    input("Pressione Enter para continuar...")
                    menu_classificacoes(membro)

                limparjanela(membro)

                classificacoesMista(id)
                break

        input("Pressione Enter para continuar...")
        menu_classificacoes(membro)
    elif OPCAO == 'S':
        print("selecionou S")
        menumembro(membro)
    else:
        menu_classificacoes(membro)

# =============================================================================================
# =============================================================================================

def provasClassificacoes():
    try:
        conn = psycopg2.connect(user="postgres",
                                password="postgres",
                                host="localhost",
                                port="5433",
                                database="CRC") 

        cur = conn.cursor()

        cur.execute("SELECT corridas.id, corridas.sitio, corridas.km, corridas.data_corrida "
                    "FROM corridas, provas, inscricoes "
                    "WHERE corridas.id = provas.corridas_id AND inscricoes.corridas_id = corridas.id AND corridas.data_corrida < '{0}' ".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))            
        conn.commit()


        for linha in cur.fetchall():
            x1 = linha[0]  # id
            x2 = linha[1]  # local
            x3 = linha[2]  # distancia
            x4 = linha[3]  # data corrida

            print("ID:", x1, "\n| Local:", x2, "| Distancia:", x3, "km | Data:", x4,"\n")

        valid = False
        while not valid: #loop until the user enters a valid int
            try:
                opid = int(input("\nIntroduza o id da prova que pretende visualizar os tempos: "))
                valid = True #if this point is reached, x is a valid int
            except ValueError:
                print('Introduza apenas numero inteiros')
        
        cur.execute("SELECT corridas_id FROM corridas,provas WHERE corridas.id = corridas_id AND corridas_id = {0} AND corridas.data_corrida < '{1}';".format(opid,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

        if cur.rowcount == 1:
            return opid 
        else:
            return 0  
        

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
    finally:
        # closing database connection.
        if(conn):
            cur.close()
            conn.close()

# =============================================================================================
# =============================================================================================

def classificacoesSexo(s,id):
    try:
        conn = psycopg2.connect(user="postgres",
                                password="postgres",
                                host="localhost",
                                port="5433",
                                database="CRC") 
        
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT hist_de_tempos.tempo_seg, membros.sexo, corridas.sitio, corridas.km, utilizadores.nome FROM hist_de_tempos "
                    "INNER JOIN membros ON hist_de_tempos.membros_utilizadores_id = membros.utilizadores_id "
                    "INNER JOIN provas ON provas.corridas_id = hist_de_tempos.provas_corridas_id "
                    "INNER JOIN corridas ON corridas.id = hist_de_tempos.provas_corridas_id "
                    "INNER JOIN utilizadores ON utilizadores.id = membros.utilizadores_id "
                    "WHERE membros.sexo = '{0}' AND provas.corridas_id = {1} "
                    "ORDER BY hist_de_tempos.tempo_seg ASC".format(s,id))
        conn.commit()
        
        i = 1
        for linha in cur.fetchall():
            x1 = linha[0] # tempo
            x2 = linha[1] # sexo
            x3 = linha[2] # local
            x4 = linha[3] # distancia
            x5 = linha[4] # nome

            print(i,"- Nome:",x5,"| Sexo:",x2,"| Local:",x3,"| Distância:",x4," | Tempo:",x1,"segundos")
            i+=1

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
    finally:
        # closing database connection.
        if(conn):
            cur.close()
            conn.close()

# =============================================================================================
# =============================================================================================

def classificacoesMista(id):
    try:
        conn = psycopg2.connect(user="postgres",
                                password="postgres",
                                host="localhost",
                                port="5433",
                                database="CRC") 
        
        cur = conn.cursor()

        cur.execute("SELECT DISTINCT hist_de_tempos.tempo_seg, membros.sexo FROM hist_de_tempos "
                    "INNER JOIN membros ON hist_de_tempos.membros_utilizadores_id = membros.utilizadores_id "
                    "INNER JOIN provas ON provas.corridas_id = hist_de_tempos.provas_corridas_id "
                    "WHERE provas.corridas_id = {0} "
                    "ORDER BY hist_de_tempos.tempo_seg ASC".format(id))
        conn.commit()

        cur.execute("SELECT DISTINCT hist_de_tempos.tempo_seg, membros.sexo, corridas.sitio, corridas.km, utilizadores.nome FROM hist_de_tempos "
                    "INNER JOIN membros ON hist_de_tempos.membros_utilizadores_id = membros.utilizadores_id "
                    "INNER JOIN provas ON provas.corridas_id = hist_de_tempos.provas_corridas_id "
                    "INNER JOIN corridas ON corridas.id = hist_de_tempos.provas_corridas_id "
                    "INNER JOIN utilizadores ON utilizadores.id = membros.utilizadores_id "
                    "WHERE provas.corridas_id = {0} "
                    "ORDER BY hist_de_tempos.tempo_seg ASC".format(id))
        conn.commit()
    
        i = 1
        for linha in cur.fetchall():
            x1 = linha[0] # tempo
            x2 = linha[1] # sexo
            x3 = linha[2] # local
            x4 = linha[3] # distancia
            x5 = linha[4] # nome

            print(i,"- Nome:",x5,"| Sexo:",x2,"| Local:",x3,"| Distância:",x4," | Tempo:",x1,"segundos")
            i+=1


    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
    finally:
        # closing database connection.
        if(conn):
            cur.close()
            conn.close()

# =============================================================================================
# =============================================================================================

def classificacoesPessoais(membro):
    try:
        conn = psycopg2.connect(user="postgres",
                                password="postgres",
                                host="localhost",
                                port="5433",
                                database="CRC") 

        cur = conn.cursor()

        limparjanela(membro)
        
        cur.execute("SELECT tempo_seg, provas_corridas_id, corridas.sitio, corridas.km "
                    "FROM hist_de_tempos, provas, corridas "
                    "WHERE provas_corridas_id = provas.corridas_id AND corridas.id = provas_corridas_id "
                    "AND membros_utilizadores_id = (SELECT id FROM utilizadores WHERE username = '{0}')".format(membro))            
        conn.commit()


        for linha in cur.fetchall():
            x1 = linha[0] # tempo
            x2 = linha[1] # id prova
            x3 = linha[2] # local
            x4 = linha[3] # distancia

            print("Id da prova:",x2,"| Local:",x3,"|Distância:",x4," | Tempo:",x1,"segundos")
    

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
    finally:
        # closing database connection.
        if(conn):
            cur.close()
            conn.close()

# =============================================================================================
# =============================================================================================

def updatePago(id_membro,id_corridas):

    try:
        conn = psycopg2.connect(user="postgres",
                                password="postgres",
                                host="localhost",
                                port="5433",
                                database="CRC") 

        cur = conn.cursor()

        cur.execute("SELECT valor FROM provas WHERE corridas_id = {0}".format(id_corridas))

        preco = cur.fetchone()[0]

        cur.execute("UPDATE inscricoes SET pago = true, datapagamento = '{0}',precopago = {1} WHERE membros_utilizadores_id = {2} AND corridas_id = {3};".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),preco,id_membro,id_corridas))   
        conn.commit()


    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
    finally:
        # closing database connection.
        if(conn):
            cur.close()
            conn.close()

# =============================================================================================
# =============================================================================================

def AUTOcriaradmin():
    try:
        conn = psycopg2.connect(user="postgres",
                                password="postgres",
                                host="localhost",
                                port="5433",
                                database="CRC") 

        cur = conn.cursor()
        while True:
            PRIMEIRONOME = input("Primeiro nome: ")
            if (PRIMEIRONOME == '' or ' ' in PRIMEIRONOME):
                print("Não insira espaços ou campos vazios!")
            else:
                break

        while True:
            APELIDO = input("Apelido: ")
            if (APELIDO == '' or ' ' in APELIDO):
                print("Não insira espaços ou campos vazios!")
            else:
                break

        NOME = PRIMEIRONOME+" "+APELIDO
        EMAIL = PRIMEIRONOME.lower()+"@gmail.com"
        PASSWORD = "pass"+PRIMEIRONOME.lower()
        USERNAME = PRIMEIRONOME.lower()+APELIDO.lower()
        print(" ")

        print(NOME)
        print(EMAIL)
        print(PASSWORD)
        print(USERNAME)
        input(" ")

        cur.execute("INSERT INTO utilizadores VALUES (DEFAULT, '{0}', '{1}', MD5('{2}'), '{3}'); "
                    "INSERT INTO administradores (utilizadores_id) "
                    "SELECT id "
                    "FROM utilizadores "
                    "WHERE username = '{3}';".format(NOME, EMAIL, PASSWORD, USERNAME))   
        conn.commit()

        input("Continuar?")

        AUTOcriaradmin()


    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
    finally:
        # closing database connection.
        if(conn):
            cur.close()
            conn.close()

# =============================================================================================
# =============================================================================================

def updatetemposNAOUSARESTE():

    # Se data da prova ja passou
        # e ainda nao tem nada no hist de tempos
        # preencher com valores aleatórios

    try:
        conn = psycopg2.connect(user="postgres",
                                password="postgres",
                                host="localhost",
                                port="5433",
                                database="CRC") 

        cur = conn.cursor()

        



        cur.execute("SELECT provas.corridas_id, corridas.km "
                    "FROM corridas, provas "
                    "WHERE corridas.id = provas.corridas_id AND corridas.num_inscritos > 0 AND corridas.data_corrida < '{0}'".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

        conn.commit()


        for linha in cur.fetchall():
            x1 = linha[0]  # id da prova
            x2 = linha[1]  # km

            cur.execute("SELECT hist_de_tempos.membros_utilizadores_id "
                    "FROM hist_de_tempos, corridas "
                    "WHERE hist_de_tempos.provas_corridas_id = corridas.id AND corridas.id = {0}".format(x1))

            conn.commit()
            i = cur.rowcount
            if i == 0:

                cur.execute("SELECT inscricoes.membros_utilizadores_id "
                    "FROM inscricoes, provas "
                    "WHERE inscricoes.corridas_id = provas.corridas_id "
                    "AND inscricoes.pago = true "
                    "AND provas.corridas_id = {0}".format(x1))
                
                conn.commit()

            for linha2 in cur.fetchall():
                x3 = linha2[0]  # id do membro

                # 1km faz-se em 300 ou 360
                tempMIN = x2 * 300
                tempMAX = x2 * 360

                TEMPOGASTO = random.randint(tempMIN, tempMAX)


                cur.execute("INSERT INTO hist_de_tempos VALUES ({0}, {1}, {2}); ".format(TEMPOGASTO, x3, x1))   
                conn.commit()


    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
    finally:
        # closing database connection.
        if(conn):
            cur.close()
            conn.close()

# =============================================================================================
# =============================================================================================

def TOP3membros():
    try:
        conn = psycopg2.connect(user="postgres",
                                password="postgres",
                                host="localhost",
                                port="5433",
                                database="CRC") 

        cur = conn.cursor()

        cur.execute("SELECT hist_de_tempos.membros_utilizadores_id, COUNT(*) "
                    "FROM hist_de_tempos "
                    "GROUP BY hist_de_tempos.membros_utilizadores_id "
                    "ORDER BY count DESC")
                
        conn.commit()
        LUGAR = 0
        for linha in cur.fetchall():
            IDMEMBRO = linha[0] 
            PARTICIPACOES = linha[1]
            USERNAME = converteidparausername(IDMEMBRO)
            LUGAR = LUGAR + 1
            if (LUGAR == 1 or LUGAR == 2 or LUGAR == 3):
                print("   #" + str(LUGAR) + " [" + str(PARTICIPACOES) + " provas]: @" + USERNAME)


        conn.commit()

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
    finally:
        # closing database connection.
        if(conn):
            cur.close()
            conn.close()

# =============================================================================================
# =============================================================================================

def AUTOaddnovaprova(admin):
    limparjanela(admin)
    print("NOVA PROVA -------------------------------------------")
    print(" ")
    MENU = "NP"
    # IDTREINADOR == 0
    TIPO = random.randint(1, 5)
    if TIPO == 1:
        DISTANCIA = 1
    elif TIPO == 2:
        DISTANCIA = 5
    elif TIPO == 3:
        DISTANCIA = 10
    elif TIPO == 4:
        DISTANCIA = 20
    elif TIPO == 5:
        DISTANCIA = 40

    LOCAL = "Local"+str(random.randint(0, 9999))

    LIMITEINSCRITOS = random.randint(3, 30)


    print("DATA DA PROVA ----------------------------------------")
    print(" ")

    ANO = random.randint(2021, 2022)
    strANO = str(ANO)
    strLIMano = strANO

    MES = random.randint(1, 12)
    if MES <= 9:
        strMES = "0"+str(MES)
        strLIMmes = strMES
    else:
        strMES = str(MES)
        strLIMmes = strMES

    DIA = random.randint(3, 27)
    if DIA <= 9:
        strDIA = "0"+str(DIA)
        strLIMdia = "0"+str(DIA-2)
    else:
        strDIA = str(DIA)
        if DIA - 2 <= 9:
            strLIMdia = "0"+str(DIA-2)
        else:
            strLIMdia = "0"+str(DIA-2)

    HORA = random.randint(7, 22)
    if HORA <= 9:
        strHORA = "0"+str(HORA)
    else:
        strHORA = str(HORA)

    randMINUTO = random.randint(1, 4)
    if randMINUTO == 1:
        MINUTO = 0
    elif randMINUTO == 2:
        MINUTO = 15
    elif randMINUTO == 3:
        MINUTO = 30
    elif randMINUTO == 4:
        MINUTO = 45

    if MINUTO <= 9:
        strMINUTO = "0"+str(MINUTO)
    else:
        strMINUTO = str(MINUTO)



    PRECO = random.randint(2, 10)


    DATACORRIDAFORMATADA = strANO+"-"+strMES+"-"+strDIA+" "+strHORA+":"+strMINUTO
    LIMITEDATAFORMATADA = strLIMano+"-"+strLIMmes+"-"+strLIMdia
    USERNAMEADMIN = admin



    print("Preço:", PRECO, "\nLocal:", LOCAL, "\nDistância:", DISTANCIA, "\nMAX inscritos:", LIMITEINSCRITOS, "\nData LIMITE:", LIMITEDATAFORMATADA, "\nData CORRIDA:", DATACORRIDAFORMATADA, "\nADMIN:", USERNAMEADMIN)


    input("\nCRIAR?")

    insere_nova_prova(PRECO, LOCAL, DISTANCIA, LIMITEINSCRITOS, LIMITEDATAFORMATADA, DATACORRIDAFORMATADA, USERNAMEADMIN)

    AUTOaddnovaprova(admin)

# =============================================================================================
# =============================================================================================

def AUTOregistarmembro():
    try:
        conn = psycopg2.connect(user="postgres",
                                password="postgres",
                                host="localhost",
                                port="5433",
                                database="CRC") 

        cur = conn.cursor()
        
        randSEXO = random.randint(1, 2)
        if randSEXO == 1:
            SEXO = "F"
            randgender = 'female'
        elif randSEXO == 2:
            SEXO = "M"
            randgender = 'male'

        PRIMEIRONOME = names.get_first_name(gender=randgender)
        APELIDO = names.get_last_name()

        NUMaleatorio = str(random.randint(0, 9999))

        NOME = PRIMEIRONOME+" "+APELIDO
        EMAIL = PRIMEIRONOME.lower()+NUMaleatorio+"@gmail.com"
        PASSWORD = "pass"+PRIMEIRONOME.lower()
        USERNAME = PRIMEIRONOME.lower()+NUMaleatorio+APELIDO.lower()
        print(" ")

        print(NOME)
        print(SEXO)
        print(EMAIL)
        print(PASSWORD)
        print(USERNAME)
        input("\nConfirmar?")


        cur.execute("INSERT INTO utilizadores VALUES (DEFAULT, '{0}', '{1}', MD5('{2}'), '{3}') RETURNING id;".format(NOME, EMAIL, PASSWORD, USERNAME))
        ID = cur.fetchone()
        conn.commit()

        cur.execute("INSERT INTO membros VALUES (%s, %s);",(SEXO, ID))
        conn.commit()
        AUTOregistarmembro()
    except (Exception, psycopg2.Error):
        if(conn):
            print(
                "Já existe uma conta com esse email e/ou username. Por favor tente outro!")

    finally:
        # closing database connection.
        if(conn):
            cur.close()
            conn.close()

# =============================================================================================
# =============================================================================================

def AUTOinscreverProva(idmembro):

    id = random.randint(16, 26)

    try:
        conn = psycopg2.connect(user="postgres",
                                password="postgres",
                                host="localhost",
                                port="5433",
                                database="CRC") 

        cur = conn.cursor()

        #verifica se é possivel inscrever na prova
        cur.execute("SELECT corridas.lim_inscritos, corridas.num_inscritos "
                    "FROM corridas, provas "
                    "WHERE corridas.id = provas.corridas_id AND corridas.id = {0}".format(id))     
        conn.commit()

        i = 0
        for linha in cur.fetchall():
            i = cur.rowcount
            x1 = linha[0]
            x2 = linha[1]
            
            vagas = x1-x2

            if vagas == 0:
                print("Não é possivel inscrever-se nessa prova")
                AUTOinscreverProva(random.randint(20, 30))
                return 0
        
        if i == 0:
            print("Não é possivel inscrever-se nessa prova")
            AUTOinscreverProva(random.randint(20, 30))
            return 0
        
        #verifica se já está inscrito na prova
        cur.execute("SELECT inscricoes.corridas_id, inscricoes.membros_utilizadores_id "
                    "FROM inscricoes, utilizadores, provas "
                    "WHERE provas.corridas_id = inscricoes.corridas_id AND membros_utilizadores_id = utilizadores.id AND utilizadores.id = {0} AND provas.corridas_id = {1}".format(idmembro,id))
        conn.commit()

        j = 0
        for linha1 in cur.fetchall():
            j = cur.rowcount
        
        if j == 1:
            print("Já está inscrito nesta prova")
            AUTOinscreverProva(random.randint(20, 30))
            return 0

        # Se chegou até aqui vai então fazer a inscrição
        cur.execute("SELECT id FROM utilizadores WHERE id = {0};".format(idmembro))
        #membroID = cur.fetchone()
        for linha2 in cur.fetchall():
            membroID = linha2[0]
        conn.commit()
        

        # Confirma se pretende fazer a inscrição
        cur.execute("SELECT provas.valor, corridas.data_corrida "
                    "FROM corridas, provas "
                    "WHERE provas.corridas_id = corridas.id AND corridas.id = {0} ".format(id))
        conn.commit()
        
        for linha3 in cur.fetchall():
            x1 = linha3[0] # valor
            x2 = linha3[1] # data
        
        print("\nEsta prova tem um preço de",x1,"euros e decorre a",x2,"\n")
        input(" ")

        #Transação
        conn.autocommit = False
        cur.execute("INSERT INTO inscricoes (pago, corridas_id,membros_utilizadores_id) VALUES(FALSE,{0},{1})".format(id,membroID))
        cur.execute("UPDATE corridas SET num_inscritos = num_inscritos + 1 WHERE id = {0}".format(id))
        conn.commit()

        AUTOinscreverProva(random.randint(20, 30))

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
        conn.rollback() #Transação
    finally:
        # closing database connection.
        if(conn):
            cur.close()
            conn.close()

# =============================================================================================
# =============================================================================================

def AUTOupdatePago():
    ID_MEMBRO = random.randint(20, 30)
    ID_CORRIDA = random.randint(16, 26)

    try:
        conn = psycopg2.connect(user="postgres",
                                password="postgres",
                                host="localhost",
                                port="5433",
                                database="CRC") 

        cur = conn.cursor()

        cur.execute("SELECT valor FROM provas WHERE corridas_id = {0}".format(ID_CORRIDA))

        preco = cur.fetchone()[0]

        cur.execute("SELECT lim_data FROM corridas WHERE id = {0}".format(ID_CORRIDA))

        datalim = cur.fetchone()[0]

        print(preco)
        print(datalim)


        cur.execute("UPDATE inscricoes SET pago = true, datapagamento = '{0}',precopago = {1} WHERE membros_utilizadores_id = {2} AND corridas_id = {3};".format(datalim,preco,ID_MEMBRO,ID_CORRIDA))   
        conn.commit()
        AUTOupdatePago()

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
    finally:
        # closing database connection.
        if(conn):
            cur.close()
            conn.close()

# =============================================================================================
# =============================================================================================

def updatetempos():

    # Se data da prova ja passou
        # e ainda nao tem nada no hist de tempos
        # preencher com valores aleatórios


    try:
        conn = psycopg2.connect(user="postgres",
                                password="postgres",
                                host="localhost",
                                port="5433",
                                database="CRC") 

        cur = conn.cursor()

        



        cur.execute("SELECT inscricoes.corridas_id, inscricoes.membros_utilizadores_id "
                    "FROM inscricoes "
                    "WHERE inscricoes.pago = TRUE")

        conn.commit()

        for linha in cur.fetchall():
            x1 = linha[0]  # id da prova
            x2 = linha[1]  # id membro

            cur.execute("SELECT corridas.id, corridas.data_corrida "
                    "FROM corridas "
                    "WHERE corridas.id = {0} AND corridas.data_corrida < '{1}'".format(x1, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

            conn.commit()
            i = cur.rowcount

            if i != 0:

                cur.execute("SELECT hist_de_tempos.tempo_seg "
                    "FROM hist_de_tempos "
                    "WHERE hist_de_tempos.provas_corridas_id = {0} AND hist_de_tempos.membros_utilizadores_id = {1}".format(x1,x2))

                conn.commit()
                j = cur.rowcount

                if j == 0:

                    cur.execute("SELECT corridas.id, corridas.km "
                    "FROM corridas "
                    "WHERE corridas.id = {0}".format(x1))

                    conn.commit()

                    for linha2 in cur.fetchall():
                        x3 = linha2[0]  # id da prova
                        x4 = linha2[1]  # km



                        # 1km faz-se em 300 ou 360
                        tempMIN = x4 * 300
                        tempMAX = x4 * 360

                        TEMPOGASTO = random.randint(tempMIN, tempMAX)

                        cur.execute("INSERT INTO hist_de_tempos VALUES ({0}, {1}, {2}); ".format(TEMPOGASTO, x2, x1))   

                        conn.commit()


    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
    finally:
        # closing database connection.
        if(conn):
            cur.close()
            conn.close()

# =============================================================================================
# =============================================================================================

def AUTOaddnovoTreino(admin):
    limparjanela(admin)
    print("NOVO TREINO ------------------------------------------")
    print(" ")
    MENU = "NP"
    TIPO = random.randint(1, 5)
    if TIPO == 1:
        DISTANCIA = 1
    elif TIPO == 2:
        DISTANCIA = 5
    elif TIPO == 3:
        DISTANCIA = 10
    elif TIPO == 4:
        DISTANCIA = 20
    elif TIPO == 5:
        DISTANCIA = 40

    LOCAL = "Local"+str(random.randint(0, 9999))

    LIMITEINSCRITOS = random.randint(3, 30)


    print("DATA DA PROVA ----------------------------------------")
    print(" ")

    ANO = random.randint(2021, 2022)
    strANO = str(ANO)
    strLIMano = strANO

    MES = random.randint(1, 12)
    if MES <= 9:
        strMES = "0"+str(MES)
        strLIMmes = strMES
    else:
        strMES = str(MES)
        strLIMmes = strMES

    DIA = random.randint(3, 27)
    if DIA <= 9:
        strDIA = "0"+str(DIA)
        strLIMdia = "0"+str(DIA-2)
    else:
        strDIA = str(DIA)
        if DIA - 2 <= 9:
            strLIMdia = "0"+str(DIA-2)
        else:
            strLIMdia = "0"+str(DIA-2)



    HORA = random.randint(7, 22)
    if HORA <= 9:
        strHORA = "0"+str(HORA)
    else:
        strHORA = str(HORA)

    randMINUTO = random.randint(1, 4)
    if randMINUTO == 1:
        MINUTO = 0
    elif randMINUTO == 2:
        MINUTO = 15
    elif randMINUTO == 3:
        MINUTO = 30
    elif randMINUTO == 4:
        MINUTO = 45

    if MINUTO <= 9:
        strMINUTO = "0"+str(MINUTO)
    else:
        strMINUTO = str(MINUTO)



    PERIODICIDADE = random.randint(1, 3)
    if PERIODICIDADE == 1:
        REPETE = 'N'
    elif PERIODICIDADE == 2:
        REPETE = 'S'
    elif PERIODICIDADE == 3:
        REPETE = 'M'

    DATACORRIDAFORMATADA = strANO+"-"+strMES+"-"+strDIA+" "+strHORA+":"+strMINUTO
    LIMITEDATAFORMATADA = strLIMano+"-"+strLIMmes+"-"+strLIMdia
    USERNAMEADMIN = admin




    TEMTREINADOR = random.randint(1, 3)

    if TEMTREINADOR == 1: #NAO
        print("SEM TREINADOR")
        print("REP:", REPETE, "\nLocal:", LOCAL, "\nDistância:", DISTANCIA, "\nMAX inscritos:", LIMITEINSCRITOS, "\nData LIMITE:", LIMITEDATAFORMATADA, "\nData CORRIDA:", DATACORRIDAFORMATADA, "\nADMIN:", USERNAMEADMIN)
        input("\nCRIAR?")
        insere_novo_treinoSEMtreinador(REPETE, datetime.datetime(int(ANO), int(MES), int(DIA)).weekday(), LOCAL, DISTANCIA, LIMITEINSCRITOS, LIMITEDATAFORMATADA, DATACORRIDAFORMATADA)



    elif TEMTREINADOR == 2: #EXISTENTE
        while True:
            IDTREINADOR = random.randint(1, 20)
            EXISTE = verifica_treinador(IDTREINADOR)

            if (EXISTE != 1):   
                print("Escolha uma resposta válida!")
            else:                    
                break
        print(IDTREINADOR)
        print("REP:", REPETE, "\nLocal:", LOCAL, "\nDistância:", DISTANCIA, "\nMAX inscritos:", LIMITEINSCRITOS, "\nData LIMITE:", LIMITEDATAFORMATADA, "\nData CORRIDA:", DATACORRIDAFORMATADA, "\nADMIN:", USERNAMEADMIN)
        input("\nCRIAR?")
        insere_novo_treinoCOMtreinador(REPETE, datetime.datetime(int(ANO), int(MES), int(DIA)).weekday(), IDTREINADOR, LOCAL, DISTANCIA, LIMITEINSCRITOS, LIMITEDATAFORMATADA, DATACORRIDAFORMATADA)




    elif TEMTREINADOR == 3: #NOVO
        randSEXO = random.randint(1, 2)
        if randSEXO == 1:
            randgender = 'female'
        elif randSEXO == 2:
            randgender = 'male'

        PRIMEIRONOME = names.get_first_name(gender=randgender)
        APELIDO = names.get_last_name()


        NOMETREINADOR = PRIMEIRONOME+" "+APELIDO
        print(NOMETREINADOR)
        print("REP:", REPETE, "\nLocal:", LOCAL, "\nDistância:", DISTANCIA, "\nMAX inscritos:", LIMITEINSCRITOS, "\nData LIMITE:", LIMITEDATAFORMATADA, "\nData CORRIDA:", DATACORRIDAFORMATADA, "\nADMIN:", USERNAMEADMIN)
        input("\nCRIAR?")
        IDTREINADOR = insere_novo_treinador(NOMETREINADOR)

        insere_novo_treinoCOMtreinador(REPETE, datetime.datetime(int(ANO), int(MES), int(DIA)).weekday(), IDTREINADOR, LOCAL, DISTANCIA, LIMITEINSCRITOS, LIMITEDATAFORMATADA, DATACORRIDAFORMATADA)



    AUTOaddnovoTreino(admin)

# =============================================================================================
# =============================================================================================

def listarProvasCOMinscritos(admin):
    limparjanela(admin)

    try:
        conn = psycopg2.connect(user="postgres",
                                password="postgres",
                                host="localhost",
                                port="5433",
                                database="CRC") 

        cur = conn.cursor()

        
        cur.execute("SELECT corridas.id, corridas.sitio, corridas.km, corridas.lim_data, corridas.data_corrida, corridas.lim_inscritos, corridas.num_inscritos, provas.valor "
                    "FROM corridas, provas "
                    "WHERE corridas.id = provas.corridas_id")
                
        conn.commit()


        for linha in cur.fetchall():
            x1 = linha[0]  # id
            x2 = linha[1]  # local
            x3 = linha[2]  # distancia
            x4 = linha[3]  # data limite
            x5 = linha[4]  # data corrida
            x6 = linha[5]  # limite inscritos
            x7 = linha[6]  # numero inscritos
            x8 = linha[7]  # valor

            vagas = x6-x7

            if vagas > 0:
                print("ID:", x1, "\n| Local:", x2, "| Distancia:", x3, "km | Data:", x5,
                      "\n| Limite Inscricao:", x4, "| Vagas:", vagas, "\n| Valor:", x8,"\n")

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
    finally:
        # closing database connection.
        if(conn):
            cur.close()
            conn.close()

# =============================================================================================
# =============================================================================================

def listarTreinosCOMinscritos(admin):
    limparjanela(admin)

    try:
        conn = psycopg2.connect(user="postgres",
                                password="postgres",
                                host="localhost",
                                port="5433",
                                database="CRC") 

        cur = conn.cursor()

        
        cur.execute("SELECT corridas.id, corridas.sitio, corridas.km, corridas.lim_data, corridas.data_corrida, corridas.lim_inscritos, corridas.num_inscritos, treinos.rep, treinadores_id "
                    "FROM corridas, treinos "
                    "WHERE corridas.id = treinos.corridas_id")
                
        conn.commit()


        for linha in cur.fetchall():
            x1 = linha[0]  # id
            x2 = linha[1]  # local
            x3 = linha[2]  # distancia
            x4 = linha[3]  # data limite
            x5 = linha[4]  # data corrida
            x6 = linha[5]  # limite inscritos
            x7 = linha[6]  # numero inscritos
            x8 = linha[7]  # repetitivo
            x9 = linha[8]  #id treinador

            if x9 == None:
                treinador = "Sem treinador"
            
            else:
                cur.execute("SELECT nome FROM treinadores WHERE id = {0}".format(x9))
                for linha1 in cur.fetchall():
                    treinador = linha1[0]

            if x8 == "S":
                REPETE = "Semanalmente"
            elif x8 == "M":
                REPETE = "Mensalmente"
            elif x8 == "N":
                REPETE = "Não"


            vagas = x6-x7

            if vagas > 0:
                print("ID:", x1, "\n| Local:", x2, "| Distancia:", x3, "km | Data:", x5,
                      "\n| Limite Inscricao:", x4, "| Vagas:", vagas, "\n| Repete:", REPETE,"| Treinador:",treinador,"\n")

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
    finally:
        # closing database connection.
        if(conn):
            cur.close()
            conn.close()

# =============================================================================================
# =============================================================================================
# =============================================================================================
# =============================================================================================
# =============================================================================================
# =============================================================================================

menuinicial()

# AUTOupdatePago()
# AUTOinscreverProva(random.randint(20, 30))
# AUTOaddnovoTreino('pedroteixeira')
# AUTOaddnovaprova('ivobotelho')

# menuestatisticas('pedroteixeira')

# updatetempos()
# updatedates()

# menuadmin('pedroteixeira')
# menuadmin('ivobotelho')

# menumembro('regina9482hernandez')
# menumembro('beverly3086gansen')
# menumembro('sarasampaio')

# menumembro('joaoratao')
# menumembro('ruipedro')

# =============================================================================================
# =============================================================================================
# =============================================================================================
# =============================================================================================


# [X] - FEITO
# [ ] - POR FAZER
# [C] - COMPLETAR


# ======================================================================

# MEMBRO

    # [X] - Registar membro. Requer nome, endereço de email e password
            # (deve ser encriptada de forma a garantir a segurança);

    # [X] - Login (o ------nome do membro------ deve ser visível nos menus disponíveis após o login) / Logout;

    # [X] - Listar todas as Provas de Corrida (permitir filtrar por corridas com inscrições ativas);

    # [X] - Listar todos os Treinos (permitir filtrar por treinos com inscrições ativas);

    # [X] - Ver os detalhes de uma prova de corrida ou de um treino;

    # [X] - Inscrever-se numa prova de corrida, mostrando o preço e a data da prova;

    # [X] - Inscrever-se num treino, mostrando a data do treino e o número de inscritos;

    # [X] - Listar todas as provas e treinos em que está inscrito neste momento,
            # bem como todos os que se inscreveu no passado;

    # [X] - Mostrar em quantas provas já participou, fazendo também distinção por distância da prova;

    # [X] - Consultar mensagens enviadas pelo administrador, devendo ser possível distinguir as lidas das não lidas;

    # [X] - Pesquisar provas usando diversos critérios: por distância, por título, por data
            # (determinada data ou entre duas datas), por local. Deve ser possível especificar
            # critérios de ordenação dos resultados.
            # Esta funcionalidade deve ser aplicável em dois contextos:
            # i) a todas as provas no sistema;
            # ii) às provas em que o membro se inscreveu.
    
    # [X] - Classificações Pessoais -> Por testar
    # [X] - Classificações Gerais


# ADMINISTRADOR

    # [X] - Login via email e password / Logout;

    # [X] - Adicionar uma nova prova ou um novo treino;

    # [X] - Visualizar e alterar todas as provas e treinos disponíveis;

    # [X] - Corrigir o preço da inscrição numa prova (deve ser mantido um histórico com as alterações,
            # incluindo a data da alteração, que também é visto quando se visualizam os detalhes de uma prova);

    # [X] - Remover uma prova (apenas se não tem inscrições);

    # [X] - Enviar uma mensagem a todos os membros;

    # [X] - Enviar uma mensagem a um membro específico 

    # [X] - ... ou a um conjunto de membros inscritos numa prova ou treino;

    # [X] - Alterar o estado de uma inscrição numa prova para pago quando valida o pagamento pelo membro 
            # (assume-se que os membros enviam o valor para o administrador de alguma forma sendo o estado alterado nessa altura);

    # [X] - Ver estatísticas: 
        # [X] - total de membros, 
        # [X] - total de provas, 
        # [X] - número e valor total das inscrições nas provas ainda a decorrer no futuro,
        # [X] - total de provas por tipo.
        # [X] - Para além destes valores indicados, apresente mais dois valores à sua escolha, que considere úteis num sistema deste tipo.

# OUTROS
    
    # [X] - uma transação e; (rollback)
    # [X] - uma função (ou procedimento ou trigger) em PL/SQL.



# [X] Mostrar quem sao os treinadores quando mostra os treinos

# [X] Nos diagramas os treinadores podem nao estar associados a nenhum treino, remover esconderes, grupos, etc




# [X] - remover print debug

# [x] - corrigir desinscrever


# [X] - Alterar limite inscricoes (treinos e provas): não permitir limite de inscricoes menor que inscritos (Pesquisar LIMITEINSCRITOS)



# [X] - Fazer Alterar DI e DT (Pesquisar ALTERACAO = DT)


# [X] - Mensagem grupos -> mostar apenas corridas que Têm inscritos

# [X] - Mensagem grupos



# [X] - desinscrever no membro

# [X] - pesquisar data e intervalo data não permite data do passado 

# [X] - Classificações -> lugares

# [X] - Classificações mostrar local e distancia

# [X] - Classificações -> provas com inscritos
