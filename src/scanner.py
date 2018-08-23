import ply.lex as lex
import sys

tokens = ('INTEIRO', 'FLUTUANTE', 'ID', 'SOMA', 'SUBTRACAO', 'MULTIPLICACAO', 'DIVISAO', 'IGUALDADE', 'VIRGULA',
            'ATRIBUICAO', 'MENOR', 'MAIOR', 'MENOR_IGUAL', 'MAIOR_IGUAL', 'ABRE_PAR', 'FECHA_PAR', 'DOIS_PONTOS',
            'ABRE_COL', 'FECHA_COL', 'E_LOGICO', 'OU_LOGICO', 'NEGACAO', 'COMENTARIO', 'NUM')

palavras_reservadas = ('SE', 'ENTÃO', 'SENÃO', 'FIM', 'REPITA', 'FLUTUANTE', 'INTEIRO', 'RETORNA', 'ATÉ', 'LEIA', 'ESCREVA')

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

#falta regra para: atribuicao, menor e maior igual, e e ou logicos, comentario, num (no geral), palavras_reservadas

t_ignore = ' \t\n'

def t_FLUTUANTE(t):
    r'[-+]?\d+\.\d+([eE][-+]?\d+)?'
    t.value = float(t.value)
    return t

#Para os outros casos não é tão simples, por isso é necessário criar uma expressão regular
def t_INTEIRO(t):
    r'\d+' #nesse caso, aceita todos os caracteres que o tamanho é maior que um
    t.value = int(t.value) #então, precisamos converter para inteiro
    return t

def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9]*'
    t.type = 'ID'
    return t

def t_error(t):
    print("Caractere '%s' Inválido!" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()

fileName = sys.argv[1]

file = open(fileName, 'r')
line = file.readline()
while line != "":
    lexer.input(line)
    while True:
        tok = lexer.token()
        if not tok:
            break
        print("<", tok.type, ",", tok.value, ">")

    line = file.readline()
file.close()