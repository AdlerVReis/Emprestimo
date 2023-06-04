import PySimpleGUI as sg
import pyodbc

dados_conexao = (
    "Driver={SQL Server};"
    "Server={localhost\SQLEXPRESS};"
    "Database={creditopython};")

conexao = pyodbc.connect(dados_conexao)

cursor = conexao.cursor()

sg.theme('Material1')   # Add a touch of color
# All the stuff inside your window.

layout = [  [sg.Text('Por gentileza, preencha o formulario abaixo para submeter sua solicitação:')],
            [sg.Text('Nome Completo'), sg.InputText(key='nome')],
            [sg.Text('Telefone'), sg.InputText(key='telefone')],
            [sg.Text('CPF:'), sg.InputText(key='CPF')],
            [sg.Text('Digite o valor desejado:'), sg.Input(key='valor')],
            [sg.Text('Valor de Entrada:'), sg.Input(key='entrada')],
            [sg.Text('Renda:'), sg.Input(key='renda')],
            [sg.Text('Quantidade de Parcelas:'), sg.Input(key='prazo')],
            [sg.Button('Submeter'), sg.Button('Cancel')] ]

layout2 = [  [sg.Text('Parabéns, seu emprestimo foi PRÉ-APROVADO. Em breve nossos colaboradores entrarão em contato')]]
layout3 = [  [sg.Text('infelizmente seu emprestimo foi não foi aprovado.')]]
layout4 = [  [sg.Text('Valor de Entrada esta abaixo do percentual exigido. Infelizmente não poderemos seguir com sua solicitação')]]

# Create the Window
window = sg.Window('Analise de Crédito', layout)

event, values = window.Read()

nome = values['nome']
telefone = values['telefone']
CPF = values['CPF']
E = values['entrada']
V = values['valor']
R = values['renda']
P = values['prazo']
E1 = float(E)
V1 = float(V)
R1 = float(R)
P1 = float(P)

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    if event == sg.WIN_CLOSED or event == 'Submeter':
        if E1 < ((20/100)*V1):
            window = sg.Window('Analise de Crédito', layout4)
            comando = f"""INSERT INTO contato(Nome, Telefone, CPF, Valor, ValorEntrada, Renda, Prazo, STATUS)
            VALUES ('{nome}','{telefone}','{CPF}',{V},{E},{R},{P},'PERCENTUAL')"""
            cursor.execute(comando)
            cursor.commit()
        else:
            PR = V1 / P1
            L = ((30/100)*R1)
            if PR == L or PR > L:
                window = sg.Window('Analise de Crédito', layout3)
                comando = f"""INSERT INTO contato(Nome, Telefone, CPF, Valor, ValorEntrada, Renda, Prazo, STATUS)
                VALUES ('{nome}','{telefone}','{CPF}',{V},{E},{R},{P},'NEGADO')"""
                cursor.execute(comando)
                cursor.commit()
            else:
                window = sg.Window('Analise de Crédito', layout2)
                comando = f"""INSERT INTO contato(Nome, Telefone, CPF, Valor, ValorEntrada, Renda, Prazo, STATUS)
                VALUES ('{nome}','{telefone}','{CPF}',{V},{E},{R},{P},'APROVADO')"""
                cursor.execute(comando)
                cursor.commit()
window.close()