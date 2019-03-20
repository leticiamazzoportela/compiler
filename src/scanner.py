# -*- coding: utf-8 -*-
import ply.lex as lex
import sys
import json

palavras_reservadas = {'se' : 'SE', 'então' : 'ENTAO', 'senão' : 'SENAO', 'fim' : 'FIM', 'repita' : 'REPITA',
                'flutuante' : 'FLUTUANTE', 'inteiro' : 'INTEIRO', 'retorna' : 'RETORNA', 'até' : 'ATE',
                'leia' : 'LEIA', 'escreva' : 'ESCREVA'}

tokens = ['NUM_INTEIRO', 'NUM_FLUTUANTE', 'ID', 'SOMA', 'SUBTRACAO', 'MULTIPLICACAO', 'DIVISAO', 'IGUALDADE', 'DIFERENTE', 'VIRGULA',
            'ATRIBUICAO', 'MENOR', 'MAIOR', 'MENOR_IGUAL', 'MAIOR_IGUAL', 'ABRE_PAR', 'FECHA_PAR', 'DOIS_PONTOS',
            'ABRE_COL', 'FECHA_COL', 'E_LOGICO', 'OU_LOGICO', 'NEGACAO']+list(palavras_reservadas.values())

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

t_ignore = ' \t\r'

symbols_table = []

#Lista de funções que definem expressões regulares:
#************************************************
def t_COMENTARIO(t):
    r'(\{(.|\n)*?\})|(\{(.|\n)*?)$'
    # r'{.*}'
    pass

def t_NUM_FLUTUANTE(t):
    r'[-+]?\d+\.\d*([eE][-+]?\d+)?'
    t.value = float(t.value)
    return t


def t_NUM_INTEIRO(t):
    r'\d+'
    t.value = int(t.value)
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

def t_DIFERENTE(t):
    r'\<\>'
    t.type = 'DIFERENTE'
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

def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1
#************************************************
#Fim das expressões

#Função que exibe erros
def t_error(t):
    print("Caractere '%s' Inválido!" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex() #executa o lexer

#Função que chama o lexer e escaneia um arquivo passado por parâmetro.
def run_scanner(file):
    naosei = {}
    if file == None:
        print("Arquivo inválido!")
    else:
        fileName = file
        f = open(fileName, 'r')
        line = f.readline()
        while line:
            lexer.input(line)
            while True:
                tok = lexer.token()
                if not tok:
                    break
                tok.lexpos = find_column(line, tok)
                print("Linha "+str(tok.lineno)+" - Pos " +str(tok.lexpos)+ ": <" +tok.type+ " , " +str(tok.value)+ ">\n")
                naosei['linha'] = tok.lineno
                naosei['posicao'] = tok.lexpos
                naosei['tipo'] = tok.type
                naosei['lexema'] = tok.value 

                symbols_table.append(naosei)
                naosei = {}
            line = f.readline()

        f.close()
        print(json.dumps(symbols_table, indent=4))