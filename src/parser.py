# -*- coding: utf-8 -*-
import ply.yacc as yacc
from anytree import Node, RenderTree
from anytree.exporter import DotExporter

from scanner import tokens
from scanner import find_column

precedence = (
    ('left', 'SOMA', 'SUBTRACAO'),
    ('left', 'MULTIPLICACAO', 'DIVISAO')
)

id_node = 0

#Lista de funções que definem regras gramaticais:
#************************************************
def p_programa(p):
    '''programa : lista_declaracoes'''
    global id_node

    id_node = id_node + 1
    p[0] = Node(str(id_node)+'.'+'programa')
    p[1].parent = p[0]

    # node.lineno
def p_lista_declaracoes(p):
    '''lista_declaracoes : lista_declaracoes declaracao
                         | declaracao'''
    global id_node

    id_node = id_node + 1
    p[0] = Node(str(id_node)+'.'+'lista_declaracoes')
    p[1].parent = p[0]

    if len(p) == 3:
        p[2].parent = p[0]

def p_declaracao(p):
    '''declaracao : declaracao_variaveis
                  | inicializacao_variaveis
                  | declaracao_funcao'''
    global id_node

    id_node = id_node + 1
    p[0] = Node(str(id_node)+'.'+'declaracao')
    p[1].parent = p[0]

def p_declaracao_variaveis(p):
    '''declaracao_variaveis : tipo DOIS_PONTOS lista_variaveis'''
    global id_node

    id_node = id_node + 1
    p[0] = Node(str(id_node)+'.'+'declaracao_variaveis')
    p[1].parent = p[0]

    id_node = id_node + 1
    Node(str(id_node)+'.'+p[2], parent=p[0], lineno=p.lineno(2))
    p[3].parent = p[0]

def p_inicializacao_variaveis(p):
    '''inicializacao_variaveis : atribuicao'''
    global id_node

    id_node = id_node + 1
    p[0] = Node(str(id_node)+'.'+'inicializacao_variaveis')
    p[1].parent = p[0]

def p_lista_variaveis(p):
    '''lista_variaveis : lista_variaveis VIRGULA var
                       | var'''
    global id_node

    id_node = id_node + 1
    p[0] = Node(str(id_node)+'.'+'lista_variaveis')
    p[1].parent = p[0]

    if len(p) == 4:
        id_node = id_node + 1
        Node(str(id_node)+'.'+p[2], parent=p[0], lineno=p.lineno(2))
        p[3].parent = p[0]

def p_var(p):
    '''var : ID
           | ID indice'''
    global id_node

    id_node = id_node + 1
    p[0] = Node(str(id_node)+'.'+'var')

    id_node = id_node + 1
    Node(str(id_node)+'.'+p[1], parent=p[0], lineno=p.lineno(1))

    if len(p) == 3:
        p[2].parent = p[0]

def p_indice(p):
    '''indice : indice ABRE_COL expressao FECHA_COL
              | ABRE_COL expressao FECHA_COL'''
    global id_node

    id_node = id_node + 1
    p[0] = Node(str(id_node)+'.'+'indice')

    if len(p) == 5:
        p[1].parent = p[0]
        id_node = id_node + 1
        Node(str(id_node)+'.'+p[2], parent=p[0], lineno=p.lineno(2))

        p[3].parent = p[0]
        id_node = id_node + 1
        Node(str(id_node)+'.'+p[4], parent=p[0], lineno=p.lineno(4))
    elif len(p) == 4:
        id_node = id_node + 1
        Node(str(id_node)+'.'+p[1], parent=p[0], lineno=p.lineno(1))
        p[2].parent = p[0]

        id_node = id_node + 1
        Node(str(id_node)+'.'+p[3], parent=p[0], lineno=p.lineno(3))

def p_tipo(p):
    '''tipo : INTEIRO
            | FLUTUANTE'''
    global id_node

    id_node = id_node + 1
    p[0] = Node(str(id_node)+'.'+'tipo')

    id_node = id_node + 1
    Node(str(id_node)+'.'+p[1], parent=p[0], lineno=p.lineno(1))

def p_declaracao_funcao(p):
    '''declaracao_funcao : tipo cabecalho
                         | cabecalho'''
    global id_node

    id_node = id_node + 1
    p[0] = Node(str(id_node)+'.'+'declaracao_funcao')
    p[1].parent = p[0]

    if len(p) == 3:
        p[2].parent = p[0]

def p_cabecalho(p):
    '''cabecalho : ID ABRE_PAR lista_parametros FECHA_PAR corpo FIM'''
    global id_node

    id_node = id_node + 1
    p[0] = Node(str(id_node)+'.'+'cabecalho')

    id_node = id_node + 1
    Node(str(id_node)+'.'+p[1], parent=p[0], lineno=p.lineno(1))

    id_node = id_node + 1
    Node(str(id_node)+'.'+p[2], parent=p[0], lineno=p.lineno(2))
    p[3].parent = p[0]

    id_node = id_node + 1
    Node(str(id_node)+'.'+p[4], parent=p[0], lineno=p.lineno(4))
    p[5].parent = p[0]

    id_node = id_node + 1
    Node(str(id_node)+'.'+p[6], parent=p[0], lineno=p.lineno(6))

def p_lista_parametros(p):
    '''lista_parametros : lista_parametros VIRGULA parametro
                        | parametro
                        | vazio'''
    global id_node

    id_node = id_node + 1
    p[0] = Node(str(id_node)+'.'+'lista_parametros')
    p[1].parent = p[0]

    if len(p) == 4:
        id_node = id_node + 1
        Node(str(id_node)+'.'+p[2], parent=p[0], lineno=p.lineno(2))
        p[3].parent = p[0]

def p_parametro(p):
    '''parametro : tipo DOIS_PONTOS ID
                 | parametro ID ABRE_COL FECHA_COL'''
    global id_node

    id_node = id_node + 1
    p[0] = Node(str(id_node)+'.'+'parametro')
    p[1].parent = p[0]

    id_node = id_node + 1
    Node(str(id_node)+'.'+p[2], parent=p[0], lineno=p.lineno(2))

    id_node = id_node + 1
    Node(str(id_node)+'.'+p[3], parent=p[0], lineno=p.lineno(3))

def p_corpo(p):
    '''corpo : corpo acao
             | vazio'''
    global id_node

    id_node = id_node + 1
    p[0] = Node(str(id_node)+'.'+'corpo')
    p[1].parent = p[0]

    if len(p) == 3:
        p[2].parent = p[0]

def p_acao(p):
    '''acao : expressao
            | declaracao_variaveis
            | se
            | repita
            | leia
            | escreva
            | retorna
            | error'''
    global id_node

    id_node = id_node + 1
    p[0] = Node(str(id_node)+'.'+'acao')
    p[1].parent = p[0]

def p_se(p):
    '''se : SE expressao ENTAO corpo FIM
          | SE expressao ENTAO corpo SENAO corpo FIM'''
    global id_node

    id_node = id_node + 1
    p[0] = Node(str(id_node)+'.'+'se')

    id_node = id_node + 1
    Node(str(id_node)+'.'+p[1], parent=p[0], lineno=p.lineno(1))
    p[2].parent = p[0]

    id_node = id_node + 1
    Node(str(id_node)+'.'+p[3], parent=p[0], lineno=p.lineno(3))
    p[4].parent = p[0]

    id_node = id_node + 1
    Node(str(id_node)+'.'+p[5], parent=p[0], lineno=p.lineno(5))

    if len(p) == 8:   
        p[6].parent = p[0]
        id_node = id_node + 1
        Node(str(id_node)+'.'+p[7], parent=p[0], lineno=p.lineno(7))

def p_repita(p):
    '''repita : REPITA corpo ATE expressao'''
    global id_node

    id_node = id_node + 1
    p[0] = Node(str(id_node)+'.'+'repita')

    id_node = id_node + 1
    Node(str(id_node)+'.'+p[1], parent=p[0], lineno=p.lineno(1))
    p[2].parent = p[0]

    id_node = id_node + 1
    Node(str(id_node)+'.'+p[3], parent=p[0], lineno=p.lineno(3))
    p[4].parent = p[0]

def p_atribuicao(p):
    '''atribuicao : var ATRIBUICAO expressao'''
    global id_node

    id_node = id_node + 1
    p[0] = Node(str(id_node)+'.'+'atribuicao')
    p[1].parent = p[0]

    id_node = id_node + 1
    Node(str(id_node)+'.'+p[2], parent=p[0], lineno=p.lineno(2))
    p[3].parent = p[0]

def p_leia(p):
    '''leia : LEIA ABRE_PAR var FECHA_PAR'''
    global id_node

    id_node = id_node + 1
    p[0] = Node(str(id_node)+'.'+'leia')

    id_node = id_node + 1
    Node(str(id_node)+'.'+p[1], parent=p[0], lineno=p.lineno(1))

    id_node = id_node + 1
    Node(str(id_node)+'.'+p[2], parent=p[0], lineno=p.lineno(2))
    p[3].parent = p[0]

    id_node = id_node + 1
    Node(str(id_node)+'.'+p[4], parent=p[0], lineno=p.lineno(4))

def p_escreva(p):
    '''escreva : ESCREVA ABRE_PAR expressao FECHA_PAR'''
    global id_node

    id_node = id_node + 1
    p[0] = Node(str(id_node)+'.'+'escreva')

    id_node = id_node + 1
    Node(str(id_node)+'.'+p[1], parent=p[0], lineno=p.lineno(1))

    id_node = id_node + 1
    Node(str(id_node)+'.'+p[2], parent=p[0], lineno=p.lineno(2))
    p[3].parent = p[0]

    id_node = id_node + 1
    Node(str(id_node)+'.'+p[4], parent=p[0], lineno=p.lineno(4))

def p_retorna(p):
    '''retorna : RETORNA ABRE_PAR expressao FECHA_PAR'''
    global id_node

    id_node = id_node + 1
    p[0] = Node(str(id_node)+'.'+'retorna')

    id_node = id_node + 1
    Node(str(id_node)+'.'+p[1], parent=p[0], lineno=p.lineno(1))

    id_node = id_node + 1
    Node(str(id_node)+'.'+p[2], parent=p[0], lineno=p.lineno(2))
    p[3].parent = p[0]

    id_node = id_node + 1
    Node(str(id_node)+'.'+p[4], parent=p[0], lineno=p.lineno(4))

def p_expressao(p):
    '''expressao : expressao_logica
                 | atribuicao'''
    global id_node

    id_node = id_node + 1
    p[0] = Node(str(id_node)+'.'+'expressao')
    p[1].parent = p[0]

def p_expressao_logica(p):
    '''expressao_logica : expressao_simples
                        | expressao_logica operador_logico expressao_simples'''
    global id_node

    id_node = id_node + 1
    p[0] = Node(str(id_node)+'.'+'expressao_logica')
    p[1].parent = p[0]

    if len(p) == 4:
        p[2].parent = p[0]
        p[3].parent = p[0]

def p_expressao_simples(p):
    '''expressao_simples : expressao_aditiva
                         | expressao_simples operador_relacional expressao_aditiva'''
    global id_node

    id_node = id_node + 1
    p[0] = Node(str(id_node)+'.'+'expressao_simples')
    p[1].parent = p[0]

    if len(p) == 4:
        p[2].parent = p[0]
        p[3].parent = p[0]

def p_expressao_aditiva(p):
    '''expressao_aditiva : expressao_multiplicativa
                         | expressao_aditiva operador_soma expressao_multiplicativa'''
    global id_node

    id_node = id_node + 1
    p[0] = Node(str(id_node)+'.'+'expressao_aditiva')
    p[1].parent = p[0]

    if len(p) == 4:
        p[2].parent = p[0]
        p[3].parent = p[0]

def p_expressao_multiplicativa(p):
    '''expressao_multiplicativa : expressao_unaria
                                | expressao_multiplicativa operador_multiplicacao expressao_unaria'''
    global id_node

    id_node = id_node + 1
    p[0] = Node(str(id_node)+'.'+'expressao_multiplicativa')
    p[1].parent = p[0]

    if len(p) == 4:
        p[2].parent = p[0]
        p[3].parent = p[0]

def p_expressao_unaria(p):
    '''expressao_unaria : fator
                        | operador_soma fator
                        | operador_negacao fator'''
    global id_node

    id_node = id_node + 1
    p[0] = Node(str(id_node)+'.'+'expressao_unaria')
    p[1].parent = p[0]

    if len(p) == 3:
        p[2].parent = p[0]

def p_operador_relacional(p):
    '''operador_relacional : MENOR
                           | MAIOR
                           | IGUALDADE
                           | DIFERENTE
                           | MENOR_IGUAL
                           | MAIOR_IGUAL'''
    global id_node

    id_node = id_node + 1
    p[0] = Node(str(id_node)+'.'+'operador_relacional')

    id_node = id_node + 1
    Node(str(id_node)+'.'+p[1], parent=p[0], lineno=p.lineno(1))

def p_operador_soma(p):
    '''operador_soma : SOMA
                     | SUBTRACAO'''
    global id_node

    id_node = id_node + 1
    p[0] = Node(str(id_node)+'.'+'operador_soma')

    id_node = id_node + 1
    Node(str(id_node)+'.'+p[1], parent=p[0], lineno=p.lineno(1))

def p_operador_negacao(p):
    '''operador_negacao : NEGACAO'''
    global id_node

    id_node = id_node + 1
    p[0] = Node(str(id_node)+'.'+'operador_negacao')

    id_node = id_node + 1
    Node(str(id_node)+'.'+p[1], parent=p[0], lineno=p.lineno(1))

def p_operador_logico(p):
    '''operador_logico : E_LOGICO
                       | OU_LOGICO'''
    global id_node

    id_node = id_node + 1
    p[0] = Node(str(id_node)+'.'+'operador_logico')

    id_node = id_node + 1
    Node(str(id_node)+'.'+p[1], parent=p[0], lineno=p.lineno(1))

def p_operador_multiplicacao(p):
    '''operador_multiplicacao : MULTIPLICACAO
                              | DIVISAO'''
    global id_node

    id_node = id_node + 1
    p[0] = Node(str(id_node)+'.'+'operador_multiplicacao')

    id_node = id_node + 1
    Node(str(id_node)+'.'+p[1], parent=p[0], lineno=p.lineno(1))

def p_fator(p):
    '''fator : ABRE_PAR expressao FECHA_PAR
             | var
             | chamada_funcao
             | numero'''
    global id_node

    id_node = id_node + 1
    p[0] = Node(str(id_node)+'.'+'fator')

    if len(p) == 4:
        id_node = id_node + 1
        Node(str(id_node)+'.'+p[1], parent=p[0], lineno=p.lineno(1))
        p[2].parent = p[0]

        id_node = id_node + 1
        Node(str(id_node)+'.'+p[3], parent=p[0], lineno=p.lineno(3))
    elif len(p) == 2:
        p[1].parent = p[0]

def p_numero(p):
    '''numero : NUM_INTEIRO
              | NUM_FLUTUANTE'''
    global id_node

    id_node = id_node + 1
    p[0] = Node(str(id_node)+'.'+'numero')

    id_node = id_node + 1
    Node(str(id_node)+'.'+str(p[1]), parent=p[0], lineno=p.lineno(1))

def p_chamada_funcao(p):
    '''chamada_funcao : ID ABRE_PAR lista_argumentos FECHA_PAR'''
    global id_node

    id_node = id_node + 1
    p[0] = Node(str(id_node)+'.'+'chamada_funcao')

    id_node = id_node + 1
    Node(str(id_node)+'.'+p[1], parent=p[0], lineno=p.lineno(1))

    id_node = id_node + 1
    Node(str(id_node)+'.'+p[2], parent=p[0], lineno=p.lineno(2))
    p[3].parent = p[0]

    id_node = id_node + 1
    Node(str(id_node)+'.'+p[4], parent=p[0], lineno=p.lineno(4))

def p_lista_argumentos(p):
    '''lista_argumentos : lista_argumentos VIRGULA expressao
                        | expressao
                        | vazio'''
    global id_node

    id_node = id_node + 1
    p[0] = Node(str(id_node)+'.'+'lista_argumentos')
    p[1].parent = p[0]

    if len(p) == 4:
        id_node = id_node + 1
        Node(str(id_node)+'.'+p[2], parent=p[0], lineno=p.lineno(2))
        p[3].parent = p[0]

def p_vazio(p):
    'vazio : '
    global id_node

    id_node = id_node + 1
    p[0] = Node(str(id_node)+'.'+str(p[0]))
#************************************************
# Fim das regras


#Função que exibe erros
def p_error(p):
    if p:
        # print("Erro sintático na linha %d - Posição %d: '%s'" % (p.lineno, p.lexpos, p.value))
        print("Erro sintático na linha %d: '%s' após sentença estranha" % (p.lineno-20, p.value))
        exit(1)
    else:
        yacc.restart()
        print("Erro sintático nas definições!")
        exit(1)

parser = yacc.yacc() #executa o parser

#Função que chama o parser e analisa um arquivo passado por parâmetro.
#O resultado é uma árvore sintática abstrata
def run_parser(file):
    if file == None:
        print("Arquivo inválido!")
    else:
        f = open(file, 'r')
        arq = f.read()
        result = parser.parse(arq)
        
        DotExporter(result).to_picture("ast.png")
        
        f.close()