from anytree import Node, PostOrderIter, PreOrderIter
from utils import name, getLine, showErrors, insertTable
import json

def findFunc(tree):
    st = {}
    funcoes = []

    for node in PreOrderIter(tree):
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
                            if name(e.parent) == 'tipo':
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

                elif name(n) == 'corpo' and len(st['lexema']) >=2:
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
                    
            
            funcoes.append(st)
            st = {}
    
    insertTable(funcoes)
    # return funcoes - vou juntar todos os imports depois para fazer um arquivo só

## ERROS TRATADOS:
# 19, 9, 3, 4
# TRATAR: 12, 13
## ERROS PARA TRATAR ANDANDO NA TABELA COMPLETA
# 1, 2, 5, 6?, 7?, 10, 11, 14, 15, 16, 17, 18