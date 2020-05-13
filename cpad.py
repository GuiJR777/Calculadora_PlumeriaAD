
# Esse app foi desenvoldo com o objetivo de facilitar as operações financeiras da Plumeria Arte e Design

# IMPORTÇÕES

import PySimpleGUI as sg
import os

#constantes 
TP_PAGAMENTO_DINHEIRO = 1
TP_PAGAMENTO_BOLETO = 2
TP_PAGAMENTO_DEBITO = 3
TP_PAGAMENTO_ELO7 = 4
TP_PAGAMENTO_POINT_AV = 5
TP_PAGAMENTO_POINT_PC = 6
TP_PAGAMENTO_MPAGO = 7
TP_PAGAMENTO_INVALIDO = -1

# TELA CONVITES


def retornar_diretorio_atual(pdiretorio_raiz):
    return os.path.dirname(os.path.realpath(pdiretorio_raiz))

def retornar_imagem(pNome, pWidth, pHeight):
    return sg.Image('%s\data\%s' % (retornar_diretorio_atual(__file__), pNome), size=(pWidth, pHeight))

def retornar_titulo():
    return sg.Text('Calculadora Plumeria Arte e Design', font=50, text_color='Black')

def retornar_label(pTexto, pKey):
    return [sg.Text(pTexto, size=(19, 0)), sg.Input(size=(15, 0), key=pKey, background_color='White', text_color='Black', do_not_clear=False)]

def retornar_aliquota_juros(pTipoPagamento):
    print(pTipoPagamento)
    ALIQUOTA_DINHEIRO = 0
    ALIQUOTA_MPAGO = 0.0499
    ALIQUOTA_BOLETO = 0.0349
    ALIQUOTA_POINT_AV = 0.0379
    ALIQUOTA_POINT_PC = 0.0436
    ALIQUOTA_DEBITO = 0.0199
    ALIQUOTA_TAXA_ELO7 = 0.12
    
    switcher = {
        TP_PAGAMENTO_DINHEIRO: ALIQUOTA_DINHEIRO,
        TP_PAGAMENTO_BOLETO: ALIQUOTA_BOLETO,
        TP_PAGAMENTO_DEBITO: ALIQUOTA_DEBITO,
        TP_PAGAMENTO_ELO7: ALIQUOTA_TAXA_ELO7,
        TP_PAGAMENTO_POINT_AV: ALIQUOTA_POINT_AV,
        TP_PAGAMENTO_POINT_PC: ALIQUOTA_POINT_PC,
        TP_PAGAMENTO_MPAGO: ALIQUOTA_MPAGO
    }
    return (switcher.get(pTipoPagamento, TP_PAGAMENTO_INVALIDO))

sg.theme('LightBrown9')  # Tema de Cores

img = [[retornar_imagem('logo250x250.png', 250,250)]] 
calculadora = [[retornar_titulo()],
                retornar_label('Número de Convites:', 'conv'),
                retornar_label('Valor da Impressão:', 'imp'),
                retornar_label('Valor do Envelope:', 'env'),
                retornar_label('Metros/Pacote:', 'tip'),
                retornar_label('Valor de Cada Pacote(laço/enfeite):', 'enf'),
                retornar_label('Valor da caixa de envio:', 'box'),
             [sg.Button('Calcular')]
             
             ]  # Fim da Calculadora

layout1 = [  [sg.Column(calculadora, size=(280, 280)), sg.Column(img, size=(250, 250))],
             [sg.Text('', font=30, size=(60, 10), text_color='Black', background_color='White', key='Resposta')]
                                   ]  # Fim do layout1

img2 = [[retornar_imagem('logo250x250.png', 250,250)]]

r_keys = ['1', '2', '3', '4', '5', '6', '7']  # Essa lista serve para identificar o Radio selecionado

telataxas = [[retornar_titulo()],
            retornar_label('Entre com o valor total do serviço', 'totalservico'),
            retornar_label('Entre com o valor total de gastos', 'totalgasto'),
            [sg.Text('Como o cliente pagou?', size=(19, 0))],
            [sg.Radio('Dinheiro', "metodo", default=True, key=r_keys[0]), 
             sg.Radio('Boleto', "metodo", key=r_keys[1]), 
             sg.Radio('Débito', "metodo", key=r_keys[2]), 
             sg.Radio('Elo7', "metodo", key=r_keys[3])],
            
            [sg.Radio('Cartão à vista', "metodo", key=r_keys[4]), 
             sg.Radio('Cartão Parcelado', "metodo", key=r_keys[5])],
            [sg.Radio('MercadoPago(parcelado)', "metodo", key=r_keys[6])],
            retornar_label('Entre com o valor do Envio', 'totalenvio'),
            [sg.Button('OK')]
            
           ]  # Fim da telataxas

layout2 = [[sg.Column(telataxas, size=(280, 280)), sg.Column(img2, size=(250, 250))],
           [sg.Text('', font=30, size=(60, 10), text_color='Black', background_color='White', key='Resposta2')]]

layout = [[sg.TabGroup([[sg.Tab('Convites', layout1), 
                         sg.Tab('Taxas', layout2,)]])],
         [sg.Button('Cancelar')]] 

# JANELA
window = sg.Window('Cpad', layout, icon=(retornar_diretorio_atual(__file__)+'\data\Grey Circle Leaves Floral Logo (26) (1).ico'))


# Loop de eventos para processar "eventos" e obter os "valores" das entradas
while True:
    event, values = window.read()
    if event in (None, 'Cancelar'):   
        break
    
# operações tela Convites
    
    if event in ('Calcular'):
        try:
            Qconvites = int(values['conv'])
            vimp = float(values['imp'].replace(",", "."))
            venv = float(values['env'].replace(",", "."))
            vpenf = float(values['enf'].replace(",", "."))
            vcaixa = float(values['box'].replace(",", "."))
            tipo = int(values['tip'])
      
            impressao = Qconvites * vimp
            envelope = Qconvites * venv
            Qunid = 70
            Tamanho_total = Qconvites * Qunid
            QuantidadeDePacotes = Tamanho_total / (tipo * 100)
            ValorTotalEnfeite = QuantidadeDePacotes * vpenf

            custototal = impressao + envelope + vcaixa + ValorTotalEnfeite
            lucro = custototal * 1.2
            valorvenda = custototal + lucro
            valorunid = valorvenda / Qconvites
            
            window['Resposta'](
                'Você deverá cobrar: R$ %s por unidade.\n\n'\
                'Compre %s pacotes de %s metros.\n\n'\
                'Você gastará um total de: R$ %s para confeccionar %s convites.\n\n'\
                'O cliente pagará um total de: R$ %s pela encomenda.' % (
                str(round(valorunid, 3)), 
                str(QuantidadeDePacotes), 
                str(tipo), 
                str(round(custototal, 2)), 
                str(Qconvites), 
                str(round(valorvenda, 2))))
            window.refresh()

        except:    
            sg.popup('Preencha todos os campos com numeros')
            
# Operações tela Taxas
    if event in ('OK'):
        try:
            ValorPago = float(values['totalservico'].replace(",", "."))
            Gasto = float(values['totalgasto'].replace(",", "."))
            TaxaEnvio = float(values['totalenvio'].replace(",", "."))
            tipo_pagamento = int([ key for key in r_keys if values[key]][0])  # Essa variavel recebe o valor da key do Radio
            print(values)
            
            aliquota_juros = retornar_aliquota_juros(tipo_pagamento)
            Valor_Receber = ValorPago - aliquota_juros
            LucroReal = Valor_Receber - Gasto - TaxaEnvio
            RESPOSTA_MERCADO_PAGO = 'Você Receberá R$ %s na sua conta.\n\nSeu lucro será de R$: %s já com taxas descontadas.'
            RESPOSTA_PADRAO = 'Você Receberá R$ %s\n\nSeu lucro será de R$ %s'
            
            resposta = RESPOSTA_PADRAO % (str(round(Valor_Receber, 2)), str(round(LucroReal, 2)))
            
            if (tipo_pagamento == TP_PAGAMENTO_MPAGO):
                resposta = RESPOSTA_MERCADO_PAGO % (str(round(Valor_Receber, 2)), str(round(LucroReal, 2)))
            
            window['Resposta2'](resposta)
        except:
            sg.popup('Preencha todos os campos com numeros')

window.close()
        