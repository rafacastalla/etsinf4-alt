'''
Práctica 1 ALT, ejercicio muy opcional

Autor: Carlos Santiago Galindo Jiménez
Autor: José Antonio Pérez
'''

a = [210, 816, 357, 107, 889, 635, 733, 930, 842, 542];

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
    return len(men);
