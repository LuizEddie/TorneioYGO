#coding: utf-8
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import sqlite3
import os
import json
from random import shuffle
from kivy.uix.spinner import Spinner
from functools import partial
from kivy.lang import Builder
Builder.load_string('''#:import Factory kivy.factory.Factory
# -*- coding: utf-8 -*-
<Inicio>:
    BoxLayout:
        orientation: "vertical"
        Button:
            text: "Comecar torneio"
            size_hint_x: 1
		    size_hint_y: .1
		    on_press: root.comecarTorneio()
        Button:
            text: "Continuar torneio"
            size_hint_x: 1
		    size_hint_y: .1
		    on_press: root.continuarTorneio()
        Button:
            text: "Historico"
            size_hint_x: 1
		    size_hint_y: .1
		    on_press: root.acessarHistorico()

<DefineTorneio>:

    name: "defineTorneio"
    quantParticipantes: quantParticipantes
    id: defineTorneio
    GridLayout:
        id: gridTorneio
        orientation: "vertical"
        cols: 1

        Label:
            text: "Numero de participantes"
            size_hint_x: 1
        TextInput:
            id: quantParticipantes
            multiline: False
            size_hint_y: 0.5

        Label:
            text: "Formato"
            size_hint_y: .5
        Spinner:
            id: formatoTorneio
            text: 'Escolha o formato'
            values: ['Mata-mata', 'Pontos Corridos']
            on_text: root.habilitarCampos()

    BoxLayout:
        orientation: "horizontal"
        size_hint_y: 0.25
        Button:
            text: "Voltar"
            size_hint_x: .5
            on_release: root.voltar()
        Button:
            text: "Confirmar"
            size_hint_x: .5
            on_press: root.abrirPopUp()

<NomearJogadores>:
    name: "nomearJogadores"
    BoxLayout:
        orientation: "vertical"
        id: boxPrincipal
        Label:
            id: lblTitulo
            text: "Jogadores"
            size_hint_y: 0.05
        GridLayout:
            id: gridLayout
            name: "gridLayout"
            cols: 4
            orientation: "vertical"

<MataMata>:
    name: "mataMata"
    BoxLayout:
        orientation: "vertical"
        id: boxMataMata


<PontosCorridos>:
    name: "pontosCorridos"
    BoxLayout:
        orientation: "vertical"
        id: boxPontosCorridos

<Placar>:
    name: "placar"
    FloatLayout:
        id: conteudo_box
        orientation: 'vertical'
        Label:
            text: "Placar"
            size_hint_y: .1
            pos_hint: {'right': .6, 'top': 1}
        GridLayout:
            canvas.before:
                Color:
                    rgb: 1,0,0
                Rectangle:
                    pos: self.pos
                    size: self.size
            size_hint_y: .1
            pos_hint: {'top': .9}
            cols: 5
            Label:
                text: "Posicao"
            Label:
                text: "Jogador"
            Label:
                text: "Vitorias"
            Label:
                text: "Derrotas"
            Label:
                text: "Pontos"

        ScrollView:
            id: scroll_placar
            size_hint_y: .7
            do_scroll_y: True
            pos_hint: {'top': .8}
            GridLayout:
                id: table_grid
                size_hint_y: None
                row_default_height: 50
                row_force_default: True
                height: self.minimum_height

<ContinuarTorneio>:
    name: "continuarTorneio"
    FloatLayout:
        Label:
            text: "Torneios em aberto"
            pos_hint: {'top': 1}
            size_hint_y: .1
        ScrollView:
            id: scroll_torneio
            size_hint_y: .8
            do_scroll_y: True
            pos_hint: {'top': .9}
            BoxLayout:
                id: lista_box
                orientation: "vertical"
                size_hint_y: None
                height: self.minimum_height

        Button:
            text: "Voltar"
            size_hint_x: .5
            pos_hint: {'top': .1}
            size_hint_y: .1
            on_release: root.voltar()


<HistoricoTorneio>:
    name: "continuarTorneio"
    FloatLayout:
        Label:
            text: "Torneios em aberto"
            pos_hint: {'top': 1}
            size_hint_y: .1
        ScrollView:
            id: scroll_torneio
            size_hint_y: .8
            do_scroll_y: True
            pos_hint: {'top': .9}
            BoxLayout:
                id: lista_box
                orientation: "vertical"
                size_hint_y: None
                height: self.minimum_height

        Button:
            text: "Voltar"
            size_hint_x: .5
            pos_hint: {'top': .1}
            size_hint_y: .1
            on_release: root.voltar()
''')
class TorneioYGO(App):
    def build(self):
        return Inicio()

class Inicio(BoxLayout):
    def __init__(self):
        super(Inicio, self).__init__()
        CheckDatabase()
        CheckDirectories()

    def comecarTorneio(self):
        janela.root_window.remove_widget(self)
        janela.root_window.add_widget(DefineTorneio())

    def continuarTorneio(self):
        janela.root_window.remove_widget(self)
        janela.root_window.add_widget(ContinuarTorneio())

    def acessarHistorico(self):
        janela.root_window.remove_widget(self)
        janela.root_window.add_widget(HistoricoTorneio())

class ContinuarTorneio(FloatLayout):

    dados_torneio = ""

    def __init__(self, **kwargs):
        super(ContinuarTorneio, self).__init__(**kwargs)
        self.construir_interface()

    def construir_interface(self):
        dict_torneios = ReadAll(False)
        box_lista = self.ids.lista_box

        for i in dict_torneios:
            box_botoes = BoxLayout(orientation="horizontal", size_hint_y=None, height=50)
            tupla_torneio = dict_torneios[i]
            btn_lista = Button(text="Id: " + str(i) + " Tipo torneio: " + tupla_torneio[1], size_hint_x=6)
            btn_lista.on_release = partial(self.pop_up_torneio, i, tupla_torneio[1])

            btn_excluir = Button(text="Excluir")
            btn_excluir.on_release = partial(self.deletar_pop_up, i, tupla_torneio[1])

            box_botoes.add_widget(btn_lista)
            box_botoes.add_widget(btn_excluir)

            box_lista.add_widget(box_botoes)

    def pop_up_torneio(self, id, tipo):
        conteudo_box = BoxLayout(orientation="vertical")

        lbl_msg = Label(text="Deseja continuar este torneio?")

        botoes_box = BoxLayout(orientation="horizontal", size_hint_y = 0.5)

        sim_button = Button(text="Sim")
        sim_button.on_release = partial(self.ir_para_torneio, id, tipo)

        nao_button = Button(text="Nao")
        nao_button.on_release = self.fechar_pop_up

        botoes_box.add_widget(sim_button)
        botoes_box.add_widget(nao_button)

        conteudo_box.add_widget(lbl_msg)
        conteudo_box.add_widget(botoes_box)

        self.popup = Popup(title="Continuar Torneio", content=conteudo_box, size_hint_x=0.5, size_hint_y=0.5)

        self.popup.open()

    def voltar(self):
        self.clear_widgets()
        janela.root_window.remove_widget(self)
        janela.root_window.add_widget(Inicio())

    def fechar_pop_up(self):
        self.popup.dismiss()

    def ir_para_torneio(self, id, tipo):
        self.fechar_pop_up()
        SetIdTorneio(id)
        tipo_torneio = tipo
        torneio_path = self.getPathTorneio('caminhoTorneioJSON')
        json_torneio = ReadDataJSON(torneio_path)
        if tipo == "Pontos Corridos":
            rodada_atual = len(json_torneio['Rodadas'])
        else:
            rodada_atual = len(json_torneio)

        if tipo_torneio == "Mata-mata":
            janela.root_window.remove_widget(self)
            janela.root_window.add_widget(MataMata(rodada=rodada_atual))
        elif tipo_torneio == "Pontos Corridos":
            janela.root_window.remove_widget(self)
            janela.root_window.add_widget(PontosCorridos(totalRodadas=json_torneio['Numero Rodadas'], rodada=rodada_atual, origem='Continuar Torneio'))

    def getPathTorneio(self, path):
        caminhoPontosCorridos = str(Read(GetIdTorneio(), path)).replace("'","").replace("(","").replace(")","").replace(",","")
        return caminhoPontosCorridos

    def deletarTorneio(self, id, tipo):
        self.fechar_pop_up()
        SetIdTorneio(id)
        caminhoTorneio = self.getPathTorneio('caminhoTorneioJSON')
        DeleteFileJSON(caminhoTorneio)
        if tipo != "Mata-mata":
            caminhoPlacar = self.getPathTorneio('caminhoPlacarJSON')
            DeleteFileJSON(caminhoPlacar)
        caminhoParticipantes = self.getPathTorneio('caminhoParticipantesJSON')
        DeleteFileJSON(caminhoParticipantes)

        Delete(GetIdTorneio())

        janela.root_window.remove_widget(self)
        janela.root_window.add_widget(ContinuarTorneio())

    def deletar_pop_up(self, id, tipo):
        conteudo_box = BoxLayout(orientation="vertical")
        label_msg = Label(text="Deseja deletar este torneio?")

        botoes_box = BoxLayout(orientation="horizontal", size_hint_y=0.5)
        sim_btn = Button(text="Sim")
        sim_btn.on_release = partial(self.deletarTorneio, id, tipo)

        nao_btn = Button(text="Nao")
        nao_btn.on_release = self.fechar_pop_up

        botoes_box.add_widget(sim_btn)
        botoes_box.add_widget(nao_btn)

        conteudo_box.add_widget(label_msg)
        conteudo_box.add_widget(botoes_box)

        self.popup = Popup(title="Deletar torneio", content=conteudo_box, size_hint_x=0.5, size_hint_y=0.5)

        self.popup.open()

class HistoricoTorneio(FloatLayout):

    vencedor_torneio = ""

    def __init__(self, **kwargs):
        super(HistoricoTorneio, self).__init__(**kwargs)
        self.construir_interface()

    def construir_interface(self):
        dict_torneios = ReadAll(True)
        box_lista = self.ids.lista_box

        for i in dict_torneios:
            box_botoes = BoxLayout(orientation="horizontal", size_hint_y=None, height=50)
            tupla_torneio = dict_torneios[i]
            btn_lista = Button(text="Id: " + str(i) + " Tipo torneio: " + tupla_torneio[1], size_hint_x=6)
            btn_lista.on_release = partial(self.pop_up_torneio, i, tupla_torneio[1])

            btn_excluir = Button(text="Excluir")
            btn_excluir.on_release = partial(self.deletar_pop_up, i, tupla_torneio[1])

            box_botoes.add_widget(btn_lista)
            box_botoes.add_widget(btn_excluir)

            box_lista.add_widget(box_botoes)

    def pop_up_torneio(self, id, tipo):
        self.get_vencedor_torneio(id)
        conteudo_box = BoxLayout(orientation="vertical")

        lbl_id = Label(text="ID = {}".format(id))
        lbl_tipo = Label(text="Tipo do Torneio = {}".format(tipo))
        lbl_vencedor = Label(text="Vencedor = {}".format(str(self.vencedor_torneio).replace("(","").replace(")","").replace(",","")))

        botoes_box = BoxLayout(orientation="horizontal", size_hint_y = 0.5)

        nao_button = Button(text="Fechar")
        nao_button.on_release = self.fechar_pop_up

        botoes_box.add_widget(nao_button)

        conteudo_box.add_widget(lbl_id)
        conteudo_box.add_widget(lbl_tipo)
        conteudo_box.add_widget(lbl_vencedor)
        conteudo_box.add_widget(botoes_box)

        self.popup = Popup(title="Histórico Torneio", content=conteudo_box, size_hint_x=0.5, size_hint_y=0.5)

        self.popup.open()

    def voltar(self):
        self.clear_widgets()
        janela.root_window.remove_widget(self)
        janela.root_window.add_widget(Inicio())

    def fechar_pop_up(self):
        self.popup.dismiss()

    def get_vencedor_torneio(self, id):
        self.vencedor_torneio = Read(id, "vencedor")
        return self.vencedor_torneio

    def getPathTorneio(self, path):
        caminhoPontosCorridos = str(Read(GetIdTorneio(), path)).replace("'","").replace("(","").replace(")","").replace(",","")
        return caminhoPontosCorridos

    def deletarTorneio(self, id, tipo):
        self.fechar_pop_up()
        SetIdTorneio(id)
        caminhoTorneio = self.getPathTorneio('caminhoTorneioJSON')
        DeleteFileJSON(caminhoTorneio)
        if tipo != "Mata-mata":
            caminhoPlacar = self.getPathTorneio('caminhoPlacarJSON')
            DeleteFileJSON(caminhoPlacar)
        caminhoParticipantes = self.getPathTorneio('caminhoParticipantesJSON')
        DeleteFileJSON(caminhoParticipantes)

        Delete(GetIdTorneio())

        janela.root_window.remove_widget(self)
        janela.root_window.add_widget(ContinuarTorneio())

    def deletar_pop_up(self, id, tipo):
        conteudo_box = BoxLayout(orientation="vertical")
        label_msg = Label(text="Deseja deletar este torneio?")

        botoes_box = BoxLayout(orientation="horizontal", size_hint_y=0.5)
        sim_btn = Button(text="Sim")
        sim_btn.on_release = partial(self.deletarTorneio, id, tipo)

        nao_btn = Button(text="Nao")
        nao_btn.on_release = self.fechar_pop_up

        botoes_box.add_widget(sim_btn)
        botoes_box.add_widget(nao_btn)

        conteudo_box.add_widget(label_msg)
        conteudo_box.add_widget(botoes_box)

        self.popup = Popup(title="Deletar torneio", content=conteudo_box, size_hint_x=0.5, size_hint_y=0.5)

        self.popup.open()

class DefineTorneio(BoxLayout):
    orientation = "vertical"
    quantParticipantes = ""
    quantRodadas = ""
    quantFinalMataMata = ""
    tipoTorneio = ""
    numeroRodadasExiste = False
    mataMataExiste = False

    labelNmrRodadas = Label(id="labelNmrRodadas", text="Numero de Rodadas")
    txtInputRodadas = TextInput(id="txtInputRodadas")

    labelNmrMataMata = Label(id="labelNmrMataMata", text="Top Mata-Mata")
    txtInputMataMata = TextInput(id="txtInputMataMata")

    def excluirCampos(self, gridTorneio):
        if self.numeroRodadasExiste == True:
            gridTorneio.remove_widget(self.labelNmrRodadas)
            self.txtInputRodadas.text = ""
            gridTorneio.remove_widget(self.txtInputRodadas)

        if self.mataMataExiste == True:
            gridTorneio.remove_widget(self.labelNmrMataMata)
            self.txtInputMataMata.text = ""
            gridTorneio.remove_widget(self.txtInputMataMata)

    def habilitarCampos(self):
        formatoTorneio = self.ids.formatoTorneio.text
        gridTorneio = self.ids.gridTorneio

        self.excluirCampos(gridTorneio)

        if formatoTorneio == "Pontos Corridos" or formatoTorneio == "Misto":
            gridTorneio.add_widget(self.labelNmrRodadas)
            gridTorneio.add_widget(self.txtInputRodadas)
            self.numeroRodadasExiste = True

        if formatoTorneio == "Misto":
            gridTorneio.add_widget(self.labelNmrMataMata)
            gridTorneio.add_widget(self.txtInputMataMata)
            self.mataMataExiste = True

    def voltar(self):
        self.excluirCampos(self.ids.gridTorneio)

        janela.root_window.remove_widget(self)
        janela.root_window.add_widget(Inicio())

    def abrirPopUp(self):
        conteudoBox = BoxLayout(orientation="vertical")

        botoesBox = BoxLayout(orientation="horizontal", size_hint_y=0.5)

        botoesBox.add_widget(Button(text="Sim", on_release=self.irParaNomear))
        botoesBox.add_widget(Button(text="Nao", on_release=self.irParaTorneio))
        botoesBox.add_widget(Button(text="Cancelar", on_release=self.fecharPopUp))

        conteudoBox.add_widget(Label(text="Deseja nomear os jogadores"))
        conteudoBox.add_widget(botoesBox)

        self.conteudoPopUp = Popup(title="Nomear Jogadores", content=conteudoBox, size_hint_y=0.6, size_hint_x=0.6)

        self.conteudoPopUp.open()

    def setQuantParticipantes(self):
        self.quantParticipantes = self.ids.quantParticipantes.text

    def getQuantParticipantes(self):
        return self.quantParticipantes

    def fecharPopUp(self, arg):
        self.conteudoPopUp.dismiss()

    def irParaNomear(self, arg):
        self.setTipoTorneio()
        self.setQuantParticipantes()

        tipoTorneio = self.getTipoTorneio()

        if tipoTorneio == 'Pontos Corridos' or tipoTorneio == 'Misto':
            self.setNmrRodadas()
            if tipoTorneio == 'Misto':
                self.setFinalMataMata()
        janelaTorneio = ""
        prosseguir = False

        if len(self.getQuantParticipantes().split()) != 0 and tipoTorneio != 'Escolha o formato':
            prosseguir = True

            if tipoTorneio == 'Pontos Corridos' or tipoTorneio == 'Misto':
                if len(self.getNmrRodadas().split()) == 0:
                    prosseguir = False

                if tipoTorneio == 'Misto':
                    if len(self.getFinalMataMata().split()) == 0:
                        prosseguir = False


        if prosseguir == True:
            final_mata_mata = 0
            self.criarTorneio()

            self.setNmrRodadas()
            if self.tipoTorneio == "Misto":
                self.setFinalMataMata()
                final_mata_mata = self.getFinalMataMata()
            janela.root_window.remove_widget(self)
            janela.root_window.add_widget(NomearJogadores(totalRodadas=self.getNmrRodadas(), corte_rodada=final_mata_mata))
            self.excluirCampos(self.ids.gridTorneio)
            self.fecharPopUp(arg)

        else:
            self.fecharPopUp(arg)
            self.erro_pop_up()

    def setNmrRodadas(self):
        self.quantRodadas = self.txtInputRodadas.text

    def getNmrRodadas(self):
        return self.quantRodadas

    def setFinalMataMata(self):
        self.quantFinalMataMata = self.txtInputMataMata.text

    def getFinalMataMata(self):
        return self.quantFinalMataMata

    def getTipoTorneio(self):
        return self.tipoTorneio

    def setTipoTorneio(self):
        self.tipoTorneio = self.ids.formatoTorneio.text

    def criarTorneio(self):
        self.setTipoTorneio()
        self.setQuantParticipantes()

        id = CreateID()
        tipoTorneio = self.getTipoTorneio()
        caminhoTorneio = CreateFileJSON(id, tipoTorneio)
        caminhoPlacar = ""
        caminhoParticipantes = CreateFileJSON(id, "Participantes")
        nmrParticipantes = self.getQuantParticipantes()

        if tipoTorneio != "Mata-mata":
            caminhoPlacar = CreateFileJSON(id, "Placar")

        Create(id, tipoTorneio, nmrParticipantes, caminhoTorneio, caminhoParticipantes, caminhoPlacar, False)
        SetIdTorneio(id)

    def setIdJogadores(self):

        caminhoParticipantes = str(Read(GetIdTorneio(), "caminhoParticipantesJSON")).replace("'","").replace("(","").replace(")","").replace(",","")
        nmrParticipantes = self.getQuantParticipantes()
        dictParticipantes = {}

        for i in range(int(nmrParticipantes)):
            dictParticipantes[str(i)] = str(i)

        WriteDataJSON(dictParticipantes, caminhoParticipantes)

    def irParaTorneio(self, arg):
        self.setTipoTorneio()
        self.setQuantParticipantes()
        tipoTorneio = self.getTipoTorneio()

        if tipoTorneio == 'Pontos Corridos' or tipoTorneio == 'Misto':
            self.setNmrRodadas()
            if tipoTorneio == 'Misto':
                self.setFinalMataMata()
        janelaTorneio = ""
        prosseguir = False
        if len(self.getQuantParticipantes()) != 0 and tipoTorneio != "Escolha o formato":
            prosseguir = True
            if tipoTorneio == 'Pontos Corridos' or tipoTorneio == 'Misto':
                if len(self.getNmrRodadas().split()) == 0:
                    prosseguir = False

                if tipoTorneio == 'Misto':
                    if len(self.getFinalMataMata().split()) == 0:
                        prosseguir = False

            if prosseguir == True:
                self.criarTorneio()
                self.setIdJogadores()

                if tipoTorneio == "Mata-mata":
                    janelaTorneio = MataMata(rodada=1)
                elif tipoTorneio == "Misto":
                    janelaTorneio = Misto(totalRodadas=self.getNmrRodadas(), rodada=1, origem="Definir torneio", corte_rodada=self.getFinalMataMata())
                else:
                    janelaTorneio = PontosCorridos(rodada=1, totalRodadas=self.getNmrRodadas(), origem="Definir torneio")

                janela.root_window.remove_widget(self)
                janela.root_window.add_widget(janelaTorneio)
                self.excluirCampos(self.ids.gridTorneio)
                self.fecharPopUp('')
            else:
                self.fecharPopUp('')
                self.erro_pop_up()
        else:
            self.fecharPopUp('')
            self.erro_pop_up()

    def erro_pop_up(self):
        conteudo_box = BoxLayout(orientation="vertical")

        msg_label = Label(text="Preencha os campos corretamente")

        botao_box = BoxLayout(orientation="horizontal", size_hint_y=0.5)
        fechar_botao = Button(text="Fechar", on_release=self.fecharPopUp)

        botao_box.add_widget(fechar_botao)

        conteudo_box.add_widget(msg_label)
        conteudo_box.add_widget(botao_box)

        self.conteudoPopUp = Popup(title="Erro", content=conteudo_box, size_hint_x=0.5, size_hint_y=0.5)
        self.conteudoPopUp.open()

class NomearJogadores(BoxLayout):
    lbl = []
    txt_input = []
    totalRodadas = 0
    corte_rodada = 0
    def __init__(self, **kwargs):
        super().__init__()
        if self.name == 'nomearJogadores':
            self.definirQuantInput()
            self.totalRodadas = kwargs.get('totalRodadas')
            self.corte_rodada = kwargs.get('corte_rodada')
    def voltar(self, arg):
        janela.root_window.remove_widget(self)
        janela.root_window.add_widget(DefineTorneio())

    def definirQuantInput(self):
        quant = str(Read(GetIdTorneio(), 'nmrParticipantes')).replace("(", "").replace(")","").replace(",","")
        '''Função que pega o numero de participantes e transforma a tupla em string '''
        convertedQuant = int(quant)
        self.lbl = []
        self.txt_input = []
        for i in range(convertedQuant):

            box_layout = BoxLayout(id="boxNomeJogador" + str(i), orientation="vertical")
            self.lbl.append(Label(id=str(i), text=str(i)))
            self.txt_input.append(TextInput(id="jgTxt" + str(i)))

            box_layout.add_widget(self.lbl[i])
            box_layout.add_widget(self.txt_input[i])

            self.ids.gridLayout.add_widget(box_layout)
            if (i == convertedQuant - 1):
                box_opcoes = BoxLayout(size_hint_y=0.1)

                btn_voltar = Button(text="Voltar", on_release=self.voltar)
                btn_avancar = Button(text="Avancar", on_press=self.abrirPopUp)

                box_opcoes.add_widget(btn_voltar)
                box_opcoes.add_widget(btn_avancar)

                self.ids.boxPrincipal.add_widget(box_opcoes)

    def setNomeJogadores(self, arg):
        prosseguir = False
        quant = str(Read(GetIdTorneio(), 'nmrParticipantes')).replace("(", "").replace(")", "").replace(",", "")
        '''Funcao que pega o numero de participantes e transforma a tupla em string '''
        convertedQuant = int(quant)
        for i in range(convertedQuant):
            '''split'''
            if len(self.txt_input[i].text.split()) == 0:
                self.fecharPopUp('')
                self.erro_pop_up()
                prosseguir = False
                break
            else:
                prosseguir = True

        if prosseguir == True:
            dictJogadores = {}
            caminhoParticipantes = str(Read(GetIdTorneio(), 'caminhoParticipantesJSON')).replace("'","").replace("(","").replace(")", "").replace(",","")

            for i in range(convertedQuant):
                dictJogadores[self.lbl[i].text] = self.txt_input[i].text

            WriteDataJSON(dictJogadores, caminhoParticipantes)
            self.irParaTorneio()

    def abrirPopUp(self, arg):
        box = BoxLayout(orientation="vertical")
        botoesBox = BoxLayout(orientation="horizontal", size_hint_y=0.5)

        botoesBox.add_widget(Button(text="Sim", on_release=self.setNomeJogadores))
        botoesBox.add_widget(Button(text="Nao", on_release=self.fecharPopUp))

        box.add_widget(Label(text="Sao esses os nomes dos participantes?"))
        box.add_widget(botoesBox)

        self.popup = Popup(title="Finalizar Nomes", content=box, size_hint_y=0.6, size_hint_x=0.6)

        self.popup.open()

    def erro_pop_up(self):
        box = BoxLayout(orientation="vertical")
        botoesBox = BoxLayout(orientation="horizontal", size_hint_y=0.5)

        botoesBox.add_widget(Button(text="Fechar", on_release=self.fecharPopUp))

        box.add_widget(Label(text="Preencha todos os campos corretamente"))
        box.add_widget(botoesBox)

        self.popup = Popup(title="Erro", content=box, size_hint_y=0.6, size_hint_x=0.6)

        self.popup.open()

    def fecharPopUp(self, arg):
        self.popup.dismiss()

    def irParaTorneio(self):
        tipoTorneio = str(Read(GetIdTorneio(), "tipoTorneio")).replace("'", "").replace("(", "").replace(")", "").replace(",", "")
        janelaTorneio = ""
        if tipoTorneio == "Mata-mata":
            janelaTorneio = MataMata(rodada=1)

        elif tipoTorneio == "Pontos Corridos" or tipoTorneio == "Misto":
            if tipoTorneio == "Misto":
                self.setFinalMataMata()
                janelaTorneio = Misto(totalRodadas=self.totalRodadas, rodada=1, origem="Definir torneio", corte_rodada=self.getFinalMataMata())
            else:
                janelaTorneio = PontosCorridos(rodada=1, totalRodadas=self.totalRodadas, origem="Definir torneio")

        self.fecharPopUp('')
        janela.root_window.remove_widget(self)
        janela.root_window.add_widget(janelaTorneio)

class MataMata(BoxLayout):

    rodadaAtual = 0
    vencedor_torneio = ""
    def __init__(self, **kwargs):
        super().__init__()
        if self.name == "mataMata":
            self.rodadaAtual = kwargs.get('rodada')
            if self.rodadaAtual == 1:
                self.setPrimeiraRodada()
            else:
                self.continuar_torneio(self.rodadaAtual)

    def setRodada(self, direcao):
        if direcao == "avancar":
            self.rodadaAtual += 1
        else:
            self.rodadaAtual -= 1

    def setPrimeiraRodada(self):
        caminhoMataMata = self.getTorneioPath()

        rodada = {
            "Rodada 1": {
            }
        }

        listaPlayers = self.getNomeJogadores()
        shuffle(listaPlayers)

        quantChave = int(len(listaPlayers) / 2 + len(listaPlayers) % 2)

        for i in range(quantChave):
            rodada["Rodada 1"]["Chave " + str(i)] = {}

        for i in range(len(rodada["Rodada 1"])):
            for i2 in range(3):
                if listaPlayers != [] and len(listaPlayers) > 1:
                    if i2 < 2:
                        rodada["Rodada 1"]["Chave " + str(i)][str(i2)] = listaPlayers[i2]
                    else:
                        rodada["Rodada 1"]["Chave " + str(i)]["Vencedor"] = ""

                elif len(listaPlayers) == 1:
                    rodada["Rodada 1"]["Chave " + str(i)][str(i2)] = listaPlayers[i2]
                    rodada["Rodada 1"]["Chave " + str(i)]["Vencedor"] = ""
                    break
                else:
                    break

            if listaPlayers != [] and len(listaPlayers) > 1:
                del listaPlayers[0:2]
            else:
                del listaPlayers[0:1]

        WriteDataJSON(rodada, caminhoMataMata)
        if len(rodada["Rodada " + str(self.rodadaAtual)]) == 1:
            self.construirInterface(self.rodadaAtual, True)
        else:
            self.construirInterface(self.rodadaAtual, False)

    def getNomeJogadores(self):
        listaJogadores = []
        caminhoParticipantes = str(Read(GetIdTorneio(), "caminhoParticipantesJSON")).replace("'","").replace("(","").replace(")","").replace(",","")
        dictJogadores = ReadDataJSON(caminhoParticipantes)

        for i in range(len(dictJogadores)):
            listaJogadores.append(dictJogadores[str(i)])

        return listaJogadores

    def construirInterface(self, rodada, final):
        caminhoMataMata = self.getTorneioPath()
        dictChaves = ReadDataJSON(caminhoMataMata)
        listaChaves = []
        valoresSpinner = []
        self.spinnerVencedor = []

        for i in dictChaves["Rodada " + str(rodada)]:
            listaChaves.append(i)

        box_titulo = BoxLayout(orientation="vertical")
        lblRodada = Label(id="lblRodada", text="Rodada " + str(rodada))
        box_titulo.add_widget(lblRodada)
        self.ids.boxMataMata.add_widget(box_titulo)

        for i in range(len(dictChaves["Rodada "+ str(rodada)])):

            box_chave = BoxLayout(orientation="horizontal")
            lblChave = Label(id="chave " + str(i), text=listaChaves[i])
            lblPlayer1 = Label(id="J1", text=str(dictChaves["Rodada " + str(rodada)]["Chave " + str(i)]['0']))
            valoresSpinner.append(str(dictChaves["Rodada " + str(rodada)]["Chave " + str(i)]['0']))

            if len(dictChaves["Rodada " + str(rodada)]["Chave " + str(i)]) > 2:
                lblVersus = Label(id="versus", text=" VS ")
                lblPlayer2 = Label(id="J2", text=str(dictChaves["Rodada " + str(rodada)]["Chave " + str(i)]['1']))
                valoresSpinner.append(str(dictChaves["Rodada " + str(rodada)]["Chave " + str(i)]['1']))

            self.spinnerVencedor.append(Spinner(id="spinnerVencedor", values=valoresSpinner))
            valoresSpinner = []
            box_chave.add_widget(lblChave)
            box_chave.add_widget(lblPlayer1)

            if len(dictChaves["Rodada " + str(rodada)]["Chave " + str(i)]) > 2:
                box_chave.add_widget(lblVersus)
                box_chave.add_widget(lblPlayer2)

            box_chave.add_widget(self.spinnerVencedor[i])

            self.ids.boxMataMata.add_widget(box_chave)

            if i == len(dictChaves["Rodada "+ str(rodada)]) - 1:
                box_botoes = BoxLayout(orientation="horizontal")
                botao_voltar = Button(id="voltar", text="Voltar", on_release=self.abrirPopUpVoltar)
                botao_avancar = Button(id="avancar", on_release=partial(self.abrirPopUpAvancar, rodada, final))

                if final == True:
                    botao_avancar.text = "Finalizar"
                else:
                    botao_avancar.text = "Proxima partida"

                box_botoes.add_widget(botao_voltar)
                box_botoes.add_widget(botao_avancar)

                self.ids.boxMataMata.add_widget(box_botoes)

    def setProximaRodada(self, rodada):
        caminhoMataMata = self.getTorneioPath()
        dictTorneio = ReadDataJSON(caminhoMataMata)
        listVencedores = []

        for i in dictTorneio["Rodada " + str(rodada)]:
            listVencedores.append(dictTorneio["Rodada " + str(rodada)][i]["Vencedor"])

        quantChaves = int(len(listVencedores)/2 + len(listVencedores)%2)

        dictTorneio["Rodada " + str(rodada + 1)] = {}

        for i in range(quantChaves):
            dictTorneio["Rodada " + str(rodada + 1)]["Chave " + str(i)] = {}

        for i in range(len(dictTorneio["Rodada " + str(rodada + 1)])):
            for i2 in range(3):
                if listVencedores != [] and len(listVencedores) > 1:
                    if i2 < 2:
                        dictTorneio["Rodada " + str(rodada + 1)]["Chave " + str(i)][str(i2)] = listVencedores[i2]
                    else:
                        dictTorneio["Rodada " + str(rodada + 1)]["Chave " + str(i)]["Vencedor"] = ""
                elif len(listVencedores) == 1:
                    dictTorneio["Rodada " + str(rodada + 1)]["Chave " + str(i)][str(i2)] = listVencedores[i2]
                    dictTorneio["Rodada " + str(rodada + 1)]["Chave " + str(i)]["Vencedor"] = ""
                    break
                else:
                    break

            if listVencedores != [] and len(listVencedores) > 1:
                del listVencedores[0:2]
            else:
                del listVencedores[0:1]

        WriteDataJSON(dictTorneio, caminhoMataMata)
        self.ids.boxMataMata.clear_widgets()

    def setVencedor(self, rodada):
        caminhoMataMata = self.getTorneioPath()
        dictTorneio = ReadDataJSON(caminhoMataMata)

        for i in range(len(dictTorneio["Rodada " + str(rodada)])):
            dictTorneio["Rodada " + str(rodada)]["Chave " + str(i)]["Vencedor"] = self.spinnerVencedor[i].text

        if len(dictTorneio["Rodada " + str(rodada)]) == 1:
            self.vencedor = self.spinnerVencedor[0].text

        WriteDataJSON(dictTorneio, caminhoMataMata)

    def abrirPopUpAvancar(self, rodada, final, arg):
        box_conteudo = BoxLayout(orientation="vertical")
        lblTexto = Label()
        box_botoes = BoxLayout(orientation="horizontal", size_hint_y=0.5)
        button_nao = Button(id="button_nao", text="Nao", on_release=self.fecharPopUp)
        button_sim = Button(id="button_sim", text="Sim")

        box_botoes.add_widget(button_nao)
        box_botoes.add_widget(button_sim)

        box_conteudo.add_widget(lblTexto)
        box_conteudo.add_widget(box_botoes)

        self.conteudoPopUp = Popup(title="Avancar", content=box_conteudo, size_hint_x=0.5, size_hint_y=0.5)

        if final == False:
            lblTexto.text = "Deseja prosseguir para a proxima partida?"
            self.conteudoPopUp.title = "Prosseguir?"
            button_sim.on_release=partial(self.avancarRodadaFunctions, rodada)

        else:
            lblTexto.text = "Deseja declarar o vencedor?"
            self.conteudoPopUp.title = "Declara vencedor?"
            button_sim.on_release=self.declararVencedorFunctions

        self.conteudoPopUp.open()

    def fecharPopUp(self, arg):
        self.conteudoPopUp.dismiss()

    def abrirPopUpVencedor(self):
        dataJSON = ReadDataJSON(self.getTorneioPath())
        nomeVencedor = dataJSON["Rodada " + str(self.rodadaAtual)]["Chave 0"]["Vencedor"]
        box_vencedor = BoxLayout(orientation="vertical")
        lbl_Vencedor = Label(text="O vencedor e " + str(nomeVencedor))

        box_botoes = BoxLayout(orientation="horizontal", size_hint_y=0.5)
        inicio_button = Button(id="inicio_button", text="Voltar para o Inicio", on_release=self.voltarParaInicio)

        box_botoes.add_widget(inicio_button)

        box_vencedor.add_widget(lbl_Vencedor)
        box_vencedor.add_widget(box_botoes)

        self.conteudoPopUp = Popup(title="Vencedor", content=box_vencedor, size_hint_x=0.5, size_hint_y=0.5)

        self.conteudoPopUp.open()

    def setRodadaAnterior(self, arg):
        if self.rodadaAtual != 1:
            self.ids.boxMataMata.clear_widgets()
            self.setRodada("voltar")
            self.construirInterface(self.rodadaAtual, False)
        else:
            print("Ja esta na primeira rodada")

    def abrirPopUpVoltar(self, arg):
        box_conteudo = BoxLayout(orientation="vertical")
        lbl_texto = Label(text="Qual acao deseja tomar?")
        box_botoes = BoxLayout(orientation="horizontal", size_hint_y=0.5)
        button_torneio = Button(id="voltarInicio", text="Voltar para o inicio", on_release=self.voltarParaInicio)
        button_rodada = Button(id="voltarRodada", text="Voltar Rodada", on_release=self.voltarRodadaPopUp)

        box_botoes.add_widget(button_torneio)
        box_botoes.add_widget(button_rodada)

        box_conteudo.add_widget(lbl_texto)
        box_conteudo.add_widget(box_botoes)

        self.conteudoPopUp = Popup(title="Voltar", content=box_conteudo, size_hint_x=0.5, size_hint_y=0.5)

        self.conteudoPopUp.open()

    def avancarRodadaFunctions(self, rodada):
        prosseguir = False

        for i in self.spinnerVencedor:
            if len(i.text.split()) == 0:
                self.fecharPopUp('')
                self.erro_pop_up()
                prosseguir = False
                break
            else:
                prosseguir = True

        if prosseguir == True:
            self.fecharPopUp('')
            self.setVencedor(rodada)
            self.setProximaRodada(rodada)
            dictTorneio = ReadDataJSON(self.getTorneioPath())
            self.setRodada("avancar")
            if len(dictTorneio["Rodada " + str(self.rodadaAtual)]) == 1:
                self.construirInterface(self.rodadaAtual, True)
            else:
                self.construirInterface(self.rodadaAtual, False)

    def continuar_torneio(self, rodada):
        self.setProximaRodada(rodada)
        dictTorneio = ReadDataJSON(self.getTorneioPath())
        if len(dictTorneio["Rodada " + str(self.rodadaAtual)]) == 1:
            self.construirInterface(self.rodadaAtual, True)
        else:
            self.construirInterface(self.rodadaAtual, False)

    def declararVencedorFunctions(self):
        self.fecharPopUp('')
        self.setVencedor(self.rodadaAtual)
        self.abrirPopUpVencedor()
        Update(True, self.vencedor, GetIdTorneio())

    def getTorneioPath(self):
        caminhoMataMata = str(Read(GetIdTorneio(), "caminhoTorneioJSON")).replace("'", "").replace(")", "").replace("(","").replace(",", "")
        return caminhoMataMata

    def voltarParaInicio(self, arg):
        self.fecharPopUp(arg)
        janela.root_window.remove_widget(self)
        janela.root_window.add_widget(Inicio())

    def voltarRodadaPopUp(self, arg):
        self.setRodadaAnterior('')
        self.fecharPopUp('')

    def erro_pop_up(self):

        conteudo_box = BoxLayout(orientation="vertical")

        lbl_mensagem = Label(text="Preencha os resultados corretamente")

        botao_box = BoxLayout(orientation="horizontal", size_hint_y=0.5)

        fechar_botao = Button(text="Fechar", on_release=self.fecharPopUp)

        botao_box.add_widget(fechar_botao)
        conteudo_box.add_widget(lbl_mensagem)
        conteudo_box.add_widget(botao_box)

        self.conteudoPopUp = Popup(title="Erro", content=conteudo_box, size_hint_x=0.5, size_hint_y=0.5)
        self.conteudoPopUp.open()

class Placar(FloatLayout):

    rodada_atual = 0
    total_rodadas = 0
    origem = ""
    tipo_torneio = ""
    def __init__(self, total_rodadas, rodada_atual, origem, tipo_torneio, **kwargs):
        super(Placar, self).__init__(**kwargs)
        self.origem = origem
        self.rodada_atual = rodada_atual
        self.total_rodadas = int(total_rodadas)
        self.tipo_torneio = tipo_torneio
        self.construirInterface()

    def construirInterface(self):
        caminho_placar = self.getCaminhoPlacar()
        json_placar = ReadDataJSON(caminho_placar)

        quant_rows = len(json_placar)

        cont_posicao = 1

        table_placar = self.ids.table_grid

        table_placar.rows = quant_rows

        dict_pontos = {}

        for i in json_placar:
            jogador = json_placar[i]
            pontos = (jogador["Pontos"] * 4 + jogador["2 X 0"] * 3 + jogador["2 X 1"] * 2 + jogador["1 X 2"])

            if jogador["BYE"] == True:
                pontos -= 1

            dict_pontos[i] = pontos

        list_pontos = sorted(dict_pontos, key=dict_pontos.__getitem__, reverse=True)

        for i in list_pontos:
            posicao_label = Label(text=str(cont_posicao))
            for i2 in json_placar:

                if i == i2:
                    jogador_lbl = Label(text=str(i))
                    vitorias_lbl = Label(text=str(json_placar[i2]["2 X 0"] + json_placar[i2]["2 X 1"]))
                    derrotas_lbl = Label(text=str(json_placar[i2]["0 X 2"] + json_placar[i2]["1 X 2"]))
                    pontos_lbl = Label(text=str(json_placar[i2]["Pontos"]))

                    table_placar.add_widget(posicao_label)
                    table_placar.add_widget(jogador_lbl)
                    table_placar.add_widget(vitorias_lbl)
                    table_placar.add_widget(derrotas_lbl)
                    table_placar.add_widget(pontos_lbl)

            cont_posicao += 1

        '''Botoes box'''

        botoes_box = BoxLayout(orientation="horizontal", size_hint_y=.1)

        button = Button()

        if self.origem == "Meio da partida":
            button.text = "Voltar"
            button.on_release = partial(self.voltarTorneio, 0)
        elif self.origem == "Final da partida":
            print(self.total_rodadas)
            print(self.rodada_atual)
            if self.total_rodadas > self.rodada_atual:

                button.text = "Proxima rodada"
                button.on_release = partial(self.voltarTorneio, 1)
            elif self.total_rodadas == self.rodada_atual:

                button.text = "Finalizar torneio"
                button.on_release = self.declarar_vencedor

        botoes_box.add_widget(button)

        self.ids.conteudo_box.add_widget(botoes_box)

    def voltarTorneio(self, soma):
        janela.root_window.remove_widget(self)
        janela.root_window.add_widget(PontosCorridos(rodada=self.rodada_atual + soma, totalRodadas=self.total_rodadas, origem="Placar"))

    def getCaminhoPlacar(self):
        caminhoPlacar = str(Read(GetIdTorneio(), "caminhoPlacarJSON")).replace("'", "").replace("(", "").replace(")","").replace(",", "")
        return caminhoPlacar

    def declarar_vencedor(self):
        caminho_placar = self.getCaminhoPlacar()
        json_placar = ReadDataJSON(caminho_placar)

        dict_pontos = {}

        for i in json_placar:
            jogador = json_placar[i]

            pontos = jogador["Pontos"] * 4 + jogador["2 X 0"] * 3 + jogador["2 X 1"] * 2 + jogador["1 X 2"]

            if jogador["BYE"] == True:
                pontos -= 1

            dict_pontos[i] = pontos

        lista_pontos = sorted(dict_pontos, key=dict_pontos.__getitem__, reverse=True)

        vencedor = lista_pontos[0]

        '''---------------------------------------------------------------------------------'''

        conteudo_box = BoxLayout(orientation="vertical")

        lbl_vencedor = Label(text="O vencedor e: " + str(vencedor) + " com a pontuacao de " + str(json_placar[vencedor]["Pontos"]) + " pontos.")

        botoes_box = BoxLayout(orientation="horizontal", size_hint_y=0.5)

        fechar_botao = Button(text="Fechar")
        fechar_botao.on_release = self.fechar_pop_up

        inicio_botao = Button(text="Voltar para o inicio")
        inicio_botao.on_release = partial(self.ir_para_inicio, vencedor)

        botoes_box.add_widget(fechar_botao)
        botoes_box.add_widget(inicio_botao)

        conteudo_box.add_widget(lbl_vencedor)
        conteudo_box.add_widget(botoes_box)

        self.popup = Popup(title="Finalizar torneio", content=conteudo_box, size_hint_x=0.5, size_hint_y=0.5)

        self.popup.open()

    def fechar_pop_up(self):

        self.popup.dismiss()

    def ir_para_inicio(self, vencedor):
        self.fechar_pop_up()
        Update(True, vencedor, GetIdTorneio())
        janela.root_window.remove_widget(self)
        janela.root_window.add_widget(Inicio())

    def ir_para_mata_mata(self):
        pass

    def corte_para_mata_mata(self):
        pass

class PontosCorridos(BoxLayout):

    rodada = 0
    totalRodadas = 0

    def __init__(self, **kwargs):
        super().__init__()
        if self.name == "pontosCorridos" or self.name == "misto":
            self.rodada = kwargs.get('rodada')
            self.totalRodadas = kwargs.get('totalRodadas')
            if kwargs.get('origem') == "Definir torneio":
                self.setEstruturaTorneio()
                self.createConfrontos()
                self.createPlacar()
            self.setRodada()
            self.construirInterface()

    def setNumeroRodada(self, acaoRodada):
        if acaoRodada == "avancar":
            self.rodada += 1
        else:
            self.rodada -= 1

    def setRodada(self):
        caminhoTorneio = self.getPathTorneio()
        caminhoPlacar = self.getPathPlacar()
        jsonTorneio = ReadDataJSON(caminhoTorneio)
        jsonPlacar = ReadDataJSON(caminhoPlacar)
        dictRodada = jsonTorneio["Rodadas"]
        dictConfrontos = jsonTorneio["Confrontos"]
        listParticipantes = []
        participanteBye = ""

        if self.rodada == 1:
            listParticipantes = self.getNomeParticipantes()
            shuffle(listParticipantes)
        else:
            dictPontos = {}
            for item in jsonPlacar:
                pontos = int(jsonPlacar[item]["Pontos"] * 4) + (int(jsonPlacar[item]["2 X 0"]) * 3) + (int(jsonPlacar[item]["2 X 1"]) * 2) + int(jsonPlacar[item]["1 X 2"])

                if jsonPlacar[item]["BYE"] == True:
                    pontos -= 1

                dictPontos[item] = pontos

            listPontos = sorted(dictPontos, key=dictPontos.__getitem__, reverse=True)
            imparParticipantes = int(len(listPontos)%2)

            print(jsonPlacar)
            print(listPontos)

            if imparParticipantes == 1:
                for i in reversed(listPontos):
                    if jsonPlacar[i]["BYE"] == False:
                        participanteBye = i
                        listPontos.remove(i)
                        break

            for item in listPontos:
                for item2 in listPontos:

                    if item != item2:
                        rodada = str(item) + " X " + str(item2)
                        rodada_reversa = str(item2) + " X " + str(item)

                        for confronto in dictConfrontos:
                                statusConfronto = dictConfrontos[confronto]

                                if rodada_reversa == confronto or rodada == confronto:
                                    if statusConfronto == False:
                                        if item not in listParticipantes and item2 not in listParticipantes:
                                            listParticipantes.append(item)
                                            listParticipantes.append(item2)

            if imparParticipantes == 1:
                listParticipantes.append(participanteBye)
                print(listParticipantes)
        quantChaves = int(len(listParticipantes)/2 + len(listParticipantes)%2)

        dictRodada["Rodada " + str(self.rodada)] = {}

        for i in range(quantChaves):
            dictRodada["Rodada "+ str(self.rodada)]["Chave " + str(i)] = {}

        for i in dictRodada["Rodada " + str(self.rodada)]:
            for i2 in range(6):
                if listParticipantes != [] and len(listParticipantes) > 1:
                    if i2 < 2:
                        dictRodada["Rodada " + str(self.rodada)][i][i2] = listParticipantes[i2]
                    elif i2 == 2:
                        dictRodada["Rodada " + str(self.rodada)][i]["Vencedor"] = ""
                    elif i2 == 3:
                        dictRodada["Rodada " + str(self.rodada)][i]["Tipo Vitoria"] = ""
                    elif i2 == 4:
                        dictRodada["Rodada " + str(self.rodada)][i]["Perdedor"] = ""
                    elif i2 == 5:
                        dictRodada["Rodada " + str(self.rodada)][i]["Tipo Derrota"] = ""
                elif len(listParticipantes) == 1:
                    dictRodada["Rodada " + str(self.rodada)][i][i2] = listParticipantes[i2]
                    dictRodada["Rodada " + str(self.rodada)][i]["Vencedor"] = ""
                    dictRodada["Rodada " + str(self.rodada)][i]["Tipo Vitoria"] = ""
                    break
                else:
                    break

            del listParticipantes[0:2]
        WriteDataJSON(jsonTorneio, caminhoTorneio)

    def setVencedor(self):

        caminhoTorneio = self.getPathTorneio()
        jsonTorneio = ReadDataJSON(caminhoTorneio)
        dictRodadas = jsonTorneio["Rodadas"]


        for i in range(len(dictRodadas["Rodada " + str(self.rodada)])):
            chave = dictRodadas["Rodada " + str(self.rodada)]["Chave " + str(i)]
            if self.txtListP1[i].text != "BYE":
                if int(self.txtListP1[i].text) > int(self.txtListP2[i].text):
                    chave["Vencedor"] = chave['0']
                    chave["Tipo Vitoria"] = self.txtListP1[i].text + " X " + self.txtListP2[i].text
                    chave["Perdedor"] = chave['1']
                    chave["Tipo Derrota"] = self.txtListP2[i].text + " X " + self.txtListP1[i].text
                else:
                    chave["Vencedor"] = chave['1']
                    chave["Tipo Vitoria"] = self.txtListP2[i].text + " X " + self.txtListP1[i].text
                    chave["Perdedor"] = chave['0']
                    chave["Tipo Derrota"] = self.txtListP1[i].text + " X " + self.txtListP2[i].text
            else:
                chave["Vencedor"] = chave['0']
                chave["Tipo Vitoria"] = "BYE"

        WriteDataJSON(jsonTorneio, caminhoTorneio)

    def createPlacar(self):
        caminhoPlacar = self.getPathPlacar()
        listParticipantes = self.getNomeParticipantes()
        jsonPlacar = {}

        for i in listParticipantes:
            jsonPlacar[str(i)] = {"Pontos": 0, "BYE": False}

        for i in jsonPlacar:
            for i1 in range(3):
                for i2 in range(3):
                    if i1 != i2:
                        if i1 != 1 or i2 != 0:
                            if i1 != 0 or i2 != 1:
                                jsonPlacar[i][str(i1) + " X " + str(i2)] = 0

        WriteDataJSON(jsonPlacar, caminhoPlacar)

    def updatePlacar(self, avancar):
        caminhoPlacar = self.getPathPlacar()
        caminhoTorneio = self.getPathTorneio()

        jsonPlacar = ReadDataJSON(caminhoPlacar)

        jsonTorneio = ReadDataJSON(caminhoTorneio)
        dictRodadas = jsonTorneio["Rodadas"]
        rodada = dictRodadas["Rodada " + str(self.rodada)]

        if avancar == True:
            for chave in rodada:
                if rodada[chave]["Tipo Vitoria"] == "BYE":
                    for participante in jsonPlacar:
                        if rodada[chave]["Vencedor"] == participante:
                            jsonPlacar[participante]["Pontos"] += 3
                            jsonPlacar[participante]["BYE"] = True
                            jsonPlacar[participante]["2 X 0"] += 1
                else:
                    for participante in jsonPlacar:
                        if rodada[chave]["Vencedor"] == participante:
                            jsonPlacar[participante]["Pontos"] += 3
                            jsonPlacar[participante][rodada[chave]["Tipo Vitoria"]] += 1

                        if rodada[chave]["Perdedor"] == participante:
                            jsonPlacar[participante][rodada[chave]["Tipo Derrota"]] += 1
        else:
            rodada = dictRodadas["Rodada " + str(self.rodada - 1)]
            for chave in rodada:
                if rodada[chave]["Tipo Vitoria"] == "BYE":
                    for participante in jsonPlacar:
                        if rodada[chave]["Vencedor"] == participante:
                            jsonPlacar[participante]["Pontos"] -= 3
                            jsonPlacar[participante]["BYE"] = False
                            jsonPlacar[participante]["2 X 0"] -= 1
                else:
                    for participante in jsonPlacar:
                        if rodada[chave]["Vencedor"] == participante:
                            jsonPlacar[participante]["Pontos"] -= 3
                            jsonPlacar[participante][rodada[chave]["Tipo Vitoria"]] -= 1

                        if rodada[chave]["Perdedor"] == participante:
                            jsonPlacar[participante][rodada[chave]["Tipo Derrota"]] -= 1

        WriteDataJSON(jsonPlacar, caminhoPlacar)

    def updateConfrontos(self, avancar):
        caminhoTorneio = self.getPathTorneio()
        jsonTorneio = ReadDataJSON(caminhoTorneio)
        dictConfrontos = jsonTorneio["Confrontos"]
        dictRodadas = jsonTorneio["Rodadas"]

        rodada = dictRodadas["Rodada " + str(self.rodada)]
        for chave in rodada:
            for confronto in dictConfrontos:
                if avancar == True:
                    if rodada[chave]["Tipo Vitoria"] != "BYE":
                        if str(rodada[chave]['0'] + " X " + rodada[chave]['1']) == str(confronto) or str(rodada[chave]['1'] + " X " + rodada[chave]['0']) == str(confronto):
                            dictConfrontos[confronto] = True
                else:
                    if rodada[chave]["Tipo Vitoria"] != "BYE":
                        if str(rodada[chave]['0'] + " X " + rodada[chave]['1']) == str(confronto) or str(rodada[chave]['1'] + " X " + rodada[chave]['0']) == str(confronto):
                            dictConfrontos[confronto] = False

        WriteDataJSON(jsonTorneio, caminhoTorneio)

    def getNomeParticipantes(self):
        caminhoParticipantes = str(Read(GetIdTorneio(), "caminhoParticipantesJSON")).replace("(","").replace(")","").replace(",","").replace("'","")
        listParticipantes = []
        dictParticipantes = ReadDataJSON(caminhoParticipantes)

        for i in dictParticipantes:
            listParticipantes.append(dictParticipantes[i])

        return listParticipantes

    def setEstruturaTorneio(self):

        torneioJSON = {
            "Numero Rodadas": self.totalRodadas,
            "Confrontos": {},
            "Rodadas": {}
        }

        WriteDataJSON(torneioJSON, self.getPathTorneio())

    def getPathTorneio(self):
        caminhoPontosCorridos = str(Read(GetIdTorneio(), "caminhoTorneioJSON")).replace("'","").replace("(","").replace(")","").replace(",","")
        return caminhoPontosCorridos

    def getPathPlacar(self):
        caminhoPlacar = str(Read(GetIdTorneio(), "caminhoPlacarJSON")).replace("'","").replace("(","").replace(")","").replace(",","")
        return caminhoPlacar

    def construirInterface(self):
        caminhoTorneio = self.getPathTorneio()
        dadosTorneio = ReadDataJSON(caminhoTorneio)
        dictRodada = dadosTorneio["Rodadas"]
        valores_spinner = ["2", "1", "0"]
        self.txtListP1 = []
        self.txtListP2 = []

        boxTorneio = self.ids.boxPontosCorridos
        labelRodada = Label(text="Rodada " + str(self.rodada))

        boxTorneio.add_widget(labelRodada)

        for i in range(len(dictRodada["Rodada " + str(self.rodada)])):
            boxChave = BoxLayout(id="boxChave", orientation="horizontal")
            labelP1 = Label(text=str(dictRodada["Rodada " + str(self.rodada)]['Chave ' + str(i)]['0']))
            spinner1 = Spinner(values=valores_spinner)
            spinner2 = Spinner(values=valores_spinner)
            boxChave.add_widget(labelP1)

            if len(dictRodada["Rodada " + str(self.rodada)]["Chave " +str(i)]) > 3:
                self.txtListP1.append(spinner1)
                labelVS = Label(text=" X ")
                self.txtListP2.append(spinner2)
                labelP2 = Label(text=str(dictRodada["Rodada " + str(self.rodada)]['Chave ' + str(i)]['1']))

                boxChave.add_widget(self.txtListP1[i])
                boxChave.add_widget(labelVS)
                boxChave.add_widget(self.txtListP2[i])
                boxChave.add_widget(labelP2)

            else:
                self.txtListP1.append(TextInput(text="BYE", readonly=True))

                boxChave.add_widget(self.txtListP1[i])

            boxTorneio.add_widget(boxChave)

            if i == len(dictRodada["Rodada " + str(self.rodada)]) - 1:
                boxBotoes = BoxLayout(orientation="horizontal", size_hint_y=0.5)
                voltarBtn = Button(text="Voltar")
                voltarBtn.on_release = self.voltar_pop_up
                placarBtn = Button(text="Placar")
                placarBtn.on_release = self.placar_pop_up

                rodadaBtn = Button()

                if self.rodada != int(self.totalRodadas):
                    rodadaBtn.text = "Proxima rodada"
                    rodadaBtn.on_release = self.avancar_pop_up
                elif self.rodada == int(self.totalRodadas):
                    rodadaBtn.text = "Finalizar"
                    rodadaBtn.on_release = self.finalizar_pop_up

                boxBotoes.add_widget(voltarBtn)
                boxBotoes.add_widget(placarBtn)
                boxBotoes.add_widget(rodadaBtn)

                boxTorneio.add_widget(boxBotoes)

    def createConfrontos(self):
        caminhoTorneio = self.getPathTorneio()
        dadosTorneio = ReadDataJSON(caminhoTorneio)
        listParticipantes = self.getNomeParticipantes()
        dictConfrontos = dadosTorneio["Confrontos"]
        listConfrontos = []

        for i in listParticipantes:
            for i2 in listParticipantes:
                if i != i2:
                    listConfrontos.append(str(i) + " X " + str(i2))

        for i in listConfrontos:
            confronto = str(i).split(" X ")
            for i2 in listConfrontos:
                confrontoReverso = str(i2).split(" X ")
                confrontoReverso.reverse()

                if confronto == confrontoReverso:
                    listConfrontos.remove(i2)

        for i in listConfrontos:
            dictConfrontos[i] = False

        WriteDataJSON(dadosTorneio, caminhoTorneio)

        return dictConfrontos

    def fechar_pop_up(self):
        self.popup.dismiss()

    def voltar_pop_up(self):
        conteudo_box = BoxLayout(orientation="vertical")
        lbl_mensagem = Label(text="Deseja voltar para o inicio ou para a rodada anterior")

        botoes_box = BoxLayout(orientation="horizontal", size_hint_y=0.5)
        nao_btn = Button(text="Nao")
        nao_btn.on_release = self.fechar_pop_up

        rodada_btn = Button(text="Rodada")
        rodada_btn.on_release = self.voltar_rodada

        inicio_btn = Button(text="Inicio")
        inicio_btn.on_release = self.voltar_inicio

        botoes_box.add_widget(nao_btn)
        botoes_box.add_widget(rodada_btn)
        botoes_box.add_widget(inicio_btn)

        conteudo_box.add_widget(lbl_mensagem)
        conteudo_box.add_widget(botoes_box)

        self.popup = Popup(title="Voltar", content=conteudo_box, size_hint_x=0.5, size_hint_y=0.5)
        self.popup.open()

    def voltar_inicio(self):
        self.fechar_pop_up()
        janela.root_window.remove_widget(self)
        janela.root_window.add_widget(Inicio())

    def voltar_rodada(self):
        if self.rodada > 1:
            self.updatePlacar(False)
            self.updateConfrontos(False)
            self.setNumeroRodada("voltar")
            self.ids.boxPontosCorridos.clear_widgets()
            self.construirInterface()
        else:
            print("Ja esta na primeira rodada")

        self.fechar_pop_up()

    def placar_pop_up(self):
        conteudo_box = BoxLayout(orientation="vertical")
        lbl_mensagem = Label(text="Deseja ver o placar?")

        botoes_box = BoxLayout(orientation="horizontal", size_hint_y=0.5)

        nao_btn = Button(text="Nao")
        nao_btn.on_release = self.fechar_pop_up

        sim_btn = Button(text="Sim")
        sim_btn.on_release = partial(self.ir_para_placar, "Meio da partida")

        botoes_box.add_widget(nao_btn)
        botoes_box.add_widget(sim_btn)

        conteudo_box.add_widget(lbl_mensagem)
        conteudo_box.add_widget(botoes_box)

        self.popup = Popup(title="Placar", content=conteudo_box, size_hint_x=0.5, size_hint_y=0.5)
        self.popup.open()

    def ir_para_placar(self, origem):
        self.fechar_pop_up()
        janela.root_window.remove_widget(self)
        janela.root_window.add_widget(Placar(self.totalRodadas, self.rodada, origem, "Pontos Corridos"))

    def avancar_pop_up(self):
        conteudo_box = BoxLayout(orientation="vertical")
        lbl_mensagem = Label(text="Deseja Avancar para a proxima rodada ?")

        botoes_box = BoxLayout(orientation="horizontal", size_hint_y = 0.5)

        nao_btn = Button(text="Nao")
        nao_btn.on_release = self.fechar_pop_up

        placar_btn = Button(text="Ver placar")
        placar_btn.on_release = self.avancar_placar

        sim_btn = Button(text="Proxima rodada")
        sim_btn.on_release = self.avancar

        botoes_box.add_widget(nao_btn)
        botoes_box.add_widget(placar_btn)
        botoes_box.add_widget(sim_btn)

        conteudo_box.add_widget(lbl_mensagem)
        conteudo_box.add_widget(botoes_box)

        self.popup = Popup(title="Avancar", content=conteudo_box, size_hint_x = 0.5, size_hint_y = 0.5)
        self.popup.open()

    def filtrar_resultado(self):
        prosseguir = False

        for i in self.txtListP1:

            if len(i.text.split()) == 0:
                prosseguir = False
                break
            else:
                prosseguir = True

        for i in self.txtListP2:

            if len(i.text.split()) == 0:
                prosseguir = False
                break
            else:
                prosseguir = True

        if prosseguir == True:
            for i in range(len(self.txtListP1)):
                if prosseguir == True:
                    for i2 in range(len(self.txtListP2)):
                        if i == i2:
                            if self.txtListP1[i].text == self.txtListP2[i2].text:
                                prosseguir = False

                            elif (self.txtListP1[i].text < '2' and self.txtListP2[i2].text <= self.txtListP1[i].text) or (self.txtListP2[i2].text < '2' and self.txtListP1[i].text <= self.txtListP2[i2].text):
                                prosseguir = False

                            elif (self.txtListP1[i].text == '2' and self.txtListP2[i2].text < self.txtListP1[i].text) or (self.txtListP2[i2].text == '2' and self.txtListP1[i].text < self.txtListP2[i2].text):
                                prosseguir = True

                            break
                else:
                    break

        return prosseguir

    def avancar(self):
        prosseguir = self.filtrar_resultado()
        print(prosseguir)
        if prosseguir == True:
            self.setVencedor()
            self.updatePlacar(True)
            self.updateConfrontos(True)
            self.setNumeroRodada("avancar")
            self.setRodada()
            self.ids.boxPontosCorridos.clear_widgets()
            self.construirInterface()
            self.fechar_pop_up()
        else:
            self.fechar_pop_up()
            self.erro_pop_up()

    def avancar_placar(self):
        prosseguir = self.filtrar_resultado()

        if prosseguir == True:
            self.setVencedor()
            self.updatePlacar(True)
            self.updateConfrontos(True)
            self.ir_para_placar("Final da partida")
        else:
            self.fechar_pop_up()
            self.erro_pop_up()

    def finalizar(self):
        prosseguir = self.filtrar_resultado()

        if prosseguir == True:
            self.setVencedor()
            self.updatePlacar(True)
            self.ir_para_placar("Final da partida")
        else:
            self.fechar_pop_up()
            self.erro_pop_up()

    def finalizar_pop_up(self):
        conteudo_box = BoxLayout(orientation="vertical")
        lbl_mensagem = Label(text="Deseja finalizar o torneio?")

        opcoes_box = BoxLayout(orientation="horizontal", size_hint_y=0.5)
        opcao_sim = Button(text="Sim")
        opcao_sim.on_release = self.finalizar

        opcao_nao = Button(text="Nao")
        opcao_nao.on_release = self.fechar_pop_up

        opcoes_box.add_widget(opcao_nao)
        opcoes_box.add_widget(opcao_sim)

        conteudo_box.add_widget(lbl_mensagem)
        conteudo_box.add_widget(opcoes_box)

        self.popup = Popup(title="Finalizar", content=conteudo_box, size_hint_x=0.5, size_hint_y=0.5)
        self.popup.open()

    def erro_pop_up(self):
        conteudo_box = BoxLayout(orientation="vertical")

        lbl_mensagem = Label(text="Preencha os campos corretamente")

        botao_box = BoxLayout(orientation="horizontal", size_hint_y=0.5)

        fechar_botao = Button(text="Fechar")
        fechar_botao.on_release = self.fechar_pop_up

        botao_box.add_widget(fechar_botao)
        conteudo_box.add_widget(lbl_mensagem)
        conteudo_box.add_widget(botao_box)

        self.popup = Popup(title="Erro", content=conteudo_box, size_hint_x=0.5, size_hint_y=0.5)

        self.popup.open()

class Misto(PontosCorridos):
    corte_rodada = 0
    totalRodadas = 0
    rodada = 0
    origem = ""
    def __init__(self, **kwargs):
        self.corte_rodada = kwargs.get('corte_rodada')
        self.totalRodadas = kwargs.get('totalRodadas')
        self.rodada = kwargs.get('rodada')
        self.origem = kwargs.get('origem')
        PontosCorridos.__init__(self, rodada=self.rodada, totalRodadas=self.totalRodadas, origem=self.origem)


'''------------------------------------Funções SQL--------------------------------'''

def Connect():
    con = sqlite3.connect("torneio.db")
    print('conectado')
    return con

def Create(id, tipoTorneio, nmrParticipantes, caminhoTorneioJSON, caminhoParticipantesJSON, caminhoPlacarJSON, finalizado):
    con = Connect()
    cursor = con.cursor()

    cursor.execute('''
    INSERT INTO dadosTorneio(id, tipoTorneio, nmrParticipantes, caminhoTorneioJSON, caminhoParticipantesJSON, caminhoPlacarJSON, finalizado) 
    values (?,?,?,?,?,?,?)
    ''', (id, tipoTorneio, nmrParticipantes, caminhoTorneioJSON, caminhoParticipantesJSON, caminhoPlacarJSON, finalizado))

    con.commit()
    print("dados inseridos")
    con.close()

def Update(finalizado, vencedor, id):
    con = Connect()
    cursor = con.cursor()

    cursor.execute('''
    UPDATE dadosTorneio SET finalizado = ?, vencedor = ? WHERE id = ?''', (finalizado, vencedor, id))

    con.commit()

    print('Dados atualizados')

    con.close()

def Read(id, *args):
    listaArgumentos = []
    tuplaDados = ""
    for i in args:
        listaArgumentos.append(i)

    strArgumentos = str(listaArgumentos).replace("[","").replace("]","").replace("'","")

    con = Connect()
    cursor = con.cursor()

    cursor.execute("SELECT "+strArgumentos+" FROM dadosTorneio WHERE id = ?", (id,))

    for linha in cursor.fetchall():
        tuplaDados = linha

    con.close()

    return tuplaDados

def ReadAll(finalizado):
    dict_dados = {}
    con = Connect()
    cursor = con.cursor()

    cursor.execute("SELECT * FROM dadosTorneio WHERE finalizado = ?", (finalizado,))

    for l in cursor.fetchall():
        dict_dados[l[0]] = l

    con.close()

    return dict_dados

def CreateID():
    id = "(0,)"
    con = Connect()
    cursor = con.cursor()

    cursor.execute('''
    SELECT id FROM dadosTorneio''')


    for linha in cursor.fetchall():
        id = str(linha)

    con.close()
    localizarNmrId = id[1:]
    replaceNmrId = localizarNmrId.replace(",", "").replace(")","")

    return int(replaceNmrId) + 1

def Delete(id):
    con = Connect()
    cursor = con.cursor()

    cursor.execute('''
    DELETE FROM dadosTorneio WHERE id = ?''', (id,))

    con.commit()

    print('Dados excluidos com sucesso')

    con.close()

'''--------------------------------Funções para lidar com ID-----------------------'''
idTorneio = ""
def SetIdTorneio(id):
    global idTorneio
    idTorneio = id

def GetIdTorneio():
    return idTorneio

'''-----------------------------------Funções JSON--------------------------------'''


def WriteDataJSON(data, caminhoJSON):

    with open(caminhoJSON, "w") as json_data:
        json.dump(data, json_data)

    print(ReadDataJSON(caminhoJSON))
    print("Dados escritos")

def ReadDataJSON(caminhoJson):
    with open(caminhoJson, "r") as json_data:
        data = json.load(json_data)

    print("Dados Carregados")
    return data

def CreateFileJSON(id, arquivo):
    path = "arquivosJSON/" + str(id) + arquivo + ".json"
    try:
        file = open(path, "x")
        file.write("[]")

        print("Arquivo criado")

        return path
    except:

        print("Arquivo ja existe")

        return path

def ReadFileJSON(caminho):
    file = open(caminho, "r")
    print(file.read())

def DeleteFileJSON(caminho):
    os.remove(caminho)

'''------------------------------------------Checar integridade dos arquivos e pastas-----------------------------------'''

def CheckDatabase():
    conexao = Connect()
    cursor = conexao.cursor()
    tabela = 'dadosTorneio'

    cursor.execute('PRAGMA table_info({})'.format(tabela))

    coluna = [tupla[1] for tupla in cursor.fetchall()]

    if len(coluna) == 0:
        cursor.execute('''CREATE TABLE dadosTorneio (id INTEGER NOT NULL PRIMARY KEY,
         tipoTorneio TEXT, 
         nmrParticipantes INTEGER,
         caminhoTorneioJSON TEXT,
         caminhoParticipantesJSON TEXT,
         caminhoPlacarJSON TEXT,
         finalizado BOOLEAN, 
         vencedor TEXT);''')
        print('Tabela criada')
    else:
        print('Dados Carregados')

    conexao.close()

def CheckDirectories():
    directory = 'arquivosJSON'

    try:
        dir = os.listdir(directory)
        print('Diretorio carregado')
    except:
        dir = os.mkdir(directory)
        print('Diretorio criado')

'''---------------------------------------------------------------------------------------------------------------------'''
janela = TorneioYGO()
janela.run()
