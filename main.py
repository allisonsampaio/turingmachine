# Maquina de Turing nao deterministica com n fitas.
#
# APS realizada para a disciplina de Linguagens Formais, Automatos e Computabilidade
# UTFPR - Campo Mourao
# Prof.: Marco Aurelio Graciotto da Silva
# Alunos: Rodrigo Paula da Silva,
#         Mara Luci Goulart,
#         Alisson Sampaio.
#
# Obs.: Foram retirados acentos e caracteres especiais do codigo para
#       nao dar problema com versoes anteriores do Python.

import sys
import turing_machine as tm

def main():
    if len(sys.argv) < 2:
        print("Uso: python main.py arquivo.txt conteudo_fita1 [conteudo_fita2... ]")
        return

    try:
        arquivo = open(sys.argv[1], 'r')
    except IOError:
        print("Erro ao abrir o arquivo")
        return

    entrada = arquivo.readlines();
    alfabeto_entrada = entrada[0].replace('\n','').replace('\r','').split(' ')
    alfabeto_fita = entrada[1].replace('\n','').replace('\r','').split(' ')
    branco = str(entrada[2].replace('\n','').replace('\r',''))
    estados = entrada[3].replace('\n','').replace('\r','').split(' ')
    inicial = str(entrada[4].replace('\n','').replace('\r',''))
    finais = entrada[5].replace('\n','').replace('\r','').split(' ')
    fitas = entrada[6].replace('\n','').replace('\r','')
    transicoes = []
    for i in range(7,len(entrada)):
        transicoes.append(entrada[i].replace('\n', '').replace('\r','').split(' '))
    conteudo = []
    for i in range(2, int(fitas)+2):
        c = []
        if i >= len(sys.argv):
            c = ['B']
            conteudo.append(c)
            continue
        for j in range(len(sys.argv[i])):
            c.append(str(sys.argv[i][j]))
        conteudo.append(c)

    TM = tm.TuringMachine(
        alfabeto_entrada = alfabeto_entrada,
        alfabeto_fita = alfabeto_fita,
        simb_branco = branco,
        estados = estados,
        estado_inicial = inicial,
        estados_finais = finais,
        fitas = int(fitas),
        transicoes = transicoes,
        conteudo = conteudo
    )
    TM.executar()

if __name__ == "__main__":
	main()