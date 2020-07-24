import requests
from tkinter import *
from tkinter import messagebox
import datetime
import threading

'''
A API utilizada no desenvolvimento foi a do site WEBMANIABR.COM
Link para solicitar: https://webmaniabr.com/docs/rest-api-cep-ibge/
Apos receber por email eh so preencher as duas variaveis a seguir
'''
APP_KEY = ""
APP_SECRET = ""

janela = Tk()
janela.resizable(FALSE, FALSE) #Desabilita as opcoes de ajuste do tamanho da janela
janela.geometry("360x230") #Define o tamanho da janela principal
janela.title("CONSULTA CEP - Versao 1.0.infinito") #Define o titulo da janela principal

def consulta():
    CEP = ENT_CEP.get() #Pega o CEP digitado no ENTRY
    #Inicia uma serie de filtros para que ao enviar os dados para a API, va apenas os 8 numeros correspondetes ao CEP
    if CEP == "" : #Verifica se o campo nao esta vazio
        messagebox.showwarning("Campo CEP vazio", "Digite um CEP, a caixa de pesquisa nao pode ser vazia.")
    elif not CEP.isnumeric(): #Verifica se apenas numeros foram digitados
        messagebox.showwarning("CEP invalido", "Digite apenas numeros, sem letras, tracos ou qualquer outro caractere especial.")
    elif len(CEP) != 8: # Verifica se o tamanho do CEP eh exatamente 8
        messagebox.showwarning("CEP incompleto", "Digite os 8 numeros correspondentes ao CEP.")
    else:
        REQ = requests.get("https://webmaniabr.com/api/1/cep/" + CEP + "/?app_key=" + APP_KEY + "&app_secret=" + APP_SECRET)
        JSON_RES = REQ.json()
        if "erro" in REQ.text: #Se o cep nao existe a API volta uma chave de erro, aqui ele trata isso e imprime oque a API mandar
            ERRO_API = JSON_RES["error"]
            messagebox.showerror("Erro ao requisitar o CEP para a API", ERRO_API)
        else:#Escreve a consulta em um arquivo e preenche as labels vazias com os resultados da consulta

            DADOS = "Endereco: " + JSON_RES["endereco"] + "\n" \
                    "Bairro: " + JSON_RES["bairro"] + "\n" \
                    "Cidade: "+ JSON_RES["cidade"] + "\n"\
                    "UF: "+  JSON_RES["uf"] + "\n" + \
                    "CEP: " + JSON_RES["cep"] + "\n" +  \
                    "IBGE: " + JSON_RES["ibge"] + "\n"

            salvar(DADOS) #funcao que escreve no arquivo chamada, o parametro eh os dados da consulta feita

            #Comeca a preencher as labels vazias com os resultados retornado
            LB_END_RES["text"] = JSON_RES["endereco"]
            LB_BAIRRO_RES["text"] = JSON_RES["bairro"]
            LB_CIDADE_RES["text"] = JSON_RES["cidade"]
            LB_UF_RES["text"] = JSON_RES["uf"]
            LB_CEP_RES["text"] = JSON_RES["cep"]
            LB_IBGE_RES["text"] = JSON_RES["ibge"]

def restantes():#Pega a quantidade de requisicoes feitas, restantes e o plano que foi contratado junto a API
    REQ = requests.get("https://webmaniabr.com/api/1/cep/requests/?app_key=" + APP_KEY + "&app_secret=" + APP_SECRET)
    REQ_JSON = REQ.json()

    #Passa tudo pra STRING e formata pra mostrar no messagebox
    LIMPO_REQ = "Requisicoes feitas: " + str(REQ_JSON["total"]) + "\n" + "Limite diario: " + str(REQ_JSON["limit"]) + "\n" +\
                "Expira em: " + str(REQ_JSON["expires_in"]) + "\n" + "Plano atual: " + str(REQ_JSON["plan"])
    messagebox.showinfo("REQUISICOES RESTANTES", LIMPO_REQ)

def limpar(): #Apenas limpa os campos de pesquisa e resultado
    LB_END_RES["text"] = ""
    LB_BAIRRO_RES["text"] = ""
    LB_CIDADE_RES["text"] = ""
    LB_UF_RES["text"] = ""
    LB_CEP_RES["text"] = ""
    LB_IBGE_RES["text"] = ""
    ENT_CEP.delete(0, "end")

def salvar(DADOS):
    ARQ_REG = open("consultas_cep.txt", "a") #Abre o arquivo, parametro "A" eh pra escrever no final do arquivo
    DATA_HORA = datetime.datetime.now()
    ARQ_REG.writelines("\n" + "Consulta feita em: " + str(DATA_HORA) + "\n") #Primeiro ele registra a data e hora em que a consulta foi feita
    ARQ_REG.writelines(DADOS) #Registra os dados voltados da consulta
    ARQ_REG.close() #Fecha o arquivo

def sair():
    exit(0)

'''
Cada vez que os botoes de CONSULTA e CONSULTA DE REQUISICOES RESTANTES eh acionado ele cria uma THREAD nova
isso evita que todo o programa fique travado ate que o codigo dentro da funcao do botao termine a execucao
'''
def THREAD_CONSULTA():
    t_consulta = threading.Thread(target=consulta)
    t_consulta.daemon = True
    t_consulta.start()

def THREAD_RESTANTES():
    t_restante = threading.Thread(target=restantes)
    t_restante.daemon = True
    t_restante.start()

LB_TITLE = Label(janela, text="Consulta de CEP", font="Arial")
LB_TITLE.place(x=125, y=10)

LB_CEP = Label(janela, text="DIGITE O CEP (APENAS NUMEROS)")
LB_CEP.place(x=10, y=40)

ENT_CEP = Entry(janela, font="AriaBlack", borderwidth=3) #Campo onde o CEP eh digitado
ENT_CEP.place(x=10, y=65)

BT_CONSULTA = Button(janela, text="CONSULTAR", width=20, command=THREAD_CONSULTA) #Botao de consulta
BT_CONSULTA.place(x=200, y=63)

BT_REQ_RESTANTES = Button(janela, text="CONS. RESTANTES", width=20, command=THREAD_RESTANTES) # Botao de consulta de requisicoes restantes
BT_REQ_RESTANTES.place(x=200, y=99)

BT_LIMPA = Button(janela, text="LIMPAR CAMPOS", width=20, command=limpar)
BT_LIMPA.place(x=200, y=135)

BT_SAIR = Button(janela, text="SAIR", width=20, command=sair)
BT_SAIR.place(x=200, y=171)

##########ENDERECO##########
LB_ENDERECO = Label(janela, text="ENDERECO: ")
LB_ENDERECO.place(x=10, y=102)
LB_END_RES = Label(janela, text="")
LB_END_RES.place(x=77, y=102)

##########BAIRRO##########
LB_BAIRRO = Label(janela, text="BAIRRO: ")
LB_BAIRRO.place(x=10, y=122)
LB_BAIRRO_RES = Label(janela, text="")
LB_BAIRRO_RES.place(x=60, y=122)

##########CIDADE##########
LB_CIDADE = Label(janela, text="CIDADE: ")
LB_CIDADE.place(x=10, y=142)
LB_CIDADE_RES = Label(janela, text="")
LB_CIDADE_RES.place(x=60, y=142)

##########UF##########
LB_UF = Label(janela, text="UF: ")
LB_UF.place(x=10, y=162)
LB_UF_RES = Label(janela, text="")
LB_UF_RES.place(x=32, y=162)

##########CEP##########
LB_CEP = Label(janela, text="CEP: ")
LB_CEP.place(x=10, y=182)
LB_CEP_RES = Label(janela, text="")
LB_CEP_RES.place(x=38, y=182)

##########IBGE##########
LB_IBGE = Label(janela, text="IBGE: ")
LB_IBGE.place(x=10, y=202)
LB_IBGE_RES = Label(janela, text="")
LB_IBGE_RES.place(x=40, y=202)

janela.mainloop()
