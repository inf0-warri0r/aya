import random


class patten:

    def __init__(self):
        self.verbs = {}
        self.adj = {}
        self.adv = {}
        self.pattens = {}
        self.greet = {}
        self.endings = {}

    def read_verbs(self):
        fv = open("verbs", 'r')
        words = fv.read().splitlines()
        for word in words:
            self.verbs[word] = 1

    def read_adjctives(self):
        fv = open("adjctives", 'r')
        words = fv.read().splitlines()
        for word in words:
            self.adj[word] = 1

    def read_adverbs(self):
        fv = open("adverbs", 'r')
        words = fv.read().splitlines()
        for word in words:
            self.adv[word] = 1

    def read_greets(self):
        fv = open("greed", 'r')
        words = fv.read().splitlines()
        for word in words:
            self.greet[word] = 1

    def process_endings(self):

        try:
            f = open("endings", 'r')
        except IOError:
            print "ERROR : ' endings ' is missing"
            exit(0)
        en = f.read().splitlines()
        for i in range(1, 12):
            self.endings[i] = {}

        for e in en:
            es = e.split()
            if es[1] == '1':
                self.endings[len(es[0])][es[0]] = 1
            elif es[1] == '2':
                self.endings[len(es[0]) + 2][es[0]] = 1

    def stm(self, word):
        l = len(word)
        if l > 11:
            counter = 11
        else:
            counter = l - 1
        for i in range(0, counter):
            end = word[l - counter + i:]
            if self.endings[counter - i].get(end, 0) == 1:
                word = word[:l - counter + i]
                return word
            elif len(end) > 2 and end[0] == end[1]:
                end = end[2:]
                if self.endings[counter - i].get(end, 0) == 1:
                    word = word[:l - counter + i + 1]
                    return word
        return word

    def add_patten(self, st, n):
        words = st.split()
        d = self.pattens
        for word in words:
            if d.get(word, 0) == 0:
                d[word] = {}
            d = d[word]
        d['='] = n

    def read_pattens(self):
        fp = open("pattens", 'r')
        pa = fp.read().splitlines()
        for p in pa:
            l = p.split(":")
            self.add_patten(l[0], l[1].split())

    def is_verb(self, word):
        if self.verbs.get(self.stm(word), 0) == 1:
            return True
        return False

    def is_greet(self, word):
        if self.greet.get(word, 0) == 1:
            return True
        return False

    def is_adj(self, word):
        if self.adj.get(word, 0) == 1:
            return True
        return False

    def is_adv(self, word):
        if self.adv.get(word, 0) == 1:
            return True
        return False

    def patten_match(self, st):
        words = st.split()

        d = self.pattens
        nv = list()
        for word in words:

            if d.get(word, 0) != 0:
                d = d[word]
                continue
            elif self.is_greet(word):
                if d.get('g', 0) != 0:
                    d = d['g']
                    nv.append(word)
                    continue
            elif self.is_adj(word):
                continue
            elif self.is_verb(word):
                if d.get('v', 0) == 0:
                    if word == 'do':
                        if d.get('do', 0) == 0:
                            continue
                        else:
                            d = d['do']
                else:
                    d = d['v']
                    nv.append(word)
            else:
                if 'you' in word:
                    if d.get(word, 0) == 0:
                        continue
                    else:
                        d = d[word]
                elif self.is_adv(word):
                    if d.get(word, 0) == 0:
                        continue
                    else:
                        d = d[word]
                else:
                    if d.get('n', 0) == 0:
                        continue
                    else:
                        d = d['n']
                        nv.append(word)

        while d.get('=', 0) == 0:
            key = random.choice(d.keys())
            d = d[key]

        return d['='], nv

    def sett(self, n, nv):
        print n
        if len(nv) == 0:
            nv.append("*")
        lst = n[:]
        co = 0
        for i in range(0, len(lst)):
            if lst[i] == 'n' or lst[i] == 'v' or lst[i] == 'g':
                lst[i] = nv[co]
                if co < len(nv) - 1:
                    co = co + 1
        print lst
        return lst
