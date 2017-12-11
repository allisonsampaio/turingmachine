class Node(object):

    def __init__(self, estado, fitas):
        self.fitas = fitas
        self.estado = estado

    def __str__(self):
        a = []
        for fita in self.fitas:
            a.append(fita.__str__())
        return a
