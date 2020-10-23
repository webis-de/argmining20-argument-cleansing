import csv
import krippendorff
import numpy as np


def main():
    manual_eval_eval()


def manual_eval_eval():
    '''
    Calculation of manual evaluation based on annotator data
    '''
    dir = '' # If necessary specify dir to annotator files and sentence rounds
    # results will be generated in the same folder
    annotator_1 = read_csv(f'{dir}annotator_1.csv')
    annotator_2 = read_csv(f'{dir}annotator_2.csv')
    annotator_3 = read_csv(f'{dir}annotator_3.csv')
    sentences_rounds = read_csv(f'{dir}sentences_matched.csv')
    results = []
    for entry_annotator_1 in annotator_1:
        breaker = False
        for entry_annotator_2 in annotator_2:
            for entry_annotator_3 in annotator_3:
                if entry_annotator_1[0] == entry_annotator_2[0] and entry_annotator_1[0] == entry_annotator_3[0]:
                    results.append([entry_annotator_1[0], entry_annotator_1[1], entry_annotator_2[1], entry_annotator_3[1]])
                    breaker = True
                    break
            if breaker:
                break

    results = results[1:]

    counter = 0
    temp = []
    for sentence in sentences_rounds:
        sentence[1] = eval(sentence[1])
        for entry in results:
            sentence_clean = re.sub(r'[^a-zA-Z]', '', sentence[1][0]).strip().lower()
            entry_clean = re.sub(r'[^a-zA-Z]', '', entry[0]).strip().lower()
            if sentence_clean == entry_clean:
                if not len(entry) == 5:
                    entry.append(sentence[1][1])
                    counter += 1
                    break

    precisions = dict()
    for entry in results:
        calc_total_prec(precisions,entry)

    for key in precisions:
        if 'Total' in key:
            precisions[key] = precisions[key]/600
        else:
            precisions[key] = precisions[key]/100

    # DATA TRANSFORMED FOR FLEISS KAPPA
    fleiss_kappa_data = []
    THANKS = True
    I = True
    for entry in results:
        if 'Thanks and I wish my opponent good luck for the debate' in entry[0] and THANKS:
            entry[0] = f'{entry[0]}.'
            THANKS = False
        if 'I wish my opponent luck and hope for an enjoyable debate' in entry[0] and I:
            entry[0] = f'{entry[0]}.'
            I = False

        counter = 0
        for num in entry[1:-1]:
            if num == 1:
                pass
            fleiss_kappa_data.append((entry[0],num))
    precisions['Fleiss Kappa'] = fleiss_kappa(fleiss_kappa_data,3)

    # DATA TRANSFORMED KRIPPENDORFFS ALPHA
    temp = []
    for entry in results:
        counter = 0
        for num in entry[1:-1]:
            if int(num) == 1:
                # print(counter)
                counter += 1
        temp.append([3-counter, counter])
    value_counts = np.array(temp)

    precisions['Krippendorffs alpha (nominal)'] = krippendorff.alpha(value_counts=value_counts, level_of_measurement='nominal')
    precisions['Krippendorffs alpha (interval)'] = krippendorff.alpha(value_counts=value_counts)

    write_dict_to_csv(precisions, f'{dict}precision_list')


def create_or_add_entry(dict, key):
    '''
    creates or adds an entry to a dictionary
    '''
    if key in dict:
        dict[key] += 1
    else:
        dict[key] = 1


def calc_part_prec(dict, entry, keyword='Total'):
    '''
    Adds entries to dict for later total precision calculation
    '''
    if entry[1] == '0':
        create_or_add_entry(dict, f'{keyword} annotator_1')
    if entry[2] == '0':
        create_or_add_entry(dict, f'{keyword} annotator_2')
    if entry[3] == '0':
        create_or_add_entry(dict, f'{keyword} annotator_3')

    if entry[1] == '0' or entry[2] == '0' or entry[3] == '0':
        create_or_add_entry(dict, f'{keyword} At least one')

    if entry[1] == '0' and entry[2] == '0':
        create_or_add_entry(dict, f'{keyword} Majority')
    elif entry[1] == '0' and entry[3] == '0':
        create_or_add_entry(dict, f'{keyword} Majority')
    elif entry[2] == '0' and entry[3] == '0':
        create_or_add_entry(dict, f'{keyword} Majority')

    if entry[1] == '0' and entry[2] == '0' and entry[3] == '0':
        create_or_add_entry(dict, f'{keyword} Full')


def calc_total_prec(dict, entry):
    '''
    Recursive fnc for call of partial precision calculation based on keywords
    '''
    if entry[4] == 'Initial':
        calc_part_prec(dict, entry, 'Initial')
    elif entry[4] == 'Round 1':
        calc_part_prec(dict, entry, 'Round 1')
    elif entry[4] == 'Round 2':
        calc_part_prec(dict, entry, 'Round 2')
    elif entry[4] == 'Round 3':
        calc_part_prec(dict, entry, 'Round 3')
    elif entry[4] == 'Round 4':
        calc_part_prec(dict, entry, 'Round 4')
    elif entry[4] == 'Round 5':
        calc_part_prec(dict, entry, 'Round 5')

    calc_part_prec(dict,entry)


# copied and modified from https://github.com/amirziai/learning/blob/master/statistics/Inter-rater%20agreement%20kappas.ipynb
def fleiss_kappa(ratings, n):
    '''
    Computes the Fleiss' kappa measure for assessing the reliability of
    agreement between a fixed number n of raters when assigning categorical
    ratings to a number of items.

    Args:
        ratings: a list of (item, category)-ratings
        n: number of raters
    Returns:
        the Fleiss' kappa score

    See also:
        http://en.wikipedia.org/wiki/Fleiss'_kappa
    '''
    items = set()
    categories = set()
    n_ij = {}

    for i, c in ratings:
        items.add(i)
        categories.add(c)
        n_ij[(i,c)] = n_ij.get((i,c), 0) + 1

    N = len(items)

    p_j = dict(((c, sum(n_ij.get((i, c), 0) for i in items) / (1.0 * n * N)) for c in categories))
    P_i = dict(((i, (sum(n_ij.get((i, c), 0) ** 2 for c in categories) - n) / (n * (n - 1.0))) for i in items))

    P_bar = sum(P_i.values()) / (1.0 * N)
    P_e_bar = sum(value ** 2 for value in p_j.values())

    kappa = (P_bar - P_e_bar) / (1 - P_e_bar)

    return kappa


def read_csv(path):
    ''' Reads csv '''
    csv_data = []
    with open(path, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for entry in reader:
            csv_data.append(entry)
    return csv_data


def write_dict_to_csv(dict, name):
    ''' writes dictionaries to csv '''
    name += '.csv'
    with open(name, mode='w') as file:
        for key in dict.keys():
            file.write('%s,"%s"\n'%(key,dict[key]))
