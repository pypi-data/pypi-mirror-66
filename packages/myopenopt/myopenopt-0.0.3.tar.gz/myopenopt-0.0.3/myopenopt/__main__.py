# model_type = 'MILP'
model_type = "NLP"

model = Model("sample", mtype=model_type)

x1 = model.addVar(vtype="C", name="x1")
if model_type == "MIP":
    x2 = model.addVar(vtype="I", name="x2")
else:
    x2 = model.addVar(vtype="C", name="x2")
x3 = model.addVar(vtype="C", ub=30, name="x3")
model.update()

c0 = model.addConstr(2 * x1 + x2 + x3 <= 60, name="C0")
if model_type == "NLP":
    c1 = model.addConstr(x1 ** 2 + 2 * x2 ** 2 <= x3 ** 2, name="C1")
else:
    c1 = model.addConstr(x1 + 2 * x2 + x3 <= 60, name="C1")
c2 = model.addConstr(x3 <= 30, name="C2")
c3 = model.addConstr(quicksum([x1, x2, x3]) <= 20, name="C3")

model.setObjective(15 * x1 + 18 * x2 + 30 * x3, GRB.MAXIMIZE)

print(model)
if model_type == "NLP":
    # r = model.optimize(solver="interalg")
    r = model.optimize(solver="ralg")
else:
    r = model.optimize(solver="lpSolve")
print("Result =", model.Status)
for v in model.getVars():
    print(v.VarName, v.X)
