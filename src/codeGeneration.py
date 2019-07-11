from llvmlite import ir
from anytree import Node, PreOrderIter
import utils as ut

def walkingTree(tree):
    for node in PreOrderIter(tree):
        node_name = ut.name(node)

        if node_name == 'declaracao_variaveis':
            varDeclaration(node)
        if node_name == 'declaracao_funcao':
            funcDeclaration(node)
        if node_name =='expressao':
            expression(node)
        if node_name == 'se':
            conditional(node)
        if node_name == 'chamada_funcao':
            callFunc(node)
        if node_name == 'repita':
            loop(node)

def readFunc(node):
    print("Fazer métodos p/ funcao leia")

def writeFunc(node):
    print("Fazer métodos p/ funcao escreva")

def varDeclaration(node): #tem que ver uma boa forma de chamar esse builder por parâmetro
    content = ut.walkTable()
    varTypes = ut.listVar(content)
    
    for n in varTypes:
        nome = n.split("_")[0]
        tipo = n.split("_")[1]
        if tipo == 'inteiro':
            # tem que usar o builder.alloca(IntType...)
            print("alocar inteiros")

def expression(node):
    print("Fazer métodos p/ expressoes")

def conditional(node):
    print("Fazer métodos p/ condicional")

def loop(node):
    print("Fazer métodos p/ laços de repetição")

def funcDeclaration(node):
    print("Fazer métodos p/ declaração de funcao")

def callFunc(node):
    print("Fazer métodos p/ chamada de funcao")