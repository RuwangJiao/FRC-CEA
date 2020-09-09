import random
import sys
import os
import shutil

def get_init_pop(size, genecount):
    pop = []
    for i in range(size):
        ind = {}
        ind['extrainfo']={}
        ind['vioclassify']={}
        ind['genes'] = [random.random() for j in range(genecount)]
        ind['extrainfo']['generation']=0
        pop.append(ind)
    return pop

def _fill_result(rst,inds):
    #for rst in rsts:

    i = rst['id']
    ind = inds[i]
    if not rst['valid']:
        ind['violation'] = sys.float_info.max
        ind['objective'] = sys.float_info.max
    else:
        ind['violation'] = sum(rst['violations'])
        ind['objective'] = rst['objective']

    if rst.get('extrainfo'):
        ind['extrainfo'].update(rst['extrainfo'])
            

def evaluate_pop_automatic(i,pop, evaluator, fill_result=_fill_result):
    if not hasattr(dtm, 'running'):
        evaluate_pop(i,pop, evaluator, fill_result)
    else:
        evaluate_pop_imap_unordered(pop, evaluator, fill_result)

def evaluate_pop(pop, evaluator, fill_result = _fill_result):
    results = []
    for i in range(len(pop)):
        pop[i]['id'] = i
        results.append(evaluator(pop[i]))
        rst = evaluator(pop[i])
    fill_result(rst, pop)
    
def evaluate_ind(i, pop, evaluator, fill_result = _fill_result):
    #results = []
    #for i in range(len(pop)):
    pop[i]['id'] = i
    #results.append(evaluator(pop[i]))
    rst = evaluator(pop[i])
    fill_result(rst, pop)

def evaluate_pop_imap_unordered(pop, evaluator, fill_result=_fill_result):
    iters = []
    for i in range(len(pop)):
        pop[i]['id'] = i

        # robust
        if global_conf.ROBUST_ENABLE:
            from robust import robust_problem
            iters += robust_problem.robust(pop[i])
        # normal
        else:
            iters.append(pop[i])
            
    imapNotOrderedObj = dtm.imap_unordered(evaluator, iters)
    results = [i for i in imapNotOrderedObj]

    # robust result select
    if global_conf.ROBUST_ENABLE:
        from robust import robust_problem
        results = robust_problem.select(results)

    ##zhoudong appended start
    for i in range(len(results)):
        if "err" in results[i].keys():
            results[i]=cst.getresult(results[i])
    
    fill_result(pop, results)

def evaluate_pop_map(pop, evaluator, fill_result=_fill_result):
    for i in range(len(pop)):
        pop[i]['id'] = i
    results = dtm.map(evaluator, pop)
    fill_result(pop, results)

def compare(a, b):
    if max(a["violations"]) < max(b["violations"]):
        return -1
    elif max(a["violations"]) > max(b["violations"]):
        return 1
    else:
        if a["objectives"] < b["objectives"]:
            return -1
        elif a["objectives"] > b["objectives"]:
            return 1
        else:
            return 0

def condition(pop):
    pop.sort(cmp=compare)
    if pop[0]['violation'] < 1e-6:
        return True

def copyFiles(sourceDir,  targetDir): 
      for file in os.listdir(sourceDir):
          sourceFile = os.path.join(sourceDir, file)
          targetFile = os.path.join(targetDir, file) 
          if os.path.isfile(sourceFile): 
              if not os.path.exists(targetDir):  
                  os.makedirs(targetDir)  
              if not os.path.exists(targetFile) or(os.path.exists(targetFile) and (os.path.getsize(targetFile) != os.path.getsize(sourceFile))):  
                  open(targetFile, "wb").write(open(sourceFile, "rb").read()) 
          if os.path.isdir(sourceFile): 
              First_Directory = False 
              copyFiles(sourceFile, targetFile)

def getindfoldername(filename):#2_1
    if os.path.basename(os.path.dirname(filename))=='result':
        return os.path.basename(filename)
    else:
        flname=os.path.dirname(filename)
        return getindfoldername(flname)
def getindfolderpath(filename):#result\2_1
    if os.path.basename(os.path.dirname(filename))=='result':
        return filename
    else:
        flname=os.path.dirname(filename)
        return getindfolderpath(flname)

              
if __name__ == '__main__':
    a = {}
    b = {}
    a['violation'] = 5
    b['violation'] = 5
    a['objective'] = 7
    b['objective'] = 5
    print compare(a, b)
