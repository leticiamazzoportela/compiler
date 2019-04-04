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
                            showErrors(linha, st['lexema'], 19)
                        if st['tipo'] != 'inteiro':
                            showErrors(linha, st['tipo'], 9)
                            return
            
            funcoes.append(st)
            st = {}
    
    insertTable(funcoes)
    # return funcoes - vou juntar todos os imports depois para fazer um arquivo só