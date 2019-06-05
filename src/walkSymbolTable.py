from utils import walkTable, showErrors, getLine

def verifyReturn():
    content = walkTable()
    varTypes = []
    paramTypes = []

    for item in content:
        if 'info' in item and item['info'][0]['categoria'] == 'variavel':
            varTypes.append(item['info'][0]['lexema']+'-'+item['tipo'])
        if 'categoria' in item and item['categoria'] == 'funcao':
            if len(item['parametros']) > 0:
                for e in item['parametros']:
                    paramTypes.append(e['lexema']+'-'+e['tipo'])

    for item in content:
        if 'categoria' in item and item['categoria'] == 'funcao':
            if 'retorno' not in item:
                showErrors(0, 'err', item['lexema'], 2)
                exit(0)
            
            # continuar depois
            # for e in range(len(varTypes)):
            #     var = e.split('-')[0]
            #     tipo = e.split('-')[1]

            if (item['tipo'] == 'flutuante' or item['tipo'] == 'inteiro'):
                linha = getLine(item['retorno'][0]['elemento'])
                showErrors(linha, 'err', item['retorno'][0]['elemento'], 2)
                exit(0)
                
                
                # Vou ter que arrumar essa funcao, pois tenho que verificar qual o tipo do retorno quando ele for 'var'
                # Vou ter que fazer mais um for para procurar o tipo da variável que está sendo retornada

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
            