from anytree import Node, PostOrderIter, PreOrderIter
from utils import name, getLine, showErrors, insertTable, walkTable
import json

def findFunc(tree):
    st = {}
    funcoes = []

    for node in PreOrderIter(tree):
        st['categoria'] = 'funcao'
        node_name = name(node)

        if node_name == 'declaracao_funcao':
            for n in PreOrderIter(node):
                if name(n) == 'tipo':
                    st['tipo'] = name(n.children[0])
                elif name(n) == 'cabecalho':
                    st['lexema'] = name(n.children[0])

                    if 'parametro' in str(n.children):
                        parametros = {}
                        st['parametros'] = []
                        for e in PreOrderIter(n):
                            father = e.parent
                            if name(father) == 'tipo' and name(father.parent) == 'parametro':
                                parametros['tipo'] = name(e)
                                parametros['lexema'] = name(e.parent.siblings[0])
                            
                                st['parametros'].append(parametros)
                            parametros = {}
                    
                    if st['lexema'] == 'principal':
                        linha = getLine('principal')
                        if len(st['parametros']) >= 1:
                            showErrors(linha, st['parametros'][0]['tipo'], 19)
    
                        if st['tipo'] != 'inteiro':
                            showErrors(linha, st['tipo'], 9)
                            return

                elif name(n) == 'corpo' and len(st['lexema']) >= 2:
                    for e in PreOrderIter(n):
                        if name(e) == 'chamada_funcao':
                            if e.children[0].is_leaf:
                                linha = e.children[0].lineno - 21
                            
                            if 'principal' in str(e.children):
                                if st['lexema'] != 'principal':
                                    linha = getLine('principal')
                                    showErrors(linha, 'principal', 3)
                                else:
                                    showErrors(linha, 'principal', 4)
                                return

                        if name(e) == 'retorna':
                            st['retorno'] = []
                            retorno = {}
                            for child in PreOrderIter(e):
                                if (child.is_leaf):
                                    retorno['tipo'] = name(child.parent)
                                    retorno['elemento'] = name(child)

                                    st['retorno'].append(retorno)
                                retorno = {}
            
            
            funcoes.append(st)
            st = {}
    
    return funcoes 

def findVar(tree):
    st = {}
    variaveis = []

    for node in PreOrderIter(tree):
        node_name = name(node)

        if node_name == 'declaracao_variaveis':
            for n in PreOrderIter(node):
                if name(n) == 'tipo':
                    st['tipo'] = name(n.children[0])

                    if 'declaracao_funcao' not in str(n.ancestors):
                        st['escopo'] = 'global'
                    else:
                        st['escopo'] = 'local'
                elif name(n) == 'lista_variaveis':
                    dados = {}
                    st['info'] = []

                    for e in PreOrderIter(n):
                        if len(n.children) >= 2:
                            if name(e) == 'var':
                                dados['lexema'] = name(e.children[0])   
                                
                                for i in PreOrderIter(e):
                                    if name(i.parent) == 'fator' and i.children[0].is_leaf:
                                        linha = i.children[0].lineno - 20
                                        
                                        if name(i) != 'numero':
                                            showErrors(linha, name(i.children[0]), 13)
                                            return

                                        dados['categoria'] = 'vetor'
                                        dados['dimensao'] = name(i.children[0])
                                            
                                    elif name(i.parent) == 'var':
                                        dados['categoria'] = 'variavel'
                                
                                st['info'].append(dados)
                                dados = {}
                        else:
                            dados['lexema'] = name(e)
                            dados['categoria'] = 'variavel'

                            st['info'] = dados
                            dados = {}

            variaveis.append(st)
            st = {}

    return variaveis

def fillSymbolTable(tree):
    funcoes = findFunc(tree)
    variaveis = findVar(tree)

    insertTable(funcoes+variaveis)
    verifyParameters(tree)

def verifyParameters(tree):
    content = walkTable()
    size = 0

    for item in content:
        if 'categoria' in item and item['categoria'] == 'funcao':
            size = len(item['parametros'])
            nameFunc = item['lexema']
    
            for e in PreOrderIter(tree):
                if name(e) == 'lista_argumentos' and name(e.siblings[0]) == nameFunc:
                    if len(e.children) != size:
                        linha = getLine(nameFunc) # problema da linha
                        showErrors(linha, nameFunc, 6)
                    
## ERROS TRATADOS:
# 19, 9, 3, 4, 13, 2(+-), 5, 6

## Em todos tem o problema da linha

## ERROS PARA TRATAR ANDANDO NA TABELA COMPLETA
# 7, 10, 11, 12, 14, 15, 16, 17, 18