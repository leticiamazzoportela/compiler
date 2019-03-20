import scanner
import parser
import semantic
import sys

if len(sys.argv) == 1:
    print("Comando incorreto! \nSintaxe: python main.py nome_arquivo.tpp") #Verifica se o arquivo foi executado corretamente
else:
    print("____________* Executando Analisador Léxico *____________\n")
    scanner.run_scanner(sys.argv[1])
    print("____________* Analisador Léxico Finalizado *____________\n")

    print("____________* Executando Analisador Sintático *____________\n")
    parser.run_parser(sys.argv[1])

    # print("____________* Executando Analisador Semântico *____________\n")
    # semantic.run_semantic()
    # print("____________* Analisador Semântico Finalizado *____________\n")