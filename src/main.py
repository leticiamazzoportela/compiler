import scanner
import parser
import sys

if len(sys.argv) == 1:
    print("Comando incorreto! \nSintaxe: python main.py nome_arquivo.tpp") #Verifica se o arquivo foi executado corretamente
else:
    print("____________* Executando Analisador Léxico *____________\n")
    result_scanner = scanner.run_scanner(sys.argv[1])
    print("____________* Analisador Léxico Finalizado *____________\n")
    print("____________* Executando Analisador Sintático *____________\n")
    parser.run_parser(result_scanner)
    print("____________* Analisador Sintático Finalizado *____________\n")