'''
Práctica 1 ALT, ejercicios 2 al 4

El ejercicio 4 presenta 2 versiones: una optimizada para emplear menos tiempo
y otra que minimiza la memoria empleada

Autor: Carlos Santiago Galindo Jiménez
Autor: José Antonio Pérez
'''

def ejercicio2(l):
    res = [];
    for i in range(0,len(l)):
        value = 0;
        for j in range(0, i):
            if l[j] < l[i] and value < res[j]:
                value = res[j];
        res.append(value + 1);
    return res;

def ejercicio3(l):
    return max(ejercicio2(l));

def ejercicio4(l, optimizar="tiempo"):
    if optimizar == "tiempo":
        return ejercicio4time(l);
    else:
        return ejercicio4space(l);

def ejercicio4time(l):
    res = [];
    p =   [];

    for i in range(0,len(l)):
        index = -1;
        value = 0;
        for j in range(0, i):
            if l[j] < l[i] and value < res[j]:
                index = j;
                value = res[j];
        res.append(value + 1);
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

a = [210, 816, 357, 107, 889, 635, 733, 930, 842, 542];

