import itertools
from collections import defaultdict
import sqlite3


#help functions : 

def transactions_from_db(table_n,db_file_name):
    with sqlite3.connect(db_file_name) as conn:
        cur = conn.cursor()
        data = cur.execute(
            f"select transactions from  data_table{table_n}").fetchall()
    return [x[0] for x in data]


def est_sa_fermeture(item, tr):
    for t in tr:
        if all_items_are_in_transaction(item[0], t) and not all_items_are_in_transaction(item[2], t):
            return False
    return True

def all_items_are_in_transaction(item, tr):
    for i in item:
        if i not in tr:
            return False
    return True

def has_infrequent_itemset(canditate, frequent_itemsets):
    frequent_itemsets = [fi[0] for fi in frequent_itemsets]
    #print(frequent_itemsets)
    canditate_subsets = itertools.combinations(
        canditate, len(canditate)-1)  # get_subsets
    for subset in canditate_subsets:
        if ''.join(subset) not in frequent_itemsets:
            return True
    return False

def is_frequent(item_sets, min_sup, canditate):
    #retourne si l'item est fréquent et son nombre d'apparition
    count = 0
    for transaction in item_sets:
        if set(canditate) <= set(transaction):
            count += 1
    if count >= min_sup:
        return True, count
    return False, count

def frequent_list_from_iteration(transactions, minsup, candidats):
    rv = [[c, is_frequent(transactions, minsup, c)[1]]
          for c in candidats if is_frequent(transactions, minsup, c)[0]]
    print(f"frequents ->{rv}")
    return rv
    
def hist(tr):
    #retourner le nombre d'appaition de chaque produit dans une liste de transacion
    transactions = defaultdict(int)
    for transaction in tr:
        for char in transaction:
            transactions[char] += 1
    return [[key,val] for key,val in transactions.items()]


#Main functions:
def apriori_gen(frequent_itemsets):
    #retourner touts les (n+1)-generatoeurs a partir des (n)-generateurs frequents 
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
    fermetures = []  # initialiser le resultat retourné
    for item in frequent_itemsets:  # parcourir les itemsets frequent d'une iteration i
        # l'itemset appartient toujours a sa fermeture
        l = [item[0]]
        # garder que les iterations qui contient l'item concerné
        tr = [t for t in transactions if all_items_are_in_transaction(item[0],t)]
        tr = hist(tr)  # recalculer l'histogramme
        for item2 in tr:
            #si son supp = a supp de l'item concerné et in n'est pas deja inclu dans l'item                                 #pour chaque element dans l'histogramme
            if item2[1] == item[1] and item2[0] not in item[0]:
                l.append(item2[0])  # on l'ajoute a une liste des items
        l = [''.join(l), item[1]]
        # retourner l'itemset , son supp ansi que sa fermeture
        fermetures.append([item[0], l[1], ''.join(sorted(l[0]))])
    print(f"fermetures -> {fermetures}\n")
    return fermetures


# outputs
def in_one_not_in_two(a, b):
    return ''.join([item for item in b if item not in a])

def output_association_rules(all_frequent):
    print('\nregles d assosiations:')
    for items in all_frequent:
        for item in items:
            if item[0]!=item[2]:
                print(f'{item[0]}  -> {in_one_not_in_two(item[0],item[2])}')
            

def close_alg(db,minsup):
    #1 ére iteration
    nb_of_tables = len(minsup)
    table_n = 0
    minsupi = minsup[table_n]
    transactions = transactions_from_db(table_n+1,db)
    L =  hist(transactions)
    L=[x[0] for x in L]

    ##filter out the non frequent itemsets
    L = frequent_list_from_iteration(transactions, minsupi, L)
    ##trouver les fermetures
    L = fermeture(L, transactions)
    all_frequent =[]
    while L != []:

        table_n +=1
        #-------------------------------
        while table_n <table_number :
            del transactions
            transactions = transactions_from_db(table_n+1, db)
            print(f"before -> {L}")
            L = list(filter(lambda x: (est_sa_fermeture(x, transactions)), L))
            print(f"After -> {L}")
            table_n +=1
        #-------------------------------
        table_n = 0
        transactions = transactions_from_db(table_n+1, db)
        all_frequent.append(L)
        ##Next generation of itemsets iteration d'appriori
        L = list(apriori_gen(L)) 

        ##filter out the non frequent itemsets
        L = frequent_list_from_iteration(transactions, minsupi, L)
        ##trouver les fermetures
        L = fermeture(L, transactions)
    return all_frequent



if __name__ == '__main__':

    db = "training_datatset.db"
    with sqlite3.connect(db) as conn:
        print("__________Database infos_________________\n")
        cur = conn.cursor()
        num_of_tables = cur.execute(
            "SELECT count(*) FROM sqlite_master WHERE type = 'table' AND name like '%data_table%'").fetchall()[0][0]
        data = [cur.execute(f"select count(transactions) from  data_table{i+1}").fetchall()[
            0][0] for i in range(num_of_tables)]
        for i, display in enumerate(data):
            print(f"number of transactions in table n:{i+1} -> {display}")
        print(f"*total transactiosn in the database -> {sum(data)}")
        print("_________________________________________\n")


    table_number = num_of_tables+1
    while table_number > num_of_tables:
        try:
            table_number = int(
                input("select the number of tables you want to use : "))
        except:
            table_number = num_of_tables+1

    minsupi = [int(input(f"enter the min sup fot the table {i+1} : ")) for i in range(table_number)]
    closed = close_alg(db, minsupi)
    output_association_rules(closed)
