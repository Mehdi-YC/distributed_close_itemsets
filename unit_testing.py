import itertools
def all_subsets(ss):
  return [''.join(i) for i in itertools.chain(*map(lambda x: itertools.combinations(ss, x), range(len(ss)-1, len(ss))))]


#print(all_subsets('ABCD'))
def all_items_are_in_transaction(item, tr):
    for i in item:
        if i not in tr:
            return False
    return True

def est_sa_fermeture(item, tr):
    for t in tr:
        if  all_items_are_in_transaction(item[0], t) and not all_items_are_in_transaction(item[2], t):
            print(item[0], item[2],t)
            return False
    return True


transactions = ['ABCDE', 'AB', 'CE', 'ABDE', 'ACD', 'F']
print(est_sa_fermeture(['A', 3, 'AB'], transactions))
print(est_sa_fermeture(['B', 3, 'AB'], transactions))



