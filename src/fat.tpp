inteiro: n[10], a
flutuante: x

inteiro fatorial(inteiro: n)
    se n > 0 então {não calcula se n > 0}
        fat := 1
        repita
            fat := fat * n
            n := n - 1
        até n = 0
        retorna(fat) {retorna o valor do fatorial de n}
    senão
        retorna(0)
    fim
fim

inteiro principal(inteiro: a)
    leia(n)
    escreva(fatorial(n))
    retorna(0)
fim