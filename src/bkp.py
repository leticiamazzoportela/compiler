from llvmlite import ir
from anytree import Node, PreOrderIter
import utils as ut

module = ir.Module('meu_modulo.bc')
arquivo = open('meu_modulo.ll', 'w')

locais = {}
globais = {}
funcoes = []

global funcs
funcs = None

global retFunc
retFunc = None

global size
size = 1

def walkingTree(tree, builder):
    for node in PreOrderIter(tree):
        node_name = ut.name(node)

        if node_name == 'chamada_funcao':
            callFunc(node, builder)
        if node_name == 'atribuicao':
            atribution(node, builder)
        if node_name == 'se':
            conditional(node, builder)
        if node_name == 'repita':
            loop(node, builder)
        if node_name == 'retorna':
            returnFunc(node, builder)
        if node_name == 'leia':
            printFunc(node, builder)
        if node_name == 'escreva':
            readFunc(node, builder)

def globalVarDeclaration():
    content = ut.walkTable()
    varTypes = ut.listVar(content)

    for n in varTypes:
        nome = n.split("_")[0]
        tipo = n.split("_")[1]
        categoria = n.split("_")[2]
        if n.split("_")[3] != '-1':
            dimensao = n.split("_")[3]
        escopo = n.split("_")[4]
        
        if escopo == 'global':
            if tipo == 'inteiro' and categoria == 'variavel':
                varI = ir.GlobalVariable(module, ir.IntType(32), nome)  # Variável inteira global
                varI.initializer = ir.Constant(ir.IntType(32), 0)  # Inicializa a variavel g
                varI.linkage = "common"  # Linkage = common
                varI.align = 4  # Define o alinhamento em 4
                globais[nome] = varI
                # self.vars.append(nome)
            elif tipo == 'inteiro' and categoria == 'vetor':
                vetI = ir.GlobalVariable(module, ir.ArrayType(element=ir.IntType(32), count=int(dimensao)), nome)
                vetI.initializer = ir.Constant(ir.ArrayType(element=ir.IntType(32), count=int(dimensao)), None)
                vetI.linkage = "common"
                vetI.align = 4
                globais[nome] = vetI
            elif tipo == 'flutuante' and categoria == 'variavel':
                varF = ir.GlobalVariable(module, ir.DoubleType(), nome)
                varF.initializer = ir.Constant(ir.DoubleType(), 0.0)
                varF.linkage = "common"
                varF.align = 4
                globais[nome] = varF
            elif tipo == 'flutuante' and categoria == 'vetor':
                vetF = ir.GlobalVariable(module, ir.ArrayType(element=ir.DoubleType(), count=int(dimensao)), nome)
                vetF.initializer = ir.Constant(ir.ArrayType(element=ir.DoubleType(), count=int(dimensao)), None)
                vetF.linkage = "common"
                vetF.align = 4
                globais[nome] = vetF

def varDeclaration(node, builder):
    content = ut.walkTable()
    varTypes = ut.listVar(content)

    for n in varTypes:
        nome = n.split("_")[0]
        tipo = n.split("_")[1]
        categoria = n.split("_")[2]
        dimensao = 0
        if n.split("_")[3] != '-1':
            dimensao = n.split("_")[3]
        escopo = n.split("_")[4]

        if escopo != 'global':
            if tipo == 'inteiro' and categoria == 'variavel':
                varI = builder.alloca(ir.IntType(32), name=nome)
                varI.align = 4
                locais[nome] = varI
            elif tipo == 'inteiro' and categoria == 'vetor':
                vetI = builder.alloca(ir.ArrayType(element=ir.IntType(32), count=int(dimensao)), name=nome)
                vetI.align = 4
                locais[nome] = vetI
            elif tipo == 'flutuante' and categoria == 'vetor':
                vetF = builder.alloca(ir.ArrayType(element=ir.DoubleType(), count=int(dimensao)), name=nome)
                vetF.align = 4
                locais[nome] = vetF
            elif tipo == 'flutuante' and categoria == 'variavel':
                varF = builder.alloca(ir.DoubleType(), name=nome)
                varF.align = 4
                locais[nome] = varF

def funcDeclaration(node):
    content = ut.walkTable()
    retorno = None
    parametros = []
    nameFunc = ''
    funcType = ''
    global retFunc
    global funcs

    globalVarDeclaration()

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
                retorno = ir.IntType(32)
            elif item['tipo'] == 'flutuante':
                funcType = ir.FunctionType(ir.DoubleType(), (parametros))
                retorno = ir.DoubleType()
            else:
                funcType = ir.FunctionType(ir.VoidType(), (parametros))

            nameFunc = item['lexema'] if item['lexema'] != 'principal' else 'main'    

    func = ir.Function(module, funcType, name=nameFunc)
    entryBlock = func.append_basic_block('inicio' + nameFunc)
    builder = ir.IRBuilder(entryBlock)
    
    if retorno:
        retFunc = builder.alloca(retorno, name='ret')

    # for arg, name in zip(func.args, [p[0] for p in item['parametros']]):
    #     arg.name = name

    funcoes.append(func)
    funcs = func
            
    for a in func.args:
        f = builder.alloca(a.type, name=a.name)
        f.align = 4
        locais[a.name] = f
        builder.store(a, f)
    
    endBlock = func.append_basic_block('fim' +nameFunc)

    varDeclaration(node, builder)  
    walkingTree(node, builder)

    builder.branch(endBlock)
    builder.position_at_end(endBlock)
    
    if not retorno:
        builder.ret_void()
    else:
        f = builder.load(retFunc)
        builder.ret(f)
    
    arquivo.write(str(module))
    arquivo.close()
    print(module)

def callFunc(node, builder):
    nome_func = ut.name(node.children[0])
    lista = []
    
    for i in node.children[1]:
        lista.append(expression(i, builder))

    salvaFunc = None

    for f in funcoes:
        if nome_func == f.name:
            salvaFunc = f
    for i,(parametroW, parametroR) in enumerate(zip(lista, salvaFunc.args)):
        if str(parametroW.type) not in str(parametroR.type):
            if "double" in str(parametroR.type):
                f = builder.uitofp(parametroW, ir.DoubleType())
                lista[i] = f
            elif "i32" in str(parametroR.type):
                f = builder.fptoui(parametroW, ir.IntType(32))
                lista[i] = f
    return builder.call(salvaFunc, lista)

def printFunc(node, builder):
    global size

    exp = expression(node.children[0], builder)
    arg = exp
    
    tipo = None
    if 'i32' in str(arg.type):
        tipo = "%d\n\0"
    elif 'double' in str(arg.type):
        tipo = "%lf\n\0"

    ptr = ir.ArrayType(ir.IntType(8), len(tipo))
    size += 1

    varGlobal = ir.GlobalVariable(module, ptr, "escreva" + str(size))
    varGlobal.initializer = ir.Constant(ptr, bytearray(tipo, encoding="utf-8"))
    varGlobal.global_constant = True

    lista_args = [varGlobal, arg]
    temp = []

    for i in lista_args:
        temp.append(i.type)

    func = ir.FunctionType(ir.IntType(32), (), var_arg=True)
    func_llvm = module.declare_intrinsic("printf", (), func)
    builder.call(func_llvm, lista_args)

def readFunc(node, builder):
    global size

    exp = expression(node.children[0], builder)
    arg = exp

    tipo = None
    if 'i32' in str(arg.type):
        tipo = "%d\0"
    elif 'double' in str(arg.type):
        tipo = "%lf\0"

    ptr = ir.ArrayType(ir.IntType(8), len(tipo))
    size  += 1

    varGlobal = ir.GlobalVariable(module, ptr, "leia" + str(size))
    varGlobal.initializer = ir.Constant(ptr, bytearray(tipo, encoding="utf-8"))
    varGlobal.global_constant = True

    lista_args = [varGlobal, arg]
    temp = []

    for i in lista_args:
        temp.append(i.type)

    func = ir.FunctionType(ir.IntType(32), (), var_arg=True)
    func_llvm = module.declare_intrinsic("scanf", (), func)
    builder.call(func_llvm, lista_args)

def retInt(e):
    return ir.Constant(ir.IntType(32), e)

def retFloat(e):
    return ir.Constant(ir.DoubleType(), e)

def expression(node, builder):
    exp = []
    for f in PreOrderIter(node):
        if f.is_leaf:
            exp.append(ut.name(f))

    if len(exp) == 3:
        if exp[1] == "+":
            if isinstance(exp[0], float) or isinstance(exp[2], float):
                return builder.fadd(retFloat(exp[0]), retFloat(exp[2]), name="addFloat")
            else:
                return builder.add(retInt(exp[0]), retInt(exp[2]), name="addInt")
        if exp[1] == "-":
            return builder.sub(retInt(exp[0]), retInt(exp[2]), name="sub")
        if exp[1] == "*":
            if isinstance(exp[0], float):
                return builder.fmul(retFloat(exp[0]), retFloat(exp[2]), name="mulFloat")
            else:
                return builder.mul(retInt(exp[0]), retInt(exp[2]), name="mulInt")
        if exp[1] == "/":
            if isinstance(exp[0], float):
                return builder.fdiv(retFloat(exp[0]), retFloat(exp[2]), name="divFloat")
            else:
                return builder.udiv(retInt(exp[0]), retInt(exp[2]), name="divInt")
        if exp[1] == "||":
            return builder.or_(retInt(exp[0]), retInt(exp[2]), name="or")
        if exp[1] == "&&":
            return builder.and_(retInt(exp[0]), retInt(exp[2]), name="and")
        if exp[1] in [">", "<", ">=", "<="]:
            return builder.icmp_signed(exp[1], retInt(exp[0]), retInt(exp[2]), name="maiorMenor")
        if exp[1] == "<>":
            return builder.icmp_signed("!=", retInt(exp[0]), retInt(exp[2]), name="dif")
        if exp[1] == "=":
            return builder.icmp_signed("==", retInt(exp[0]), retInt(exp[2]), name="igual")
    
    elif len(exp) == 1:
        return retInt(exp[0])

def atribution(node, builder):
    nome = ''
    elem = None

    for n in PreOrderIter(node):
        if n.is_leaf and ut.name(n.parent) == 'var':
            nome = ut.name(n)
    
    if nome in locais.keys():
        elem = locais[nome]
    if nome in globais.keys():
        elem = globais[nome]
    
    resultado = expression(node.children[1], builder)

    if str(resultado.type) not in str(elem.type):
        if str(elem.type) == "i32*":
            resultado = builder.fptoui(resultado, ir.IntType(32))
        else:
            resultado = builder.uitofp(resultado, ir.DoubleType())

    builder.store(resultado, elem)

def conditional(node, builder):
    exp = expression(node.children[0], builder)
    zero = retInt(0)
    cond = builder.icmp_signed("!=", exp, zero, name="comparacao")

    if len(node.children) == 2:
        with builder.if_then(cond):
            walkingTree(node.children[1], builder)
    else:
        with builder.if_else(cond) as (then, otherwise):
            with then:
                walkingTree(node.children[4], builder)
            with otherwise:
                walkingTree(node.children[5], builder)

def loop(node, builder):
    global funcs

    bloco_condicao = funcs.append_basic_block('condicao_repita')
    bloco_repita = funcs.append_basic_block('bloco_repita')
    bloco_fim_repita = funcs.append_basic_block('bloco_fim_repita')

    br = builder.branch(bloco_repita)
    builder.position_at_end(bloco_repita)

    walkingTree(node.children[0], builder)  # 'então'
    
    builder.branch(bloco_condicao) 
    builder.position_at_end(bloco_condicao)
    
    resultado = expression(node.children[2], builder)  # 'condicao'
    
    zero = retInt(0)
    cond = builder.icmp_signed("==", resultado, zero, name="comparacao_repita")
    builder.cbranch(cond, bloco_repita, bloco_fim_repita)
    builder.position_at_end(bloco_fim_repita)

def returnFunc(node, builder):
    global retFunc

    retorno = expression(node.children[0], builder)
    builder.store(retorno, retFunc)