from anytree import Node, PostOrderIter, PreOrderIter
import json


                    # st['linha'] = n.lineno
                    # st['posicao'] = '-'
                    # st['categoria'] = 'funcao'
                    # st['parametros'] = 'lista'
                    # st['tipo'] = name(n)
                    # st['token'] = name(n)
                    # st['lexema'] = 'estou confusa'
                    # st['escopo'] = 'nao sei ainda'
                    # st['utilizado'] = 'averiguar'
def name(node):
    node_name = node.name.split('.')[1]
    return node_name

def showErrors(line, element, code):
    with open('errors.json', 'r') as f:
        errors = json.loads(f.read())
        
    print('****ERRO SEMÂNTICO***\n')
    for error in errors:
        if error['code'] == code:
            print('Linha: '+str(line)+'\nElemento: '+str(element)+'\nDescrição: '+str(error['message']))
            print('\n************\n')

def insertTable(content):
    with open('symbols_table_complete.json', 'w') as f:
        json.dump(content, f, indent=4)

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

                    if 'parametro' in n.children:
                        parametros = {}
                        for e in PreOrderIter(n):
                            if name(e.parent) == 'tipo':
                                parametros['tipo'] = name(e)
                                parametros['lexema'] = name(e.parent.siblings[0])
                            
                            st['parametros'].append(parametros)
                            parametros = {}
                    else:
                        showErrors(6, name(n), 1)
    
            funcoes.append(st)
            st = {}
    
    insertTable(funcoes)
    # return funcoes