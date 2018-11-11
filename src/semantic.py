# -*- coding: utf-8 -*-
from anytree import PreOrderIter, PostOrderIter, Node, RenderTree
from anytree.exporter import DotExporter
import sys
import json

symbols_table = []

def walk_tree(tree):
    for node in PostOrderIter(tree):
        node_name = node.name.split(".")

        if (node_name[1] == ':' or node_name[1] == ',' or node_name[1] == '(' or
            node_name[1] == ')' or node_name[1] == '[' or node_name[1] == ']' or
            node_name[1] == ':='):
            node.parent = None

    declaracao_variaveis(tree)
    declaracao_funcao(tree)
    run_semantic()

def walk_subtree_var(node):
    leaf_nodes = []
    for n in PreOrderIter(node):
        n_name = n.name.split(".")

        if 'indice' not in str(n.parent) and 'indice' not in str(n.siblings) and n.is_leaf == True:
            leaf_nodes.append(n_name[1])
        elif n_name[1] == 'var': # verifico as variaveis
            leaf_nodes_temp = ''
            for child in PreOrderIter(n):
                child_name = child.name.split(".")
                if child.is_leaf == True and 'indice' not in str(child.ancestors): # verifico se é só a variavel
                    leaf_nodes_temp = child_name[1]
                elif child.is_leaf == True and 'indice' in str(child.ancestors): # verifico se chegou no indice
                    leaf_nodes.append(leaf_nodes_temp + '['+child_name[1]+']')
    return leaf_nodes

def walk_subtree_func(node):
    leaf_nodes = []
    temp = {}

    for n in PreOrderIter(node):
        n_name = n.name.split(".")

        if n.is_leaf == True and 'cabecalho' not in str(n.ancestors):
            leaf_nodes.append(n_name[1]) # tipo
        elif n.is_leaf == True and 'cabecalho' in str(n.ancestors) and 'fim' in str(n.siblings) and 'lista_parametros' in str(n.siblings):
            leaf_nodes.append(n_name[1]) # nome
        elif n_name[1] == 'lista_parametros':
            for child in PreOrderIter(n):
                child_name = child.name.split(".")
                if child.is_leaf == True and 'tipo' in str(child.ancestors):
                    temp['tipo_param'] = child_name[1] # tipo param
                elif child.is_leaf == True and 'tipo' not in str(child.ancestors):
                    temp['nome_param'] = child_name[1] # nome param
                
                leaf_nodes.append(temp)

    return leaf_nodes

def walk_subtree_body_func(node):
    leaf_nodes = []

    for n in PreOrderIter(node):
        n_name = n.name.split(".")

        # if n_name[1] == 'corpo':
            # eu tenho que ver que se tem um tipo inteiro ou flutuante, tem retorno
            # ver as variaveis locais de cada função
    
    return leaf_nodes

def declaracao_funcao(tree):
    sb = {}

    for node in PreOrderIter(tree):
        node_name = node.name.split(".")

        if node_name[1] == 'declaracao_funcao':
            leaf_nodes = walk_subtree_func(node)            
            
            if len(leaf_nodes) <= 1: # se vier faltando um parametro, dará erro sintático ou semantico, se for semantico, esta faltando o tipo
                print("Erro semântico (linha X): A função precisa ter um tipo")
            else:
                sb['tipo_func'] = leaf_nodes[0]
                sb['nome_func'] = leaf_nodes[1]
                sb['param_func'] = leaf_nodes[2]
                
                # if sb['tipo_func'] == 'inteiro' or sb['tipo_func'] != 'flutuante':

                symbols_table.append(sb)
                sb = {}

    # print(json.dumps(symbols_table, indent=4))


def declaracao_variaveis(tree):
    sb = {}

    for node in PreOrderIter(tree):
        node_name = node.name.split(".")
        p = str(node.parent)
        leaf_nodes = walk_subtree_var(node)

        if node_name[1] == 'declaracao_variaveis':
            if 'declaracao_funcao' not in p: # verifico se é uma declaracao global
                sb['tipo'] = leaf_nodes[0]
                sb['nome_variavel'] = []

                for i in range(1, len(leaf_nodes)):
                    sb['nome_variavel'].append(leaf_nodes[i])

                symbols_table.append(sb)
                sb = {}
            # elif:

def run_semantic():
    print(json.dumps(symbols_table, indent=4))

    # DotExporter(tree).to_picture("astNova.png")