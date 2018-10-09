# -*- coding: utf-8 -*-
import ply.yacc as yacc
import sys

from scanner import tokens #importa tokens definidos no scanner

#The values of p[i] are mapped to grammar symbols
#expression : expression PLUS term
# p[0]      : p[1]       p[1]  p[2]

#Definição da gramática

def p_programa(p):
    '''programa : lista_declaracoes'''
    p[0] = p[1]

def p_lista_declaracoes(p):
    '''lista_declaracoes : lista_declaracoes declaracao
                         | declaracao'''
    if len(p) == 3: #nao sei se isso funciona
        p[0] = (p[1], p[2])
    elif len(p) == 2:
        p[0] = p[2]

def p_declaracao(p):
    '''declaracao : declaracao_variaveis
                  | inicializacao_variaveis
                  | declaracao_funcao'''
    p[0] = p[1]

def p_declaracao_variaveis(p):
    '''declaracao_variaveis : tipo DOIS_PONTOS lista_variaveis'''
    p[0] = (p[1], p[3])

def p_inicializacao_variaveis(p):
    '''inicializacao_variaveis : atribuicao'''
    p[0] = p[1]

def p_lista_variaveis(p):
    '''lista_variaveis : lista_variaveis VIRGULA var
                       | var'''
    if len(p) == 4:
        p[0] = (p[1], p[3])
    elif len(p) == 2:
        p[0] = p[1]

def p_var(p):
    '''var : ID
           | ID indice'''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = (p[1], p[2])

def p_indice(p):
    '''indice : indice ABRE_COL expressao FECHA_COL
              | ABRE_COL expressao FECHA_COL'''
    if len(p) == 5:
        p[0] = (p[1], p[3])
    elif len(p) == 4:
        p[0] = p[2]

def p_tipo(p):
    '''tipo : INTEIRO
            | FLUTUANTE'''
    p[0] = p[1]

def p_declaracao_funcao(p):
    '''declaracao_funcao : tipo cabecalho
                         | cabecalho'''
    if len(p) == 3:
        p[0] = (p[1], p[2])
    elif len(p) == 2:
        p[0] = p[1]

def p_cabecalho(p):
    '''cabecalho : ID ABRE_PAR lista_parametros FECHA_PAR corpo FIM'''
    p[0] = (p[1], p[3], p[5])

def p_lista_parametros(p):
    '''lista_parametros : lista_parametros VIRGULA parametro
                        | parametro
                        | vazio'''
    if len(p) == 4:
        p[0] = (p[1], p[3])
    elif len(p) == 2:
        p[0] = p[1]

def p_parametro(p):
    '''parametro : tipo DOIS_PONTOS ID
                 | parametro ABRE_COL FECHA_COL'''
    p[0] = (p[1], p[3])

def p_corpo(p):
    '''corpo : corpo acao
             | vazio'''
    if len(p) == 3:
        p[0] = (p[1], p[2])
    elif len(p) == 2:
        p[0] = p[1]

def p_acao(p):
    '''acao : expressao
            | declaracao_variaveis
            | se
            | repita
            | leia
            | escreva
            | retorna
            | error'''
    p[0] = p[1]

def p_se(p):
    '''se : SE expressao ENTAO corpo FIM
          | SE expressao ENTAO corpo SENAO corpo FIM'''
    if len(p) == 6:
        p[0] = (p[2], p[4])
    elif len(p) == 8:
        p[0] = (p[2], p[4], p[6])

def p_repita(p):
    '''repita : REPITA corpo ATE expressao'''
    p[0] = (p[2], p[4])

def p_atribuicao(p):
    '''atribuicao : var ATRIBUICAO expressao'''
    p[0] = (p[1], p[3])

def p_leia(p):
    '''leia : LEIA ABRE_PAR var FECHA_PAR'''
    p[0] = p[3]

def p_escreva(p):
    '''escreva : ESCREVA ABRE_PAR expressao FECHA_PAR'''
    p[0] = p[3]

def p_retorna(p):
    '''retorna : RETORNA ABRE_PAR expressao FECHA_PAR'''
    p[0] = p[3]

def p_expressao(p):
    '''expressao : expressao_logica
                 | atribuicao'''
    p[0] = p[1]

def p_expressao_logica(p):
    '''expressao_logica : expressao_simples
                        | expressao_logica operador_logico expressao_simples'''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = (p[1], p[2], p[3])

def p_expressao_simples(p):
    '''expressao_simples : expressao_aditiva
                         | expressao_simples operador_relacional expressao_aditiva'''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = (p[1], p[2], p[3])

def p_expressao_aditiva(p):
    '''expressao_aditiva : expressao_multiplicativa
                         | expressao_aditiva operador_soma expressao_multiplicativa'''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = (p[1], p[2], p[3])

def p_expressao_multiplicativa(p):
    '''expressao_multiplicativa : expressao_unaria
                                | expressao_multiplicativa operador_multiplicacao expressao_unaria'''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = (p[1], p[2], p[3])

def p_expressao_unaria(p):
    '''expressao_unaria : fator
                        | operador_soma fator
                        | operador_negacao fator'''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = (p[1], p[2])

def p_operador_relacional(p):
    '''operador_relacional : MENOR
                           | MAIOR
                           | IGUALDADE
                           | MENOR_IGUAL
                           | MAIOR_IGUAL'''
    p[0] = p[1]

def p_operador_soma(p):
    '''operador_soma : SOMA
                     | SUBTRACAO'''
    p[0] = None

def p_operador_negacao(p):
    '''operador_negacao : NEGACAO'''
    p[0] = None

def p_operador_logico(p):
    '''operador_logico : E_LOGICO
                       | OU_LOGICO'''
    p[0] = None

def p_operador_multiplicacao(p):
    '''operador_multiplicacao : MULTIPLICACAO
                              | DIVISAO'''
    p[0] = None

def p_fator(p):
    '''fator : ABRE_PAR expressao FECHA_PAR
             | var
             | chamada_funcao
             | numero'''
    if len(p) == 4:
        p[0] = p[2]
    elif len(p) == 2:
        p[0] = p[1]

def p_numero(p):
    '''numero : NUM_INTEIRO
              | NUM_FLUTUANTE'''
    p[0] = None

def p_chamada_funcao(p):
    '''chamada_funcao : ID ABRE_COL lista_argumentos FECHA_COL'''
    p[0] = p[3]

def p_lista_argumentos(p):
    '''lista_argumentos : lista_argumentos VIRGULA expressao
                        | expressao
                        | vazio'''
    if len(p) == 4:
        p[0] = (p[1], p[3])
    elif len(p) == 2:
        p[0] = p[1]

def p_error(p):
    if p:
        print("Erro sintático na linha '%d': '%s'" % (p.lineno, p.value))
    else:
        yacc.restart()
        print("Erro sintático nas definições!")
        exit(1)

def p_vazio(p):
    'vazio :'
    pass

parser = yacc.yacc()
while True:
    try:
        s = input('')
    except EOFError:
        break
    if not s: continue
    result = parser.parse(s)
    print(result)

#O que falta:
#1) Fazer leitura do mesmo arquivo lido no scanner;
#2) Mostrar a árvore
#3) Verificar se os p[0] = (p[1], p[2]) funcionam
#4) Verificar se o p[0] = None funciona
#5) Arrumar comentario no scanner
#6) Relatório