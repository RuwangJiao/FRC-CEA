# -*- coding: utf-8 -*-
import random
import sys

def select_next_parent_population(_S, _pop, N):
    next_parent_pop = []
    C = []
    #combine parent and offspring population
    for j in range(len(_S)):
        C.append(_S[j])
    for j in range(len(_pop)):
        C.append(_pop[j])

    ### reserve around a half of population size feasible solutions ###
    RESERVE_NUM = N/2
    feasi_list = []
    for i in xrange(len(C)):
        if C[i]["violation_objectives"][0] == 0:
            feasi_list.append(C[i])
            
    if len(feasi_list) < RESERVE_NUM:
        next_parent_pop.extend(feasi_list)
    else:
        nondominated_rank = fast_non_dominated_sort(feasi_list, len(feasi_list))
        for i in xrange(len(nondominated_rank)):
            if len(next_parent_pop)+len(nondominated_rank[i]) <= RESERVE_NUM:
                for h in range(len(nondominated_rank[i])):
                    next_parent_pop.append(nondominated_rank[i][h])
            elif len(next_parent_pop)+len(nondominated_rank[i]) > RESERVE_NUM:
                temp = crowding_distance(nondominated_rank[i])
                num = RESERVE_NUM - len(next_parent_pop)
                for h in xrange(num):
                    next_parent_pop.append(temp[h])
    for p in next_parent_pop:
        C.remove(p)

    #all nondominated fronts of C
    nondominated_rank = fast_non_dominated_sort(C, len(C))
    
    #the number of members in first front
    Num = len(nondominated_rank[0])
    
    #fill the next_parent_pop with nondominated_rank ,
    #until |next_parent_pop|+|nondominated_rank[i]|>N
    #calculate crowding_distance in nondominated_rank[i]
    #choose the first (N-|next_parent_pop|)elements of nondominated_rank[i]
    for i in xrange(len(nondominated_rank)):
        if len(next_parent_pop) + len(nondominated_rank[i]) <= N:
            for h in range(len(nondominated_rank[i])):
                next_parent_pop.append(nondominated_rank[i][h])
        elif len(next_parent_pop)+len(nondominated_rank[i]) > N:
            temp = crowding_distance(nondominated_rank[i])
            num = N - len(next_parent_pop)
            for h in xrange(num):
                next_parent_pop.append(temp[h])        
    return next_parent_pop

def fast_non_dominated_sort(pop, size): #get the nondominated rank
    f_pop = [{'num':0,'set':[]} for i in xrange(size)]    
    for i in xrange(size):
        for j in xrange(size):
            flag = compare_indivial(pop[i], pop[j])
            #if pop[i] dominates pop[j]
            #add position flag j for pop[j] to set of solutions dominated by pop[i]
            #increment the domination counter of pop[j]
            if flag == True:                  
                f_pop[i]['set'].append(j)      
                f_pop[j]['num'] += 1
    front = []   #uesd to store the members of the front
    count = 0
    for i in range(size):
        temp = []
        temp_1 = []
        for j in xrange(size):
            if f_pop[j]['num'] == 0:
                pop[j]['nondomLayer'] = [i]
                temp.append(pop[j])
                f_pop[j]['num'] += -1
                count += 1
                temp_1.append(j)
        for j in xrange(len(temp_1)):
            index = temp_1[j]
            for k in xrange(len(f_pop[index]['set'])):
                f_pop[f_pop[index]['set'][k]]['num'] += -1
        if len(temp) != False:
            front.append(temp)
        if count == size:
            break
    return front

def compare_indivial(a, b): # compare a and b
    if a['efeasible'] != b['efeasible']:
        if a['efeasible'] == 1:
            return True
        else:
            return False
    elif a['efeasible'] == 1 and b['efeasible'] == 1:
        for i in xrange(len(a['objectives'])):
            if a['objectives'][i] > b['objectives'][i]:
                return False
        for i in xrange(len(a['violation_objectives'])):
            if a['violation_objectives'][i] > b['violation_objectives'][i]:
                return False
        if a['objectives'] == b['objectives'] and a['violation_objectives'] == b['violation_objectives']:
            return False
        else:
            return True
    elif a['efeasible'] == 0 and b['efeasible'] == 0:
        if a['violation_objectives'][0] < b['violation_objectives'][0]:
            return True
        else:
            return False

def crowding_distance(pop):
    #number of solutions in pop
    #initialize distance ,for each i in pop ,pop[i]distance=0
    for i in pop:
        i['distance'] = 0.0 
    #for each objective m
    #sort using each objective value 
    #set the boundary points'distance infinity, so that boundary points are always selected
    #for all other points
    #pop[i]distance=pop[i]distance +(pop[i+1].m-pop[i-1].m)/(fmax.m-fmin.m)
    for j in xrange(len(pop[0]['violation_objectives'])):
        pop.sort(key = lambda x : x['violation_objectives'][j], reverse = True)
        pop[0]['distance'] = pop[-1]['distance'] = sys.float_info.max
        temp = pop[0]['violation_objectives'][j] - pop[-1]['violation_objectives'][j]
        if temp < 0.0001:
            temp = 0.0001
        for i in xrange(1, len(pop)-1):
            dis = pop[i-1]['violation_objectives'][j] - pop[i+1]['violation_objectives'][j]
            dis = dis/temp
            pop[i]['distance'] += dis
    for j in xrange(len(pop[0]['objectives'])):
        pop.sort(key = lambda x : x['objectives'][j], reverse = True)
        temp = pop[0]['objectives'][j] - pop[-1]['objectives'][j]
        if temp < 0.0001:
            temp = 0.0001
        for i in xrange(1, len(pop)-1):
            dis = pop[i-1]['objectives'][j] - pop[i+1]['objectives'][j]
            dis = dis/temp
            pop[i]['distance'] += dis       
    pop.sort(key = lambda x : x['distance'], reverse = True)
    return pop
