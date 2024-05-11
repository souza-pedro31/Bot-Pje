import PySimpleGUI as sg
import etl

sg.theme('Reddit')

layout = [
    [sg.Text('Caminho: '), sg.InputText(key='-caminho_arquivo-'), sg.FileBrowse('Buscar')],
    [sg.Button('Iniciar Bot', size=(56))],
    [sg.Text('Bot consultor v1.0', size=(38)), sg.Text('GitHub: souza-pedro31', size=(16))],
 ]

interface = sg.Window('Bot consultor de processos', layout)

while True:
    evento, valor = interface.read()

    if evento == sg.WIN_CLOSED:
        break
    elif evento == 'Iniciar Bot':
        caminho_plan = valor['-caminho_arquivo-']
        if caminho_plan in ' ':
            sg.popup('Insira o caminho da sua planilha', title='Bot')
        else:
            sg.popup_timed('Vou iniciar sua consulta...\n\nVocê terá 5 segundos para autenticar manualmente!', auto_close_duration=3, title='Bot')
            interface.hide()
            resultado = etl.iniciar_bot(caminho_plan)
            sg.popup(f'Resultado da Consulta:\n\nEntraram: {resultado[0]} processos.\nSaíram: {resultado[1]} processos.')
            sg.popup(f'Consulta concluída!')
            break
