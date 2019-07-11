import json
from termcolor import colored

def name(node):
    node_name = node.name.split('#')[1]
    return node_name

def walkTable():
    with open('symbols_table_complete.json', 'r') as f:
        content = json.loads(f.read())
    
        return content

def getLine(element):
    with open('symbols_table.json', 'r') as f:
        tokens = json.loads(f.read())
    
    for tok in tokens:
        for x in tok['conteudo']:
            if x['token'] == 'ID' and x['lexema'] == element:
                return tok['linha']
        
    return None

def showErrors(line, tipo, element, code):
    with open('errors.json', 'r') as f:
        errors = json.loads(f.read())
    
    color = ''
    if tipo == 'err':
        color = 'red'
        print(colored('****ERRO SEMÂNTICO***\n', color))

    else:
        color = 'yellow'
        print(colored('****AVISO***\n', color))

    for error in errors:
        if error['code'] == code:
            print(colored('Linha: '+str(line)+'\nElemento: '+'"'+str(element)+'"'+'\nDescrição: '+str(error['message']), color))
            print(colored('\n************\n', color))

def insertTable(content):
    with open('symbols_table_complete.json', 'w') as f:
        json.dump(content, f, indent=4)

def isFloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

def listVar(content):
    varTableTypes = []
    for item in content:
        if 'info' in item:
            if 'lexema' in item['info']:
                if item['categoria'] == 'variavel':
                    varTableTypes.append(item['info']['lexema']+'_'+item['tipo']+'_'+item['categoria']+'_'+'-1')
                else:
                    varTableTypes.append(item['info']['lexema']+'_'+item['tipo']+'_'+item['categoria']+'_'+item['dimensao'])
            else:
                for e in range(len(item['info'])):
                    if 'lexema' in item['info'][e]:
                        if item['categoria'] == 'variavel':
                            varTableTypes.append(item['info'][e]['lexema']+'_'+item['tipo']+'_'+item['categoria']+'_'+'-1')
                        else:
                            varTableTypes.append(item['info'][e]['lexema']+'_'+item['tipo']+'_'+item['categoria']+'_'+item['dimensao'])
    return varTableTypes
