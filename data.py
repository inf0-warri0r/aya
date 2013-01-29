import patten


class data:

    def __init__(self):
        self.dic = {}
        self.mapper = {}
        self.p = patten.patten()
        self.stop = {}

    def rep(self, l):
        l = l.replace("[p:", "")
        l = l.replace("[a:", "")
        l = l.replace("[s:", "")
        l = l.replace("[n:", "")
        l = l.replace("[m:", "")
        l = l.replace("[f:", "")
        l = l.replace("[t:", "")
        l = l.replace("[k:", "")
        l = l.replace("]", "")
        return l

    def map(self):
        f = open("cat2", 'r')
        cat = f.read().splitlines()
        for line in cat:
            s = line.split(":")
            for a in s[1].split(","):
                self.mapper[self.p.stm(a)] = s[0]
            s = line.split(":")

    def process_stop(self):
        f = open("stop", 'r')
        lines = f.read().splitlines()
        for line in lines:
            self.stop[line] = 1

    def train(self):
        f = open("list5", 'r')
        lines = f.read().splitlines()
        for line in lines:
            line = line.lower()
            words = line.split()
            l = len(words)
            for i in range(0, l - 1):
                if self.dic.get(words[i], 0) == 0:
                    self.dic[words[i]] = {}
                if self.dic[words[i]].get(words[i + 1], 0) == 0:
                    self.dic[words[i]][words[i + 1]] = {}

                self.dic[words[i]][words[i + 1]][words[i + 2]] = 1

    def train2(self):
        f = open("list5", 'r')
        lines = f.read().splitlines()
        for line in lines:
            line = line.lower()
            words = line.split()
            l = len(words)
            for i in range(0, l - 3):
                if self.dic.get(words[i], 0) == 0:
                    self.dic[words[i]] = {}
                if self.dic[words[i]].get(words[i + 1], 0) == 0:
                    self.dic[words[i]][words[i + 1]] = {}
                if self.dic[words[i]][words[i + 1]].get(words[i + 2], 0) == 0:
                    self.dic[words[i]][words[i + 1]][words[i + 2]] = {}
                self.dic[words[i]][words[i + 1]][words[i + 2]][words[i + 3]] = 1

    def search(self, lst, s, a, b, ls, old, r, r_old):
        if not "." in b:
            if len(s) > 90:
                return 0
            if self.dic.get(a, 0) != 0:
                if self.dic[a].get(b, 0) != 0:

                    for key in self.dic[a][b]:
                        self.search(lst, s + " " + b, b, key,
                            ls, old, r, r_old)
                    return 0
        co = 0
        #print "aaa ", old, " ", r
        for word in ls:
            if self.p.stm(word) in s + " " + b:
                co = co + 5
        for word in old:
            if self.p.stm(word) in s + " " + b:
                co = co + 1
        words = (s + " " + b).split()
        for word in words:
            if self.mapper.get(word, '1') == r:
                co = co + 25
            elif self.mapper.get(word, '1') == r_old:
                if self.mapper.get(word, '1') == r_old:
                    co = co + 15

        if co > 2:
            l = s + " " + b
            l = self.rep(l)
            lst.append((co, -len(l), l))

    def search2(self, lst, s, a, b, c, ls, old, r, r_old, sc):
        if not "." in c:
            if len(s.split()) > len(ls) + 5:  # and c != 'and' and c != 'a':
                return 0
            if self.dic.get(a, 0) != 0:
                if self.dic[a].get(b, 0) != 0:
                    if self.dic[a][b].get(c, 0) != 0:
                        for key in self.dic[a][b][c]:
                            self.search2(lst, s + " " + c, b, c,
                                key, ls, old, r, r_old, sc)
                        return 0

        if c == 'and' or c == 'a':
            return 0
        co = sc
        print "aaa ", r, " ", r_old
        for word in ls:
            if self.p.stm(word) in s + " " + c:
                co = co + 5
        for word in old:
            if self.p.stm(word) in s + " " + c:
                co = co + 1
        words = (s + " " + c).split()
        fl = True
        for word in words:
            if self.mapper.get(word, '1') == r or self.mapper.get(self.p.stm(word), '1') == r:
                co = co + 25
                fl = False
                break
        if fl:
            for word in words:
                if self.mapper.get(word, '1') == r_old or self.mapper.get(self.p.stm(word), '1') == r_old:
                    co = co + 15
                    break

        if co > 2:
            l = s + " " + c
            l = self.rep(l)
            lst.append((co, -len(l), l))

    def s2(self, ls, old, r, r_old):
        lst = list()
        for a in ls:
            if self.p.is_adv(a):
                continue
            if self.dic.get(a, 0) != 0:
                for b in self.dic[a]:
                    self.search(lst, a, a, b, ls, old, r, r_old)

        l = self.dic.keys()
        for a in l:
            if self.mapper.get(a, '1') == r:
                for b in self.dic[a]:
                    self.search(lst, a, a, b, ls, old, r, r_old)
        return lst

    def s3(self, ls, old, r, r_old):
        lst = list()
        sc = len(lst) + 10
        for a in ls:
            if self.p.is_adv(a) or a == 'like':
                continue
            if self.dic.get(a, 0) != 0:
                for b in self.dic[a]:
                    for c in self.dic[a][b]:
                        self.search2(lst, a + " " + b, a, b,
                            c, ls, old, r, r_old, sc)
            sc = sc - 1
            #if a == 'i':
                #break
        l = self.dic.keys()
        for a in l:
            if self.mapper.get(a, '1') == r:
                for b in self.dic[a]:
                    self.search2(lst, a + " " + b, a, b,
                        c, ls, old, r, r_old, 0)
        return lst
