# -*- coding: utf-8 -*-
import ply.lex as lex
import sys

palavras_reservadas = {'se' : 'SE', 'então' : 'ENTAO', 'senão' : 'SENAO', 'fim' : 'FIM', 'repita' : 'REPITA',
                'flutuante' : 'FLUTUANTE', 'inteiro' : 'INTEIRO', 'retorna' : 'RETORNA', 'ate' : 'ATE',
                'leia' : 'LEIA', 'escreva' : 'ESCREVA'}

tokens = ['NUM_INTEIRO', 'NUM_FLUTUANTE', 'ID', 'SOMA', 'SUBTRACAO', 'MULTIPLICACAO', 'DIVISAO', 'IGUALDADE', 'VIRGULA',
            'ATRIBUICAO', 'MENOR', 'MAIOR', 'MENOR_IGUAL', 'MAIOR_IGUAL', 'ABRE_PAR', 'FECHA_PAR', 'DOIS_PONTOS',
            'ABRE_COL', 'FECHA_COL', 'E_LOGICO', 'OU_LOGICO', 'NEGACAO', 'COMENTARIO']+list(palavras_reservadas.values())

t_SOMA = r'\+'
t_SUBTRACAO = r'\-'
t_MULTIPLICACAO = r'\*'
t_DIVISAO = r'\/'
t_IGUALDADE = r'\='
t_VIRGULA = r'\,'
t_MENOR = r'\<'
t_MAIOR = r'\>'
t_ABRE_PAR = r'\('
t_FECHA_PAR = r'\)'
t_ABRE_COL = r'\['
t_FECHA_COL = r'\]'
t_DOIS_PONTOS = r'\:'
t_NEGACAO = r'\!'

t_ignore = ' \t\n\r'
# t_ignore_COMENTARIO = r'(\{(.|\n)*?\})|(\{(.|\n)*?)$'
t_ignore_COMENTARIO = r'\{[^}]*[^{]*\}$'

def t_NUM_FLUTUANTE(t):
    r'[-+]?\d+\.\d*([eE][-+]?\d+)?'
    t.value = float(t.value)
    return t

#Para os outros casos não é tão simples, por isso é necessário criar uma expressão regular
def t_NUM_INTEIRO(t):
    r'\d+' #nesse caso, aceita todos os caracteres que o tamanho é maior que um
    t.value = int(t.value) #então, precisamos converter para inteiro
    return t

def t_ID(t):
    r'[a-zA-ZáàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ_][a-zA-ZáàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ0-9_]*'
    t.type = palavras_reservadas.get(t.value, 'ID')
    return t

def t_ATRIBUICAO(t):
    r'\:\='
    t.type = 'ATRIBUICAO'
    return t

def t_MENOR_IGUAL(t):
    r'\<\='
    t.type = 'MENOR_IGUAL'
    return t

def t_MAIOR_IGUAL(t):
    r'\>\='
    t.type = 'MAIOR_IGUAL'
    return t

def t_E_LOGICO(t):
    r'\&\&'
    t.type = 'E_LOGICO'
    return t

def t_OU_LOGICO(t):
    r'\|\|'
    t.type = 'OU_LOGICO'
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print("Caractere '%s' Inválido!" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex() #executa o lexer

if len(sys.argv) == 1:
    print("Comando incorreto! \nSintaxe: python scanner.py nome_arquivo_teste.tpp") #Verifica se o arquivo foi executado corretamente
else:
    fileName = sys.argv[1] #Recebe nome do arquivo a ser escaneado
    file = open(fileName, 'r') #abre o arquivo
    line = file.readline() #lê a primeira linha do arquivo
    cont = 1
    while line: #enquanto o arquivo tiver linha para ser lida
        lexer.input(line) #alimenta o lexer com uma linha
        while True:
            tok = lexer.token() #pega o próximo token
            if not tok: #se não tiver mais nenhum, para
                break
            print("Linha",cont,": <", tok.type, ",", tok.value, ">") #do contrário, vai mostrando os tokens

        line = file.readline() #passa para a próxima linha
        cont = cont + 1

    file.close()