#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 17:37:19 2024

@author: haozheyang
"""

from pyomo.environ import *

model=AbstractModel()

model.project=Set(dimen=1)

#model.Capacity=Var(model.project, domain = NonNegativeIntegers)

model.Generation=Var(model.project, domain = NonNegativeIntegers)

#model.Capacity_Cost=Param(model.project)
model.Operation_Cost=Param(model.project,initialize=1)

model.Demand=Param()



data = {None: {
    'project': {None: [1,2,3]},
    'Operation_Cost': {1: 100,2:20,3:40},
    'Demand': {None: 40}
}}


def balance(model):
    return model.Demand == sum(model.Generation[i] for i in model.project)
    
#model.Gen_balannce=Constraint(model.project)
model.Supply_Demand=Constraint(rule=balance)




def ObjRule(model):
    return sum(model.Operation_Cost[i] * model.Generation[i] for i in model.project) 

model.Total_cost = Objective(rule=ObjRule)


data_model = model.create_instance(data)

data_model.pprint()

opt = SolverFactory('cbc')
opt.solve(data_model) 


