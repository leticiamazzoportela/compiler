from anytree import Node, PostOrderIter, PreOrderIter
import json

# minha tabela tem que ser por linha! Exemplo: linha x, conteudo {...}; linha y, conteudo {...}
# Ainda não está assim, mas vou fazer

def findFunc(tree):
    st = {}
    cabecalho = {}

    cabecalho['conteudo'] = []
    
    for node in PreOrderIter(tree):
        node_name = node.name.split('.')[1]

        if node_name == 'declaracao':
            if node.children[0].name.split('.')[1] == 'declaracao_funcao':
                st['categoria'] = 'funcao'

                for n in PreOrderIter(node):
                    if n.is_leaf == True and n.parent.name.split('.')[1] == 'tipo':
                        st['tipo'] = n.name.split('.')[1]
                        st['linha'] = n.lineno
        
                cabecalho['conteudo'].append(st)
        st = {}
    

    with open('sb.json', 'w') as stFile:
        json.dump(cabecalho, stFile, indent=4)
            
# def findVar(tree):
