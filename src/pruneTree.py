from anytree import Node, RenderTree, AsciiStyle, PreOrderIter, PostOrderIter
from anytree.exporter import DotExporter
from utils import name

def cutUselessElements(tree):
    for node in PostOrderIter(tree):
        if (name(node) == ':' or name(node) == ',' or name(node) == '(' or
            name(node) == ')' or name(node) == '[' or name(node) == ']' or
            name(node) == ':='):
            node.parent = None

def cutRepeatedElements(tree):
    for node in PostOrderIter(tree):
        no = node.parent

        if node.parent != None:
            father = name(node.parent)

            # Elimina um pai e leva seus filhos para outro pai
            if name(node) == father:
                node.parent = no.parent
                if len(no.children) > 0:
                    i = 0
                    while i < len(no.children):
                        no.children[i].parent = node
                        i += 1
                no.parent = None

def cutExpressionElements(tree):
    for node in PreOrderIter(tree):
        if name(node) == 'expressao' and len(node.children) > 0 and name(node.children[0]) == 'expressao_logica':
            for n in PreOrderIter(node):
                if name(n) == 'fator' and 'chamada_funcao' not in str(n.children):
                    n.parent = node
                    node.children[0].parent = None
                
                if name(n) == 'chamada_funcao':
                    father = n.parent
                    father.parent = node
                    node.children[0].parent = None
        
        if name(node) == 'lista_argumentos' and name(node.parent) == 'chamada_funcao':
            for n in PreOrderIter(node):
                if name(n) == 'expressao' and len(n.children) > 0 and name(n.children[0]) == 'expressao_logica':
                    for k in PreOrderIter(n):
                        if name(k) == 'fator':
                            k.parent = n
                            n.children[0].parent = None

def prune(tree):
    cutUselessElements(tree)
    cutRepeatedElements(tree)
    cutExpressionElements(tree)

    showPruneTree(tree)
    
    return tree

def showPruneTree(tree):
    DotExporter(tree).to_picture("pruneAst.png")