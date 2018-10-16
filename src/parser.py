# -*- coding: utf-8 -*-
import ply.yacc as yacc
from anytree import Node, RenderTree
from anytree.exporter import DotExporter
import sys

from scanner import tokens

precedence = (
    ('left', 'SOMA', 'SUBTRACAO'),
    ('left', 'MULTIPLICACAO', 'DIVISAO')
)

def p_programa(p):
    '''programa : lista_declaracoes'''
    p[0] = Node('programa', parent=p[1])

def p_lista_declaracoes(p):
    '''lista_declaracoes : lista_declaracoes declaracao
                         | declaracao'''
    if len(p) == 3:
        p[0] = Node('lista_declaracoes', parent=[p[1], p[2]])
    elif len(p) == 2:
        p[0] = Node('lista_declaracoes', parent=[p[2]])

def p_declaracao(p):
    '''declaracao : declaracao_variaveis
                  | inicializacao_variaveis
                  | declaracao_funcao'''
    p[0] = Node('declaracao', parent=[p[1]])

def p_declaracao_variaveis(p):
    '''declaracao_variaveis : tipo DOIS_PONTOS lista_variaveis'''
    p[0] = Node('declaracao_variaveis', parent=[p[1], p[3]])

def p_inicializacao_variaveis(p):
    '''inicializacao_variaveis : atribuicao'''
    p[0] = Node('inicializacao_variaveis', parent=[p[1]])

def p_lista_variaveis(p):
    '''lista_variaveis : lista_variaveis VIRGULA var
                       | var'''
    if len(p) == 4:
        p[0] = Node('lista_variaveis', parent=[p[1], p[3]])
    elif len(p) == 2:
        p[0] = Node('lista_variaveis', parent=[p[1]])

def p_var(p):
    '''var : ID
           | ID indice'''
    if len(p) == 2:
        p[0] = Node('var', parent=[p[1]])
    elif len(p) == 3:
        p[0] = Node('var', parent=[p[1], p[2]])

def p_indice(p):
    '''indice : indice ABRE_COL expressao FECHA_COL
              | ABRE_COL expressao FECHA_COL'''
    if len(p) == 5:
        p[0] = Node('indice', parent=[p[1], p[3]])
    elif len(p) == 4:
        p[0] = Node('indice', parent=[p[2]])

def p_tipo(p):
    '''tipo : INTEIRO
            | FLUTUANTE'''
    p[0] = Node('tipo', parent=[p[1]])

def p_declaracao_funcao(p):
    '''declaracao_funcao : tipo cabecalho
                         | cabecalho'''
    if len(p) == 3:
        p[0] = Node('declaracao_funcao', parent=[p[1], p[2]])
    elif len(p) == 2:
        p[0] = Node('declaracao_funcao', parent=[p[1]])

def p_cabecalho(p):
    '''cabecalho : ID ABRE_PAR lista_parametros FECHA_PAR corpo FIM'''
    p[0] = Node('cabecalho', parent=[p[1], p[3], p[5]])

def p_lista_parametros(p):
    '''lista_parametros : lista_parametros VIRGULA parametro
                        | parametro
                        | vazio'''
    if len(p) == 4:
        p[0] = Node('lista_parametros', parent=[p[1], p[3]])
    elif len(p) == 2:
        p[0] = Node('lista_parametros', parent=[p[1]])

def p_parametro(p):
    '''parametro : tipo DOIS_PONTOS ID
                 | parametro ABRE_COL FECHA_COL'''
    p[0] = Node('parametro', parent=[p[1], p[3]])

def p_corpo(p):
    '''corpo : corpo acao
             | vazio'''
    if len(p) == 3:
        p[0] = Node('corpo', parent=[p[1], p[2]])
    elif len(p) == 2:
        p[0] = Node('corpo', parent=[p[1]])

def p_acao(p):
    '''acao : expressao
            | declaracao_variaveis
            | se
            | repita
            | leia
            | escreva
            | retorna
            | error'''
    p[0] = Node('acao', parent=[p[1]])

def p_se(p):
    '''se : SE expressao ENTAO corpo FIM
          | SE expressao ENTAO corpo SENAO corpo FIM'''
    if len(p) == 6:
        p[0] = Node('se', parent=[p[2], p[4]])
    elif len(p) == 8:
        p[0] = Node('se', parent=[p[2], p[4], p[6]])

def p_repita(p):
    '''repita : REPITA corpo ATE expressao'''
    p[0] = Node('repita', parent=[p[2], p[4]])

def p_atribuicao(p):
    '''atribuicao : var ATRIBUICAO expressao'''
    p[0] = Node('atribuicao', parent=[p[1], p[3]])

def p_leia(p):
    '''leia : LEIA ABRE_PAR var FECHA_PAR'''
    p[0] = Node('leia', parent=[p[3]])

def p_escreva(p):
    '''escreva : ESCREVA ABRE_PAR expressao FECHA_PAR'''
    p[0] = Node('escreva', parent=[p[3]])

def p_retorna(p):
    '''retorna : RETORNA ABRE_PAR expressao FECHA_PAR'''
    p[0] = Node('retorna', parent=[p[3]])

def p_expressao(p):
    '''expressao : expressao_logica
                 | atribuicao'''
    p[0] = Node('expressao', parent=[p[1]])

def p_expressao_logica(p):
    '''expressao_logica : expressao_simples
                        | expressao_logica operador_logico expressao_simples'''
    if len(p) == 2:
        p[0] = Node('expressa0_logica', parent=[p[1]])
    elif len(p) == 4:
        p[0] = Node('expressao_logica', parent=[p[1], p[2], p[3]])

def p_expressao_simples(p):
    '''expressao_simples : expressao_aditiva
                         | expressao_simples operador_relacional expressao_aditiva'''
    if len(p) == 2:
        p[0] = Node('expressao_simples', parent=[p[1]])
    elif len(p) == 4:
        p[0] = Node('expressao_simples', parent=[p[1], p[2], p[3]])

def p_expressao_aditiva(p):
    '''expressao_aditiva : expressao_multiplicativa
                         | expressao_aditiva operador_soma expressao_multiplicativa'''
    if len(p) == 2:
        p[0] = Node('expressao_aditiva', parent=[p[1]])
    elif len(p) == 4:
        p[0] = Node('expressao_aditiva', parent=[p[1], p[2], p[3]])

def p_expressao_multiplicativa(p):
    '''expressao_multiplicativa : expressao_unaria
                                | expressao_multiplicativa operador_multiplicacao expressao_unaria'''
    if len(p) == 2:
        p[0] = Node('expressao_multiplicativa', parent=[p[1]])
    elif len(p) == 4:
        p[0] = Node('expressao_multiplicativa', parent=[p[1], p[2], p[3]])

def p_expressao_unaria(p):
    '''expressao_unaria : fator
                        | operador_soma fator
                        | operador_negacao fator'''
    if len(p) == 2:
        p[0] = Node('expressao_unaria', parent=[p[1]])
    elif len(p) == 3:
        p[0] = Node('expressao_unaria', parent=[p[1], p[2]])

def p_operador_relacional(p):
    '''operador_relacional : MENOR
                           | MAIOR
                           | IGUALDADE
                           | MENOR_IGUAL
                           | MAIOR_IGUAL'''
    p[0] = Node('operador_relacional', parent=[p[1]])

def p_operador_soma(p):
    '''operador_soma : SOMA
                     | SUBTRACAO'''
    p[0] = Node('operador_soma', parent=[])

def p_operador_negacao(p):
    '''operador_negacao : NEGACAO'''
    p[0] = Node('operador_negacao', parent=[])

def p_operador_logico(p):
    '''operador_logico : E_LOGICO
                       | OU_LOGICO'''
    p[0] = Node('operador_logico', parent=[])

def p_operador_multiplicacao(p):
    '''operador_multiplicacao : MULTIPLICACAO
                              | DIVISAO'''
    p[0] = Node('operador_multiplicacao', parent=[])

def p_fator(p):
    '''fator : ABRE_PAR expressao FECHA_PAR
             | var
             | chamada_funcao
             | numero'''
    if len(p) == 4:
        p[0] = Node('fator', parent=[p[2]])
    elif len(p) == 2:
        p[0] = Node('fator', parent=[p[1]])

def p_numero(p):
    '''numero : NUM_INTEIRO
              | NUM_FLUTUANTE'''
    p[0] = Node('numero', parent=[])

def p_chamada_funcao(p):
    '''chamada_funcao : ID ABRE_COL lista_argumentos FECHA_COL'''
    p[0] = Node('chamada_funcao', parent=[p[3]])

def p_lista_argumentos(p):
    '''lista_argumentos : lista_argumentos VIRGULA expressao
                        | expressao
                        | vazio'''
    if len(p) == 4:
        p[0] = Node('lista_argumentos', parent=[p[1], p[3]])
    elif len(p) == 2:
        p[0] = Node('lista_argumentos', parent=[p[1]])

def p_vazio(p):
    'vazio :'
    pass

def p_error(p):
    if p:
        print("Erro sintático na linha '%d': '%s'" % (p.lineno, p.value))
    else:
        yacc.restart()
        print("Erro sintático nas definições!")
        exit(1)

# parser = yacc.yacc()

def run_parser(file):
    if file == None:
        print("Arquivo inválido!")
    else:
        f = open(file, 'r')
        arq = f.read()
        parser = yacc.yacc()
        result = parser.parse(arq)

        # while True:
        #     try:
        #         s = input(f.read())
        #     except EOFError:
        #         break
        #     if not s: continue
        #     result = parser.parse(s)
        print(result)
        
        f.close()