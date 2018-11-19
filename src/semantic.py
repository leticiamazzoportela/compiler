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

def walk_subtree_call_func(node):
    call_func = []

    for n in PreOrderIter(node):
        n_name = n.name.split(".")

        if n_name[1] == 'corpo':
            for no in PreOrderIter(n):
                no_name = no.name.split(".")
                if no_name[1] == 'chamada_funcao':
                    for nd in PreOrderIter(no):
                        nd_name = nd.name.split(".")
                        if nd.is_leaf == True:
                            call_func.append(nd_name[1])
    return call_func

def declaracao_funcao(tree):
    sb = {}
    ln = []
    for node in PreOrderIter(tree):
        node_name = node.name.split(".")
        if node_name[1] == 'declaracao_funcao':
            ln = walk_subtree_func(node)

    if 'principal' not in ln:
        print("Erro semântico (linha X, Coluna Y): O programa precisa ter uma função principal!")
        return
    else:
        for node in PreOrderIter(tree):
            node_name = node.name.split(".")

            if node_name[1] == 'declaracao_funcao':
                leaf_nodes = walk_subtree_func(node)            
                body_func = walk_subtree_body_func(node)
                func = walk_subtree_call_func(node)
                print(func)
                if any(d.get('nome_func', None) == leaf_nodes[1] for d in symbols_table):
                    print("Erro semântico (linha X, Coluna Y): A função '%s' já foi declarada!" % leaf_nodes[1])
                    return
                elif str(leaf_nodes[1]) == 'principal' and len(leaf_nodes[2]) > 1:
                    print("Erro semântico (linha X, Coluna Y): A função principal não recebe parâmetros!")
                    return
                elif str(leaf_nodes[1]) != 'principal' and 'principal' in func:
                    print("Erro semântico (linha X, Coluna Y): A função principal não pode ser invocada por outras funções!")
                    return
                else:
                    sb['tipo_func'] = leaf_nodes[0]
                    sb['nome_func'] = leaf_nodes[1]
                    sb['param_func'] = leaf_nodes[2]
                    # for item in sb['param_func']:
                    #     print(item)
                    
                    # if sb['param_func'].__contains__(
                    #         'tipo_param') and 'inteiro' not in sb['param_func']['tipo_param'] and 'flutuante' not in sb['param_func']['tipo_param'] and 'None' not in sb['param_func']['tipo_param']:
                    #     print("Erro semântico (linha X, Coluna Y): Os parâmetros da função precisam ter um tipo válido")
                    #     break
                    
                    sb['variaveis'] = body_func
                    for j in range(0, len(symbols_table)):
                        for i in range(0, len(sb['variaveis'])):
                            for k in sb['variaveis'][i]['nome_variavel']: 
                                if k in symbols_table[j]['nome_variavel']:
                                    print("Erro semântico (linha X, Coluna Y): A variável '%s' já foi declarada" % k)
                                    return
                    
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

# TODO verificar qtd de parametros - tem 3, devem ser passados 3
# TODO warning para definicao de função e variaveis não utilizadas
# TODO variaveis estão recebendo coisas conforme o tipo
# TODO se retorno bate com tipo da função - comparar subarvore do retorno com a do parametro da funcao
# TODO se condicionais estao certas
# TODO comparações estão certas -> tipos certos