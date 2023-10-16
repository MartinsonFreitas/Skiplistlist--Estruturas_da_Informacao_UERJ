"""A skiplist implementation of the List interface

W. Pugh. Skip Lists: A probabilistic alternative to balanced trees.
  In Communications of the ACM, 33(6), pp. 668-676, June 1990.

W. Pugh. A skip list cookbook. CS-TR-2286.1, University of Maryland,
  College Park, 1990.
"""
import random
import numpy
from .utils import new_array
from .base import BaseList


class SkiplistList(BaseList):
    class Node(object):
        """A node in a skip list"""
        def __init__(self, x, h):
            self.x = x
            self.next = new_array(h+1)
            self.length = numpy.ones(h+1, dtype=int)

        def height(self):
            return len(self.next) - 1

    def _new_node(self, x, h):
        return SkiplistList.Node(x, h)

    def __init__(self, iterable=[]):
        self._initialize()
        self.add_all(iterable)

    def _initialize(self):
        self.h = 0
        self.n = 0
        self.sentinel = self._new_node(None, 32)
        self.stack = new_array(self.sentinel.height()+1)

    def find_pred(self, i):
        u = self.sentinel
        r = self.h
        j = -1
        while r >= 0:
            while u.next[r] is not None and j + u.length[r] < i:
                j += u.length[r]
                u = u.next[r]  # go right in list r
            r -= 1  # go down into list r-1
        return u

    def get(self, i):
        if i < 0 or i > self.n-1: raise IndexError()
        return self.find_pred(i).next[0].x

    def set(self, i, x):
        if i < 0 or i > self.n-1: raise IndexError()
        u = self.find_pred(i).next[0]
        y = u.x
        u.x = x
        return y

    def _add(self, i, w):
        u = self.sentinel
        k = w.height()
        r = self.h
        j = -1
        while r >= 0:
            while u.next[r] is not None and j+u.length[r] < i:
                j += u.length[r]
                u = u.next[r]
            u.length[r] += 1
            if r <= k:
                w.next[r] = u.next[r]
                u.next[r] = w
                w.length[r] = u.length[r] - (i-j)
                u.length[r] = i - j
            r -= 1
        self.n += 1
        return u

    def add(self, i, x):
        if i < 0 or i > self.n: raise IndexError()
        w = self._new_node(x, self.pick_height())
        if w.height() > self.h:
            self.h = w.height()
        self._add(i, w)

    def remove(self, i):
        if i < 0 or i > self.n-1: raise IndexError()
        u = self.sentinel
        r = self.h
        j = -1
        while r >= 0:
            while u.next[r] is not None and j + u.length[r] < i:
                j += u.length[r]
                u = u.next[r]
            u.length[r] -= 1
            if j + u.length[r] + 1 == i and u.next[r] is not None:
                x = u.next[r].x
                u.length[r] += u.next[r].length[r]
                u.next[r] = u.next[r].next[r]
                if u == self.sentinel and u.next[r] is None:
                    self.h -= 1
            r -= 1
        self.n -= 1
        return x

    def __iter__(self):
        u = self.sentinel.next[0]
        while u is not None:
            yield u.x
            u = u.next[0]

    def pick_height(self):
        z = random.getrandbits(32)
        k = 0

        while z & 1:
            k += 1
            z = z // 2
        return k
    
# Escreva um método, truncate(i), que trunca uma Skiplist-List na posição i. 
# Após a execução deste método, o tamanho da lista é i e contém apenas os 
# elementos nos índices 0, . . . , i − 1. 
# O valor de retorno é outra SkiplistList que contém os elementos nos 
# índices i, . . . , n − 1. Esse método deve ser executado em um tempo O(log n).        
    def truncate(self, i):            
        # Cria skiplistlist para a lista truncada
        l2 = SkiplistList()
        # Escreva sua solução aqui.
        
        # Atualiza o sentinela
        u = self.sentinel
        # Atualiza a altura
        r = self.h
        # Atualiza o indice
        j = -1
        h2 = None
        h1 = None
        
        while r >= 0:

            # Percorre para direita ate achar o proximo no nulo ou no depois do indice de truncar
            while u.next[r] != None and j + u.length[r] < i:
                # Atualiza o indice
                if h1 == None:
                    # Atualiza a altura do no
                    h1 = r
                    
                # Atualiza o indice 
                j += u.length[r]
                # Atualiza o no
                u = u.next[r]

            # Cai nesse caso, apenas se houver um nó depois do indice de truncar
            if u.next[r] != None:
                # Atualiza o indice
                if h2 == None:
                    # Atualiza a altura do no
                    h2 = r 
                    # Atualiza o no
                    w = self._new_node(None, h2)
                    # Atualiza o indice
                    self._add(i, w)
                    
                    # Cria skiplistlist de retorno        
                    l2.sentinel = w
                    l2.h = h2
                    l2.n = self.n - i - 1
                    
                u.next[r] = None
                u.length[r] = 1 

            r = r - 1

        if h1 == None:
            h1 = 0        

        # Atualiza a altura e numero de elementos da lista truncada
        self.h = h1
        self.n = i
        
        return l2 # Retorna a lista truncada