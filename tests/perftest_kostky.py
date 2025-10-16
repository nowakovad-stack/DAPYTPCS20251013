'''
    Play game: test rychlosti vypoctu skore 
'''
import os
import re
import time
import random


def score_postupky_tuplein(*throw):
    ''' Calculate score using LIST 'in' clause '''
    score = 0
    if len(throw) == 6 and 1 in throw and 2 in throw:
        score = 20
        if 3 in throw:
            score = 30
            if 4 in throw:
                score = 50
                if 5 in throw:
                    score = 90
                    if 6 in throw:
                        score = 200
    #log.debug("Calculated score for %s is %d",throw,score)
    return score

def score_table(*throw):
    '''
    Calculate using scoring table
    '''
    score = 0
    skoreTable = {
        1 : 0,
        2 : 20,
        3 : 30,
        4 : 50,
        5 : 90,
        6 : 200
    }
    if len(throw) == 6:
        score = -1
        for i in skoreTable.keys():
            for val in throw:
                if val == i:
                    score = skoreTable[i]
                    break  
            if score != skoreTable[i]:
                break
        if score == -1:
            score =0
    return score


def score_loop(*throw):
    last = 0
    score = 0
    score_list = (0, 20, 30, 50, 90, 200)
    set_throw = set(throw)
    if len(throw) == 6: 
        for ii in range(1, 7):
            if ii in set_throw:
                score = score_list[last]
                last += 1
            else:
                break
    return score


def score_postupky_setops(*throw):
    ''' calculate score using SET operations '''
    #log.debug("Calculating score for %s",throw)
    if len(throw) != 6:
        return 0
    throw = set(throw)
    score = 0
    if len(throw & {1,2,3,4,5,6}) == 6:
        score = 200
    elif len(throw & {1,2,3,4,5}) == 5:
        score = 90
    elif len(throw & {1,2,3,4}) == 4:
        score = 50
    elif len(throw & {1,2,3}) == 3:
        score = 30
    elif len(throw & {1,2}) == 2:
        score = 20
    #log.debug("Calculated score for %s is %d",throw,score)
    return score


def score_postupky_setin(*throw):
    ''' Calculate score using SET 'in' clause '''
    #log.debug("Calculating score for %s",throw)
    if len(throw) != 6:
        return 0
    score = 0
    if set([1,2]).issubset(throw):
        score = 20
        if 3 in throw:
            score = 30
            if 4 in throw:
                score = 50
                if 5 in throw:
                    score = 90
                    if 6 in throw:
                        score = 200
    #log.debug("Calculated score for %s is %d",throw,score)
    return score


def score_postupky_strin(*throw):
    ''' Calculate score using str operations '''
    #log.debug("Calculating score for %s",throw)
    if len(throw) != 6:
        return 0
    throw = f"{throw}"
    score = 0
    if throw.find("1")>-1:
        if throw.find("2")>-1:
            score = 20
            if throw.find("3")>-1:
                score = 30
                if throw.find("4")>-1:
                    score = 50
                    if throw.find("5")>-1:
                        score = 90
                        if throw.find("6")>-1:
                            score = 200
    #log.debug("Calculated score for %s is %d",throw,score)
    return score


def score_postupky_regex(*throw):
    ''' calculate score using regex '''
    #log.debug("Calculating score for %s",throw)
    if len(throw) != 6:
        return 0
    throw = list(throw[0:6])
    throw.sort()
    throw = f"{throw[0]}{throw[1]}{throw[2]}{throw[3]}{throw[4]}{throw[5]}"
    score = 0
    if re.match('123456',throw):
        score = 200
    elif re.match('1+2+3+4+5+',throw):
        score = 90
    elif re.match('1+2+3+4+',throw):
        score = 50
    elif re.match('1+2+3+',throw):
        score = 30
    elif re.match('1+2+',throw):
        score = 20
    #log.debug("Calculated score for %s is %d",throw,score)
    return score


def score_postupky_eqset_desc(*throw):
    ''' calculate score using set equality '''
    # Scoring logic for throwing six dice
    if len(throw) != 6:
        return 0
    dice_set = set(throw)  # Removing duplicates from the dice values
    score = 0
    # Scoring rules
    if dice_set & {1, 2, 3, 4, 5, 6} == {1, 2, 3, 4, 5, 6}:
        score = 200
    elif dice_set & {1, 2, 3, 4, 5} == {1, 2, 3, 4, 5}:
        score = 90
    elif dice_set & {1, 2, 3, 4} == {1, 2, 3, 4}:
        score = 50
    elif dice_set & {1, 2, 3} == {1, 2, 3}:
        score = 30
    elif dice_set & {1, 2} == {1, 2}:
        score = 20

    return score


def score_dict_counts(*throw):
    if len(throw) != 6:
        return 0  

    counts = {i: throw.count(i) for i in set(throw)}
    score = 0
    if counts.get(1, 0) >= 1 and counts.get(2, 0) >= 1:
        score = 20
        if counts.get(3, 0) >= 1:
            score = 30
            if counts.get(4, 0) >= 1:
                score = 50
                if counts.get(5, 0) >= 1:
                    score = 90
                    if counts.get(6, 0) >= 1:
                        score = 200

    return score


def score_postupky_supersets(*throw):
    score = 0
    if len(throw) == 6:
        sorted_throw = set(throw)
        if sorted_throw.issuperset({1, 2, 3, 4, 5, 6}):
            score = 200
        elif sorted_throw.issuperset({1, 2, 3, 4, 5}):
            score = 90
        elif sorted_throw.issuperset({1, 2, 3, 4}):
            score = 50
        elif sorted_throw.issuperset({1, 2, 3}):
            score = 30
        elif sorted_throw.issuperset({1, 2}):
            score = 20
    return score



def score_postupky_manual_unique(*throw):
    score = 0
    if len(throw) != 6:
            return 0
    uniq = []
    vstup = list(throw)
    vstup.sort()
    vystup = []
    for hod in vstup: 
        if hod not in uniq: 
            uniq.append(hod)
    if uniq[0] == 1 and uniq[1] == 2:
        vystup.append(uniq[0])
        for hod in range(1, len(uniq)):
            if uniq[hod] == uniq[hod-1] + 1:
                vystup.append(uniq[hod])
            else:
                break
    
    if vystup == [1, 2]:
        score = 20
    if vystup == [1, 2, 3]:
        score = 30
    if vystup == [1, 2, 3, 4]:
        score = 50
    if vystup == [1, 2, 3, 4, 5]:
        score = 90
    if vystup == [1, 2, 3, 4, 5, 6]:
        score = 200    

    return score


def score_postupky_for(*throw):
    score = 0
    if len(throw) != 6:
        return 0
    seen = set(throw)
    sorted_t= sorted(seen)

    points = [20, 30, 50, 90, 200]
    if (sorted_t[0] == 1 and len(sorted_t) > 0 and len(throw) < 7):
        for i in range(1,len(sorted_t)):
            if ((sorted_t[i]) - 1 == sorted_t[i - 1]):
                 score = points[i - 1]
            else:
                 break
    return score


def score_postupky_for_match(*throw):
    score = 0 
    if len(throw) == 6:
        postupka = 0
        set_hody = {*throw}
        list_hody = list(set_hody)
        #print(list_hody)

        for i in range(0,len(list_hody) ):
            #print(i)
            if i+1 == list_hody[i]:
                postupka += 1
                #print(list_hody[i])
            else:
                break
        #print(f"pocet cisel jdoucich po sobe je {postupka} ")
        
        match postupka:
            case 2:
                score = 20
            case 3:
                score = 30
            case 4:
                score = 50
            case 5:
                score = 90
            case 6:
                score = 200
    return score


def performance(throws,executor):
    start = time.time_ns()
    for throw in throws:
        executor(*throw)
    exectime = time.time_ns() - start
    #print(f"{executor.__name__} in {exectime/1000000:,}ms")
    return (exectime,executor.__name__)


funcs = [
        score_postupky_tuplein,
        score_postupky_supersets,
        score_postupky_setin,
        score_postupky_setops,
        score_postupky_eqset_desc,
        score_postupky_regex,
        score_dict_counts,
        score_postupky_strin,
        score_postupky_manual_unique,
        score_postupky_for_match,
        score_postupky_for,
        score_loop,
        score_table,
    ]

TESTS = (
    ([1,2,3,4,5,6],200),
    ([6,6,3,2,1,7],30),
    ([1,2,4,4,5,6],20),
    ([2,2,3,4,1,6],50),
    ([2,5,3,4,1,3],90),
    ([1,2,3,4],0),
    ([6,5,4,4,3,2,1],0),
)

# test validity
cont = True 
for func in funcs:
    ok = True
    for test in TESTS:
        res = func(*test[0])
        tok = res == test[1]
        if tok:
            print(test[0]," - OK")
        else:
            print(test[0],f" - expected '{test[1]}', got '{res}'")
        ok = ok & tok
    print(f"{func.__name__}': ","OK" if ok else "někde je chyba")
    cont &= ok

if cont:
    # perf test
    reps = 200000
    throws = []
    for ii in range(0,reps):
        throws.append(random.sample(range(1,7),6))

    print("\nPerformance test start:",reps,"opakování")

    results = []
    for func in funcs:
        results.append(performance(throws, func))

    print("\nPerformance test finish:")
    for rs in sorted(results):
        print(f"\t{rs[1].ljust(30,' ')} {rs[0]/1000000:,}ms")
