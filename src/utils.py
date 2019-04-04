import json

def name(node):
    node_name = node.name.split('.')[1]
    return node_name

def getLine(element):
    with open('symbols_table.json', 'r') as f:
        tokens = json.loads(f.read())
    
    for tok in tokens:
        for x in tok['conteudo']:
            if x['token'] == 'ID' and x['lexema'] == element:
                return tok['linha']
        
    return None

def showErrors(line, element, code):
    with open('errors.json', 'r') as f:
        errors = json.loads(f.read())
        
    print('****ERRO SEMÂNTICO***\n')
    for error in errors:
        if error['code'] == code:
            print('Linha: '+str(line)+'\nElemento: '+'"'+str(element)+'"'+'\nDescrição: '+str(error['message']))
            print('\n************\n')

def insertTable(content):
    with open('symbols_table_complete.json', 'w') as f:
        json.dump(content, f, indent=4)