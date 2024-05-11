from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from time import sleep
from abc import ABC, abstractmethod
from copy import deepcopy
from selenium.webdriver.common.alert import Alert

class Bot:
    def __init__(self):
        self._navegador = None
        self._login = None
        self._senha = None
        self._servico = Service(ChromeDriverManager().install())


    def navegar(self, url:str) -> None:
        self._navegador = webdriver.Chrome(service=self._servico)
        self._navegador.get(url)
        self._navegador.implicitly_wait(10)
        return None
    
    @abstractmethod
    def autenticar(self) -> None:
        pass
        return None
    

    def finalizar(self):
        __opcao_finalizar = str(input('Pressione qualquer tecla para finalizar...'))
        return


class Pje(Bot):
    def __init__(self):
        super().__init__()
        self._xpath_campo_numero_processo = '//div[@id="fPP:numProcessoDiv"]/div/div/div[2]/input[@id="fPP:numeroProcesso:numeroSequencial"]' 
        self._janela_original = None
        self._janela_processo = None
        self._lista_detalhes_titulos = []
        self._lista_detalhes_conteudo = []
        self._contador_titulos = 1
        self._contador_qtd_processos = 0
    
    def autenticar(self):
        print('Autenticação: você tem 5 segundos para realizar a autenticação manualmente!')
        sleep(5)
        url_falha_autenticação = ('https://tjrj.pje.jus.br/1g/login.seam?loginComCertificado=false')
        url = self._navegador.current_url

        if url in url_falha_autenticação:
            raise PermissionError('Você não autenticou a tempo e por isso o Bot foi finalizado.')
        
        try:
            print('Autenticado!')
            return
        except PermissionError:
            self._navegador.close()
        return
    
    def pagina_pesquisa(self, url:str) -> None:
        self._navegador.get(url)
        self._janela_original = self._navegador.current_window_handle
        return None

    def esconder_navegador(self) -> None:
        self._navegador.minimize_window()
        return None

    def pesquisar_processo(self, numero_processo_tratado:str, numero_processo_cru:str) -> None:
        def __fechar_janela_processo():
            self._navegador.close()
            return None
        

        def __pegar_informacoes_campos() -> list[str]:
            detalhes_conteudo_pt1 = self._navegador.find_elements(By.XPATH,'//div[@id="maisDetalhes"]/dl/dd')
            detalhes_conteudo_pt2 = self._navegador.find_element(By.XPATH,'//div[@id="maisDetalhes"]/div[1]/dl/dd').text
            detalhes_conteudo_pt3 = self._navegador.find_element(By.XPATH,'//div[@id="maisDetalhes"]/div[2]/dl/dd').text
            detalhes_conteudo_pt4 = self._navegador.find_element(By.XPATH,'//div[@id="maisDetalhes"]/div[3]/dl/dd').text

            polo_ativo_autor = self._navegador.find_element(By.XPATH,'//div[@id="poloAtivo"]/table/tbody/tr/td/span').text
            try:
                polo_ativo_advogado = self._navegador.find_element(By.XPATH,'//div[@id="poloAtivo"]/table/tbody/tr/td/ul/div/li').text
            except Exception:
                polo_ativo_advogado = 'NÃO INFORMADO'

            polo_passivo_autor = self._navegador.find_element(By.XPATH, '//div[@id="poloPassivo"]/table/tbody/tr/td/span').text
            polo_passivo_advogado = self._navegador.find_element(By.XPATH,'//div[@id="poloPassivo"]/table/tbody/tr/td/ul').text

            conteudo = []
            conteudo.append(numero_processo_cru)
            for e in detalhes_conteudo_pt1:
                conteudo.append(e.text)
            conteudo.append(detalhes_conteudo_pt2)
            conteudo.append(detalhes_conteudo_pt3)
            conteudo.append(detalhes_conteudo_pt4)
            conteudo.append(polo_ativo_autor)
            conteudo.append(polo_ativo_advogado)
            conteudo.append(polo_passivo_autor)
            conteudo.append(polo_passivo_advogado)
            
            transferencia_conteudo = deepcopy(conteudo)
            self._lista_detalhes_conteudo.append(transferencia_conteudo)
            return None

        def __aceitar_popup() -> None:
            popup = Alert(self._navegador)
            popup.accept()
            sleep(2)
            return None

        campo_processo = self._navegador.find_element(By.XPATH, self._xpath_campo_numero_processo).send_keys(numero_processo_tratado)
        botao_pesquisar = self._navegador.find_element(By.XPATH, '//input[@id="fPP:searchProcessos"]').click()
        processo = self._navegador.find_element(By.XPATH, '//tbody[@id="fPP:processosTable:tb"]/tr/td[2]/a').click()
        sleep(2)

        __aceitar_popup()

        janelas_abertas = self._navegador.window_handles
        self._janela_original = janelas_abertas[0]
        self._janela_processo = janelas_abertas[-1]
        self._navegador.switch_to.window(self._janela_processo)        

        menu_dropdown = self._navegador.find_element(By.XPATH, '//form[@id="navbar"]/ul/li[@class="dropdown drop-menu mais-detalhes"]').click()
        
        __pegar_informacoes_campos()
        __fechar_janela_processo()

        self._navegador.switch_to.window(self._janela_original)

        return self._lista_detalhes_conteudo
