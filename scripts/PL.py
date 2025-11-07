from pyomo.environ import *

def PL(A,P,E,V):
    # Modèle
    model = ConcreteModel()

    # Ensembles d’indices
    model.I = RangeSet(0, len(A)-1)
    model.J = RangeSet(0, len(P)-1)

    model.x = Var(model.I, model.J, bounds=(0, 1))

    model.K = RangeSet(0, len(E)-1)
    model.u = Var(model.K, domain=Binary)

    # Fonction objectif
    model.obj = Objective( expr=sum(A[i][2] * model.x[i, j] for i in model.I for j in model.J), sense=minimize)

    
    
    # Contrainte chemins

    model.path_constraints = ConstraintList()
    for node in V:
        for j in model.J:
            if node != P[j][0] and node != P[j][1]:
                entree = []
                sortie = []
                for i in model.I:
                    if A[i][0] == node:
                        entree.append(i)
                    elif A[i][1] == node:
                        sortie.append(i)
                model.path_constraints.add(sum(model.x[u,j] for u in entree) - sum(model.x[v,j] for v in sortie) == 0)



    # Contrainte entrée-sortie

    def start_constraint_rule(model, j):
        return (sum(model.x[i,j] for i in model.I if A[i][0]==P[j][0])- sum(model.x[i,j] for i in model.I if A[i][1]==P[j][0])) == 1
    
    def finish_constraint_rule(model, j):
        return (sum(model.x[i,j] for i in model.I if A[i][1]==P[j][1])- sum(model.x[i,j] for i in model.I if A[i][0]==P[j][1])) == 1


    model.start_constraints = Constraint(model.J, rule=start_constraint_rule)
    model.finish_constraints = Constraint(model.J, rule=finish_constraint_rule)


    # Contrainte sur les u
    
    def xinf_constraint_rule(model,k,j):
        return model.x[E[k],j] <= model.u[k]
    model.xinf_constraints = Constraint(model.K,model.J, rule=xinf_constraint_rule)


    model.PAIRS = RangeSet(0, len(E)-2, 2)
    def pair_constraint_rule(model, i):
        return model.u[i] + model.u[i+1] == 1

    model.pair_constraints = Constraint(model.PAIRS, rule=pair_constraint_rule)

    # Résolution avec GLPK

    solver = SolverFactory('glpk')
    result = solver.solve(model, tee=True)


    if result.solver.status == SolverStatus.ok and result.solver.termination_condition == TerminationCondition.optimal:
        # Le modèle a une solution optimale
        return [E[k] for k in model.K if model.u[k].value is not None and value(model.u[k]) == 1], value(model.obj), result.solver.time
    elif result.solver.termination_condition == TerminationCondition.infeasible:
        print("❌ Le problème est infaisable (aucune solution réalisable).")
        return []
    else:
        print("⚠️ Problème lors de la résolution :", result.solver.status, result.solver.termination_condition)
        return []