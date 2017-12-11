class Tape(object):

    def __init__(self, conteudo, simb_branco):
        self.conteudo = conteudo
        self.cabeca = 0
        self.simb_branco = simb_branco

    # move a cabeca de leitura/escrita para a direcao especificada:
    # direita('R') ou esquerda('L')
    def mover(self, dir):
        if dir == 'R':
            self.cabeca += 1
            # caso a cabeca mova alem do tamanho atual da fita,
            # acrescente um simbolo branco ao final da fita,
            # mantendo a infinitude da mesma
            if self.cabeca == len(self.conteudo):
                self.conteudo.append(self.simb_branco)
        if dir == 'L':
            self.cabeca -= 1
            # caso a cabeca mova a esquerda da posicao zero da fita,
            # acrescente um simbolo branco e mova a cabeca para a posicao zero,
            # mantendo a infinitude da fita
            if self.cabeca < 0:
                self.cabeca = 0
                self.conteudo.insert(0, self.simb_branco)

    # insere o simbolo na posicao onde se encontra a cabeca da fita,
    # substituindo o simbolo ja existente
    def escrever(self, simb):
        self.conteudo[self.cabeca] = simb

    # retorna simbolo atual da fita
    def ler(self):
        return self.conteudo[self.cabeca]

    def __str__(self):
        return "f={},c={}".format(self.conteudo, self.cabeca)