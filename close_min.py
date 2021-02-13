import itertools
from collections import defaultdict
def in_one_not_in_two(a,b):
    return ''.join([item for item in b if item not in a])


def containsAll(item, tr):
    for i in item:
      if i not in tr:

         return False
    return True
def all_items_are_in_transaction(item, tr):
    for i in item:
        if i not in tr:return False
    print(i,tr,"True")
    return True
def has_infrequent_itemset(canditate, frequent_itemsets):
    frequent_itemsets = [fi[0] for fi in frequent_itemsets]
    canditate_subsets = itertools.combinations(canditate, len(canditate)-1)
    for subset in canditate_subsets:
        if ''.join(subset) not in frequent_itemsets:return True
    return False
def is_frequent(item_sets, min_sup, canditate):
    count = 0
    for transaction in item_sets:
        if set(canditate) <= set(transaction):count += 1       
    if count >= min_sup:return True, count
    return False, count
def frequent_list_from_iteration(transactions, minsup, candidats):
    return [[c, is_frequent(transactions, minsup, c)[1]]for c in candidats if is_frequent(transactions, minsup, c)[0]]
def hist(tr):
    transactions = defaultdict(int)
    for transaction in tr:
        for char in transaction:transactions[char] += 1
    return [[key,val] for key,val in transactions.items()]
def apriori_gen(frequent_itemsets):
    length = len(frequent_itemsets[0][0])
    if length == 1:
        for i in range(len(frequent_itemsets)-1):
            for j in range(i+1, len(frequent_itemsets)):
                canditate = sorted(
                    [frequent_itemsets[i][0], frequent_itemsets[j][0]])
                if frequent_itemsets[i][2] != ''.join(canditate) and frequent_itemsets[j][2] != ''.join(canditate):
                    yield ''.join(canditate)
    else:
        for i in range(len(frequent_itemsets)-1):
            for j in range(i+1, len(frequent_itemsets)):
                if frequent_itemsets[i][0][:length-1] == frequent_itemsets[j][0][:length-1]:
                    canditate = set(frequent_itemsets[i][0]).union(
                        set(frequent_itemsets[j][0]))
                    canditate = sorted(canditate)
                    if not has_infrequent_itemset(''.join(canditate), frequent_itemsets):
                        if frequent_itemsets[i][2] != ''.join(canditate) and frequent_itemsets[j][2] != ''.join(canditate):
                            yield ''.join(canditate)
def fermeture(frequent_itemsets, transactions):
    fermetures = []
    print(frequent_itemsets, transactions)
    for item in frequent_itemsets: 
        l = [item[0]]
        tr = [t for t in transactions if containsAll(item[0], t)]
        tr = hist(tr)
        #print(tr)
        for item2 in tr:
            if item2[1] == item[1] and item2[0] not in item[0]:
                l.append(item2[0])
        l = [''.join(l), item[1]]
        fermetures.append([item[0], l[1], ''.join(sorted(l[0]))])
    return fermetures
def output_association_rules(all_frequent):
    for items in all_frequent:
        for item in items:
            if item[0]!=item[2]:
                print(f'{item[0]}  -> {in_one_not_in_two(item[0],item[2])}')
transactions = ['ABCDE', 'AB', 'CE', 'ABDE', 'ACD','F']
minsup = 2
L =  hist(transactions)
L = fermeture(frequent_list_from_iteration(transactions, minsup, [x[0] for x in L]), transactions)
all_frequent =[]
while L != []:
    all_frequent.append(L)
    L = fermeture(frequent_list_from_iteration(transactions, minsup, list(apriori_gen(L))), transactions)
output_association_rules(all_frequent)
