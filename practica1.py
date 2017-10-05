
def ejercicio2(l):
    res = [1] * len(l);
    for i in range(1,len(l)):
        value = 0;
        for j in range(0, i):
            if l[j] < l[i] and value < res[j]:
                value = res[j];
        res[i] += value;
    return res;

def ejercicio3(l):
    return max(ejercicio2(l));

def ejercicio4(l, optimizar="tiempo"):
    if optimizar == "tiempo":
        return ejercicio4time(l);
    else:
        return ejercicio4space(l);

def ejercicio4time(l):
    res = [1] * len(l);
    p = [-1];

    for i in range(1,len(l)):
        index = -1;
        value = 0;
        for j in range(0, i):
            if l[j] < l[i] and value < res[j]:
                index = j;
                value = res[j];
        res[i] += value;
        p.append(index);

    prev = res.index(max(res));
    a = [];
    while(prev != -1):
        a.append(l[prev]);
        prev = p[prev];

    a.reverse();
    return a;

def ejercicio4space(l):
    res = ejercicio2(l);
    quedan = max(res);
    pos = res.index(quedan);
    a = [];

    while(quedan > 0):
        a.append(l[pos]);
        quedan -= 1;
        for i in range(0, pos):
            if l[i] < l[pos] and res[i] == quedan:
                pos = i;

    a.reverse();
    return a;

def menores(l):
    men = [];

    for i in l:
        if len(men) == 0 or i > men[-1]:
            men.append(i);
        else:
            a = 0;
            b = len(men);
            found = False;
            while not found and a + 1 != b:
                c = int((a + b) / 2);
                if (i > men[c]):
                    a = c;
                elif (i < men[c]):
                    b = c;
                else:
                    found = True;

            if not found:
                if a == 0 and (len(men) == 1 or men[a] > i):
                        men[a] = i;
                else:
                    men[b] = i;
    return men;

a = [210, 816, 357, 107, 889, 635, 733, 930, 842, 542];

