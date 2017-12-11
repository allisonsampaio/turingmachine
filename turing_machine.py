from node import Node
from tape import Tape
from copy import deepcopy


class TuringMachineDeterministic(object):
    def __init__(self, alfabeto_entrada, alfabeto_fita, simb_branco,
                 estados, estado_inicial, estados_finais, fitas,
                 transicoes):
        self._alfabeto_entrada = alfabeto_entrada
        self._alfabeto_fita = alfabeto_fita
        self._simb_branco = simb_branco
        self._estados = estados
        self._estado_inicial = estado_inicial
        self._estados_finais = estados_finais
        self._fitas = fitas
        self._transicoes = transicoes
        self._cabeca = [0]
        self._conteudo = []
        self._estado_atual = estado_inicial

    def _transicao(self, t, fitas):
        print(t)
        # atribui os valores correspondente a cada fita
        estado = t[0]
        estado_destino = t[1]
        simb = []
        simb_novo = []
        movimento = []
        for i in range(0, fitas):
            simb.append(t[2 + 3*i])
            simb_novo.append(t[3 + 3*i])
            movimento.append(t[4 + 3*i])

        # testa condicao, se nao -> retorna, se sim ->continua.
        if not self._estado_atual == estado:
            return False
        for i in range(fitas):
            if not self._conteudo[self._cabeca[i]] == simb[i]:
                return False

        # faz as modificacoes nas fitas
        self._estado_atual = estado_destino
        for i in range(self._fitas):
            self._conteudo[self._cabeca[i]] = simb_novo[i]
            if movimento[i] == 'L':
                self._cabeca[i] -= 1
                if self._cabeca[i] < 0:
                    self._conteudo.insert(0, 'B')
                    self._cabeca[i] = 0
                if self._conteudo[self._cabeca[i]] == '#':
                    self._cabeca[i] += 1
                    self._conteudo = self._insere(self._conteudo, self._cabeca[i], 'B')
            if movimento[i] == 'R':
                self._cabeca[i] += 1
                if self._conteudo[self._cabeca[i]] == '#':
                    self._conteudo = self._insere(self._conteudo, self._cabeca[i], 'B')

        print('fita: {}, cabeca: {}, estado: {}'.format(self._conteudo, self._cabeca, self._estado_atual))
        return True

    def executar(self, conteudo):
        self._conteudo = conteudo
        self._conteudo.append('#')
        for i in range(self._fitas-1):
            self._cabeca.append(len(self._conteudo))
            self._conteudo.append('B')
            self._conteudo.append('#')

        print('Alfabeto de entrada: {}\n'
              'Alfabeto da fita: {}\n'
              'Simbolo branco: {}\n'
              'Estados: {}\n'
              'Estado inicial: {}\n'
              'Estados finais: {}\n'
              'Fitas: {}\n'
              'Transicoes: {}\n'
              'Conteudo: {}'.format(self._alfabeto_entrada,
                                    self._alfabeto_fita,
                                    self._simb_branco,
                                    self._estados,
                                    self._estado_inicial,
                                    self._estados_finais,
                                    self._fitas,
                                    self._transicoes,
                                    self._conteudo))
        print('\nExecutando..\n')

        try:
            while self._estado_atual not in self._estados_finais:
                if not self._testa_transicoes():
                    if self._estado_atual in self._estados_finais:
                        print('0\nAceito')
                        return
                    else:
                        print('1\nRejeito')
                        return
            print('0\nAceito')
        except KeyboardInterrupt:
            print('Computacao interrompida.')

    # testa todas as transicoes possiveis para determinado estado ate encontrar alguma que aceite.
    def _testa_transicoes(self):
        for t in self._transicoes:
            if self._transicao(t, self._fitas):
                return True
        return False

    def _insere(self, a, n, x):
        b = a[:n] + [x] + a[n:]
        for i in range(len(self._cabeca)):
            if self._cabeca[i] > n:
                self._cabeca[i] += 1
        return b


class TuringMachineNonDeterministic(object):

    def __init__(self, alfabeto_entrada, alfabeto_fita, simb_branco,
                 estados, estado_inicial, estados_finais, fitas,
                 transicoes, conteudo=[]):
        self._alfabeto_entrada = alfabeto_entrada
        self._alfabeto_fita = alfabeto_fita
        self._simb_branco = simb_branco
        self._estados = estados
        self._estado_inicial = estado_inicial
        self._estados_finais = estados_finais
        self._fitas = fitas
        self._transicoes = transicoes
        self._conteudo = conteudo

    # executa a TM
    def executar(self):
        #self.print_info()

        # busca em largura ate encontrar um estado final ou
        # nao existir mais transicoes validas
        tapes = self._init_tapes()
        fila = [Node(self._estado_inicial, tapes)]

        try:
            while fila:
                node = fila.pop()
                #print(node.__str__())
                if node.estado in self._estados_finais:
                    print('0: Aceito')
                    return
                transicoesvalidas = self._transicoes_validas(node)
                for transicao in transicoesvalidas:
                    fila.insert(0, self._transicao(transicao, node))
            print('1: Rejeitado')
        except KeyboardInterrupt:
            print('\nComputacao interrompida.')

    # aplica a transicao em um node e retorna o node gerado
    def _transicao(self, t, node):
        newnode = deepcopy(node)
        newnode.estado = t[1]
        fitas = newnode.fitas
        for i in range(self._fitas):
            k = self._fitas * i
            fitas[i].escrever(t[3 + k])
            fitas[i].mover(t[4 + k])
        return newnode

    # retorna as transicoes validas para determinado node
    def _transicoes_validas(self, node):
        tv = []
        for transicao in self._transicoes:
            if self._testa_transicao(transicao, node):
                tv.append(transicao)
        return tv

    def _testa_transicao(self, t, node):
        fitas = node.fitas
        if not node.estado == t[0]:
            return False
        for i in range(self._fitas):
            if not fitas[i].ler() == t[2 + (self._fitas * i)]:
                return False
        return True

    # inicializa as fitas
    def _init_tapes(self):
        tapes = [Tape(self._conteudo, self._simb_branco)]
        for i in range(1, self._fitas):
            tapes.append(Tape([self._simb_branco], self._simb_branco))
        return tapes

    # imprime informacoes
    def print_info(self):
        print('Alfabeto de entrada: {}\n'
              'Alfabeto da fita: {}\n'
              'Simbolo branco: {}\n'
              'Estados: {}\n'
              'Estado inicial: {}\n'
              'Estados finais: {}\n'
              'Fitas: {}\n'
              'Transicoes: {}\n'
              'Conteudo: {}'.format(self._alfabeto_entrada,
                                    self._alfabeto_fita,
                                    self._simb_branco,
                                    self._estados,
                                    self._estado_inicial,
                                    self._estados_finais,
                                    self._fitas,
                                    self._transicoes,
                                    self._conteudo))