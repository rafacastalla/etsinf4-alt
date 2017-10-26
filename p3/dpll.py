# -*- coding: utf-8 -*-
import sys

'''
Nombre: Carlos S. Galindo Jiménez
Nombre: José Antonio Pérez
Fecha: 27/10/2017
'''

def read_cnf_dimacs(filename):
  linenumber = 0
  num_variables = 0
  num_clauses = 0
  clauses = []
  try:
    with open(filename) as f:
      for line in f:
        linenumber += 1
        line = line.split()
        if len(line)==0 or line[0]=='c': continue
        if len(line)==4 and line[0]=='p' and line[1]=='cnf':
          num_variables = int(line[2])
          num_clauses = int(line[3])
          break;
        sys.exit("error reading cnf file '%s' at line %d" % (filename,linenumber))
      for line in f:
        linenumber += 1
        line = line.split()
        if len(line)==0 or line[0]=='c': continue
        clause = [int(x) for x in line]
        if clause[-1] != 0:
          sys.exit("error reading cnf file '%s' at line %d expecting 0 at last position" \
                   % (filename,linenumber))
        del clause[-1] # remove last element
        if any(abs(x)>num_variables for x in clause):
          sys.exit("error reading cnf file '%s' at line %d variable out of range" \
                   % (filename,linenumber))
        clauses.append(clause)
  except ValueError:
      sys.exit("error reading cnf file '%s' at line %d parsing int" % (filename,linenumber))
  if len(clauses) != num_clauses:
      sys.exit("error reading cnf file '%s' number of clauses differ" % (filename,))
  # just in case, remove empty clauses
  clauses = [c for c in clauses if len(clause)>0]
  return num_variables,clauses

def choose_literal(clauses):
  smallest = min(len(clause) for clause in clauses)
  variables = set(y for clause in clauses for y in clause if len(clause)==smallest)
  #return random.choice(tuple(variables))
  return variables.pop()

def simplify(clauses,literal):
  aux = [c for c in clauses if literal not in c]
  if len(aux) == 0:
    return True;
  res = [];
  for c in aux:
    clausula = [x for x in c if -literal != x]
    if len(clausula) == 0:
      return False
    else:
      res.append(clausula);
  return res;

def check(formula,listofliterals):
  # determines if the list of literals is able to assign a True value
  # to the formula
  for literal in listofliterals:
    formula = simplify(formula,literal)
    print("Despejando literal",literal)
    print(formula)
    if isinstance(formula,bool):
      return formula
  # at this point, the formula has not been fully simplified
  return False

def backtracking(formula):
  if formula is True:
    return []
  elif formula is False:
    return None

  literal = choose_literal(formula)
  positive = backtracking(simplify(formula, literal))
  if positive is not None:
    positive.append(literal)
    return positive
  negative = backtracking(simplify(formula, -literal))
  if negative is not None:
    negative.append(-literal)
    return negative
  return None

def unit_propagation(clauses):
  literals = []
  change = True
  while change:
    change = False
    for c in clauses:
      if len(c) == 1:
        literals.append(c[0])
        clauses = simplify(clauses, c[0])
        change = True
        break
  return clauses, literals

def pure_literal_elimination(clauses):
  literals = []
  mydict = {}
  for c in clauses:
    for x in c:
      v = mydict.get(abs(x), None)
      if v is None:
        mydict[abs(x)] = x
      elif v != x:
        mydict[abs(x)] = 0

  for key, value in mydict.items():
    if value != 0:
      literals.append(value)
      clauses = simplify(clauses, value);

  return clauses, literals

def dpll(formula):
  if formula is True:
    return []
  elif formula is False:
    return None

  (formula, l1) = unit_propagation(formula)
  (formula, l2) = pure_literal_elimination(formula)

  literal = choose_literal(formula)
  positive = backtracking(simplify(formula, literal))
  if positive is not None:
    positive.append(literal)
    return positive + l1 + l2
  negative = backtracking(simplify(formula, -literal))
  if negative is not None:
    negative.append(-literal)
    return negative + l1 + l2
  return None

######################################################################
######################       MAIN PROGRAM       ######################
######################################################################
if __name__ == "__main__":
  if len(sys.argv) != 2:
    print('\n%s dimacs_cnf_file\n' % (sys.argv[0],))
    sys.exit()

  file_name = sys.argv[1]
  num_variables,clauses = read_cnf_dimacs(file_name)
  print(clauses)
  # replace backtracking by dpll when checking dpll
  resul = dpll(clauses)
  # resul = backtracking(clauses)
  if resul != None:
    print("We have found a solution:",resul)
    print("The check returns:",check(clauses,resul))
  else:
    print("Not solution has been found")

