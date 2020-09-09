# -*- coding: utf-8 -*-
import os
import copy
import poptools
import conf
import dynamic_tools
import sys
import first_phase

WORKING_DIR  = os.getcwd()
#PROBLEM_DIR = WORKING_DIR + r"/PROBLEM CEC2010"
PROBLEM_DIR = WORKING_DIR + r"/PROBLEM"
RESULT_DIR  = WORKING_DIR + r"/RESULT"
LOCAL_PATH  = [WORKING_DIR, PROBLEM_DIR, RESULT_DIR]
sys.path.extend(LOCAL_PATH)


    
def init(size, problem_initialize, evaluator):
    global K, g, _size, _genecount, _evaluator, parent_pop, upper, lower, objective_num, constraints_num
    _size, _genecount, _evaluator, upper, lower = size, problem_initialize[0], evaluator, problem_initialize[1], problem_initialize[2]
    objective_num, constraints_num = problem_initialize[5], problem_initialize[4]
    parent_pop = dynamic_tools.initialize_parent_population(_size, _genecount)
    for i in xrange(_size):
        parent_pop[i]["genes"] = first_phase_final_pop[i]
    dynamic_tools.caculate_pheno(parent_pop, upper, lower, _genecount, _size)
    dynamic_tools.evaluate_population(parent_pop, evaluator, dynamic_tools.get_fill_result)


def loop():
    global K, g
    MaxK = conf.MaxK
    while K <= MaxK:
        print "g:",g," K:",K
        tmp  = copy.deepcopy(parent_pop)
        tmp1 = copy.deepcopy(parent_pop)
        tmp1.sort(cmp = poptools.compare)
        best_individual = tmp1[0]
        for i in range(_size):
            tmp[i] = dynamic_tools.DE2_best(i, tmp, parent_pop, _size, _genecount, best_individual)
            #tmp[i] = dynamic_tools.DE1_bin(i, tmp, parent_pop, _size, _genecount)
            tmp[i] = dynamic_tools.cal_kth_pheno(i, tmp, upper, lower, _genecount)
            poptools.evaluate_ind(i, tmp, _evaluator, dynamic_tools._fill_result)
            tmp[i] = dynamic_tools.cal_kth_pheno(i, tmp, upper, lower, _genecount)
            if poptools.compare(tmp[i], parent_pop[i]) == -1:
                parent_pop[i], tmp[i] = tmp[i], parent_pop[i]
        K += 1
        g += 1
        feaNum = 0
        for p in parent_pop:
            if max(p["violations"]) == 0:
                feaNum += 1
        #print "feasible num:", feaNum

    


def leave():
    parent_pop.sort(cmp = poptools.compare)
    print "Second-stage Best:   ", parent_pop[0]
    print "Second-stage Worst:  ", parent_pop[-1]
    return parent_pop[0], parent_pop

def run(problem_initialize, evaluator):
    global popsize
    popsize = conf.popsize
    if problem_initialize[0] != 0 and problem_initialize[5] != 0:
        init(popsize, problem_initialize, evaluator)
        loop()
        return leave()
    else:
        print "ERROR: objectvies num = 0 or genecount = 0!"
        print "please click any letter"
        t = raw_input()
        return -1


def get_average(res):
    c = sum(res)
    ave = float(c)/len(res)
    return ave

def get_variance(res,ave):
    sumvar = 0.0
    for i in range(len(res)):
        sumvar = sumvar+pow(float(res[i])-ave,2)
    var = pow(sumvar/len(res),0.5)
    return var


if __name__=='__main__':
    import g01,g02,g03,g04,g05,g06,g07,g08,g09,g10,g11,g12,g13,g14,g15,g16,g17,g18,g19,g21,g23,g24
    #import c01,c02,c03,c04,c05,c06,c07,c08,c09,c10,c13,c14,c15,c16,c17,c18,c11,c12
    #module = [c01,c02,c03,c04,c05,c06,c07,c08,c09,c10,c13,c14,c15,c16,c17,c18,c11,c12]
    module = [g01]
    print "=====================    This is FRC-CEA   ==================================="
    for m in module:
        print "++++++++++++  This is", m.__name__, "problem  ++++++++++++"
        problem_initialize = m.problem_initialize()
        print "D is ",problem_initialize[0]
        t = 25
        res, res1, res2 = [], [], []
        initFile = open(RESULT_DIR + "/" + str(m.__name__) + ".txt",'w')
        initFile.write("This is FRC-CEA:\n")
        initFile.close()
        while t > 0:
            first_phase_final_pop, K, g = first_phase.mainpro(m)
            avr = (run(problem_initialize, m.evaluate))
            res.append(avr[0])
            res1.append(avr[1])
            initFile = open(RESULT_DIR + "/" + str(m.__name__) + ".txt", 'a')
            initFile.write('run is ' + str(t) + '\n')
            initFile.write(str(avr[0]) + '\n')
            t -= 1
            initFile.close()
        tmp_avr = []
        for i in range(len(res1)):
            tmp_avr.append(res[i]["objectives"])
        initFile = open(RESULT_DIR + "/" + str(m.__name__) + ".txt", 'a')
        print "Result:  ", tmp_avr
        print 'Worst is:', max(tmp_avr)
        print 'Best is :', min(tmp_avr)
        maxo, mino = max(tmp_avr), min(tmp_avr)
        ave = get_average(tmp_avr)
        print 'Average is:', ave
        var = get_variance(tmp_avr, ave)
        print 'Std is:   ', var
        initFile.write("worst is " + str(maxo) + '\n')
        initFile.write("best is  " + str(mino) + '\n')
        initFile.write("mean is  " + str(ave)  + '\n')
        initFile.write("std is   " + str(var)  + '\n')
        print "================================================================================"
        initFile.close()
