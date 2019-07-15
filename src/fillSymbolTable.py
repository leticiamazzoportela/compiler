from anytree import Node, PostOrderIter, PreOrderIter
from utils import name, getLine, showErrors, insertTable, walkTable, isFloat
from walkSymbolTable import verifyVarStatement, verifyFuncStatement, verifyReturn
import bkp
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
                if name(n) == 'tipo' and name(n.parent) == 'declaracao_funcao':
                    st['tipo'] = name(n.children[0])
                elif name(n) == 'cabecalho':
                    st['lexema'] = name(n.children[0])
                    
                    if 'tipo' not in str(n.siblings):
                        st['tipo'] = 'vazio'

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
                    newSize = -1
                    if name(e.children[0]) == 'None':
                        newSize = 0
                    else:
                        newSize = len(e.children)
                    if newSize != size:
                        linha = getLine(nameFunc)
                        showErrors(linha, 'err', nameFunc, 6)
                        exit(0)
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
    
    for func in funcsTable:
        if func not in funcsTree and func != 'principal':
            linha = getLine(func)
            showErrors(linha, 'warn', func, 8)

def verifyCallVar(tree):
    content = walkTable()
    varTable = []
    varTableTypes = []
    varTree = []
    params = []
    attrVar = []
    funcsTable = []
    exp = []
    temp = []

    for e in PreOrderIter(tree):
        if name(e) == 'var':
            varTree.append(name(e.children[0]))
            if 'escreva' in str(e.ancestors) or 'leia' in str(e.ancestors):
                temp.append(name(e.children[0]))
        if name(e) == 'indice':
            for i in PreOrderIter(e):
                if i.is_leaf and name(i.parent) != 'numero' or '.' in name(i):
                    showErrors(getLine(name(e.siblings[0])), 'err', name(e.siblings[0]), 13)
                    exit(0)
        if name(e) == 'var' and name(e.parent) == 'atribuicao':
            if ('operador_soma' not in str(e.parent.descendants) and
                'operador_multiplicacao' not in str(e.parent.descendants)):
                for i in PreOrderIter(e.siblings[0]):
                    if i.is_leaf and name(i.parent) != 'chamada_funcao':
                        attrVar.append(name(e.children[0])+'_'+name(i)+'_var')
                    elif i.is_leaf and name(i.parent) == 'chamada_funcao':
                        attrVar.append(name(e.children[0])+'_'+name(i)+'_func')
            else:
                for i in PreOrderIter(e.siblings[0]):
                    if name(i).startswith('operador_'):
                        for j in PreOrderIter(i.siblings[0]):
                            if j.is_leaf:
                                exp.append(name(e.children[0])+'_'+name(j))
                        for k in PreOrderIter(i.siblings[1]):
                            if k.is_leaf:
                                exp.append(name(e.children[0])+'_'+name(k))

    for item in content:
        if 'info' in item:
            if 'lexema' in item['info']:
                varTable.append(item['info']['lexema'])
                varTableTypes.append(item['info']['lexema']+'_'+item['tipo'])
            else:
                for e in range(len(item['info'])):
                    if 'lexema' in item['info'][e]:
                        varTable.append(item['info'][e]['lexema'])
                        varTableTypes.append(item['info'][e]['lexema']+'_'+item['tipo'])
        elif 'parametros' in item and len(item['parametros']) > 0:
            for e in range(len(item['parametros'])):
                params.append(item['parametros'][e]['lexema'])
        if 'categoria' in item and item['categoria'] == 'funcao':
            funcsTable.append(item['lexema']+'_'+item['tipo'])
    
    
    for e in varTableTypes:
        nameVt = e.split('_')[0]
        typeVt = e.split('_')[1]
        for i in attrVar:
            nameVar = i.split('_')[0]
            receptVar = i.split('_')[1]
            category = i.split('_')[2]
            if category == 'var' and nameVt == nameVar:
                for j in varTableTypes:
                    if j.split('_')[0] == receptVar and j.split('_')[1] != typeVt:
                        showErrors(getLine(nameVt), 'err', nameVt, 20)
                        exit(0)
                    elif receptVar.isdigit():
                        if typeVt != 'inteiro':
                            showErrors(getLine(nameVar), 'err', nameVar, 20)
                            exit(0)
                    elif isFloat(receptVar):
                        if typeVt != 'flutuante':
                            showErrors(getLine(nameVar), 'err', nameVar, 20)
                            exit(0)
                    
    for e in funcsTable:
        nameFunc = e.split('_')[0]
        typeFunc = e.split('_')[1]
        for i in attrVar:
            nameVar = i.split('_')[0]
            receptVar = i.split('_')[1]
            category = i.split('_')[2]
            for j in varTableTypes:
                if category == 'func' and nameFunc == receptVar and typeFunc != j.split('_')[1] and nameVar == j.split('_')[0]:
                    showErrors(getLine(nameVar), 'err', nameVar, 20)
                    exit(0)

    for e in varTableTypes:
        nameVt = e.split('_')[0]
        typeVt = e.split('_')[1]
        for j in exp:
            nameVar = j.split('_')[0]
            receptVar = j.split('_')[1]
            if nameVar == nameVt:
                for k in varTableTypes:
                    if k.split('_')[0] == receptVar and k.split('_')[1] != typeVt:
                        showErrors(getLine(nameVar), 'err', nameVar, 20)
                        exit(0)
            elif receptVar.isdigit():
                if typeVt != 'inteiro':
                    showErrors(getLine(nameVar), 'err', nameVar, 20)
                    exit(0)
            elif isFloat(receptVar):
                if typeVt != 'flutuante':
                    showErrors(getLine(nameVar), 'err', nameVar, 20)
                    exit(0)
    noRepeat = []
    
    for e in varTree:
        if varTree.count(e) == 1:
            noRepeat.append(e)

    for e in noRepeat:
        if e not in params and e in varTable:
            linha = getLine(e)
            showErrors(linha, 'warn', e, 21)
        
    for i in range(0, len(varTree)):
        element = varTree[i]
        if element not in varTable and element not in params:
            linha = getLine(element)
            showErrors(linha, 'err', element, 14)
            exit(0)

    for i in range(0, len(varTable)):
        element = varTable[i]
        if element not in varTree or element in temp and element not in attrVar:
            linha = getLine(element)
            showErrors(linha, 'warn', element, 1)

def semantic(tree):
    funcoes = findFunc(tree)
    variaveis = findVar(tree)

    insertTable(funcoes+variaveis)
    verifyParameters(tree)
    verifyFuncStatement()
    verifyCallFunc(tree)
    verifyVarStatement()
    verifyCallVar(tree)
    verifyReturn()

    print("____________* Executando Geração de Código *____________\n")
    
    bkp.funcDeclaration(tree) 