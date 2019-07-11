from llvmlite import ir
from anytree import Node, PreOrderIter
import utils as ut

# def createModule():
#     module = ir.Module('meu_modulo.bc')
#     arquivo = open('meu_modulo.ll', 'w')
#     arquivo.write(str(module))
#     arquivo.close()
#     print(module)

module = ir.Module('meu_modulo.bc')
arquivo = open('meu_modulo.ll', 'w')
arquivo.write(str(module))
arquivo.close()
print(module)

def walkingTree(tree, builder):
    for node in PreOrderIter(tree):
        node_name = ut.name(node)

        if node_name == 'declaracao_variaveis':
            varDeclaration(node, builder)
        if node_name == 'declaracao_funcao':
            funcDeclaration(node)
        # if node_name =='expressao':
            # expression(node)
        # if node_name == 'se':
            # conditional(node)
        # if node_name == 'chamada_funcao':
            # callFunc(node)
        # if node_name == 'repita':
            # loop(node)

def globalVarDeclaration(node):
    content = ut.walkTable()
    varTypes = ut.listVar(content)

    for n in varTypes:
        nome = n.split("_")[0]
        tipo = n.split("_")[1]
        categoria = n.split("_")[2]
        if n.split("_")[3] != '-1':
            dimensao = n.split("_")[3]

        if tipo == 'inteiro' and categoria == 'variavel':
            varI = ir.GlobalVariable(module, ir.IntType(32), nome)  # Variável inteira global
            varI.initializer = ir.Constant(ir.IntType(32), 0)  # Inicializa a variavel g
            varI.linkage = "common"  # Linkage = common
            varI.align = 4  # Define o alinhamento em 4
            # self.global_var[nome] = g
            # self.vars.append(nome)
        elif tipo == 'inteiro' and categoria == 'vetor':
            vetI = ir.GlobalVariable(module, ir.ArrayType(element=ir.IntType(32), count=int(dimensao)), nome)
            vetI.initializer = ir.Constant(ir.ArrayType(element=ir.IntType(32), count=int(dimensao)), None)
            vetI.linkage = "common"
            vetI.align = 4
            # self.global_var[w.type] = tempRef
        elif tipo == 'flutuante' and categoria == 'variavel':
            varF = ir.GlobalVariable(module, ir.DoubleType(), nome)
            varF.initializer = ir.Constant(ir.DoubleType(), 0.0)
            varF.linkage = "common"
            varF.align = 4
            # self.global_var[nome] = g
            # self.vars.append(nome)
        elif tipo == 'flutuante' and categoria == 'vetor':
            vetF = ir.GlobalVariable(module, ir.ArrayType(element=ir.DoubleType(), count=int(dimensao)), nome)
            vetF.initializer = ir.Constant(ir.ArrayType(element=ir.DoubleType(), count=int(dimensao)), None)
            vetF.linkage = "common"
            vetF.align = 4

def varDeclaration(node, builder):
    content = ut.walkTable()
    varTypes = ut.listVar(content)

    for n in varTypes:
        nome = n.split("_")[0]
        tipo = n.split("_")[1]
        categoria = n.split("_")[2]
        if n.split("_")[3] != '-1':
            dimensao = n.split("_")[3]

        if tipo == 'inteiro' and categoria == 'variavel':
            varI = builder.alloca(ir.IntType(32), name=nome)
            varI.align = 4
        elif tipo == 'inteiro' and categoria == 'vetor':
            vetI = builder.alloca(ir.ArrayType(element=ir.IntType(32), count=int(dimensao), name=nome))
            vetI.align = 4
        elif tipo == 'flutuante' and categoria == 'variavel':
            vetF = builder.alloca(ir.ArrayType(element=ir.DoubleType(), count=int(dimensao), name=nome))
            vetF.align = 4
        elif tipo == 'flutuante' and categoria == 'vetor':
            varF = builder.alloca(ir.DoubleType(), name=nome)
            varF.align = 4

def funcDeclaration(node):
    content = ut.walkTable()
    parametros = []
    retorno = []
    funcType = ''

    for item in content:
        if 'categoria' in item and item['categoria'] == 'funcao':
            if len(item['parametros']) > 0:
                for p in item['parametros']:
                    if p['tipo'] == 'inteiro':
                        parametros.append(ir.IntType(32))
                    elif p['tipo'] == 'flutuante':
                        parametros.append(ir.DoubleType())
            if item['tipo'] == 'inteiro':
                funcType = ir.FunctionType(ir.IntType(32), (parametros))
            elif item['tipo'] == 'flutuante':
                funcType = ir.FunctionType(ir.DoubleType(), (parametros))
            else:
                funcType = ir.FunctionType(ir.VoidType(), (parametros))
    
        func = ir.Function(module, funcType, item['lexema'])
        entryBlock = func.append_basic_block('inicio' + item['lexema'])
        builder = ir.IRBuilder(entryBlock)

        if item['tipo'] == 'inteiro':
            retFunc = builder.alloca(ir.IntType(32), name='ret')
        elif item['tipo']  == 'flutuante':
            retFunc = builder.alloca(ir.DoubleType(), name='ret')

        for arg, name in zip(func.args, [p[0] for p in item['parametros']]):
            arg.name = name
        
        for a in func.args:
            f = builder.alloca(a.type, name=a.name)
            f.align = 4
            builder.store(a, f)
        
        endBlock = func.append_basic_block('fim' +item['lexema'])

        walkingTree(node, builder)

        builder.branch(endBlock)
        builder.position_at_end(endBlock)
        if item['tipo'] != 'inteiro' and item['tipo'] == 'flutuante':
            builder.ret_void()
        else:
            r = builder.load(retFunc)
            builder.ret(r)

