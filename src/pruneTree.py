from anytree import Node, RenderTree, AsciiStyle, PreOrderIter, PostOrderIter
from anytree.exporter import DotExporter
from utils import name
import re

def cutUselessElements(tree):
    for node in PostOrderIter(tree):
        if (name(node) == ':' or name(node) == ',' or name(node) == '(' or
            name(node) == ')' or name(node) == '[' or name(node) == ']' or
            name(node) == ':='):
            node.parent = None

def cutRepeatedElements(tree):
    for node in PostOrderIter(tree):
        no = node.parent # pai no atual

        if node.parent != None:
            father = name(node.parent) # nome pai no atual

            # Elimina um pai e leva seus filhos para o vô
            if name(node) == father: # no autal == pai
                node.parent = no.parent # meu novo pai e meu vo
                if len(no.children) > 0:
                    for item in no.children:
                        item.parent = node
                # if len(no.children) > 0: # tamanho peu pai antigo
                #     i = 0
                #     while i < len(no.children): # varios filhos meu pai antigo
                #         no.children[i].parent = node ## os filhos do meu pai antigo vem para mim
                #         i += 1

                no.parent = None ## pai antigo retirado

def cutExpressionElements(tree):
    for node in PreOrderIter(tree):
        if name(node) == 'expressao' and len(node.children) > 0 and name(node.children[0]) == 'expressao_logica':
            for n in PreOrderIter(node):
                if name(n) == 'expressao_aditiva':
                    n.parent = node
                    node.children[0].parent = None
                        
        #         if name(n) == 'chamada_funcao':
        #             father = n.parent
        #             father.parent = node
        #             node.children[0].parent = None
        
        # if name(node) == 'lista_argumentos' and name(node.parent) == 'chamada_funcao':
        #     for n in PreOrderIter(node):
        #         if name(n) == 'expressao' and len(n.children) > 0 and name(n.children[0]) == 'expressao_logica':
        #             for k in PreOrderIter(n):
        #                 if name(k) == 'fator':
        #                     k.parent = n
        #                     n.children[0].parent = None

def prune(tree):
    cutUselessElements(tree)
    cutRepeatedElements(tree)
    # cutExpressionElements(tree)

    showPruneTree(tree)
    
    return tree

def showPruneTree(tree):
    DotExporter(tree).to_picture("pruneAst.png")