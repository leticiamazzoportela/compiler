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
            leaf_nodes.append(n_name[1]) # tipo
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
    temp = {}
    vars_func = []

    for n in PreOrderIter(node):
        n_name = n.name.split(".")
    
        if n_name[1] == 'corpo':
            for no in PreOrderIter(n):
                var_func = walk_subtree_var(no)
                no_name = no.name.split(".")
                if no_name[1] == 'declaracao_variaveis':
                    temp['tipo_var'] = var_func[0]
                    temp['nome_variavel'] = []

                    for i in range(1, len(var_func)):
                        temp['nome_variavel'].append(var_func[i])

                    vars_func.append(temp)

        # if n_name[1] == 'corpo' and 'declaracao_variaveis' in str(n.descendants):
    # print(vars_func)
    return vars_func

def declaracao_funcao(tree):
    sb = {}

    for node in PreOrderIter(tree):
        node_name = node.name.split(".")

        if node_name[1] == 'declaracao_funcao':
            leaf_nodes = walk_subtree_func(node)            
            body_func = walk_subtree_body_func(node)
            
            if leaf_nodes[0] != 'inteiro' and leaf_nodes[0] != 'flutuante':
                print("Erro semântico (linha X, Coluna Y): A função precisa ter um tipo válido")
                break
            elif any(d.get('nome_func', None) == leaf_nodes[1] for d in symbols_table):
                print("Erro semântico (linha X, Coluna Y): a função '%s' já foi declarada" % leaf_nodes[1])
                break
            # elif body_func['nome_variavel'][0] 
            else:
                sb['tipo_func'] = leaf_nodes[0]
                sb['nome_func'] = leaf_nodes[1]
                sb['param_func'] = leaf_nodes[2]
            
                # if 'inteiro' not in sb['param_func'].values() and 'flutuante' not in sb['param_func'].values() and 'None' not in sb['param_func'].values():
                #     print("Erro semântico (linha X, Coluna Y): Os parâmetros da função precisam ter um tipo válido")
                #     break

                sb['variaveis'] = body_func

                # FALTA:
                # verificar se var já foi declarada
                # se retorno bate com tipo da função
                # se condicionais estao certas
                # se tem função principal - impedir passagem de parametro
                # outras funções não chamam a principal, ela que chama as outras
                # warning para definicao de função e variaveis não utilizadas
                # variaveis estão recebendo coisas conforme o tipo
                # comparações estão certas -> tipos certos

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