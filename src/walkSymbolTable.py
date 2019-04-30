from utils import walkTable, showErrors, getLine

def verifyReturn():
    content = walkTable()

    for item in content:
        if 'categoria' in item and item['categoria'] == 'funcao':
            if (item['tipo'] == 'flutuante' or item['tipo'] == 'inteiro') and item['retorno'][0]['tipo'] != 'numero':
                linha = getLine(item['retorno'][0]['elemento'])
                showErrors(linha, item['retorno'][0]['elemento'], 2)
                # Vou ter que arrumar essa funcao, pois tenho que verificar qual o tipo do retorno quando ele for 'var'
                # Vou ter que fazer mais um for para procurar o tipo da variável que está sendo retornada

def verifyFuncStatement():
    content = walkTable()
    funcs = []

    for item in content:
        if 'categoria' in item and item['categoria'] == 'funcao':
            funcs.append(item['lexema'])
    
    for i in range(0, len(funcs)):
        for j in range(0, i):
            if funcs[i] == funcs[j]:
                linha = getLine(funcs[i]) # Isso tem aque arrumar, pois não pega a linha do nome certo quando tem o nome repetido varias vezes
                showErrors(linha, funcs[i], 5)
                return
    
    print(funcs)