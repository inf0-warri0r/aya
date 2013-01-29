import data


dt = data.data()
dt.p.read_verbs()
dt.p.read_adjctives()
dt.p.read_adverbs()
dt.p.read_greets()
dt.p.read_pattens()
dt.p.process_endings()

dt.process_stop()
dt.train2()
dt.map()


def reduse(ls):
    new = list()
    for i in range(0, len(ls)):
        if not ls in new:
            new.append(ls[i])
    return new

print dt.p.stm('politic')
print dt.p.stm('politics')
old = list()
r = ""
r_old = ""
while 1:
    st = raw_input("you : ")
    st = st.lower()
    if st == 'q':
        break

    n, nv = dt.p.patten_match(st)
    lt = dt.p.sett(n, nv)

    wd = st.split()
    wrds = list()
    wd = wd
    r = ""
    for word in lt:
        if word != "*":
            wrds.append(word)

    for word in wd:
        if dt.stop.get(word, 0) == 0:
            if dt.mapper.get(dt.p.stm(word), 0) != 0:
                r = dt.mapper[dt.p.stm(word)]
                wrds.append(word)
            else:
                wrds.append(word)
    wrds = reduse(wrds)
    print wrds
    if len(wrds) > 0:

        list_ = sorted(dt.s3(wrds, old, r, r_old))
        print list_
        if len(list_) > 0:
            ans = list_[len(list_) - 1][2]
            print "A.I. : ", ans
            old = list()
            for word in ans.split():
                if dt.stop.get(word, 0) == 0:
                    old.append(word)
        else:
            if "?" in st:
                print "A.I. : I have no idea"
            else:
                print "A.I. : ok"

    else:
        if "?" in st:
            print "A.I. : I have no idea"
        else:
            print "A.I. : ok"
    r_old = r
