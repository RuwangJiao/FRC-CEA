# -*- coding: utf-8 -*-
import tools
import conf
import dynamic_tools
import copy
import os
import niche
import sys

def init(popSize,  problem_initialize, evaluator):
    global parent_size, offspring_size,  _genCount, _evaluator, parent_pop, upper, lower, constraints_num, objectives_number, evaluationTime
    parent_size, offspring_size, _genCount, _evaluator, upper, lower = popSize, popSize, problem_initialize[0], evaluator, problem_initialize[1], problem_initialize[2]
    constraints_num, objectives_number = problem_initialize[4], problem_initialize[5]
    parent_pop = dynamic_tools.initialize_parent_population(parent_size, _genCount)
    dynamic_tools.caculate_pheno(parent_pop, upper, lower, _genCount, parent_size)
    dynamic_tools.evaluate_population(parent_pop, _evaluator, dynamic_tools.get_fill_result)

def loop(generation, outputfreq, condition):
    global parent_pop, evaluationTime
    initialMaxViolation = dynamic_tools.caculate_initial_max_violation(parent_pop)
    e = initialMaxViolation
    dynamic_tools.caculate_violation_objective(initialMaxViolation, parent_pop)
    dynamic_tools.mark_individual_efeasible(e, parent_pop)
    K, g = 0, 0
    MaxK_first_phase = conf.MaxK * conf.Alpha
    normalized_upper, normalized_lower = [1.0] * _genCount, [0.0] * _genCount
    R = niche.caculate_initial_radius(_genCount, parent_size + offspring_size, normalized_upper, normalized_lower)    # modify, Setepeter 6,2016, by Zeng Sanyou , Jiao Ruwang
    while K <= MaxK_first_phase:
        print "g:",g," K:",K
        #bool_efeasible = dynamic_tools.judge_population_efeasible(parent_pop)
        bool_efeasible = 1
        if bool_efeasible == 1 :
            K += 1
            if K >= MaxK_first_phase + 1:
                break
            e = dynamic_tools.reduce_boundary(initialMaxViolation, K, MaxK_first_phase)
            r = niche.reduce_radius(K, MaxK_first_phase, _genCount, R, upper, lower)
            dynamic_tools.mark_individual_efeasible(e, parent_pop)   
        offspring_pop = dynamic_tools.generate_offspring_population(g, offspring_size, parent_pop, _genCount)
        dynamic_tools.caculate_pheno(offspring_pop, upper, lower, _genCount, offspring_size)
        dynamic_tools.evaluate_population(offspring_pop, _evaluator, dynamic_tools.get_fill_result)
        dynamic_tools.caculate_violation_objective(initialMaxViolation, offspring_pop)
        dynamic_tools.mark_individual_efeasible(e, offspring_pop)
        niche.caculate_nichecount(parent_pop, offspring_pop, _genCount, r, parent_size + offspring_size)
        parent_pop = tools.select_next_parent_population(offspring_pop, parent_pop, parent_size)
        
        if g == generation:
            break
        else:
           g += 1

    parent_pop.sort(cmp = compare)
    bestObj = parent_pop[0]
    print "First-stage Best:   ", bestObj
    print "First-stage Worst:  ", parent_pop[-1]
    
    final_pop = []
    for p in parent_pop:
        final_pop.append(p["genes"])
    return final_pop, K, g

def compare(a, b):
    if a["violation_objectives"][0] < b["violation_objectives"][0]:
        return -1
    elif a["violation_objectives"][0] > b["violation_objectives"][0]:
        return 1
    else:
        if a["objectives"] < b["objectives"]:
            return -1
        elif a["objectives"] > b["objectives"]:
            return 1
        else:
            return 0
        
def run(problem_initialize, generation, popsize, evaluator, outputfreq = 1, condition = lambda x : False):
    init(popsize, problem_initialize, evaluator)
    return loop(generation, outputfreq, condition)


def mainpro(m):
    problem_initialize = m.problem_initialize()
    avr = ( run(problem_initialize, 10000, conf.popsize, m.evaluate ,0) )
    return avr

