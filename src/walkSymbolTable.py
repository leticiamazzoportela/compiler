from utils import walkTable, showErrors, getLine

def verifyReturn():
    content = walkTable()
    varTypes = []
    paramTypes = []
    retorno = []

    for item in content:
        if 'info' in item and item['info'][0]['categoria'] == 'variavel':
            varTypes.append(item['info'][0]['lexema']+'-'+item['tipo'])

        if 'categoria' in item and item['categoria'] == 'funcao':
            if len(item['parametros']) > 0:
                for e in item['parametros']:
                    paramTypes.append(e['lexema']+'-'+e['tipo'])

        if 'retorno' in item:
            for r in item['retorno']:
                retorno.append(r['elemento'])

    for item in content:
        if 'categoria' in item and item['categoria'] == 'funcao':
            if 'retorno' not in item:
                showErrors(0, 'err', item['lexema'], 2)
                exit(0)
          
            for e in range(len(varTypes)):
                for i in range(len(paramTypes)):
                    var = varTypes[e].split('-')[0]
                    param = paramTypes[i].split('-')[0]
                    tipo = varTypes[e].split('-')[1]
                    tipoP = paramTypes[i].split('-')[1]

                    if var in retorno and tipo != item['tipo']:
                        showErrors(getLine(var), 'err', var, 2)
                        exit(0)
                    elif param in retorno and tipoP != item['tipo']:
                        showErrors(getLine(param), 'err', param, 2)
                        exit(0)
            
            for r in retorno:
                if '.' in r and item['tipo'] == 'inteiro':
                    showErrors(getLine('retorna'), 'err', r, 2)
                    exit(0)
                elif '.' not in r and item['tipo'] == 'flutuante':
                    showErrors(getLine('retorna'), 'err', r, 2)
                    exit(0)
                    

def verifyFuncStatement():
    content = walkTable()
    funcs = []

    for item in content:
        if 'categoria' in item and item['categoria'] == 'funcao':
            funcs.append(item['lexema'])
    
    if 'principal' not in funcs:
        showErrors('-', 'err', 'programa', 18)
        exit(0)
    
    for i in range(0, len(funcs)):
        for j in range(0, i):
            if funcs[i] == funcs[j]:
                linha = getLine(funcs[i])
                showErrors(linha, 'err', funcs[i], 5)
                exit(0)
    


def verifyVarStatement():
    content = walkTable()
    var = []

    for item in content:
        if 'info' in item:
            if 'lexema' in item['info']:
                var.append(item['info']['lexema']+'-'+item['escopo'])
            else:
                for e in range(len(item['info'])):
                    if 'lexema' in item['info'][e]:
                        var.append(item['info'][e]['lexema']+'-'+item['escopo'])

    for i in range(0, len(var)):
        elementi = var[i].split('-')[0]
        escopo = var[i].split('-')[1]

        for j in range(0, i):
            elementj = var[j].split('-')[0]
            escopoSec = var[j].split('-')[1]

            if (var[i] == var[j] or (elementi == elementj and escopo != escopoSec)):
                linha = getLine(elementi)
                showErrors(linha, 'err', elementi, 11)
                exit(0)
            