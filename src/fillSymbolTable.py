from anytree import Node, PostOrderIter, PreOrderIter
from utils import name, getLine, showErrors, insertTable, walkTable
import json
from sys import exit

def findFunc(tree):
    st = {}
    funcoes = []
    retorno = False

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
                            showErrors(linha, 'err', st['parametros'][0]['tipo'], 19)
                            exit(0)
    
                        if st['tipo'] != 'inteiro':
                            showErrors(linha, 'err', st['tipo'], 9)
                            exit(0)

                elif name(n) == 'corpo' and len(st['lexema']) >= 2:
                    for e in PreOrderIter(n):
                        if name(e) == 'chamada_funcao':
                            if e.children[0].is_leaf:
                                linha = e.children[0].lineno - 21
                            
                            if 'principal' in str(e.children):
                                if st['lexema'] != 'principal':
                                    linha = getLine('principal')
                                    showErrors(linha, 'err', 'principal', 3)
                                else:
                                    showErrors(linha, 'err', 'principal', 4)
                                exit(0)
                            
                        if name(e) == 'retorna':
                            retorno = True
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
                        if len(n.children) >= 1:
                            if name(e) == 'var':
                                dados['lexema'] = name(e.children[0])   
                                for i in PreOrderIter(e):
                                    if name(i.parent) == 'fator' and i.children[0].is_leaf:
                                        linha = getLine(dados['lexema'])
                                        
                                        if name(i) != 'numero' or '.' in name(i.children[0]):
                                            showErrors(linha, 'err', dados['lexema']+'['+name(i.children[0])+']', 13)
                                            exit(0)

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
    verifyCallFunc(tree)
    verifyCallVar(tree)

def verifyParameters(tree):
    content = walkTable()
    size = 0
    args = []
    params = []
    argsComp = []
    p = {}
    a = {}
    ags = {}

    for item in content:
        if 'categoria' in item and item['categoria'] == 'funcao':
            size = len(item['parametros'])
            nameFunc = item['lexema']

            if size > 0:
                p['func'] = nameFunc
                p['tipo'] = item['parametros'][0]['tipo']
                p['nome'] = item['parametros'][0]['lexema']
                params.append(p)
                p = {}
    
            for e in PreOrderIter(tree):
                if name(e) == 'lista_argumentos' and name(e.siblings[0]) == nameFunc:
                    if len(e.children) != size:
                        linha = getLine(nameFunc)
                        showErrors(linha, 'err', nameFunc, 6)
                    else:
                        for i in PreOrderIter(e):
                            if i.is_leaf and name(i.parent) == 'var':
                                a['func'] = nameFunc
                                a['nome'] = name(i)
                                args.append(a)
                                a = {}
    for item in content:
        if 'info' in item:
            if 'lexema' in item['info']:
                for a in args:
                    if a['nome'] == item['info']['lexema']:
                        ags['func'] = a['func']
                        ags['nome'] = a['nome']
                        ags['tipo'] = item['tipo']

                        argsComp.append(ags)
                        ags = {}
            else:
                for e in range(len(item['info'])):
                    if 'lexema' in item['info'][e]:
                        for a in args:
                            if a['nome'] == item['info'][e]['lexema']:
                                ags['func'] = a['func']
                                ags['nome'] = a['nome']
                                ags['tipo'] = item['tipo']

                                argsComp.append(ags)
                                ags = {}            

    for e in params:
        for i in argsComp:
            if e['func'] == i['func'] and e['tipo'] != i['tipo']:
                showErrors(getLine(e['func']), 'err', e['func'], 7)
                exit(0)


def verifyCallFunc(tree):
    content = walkTable()
    funcsTable = []
    funcsTree = []

    for item in content:
        if 'categoria' in item and item['categoria'] == 'funcao':
            funcsTable.append(item['lexema'])
    
    for e in PreOrderIter(tree):
        if name(e) == 'chamada_funcao':
            funcsTree.append(name(e.children[0]))
    
    for func in funcsTree:
        if func not in funcsTable:
            linha = getLine(func)
            showErrors(linha, 'err', func, 10)
            exit(0)

def verifyCallVar(tree):
    content = walkTable()
    varTable = []
    varTree = []
    params = []

    for item in content:
        if 'info' in item:
            if 'lexema' in item['info']:
                varTable.append(item['info']['lexema'])
            else:
                for e in range(len(item['info'])):
                    if 'lexema' in item['info'][e]:
                        varTable.append(item['info'][e]['lexema'])
        elif 'parametros' in item and len(item['parametros']) > 0:
            params.append(item['parametros'][0]['lexema'])
    
    for e in PreOrderIter(tree):
        if name(e) == 'var' and name(e.parent) == 'atribuicao':
            varTree.append(name(e.children[0]))

    for i in range(0, len(varTree)):
        element = varTree[i]
        if element not in varTable and element not in params:
            linha = getLine(element)
            showErrors(linha, 'err', element, 14)
            exit(0)
    
    for i in range(0, len(varTable)):
        element = varTable[i]
        if element not in varTree:
            linha = getLine(element)
            showErrors(linha, 'warn', element, 1)
    

## AVISOS
### 8

## FALTA
### ERROS: 12, arrumar 2 (por exemplo, se declaro uma funcao vazia, sem retornar nada, buga tudo)
### Salvar if else na tabela de simbolo, laco de repeticao na tabela