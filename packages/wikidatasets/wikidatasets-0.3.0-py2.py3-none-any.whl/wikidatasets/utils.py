import pickle
import json
import pandas as pd
import os

from wikidatasets.exceptions import ParsingException
from tqdm import tqdm

from SPARQLWrapper import SPARQLWrapper, JSON


def get_results(endpoint_url, query):
    sparql = SPARQLWrapper(endpoint_url)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


def to_json(line):
    if line[-1] == ',':
        line = line[:-1]  # all lines should end with a ','

    # turn string to json
    if line[0] != '{' or line[-1] != '}':
        # then this line is not a proper json file we should deal with it later
        raise ParsingException

    return json.loads(line)


def concat_claims(claims):
    """

    Parameters
    ----------
    claims: dict

    Returns
    -------
    iter: iterator
        iterator through the claims
    """

    for rel_id, rel_claims in claims.items():
        for claim in rel_claims:
            yield claim


def to_triplets(ent):
    """

    Parameters
    ----------
    ent: dict
        Dictionary coming from the parsing of a json line of the dump.

    Returns
    -------
    triplets: list
        List of triplets of this entity (head, rel, tail).
    """
    if len(ent['claims']) == 0:
        return []
    claims = concat_claims(ent['claims'])
    triplets = []
    instanceof = []
    e1 = ent['id']
    for claim in claims:
        mainsnak = claim['mainsnak']
        if mainsnak['snaktype'] != "value":
            continue
        if mainsnak['datatype'] == 'wikibase-item':
            rel = mainsnak['property']
            e2 = 'Q{}'.format(mainsnak['datavalue']['value']['numeric-id'])
            triplets.append((e1, rel, e2))
            if rel == 'P31':
                instanceof.append(e2)
    return triplets, instanceof


def get_type(ent):
    return ent['type']


def get_id(ent):
    return ent['id']


def get_label(ent):
    """

    Parameters
    ----------
    ent: dict
        Dictionary coming from the parsing of a json line of the dump.

    Returns
    -------
    label: str
        Label of ent in english if available of any other language else.
    """

    labels = ent['labels']
    if len(labels) == 0:
        return 'No label {}'.format(ent['id'])
    if 'en' in labels.keys():
        return labels['en']['value']
    else:
        return labels[list(labels.keys())[0]]['value']


def relabel(x, labels):
    try:
        lab = labels[x]
        if ':' in lab:
            return lab[lab.index(':')+1:]
        else:
            return lab
    except KeyError:
        return x


def clean(str_):
    if str_[:31] == 'http://www.wikidata.org/entity/':
        return str_[31:]
    else:
        print('problem')
        return ''


def get_pickle_path(path):
    if path[-1] != '/':
        path = path+'/'
    pickle_path = path + 'pickles/'
    if not os.path.exists(pickle_path):
        os.makedirs(pickle_path)
    return pickle_path


def write_to_pickle(pickle_path, facts, fails, n_pickle_dump):
    pickle.dump((facts, fails),
                open(pickle_path + 'dump{}.pkl'.format(n_pickle_dump), 'wb'))
    print('Just made pickle dump number {}'.format(n_pickle_dump))
    return [], []


def intersect(long_list, short_list):
    return len(set(long_list).intersection(set(short_list))) > 0


def count_true_fails(fails):
    true_fails = 0
    for f in fails:
        try:
            if str(f) == ']':
                continue  # in this case it's the last line of the original dump file
            if len(f['claims']) > 0:
                true_fails += 1
        except:
            print(f)
    return true_fails


def concatpkls(n_dump, path_pickle, labels=None):
    df = pd.DataFrame(columns=['headEntity', 'relation', 'tailEntity'])

    for nd in tqdm(range(n_dump)):
        with open(path_pickle + 'dump{}.pkl'.format(nd + 1), 'rb') as f:
            facts, fails = pickle.load(f)
            true_fails = count_true_fails(fails)
            if true_fails > 0:
                print('{} true fails'.format(true_fails))
        df = pd.concat([df, pd.DataFrame(facts, columns=['headEntity', 'relation', 'tailEntity'])])
    df = df.drop_duplicates()

    if labels is not None:
        df['headEntity'] = df['headEntity'].apply(relabel, args=(labels,))
        df['relation'] = df['relation'].apply(relabel, args=(labels,))
        df['tailEntity'] = df['tailEntity'].apply(relabel, args=(labels,))

    return df


def write_csv(df, name):
    with open(name, 'w', encoding='utf-8') as f:
        f.write('headEntity\ttailEntity\trelation\n')
        df.to_csv(f, sep='\t', header=False, index=False)


def write_ent_dict(df, name):
    with open(name, 'w', encoding='utf-8') as f:
        f.write('entityID\twikidataID\tlabel\n')
        df.to_csv(f, sep='\t', header=False, index=False)


def write_rel_dict(df, name):
    with open(name, 'w', encoding='utf-8') as f:
        f.write('relationID\twikidataID\tlabel\n')
        df.to_csv(f, sep='\t', header=False, index=False)


def write_readme(name, n_core_ents, n_attrib_ents,
                 n_core_rels, n_attrib_rels,
                 n_core_facts, n_attrib_facts,
                 dump_date):
    with open(name, 'w', encoding='utf-8') as f:
        f.write('Built with WikiData dump from {}.\n'.format(dump_date))
        f.write("Here are some meta data about this data set:\n")
        f.write("Core entities: {}\n".format(n_core_ents))
        f.write("Attribute entities: {}\n".format(n_attrib_ents))
        f.write("Core relations: {} (number of different relations involving only core entities)\n".format(n_core_rels))
        f.write("Attribute relations: {} (number of different relations from core entities "
                "to attribute entities)\n".format(n_attrib_rels))
        f.write("Core facts: {} (facts involving only core entities)\n".format(n_core_facts))
        f.write("Attribute facts : {} (facts linking core entities "
                "to their attribute entities)\n".format(n_attrib_facts))
        f.write("Find more details about this dataset at https://arxiv.org/abs/1906.04536.")


def load_data_labels(path, attributes=False, return_dicts=False):
    """This function loads the edges and attributes files into Pandas dataframes and merges the labels of entities and \
    relations to get.

    Parameters
    ----------
    path: str
        Path to the directory containing the edges.txt, attributes.txt, entities.txt, relations.txt files.
    attributes: bool
        Boolean indicating if we should read the attributes files. If False, then the edges file is read.
    return_dicts: bool
        Boolean indicating if the entities and relations labels dictionaries should be returned.

    Returns
    -------
    df: pandas.DataFrame
        DataFrame containing either the edges or the attributes depending on the value of `attributes`.
    entities: pandas.DataFrame
        DataFrame containing the list of all entities and wikidata IDs and labels.
    relations: pandas.DataFrame
        DataFrame containing the list of all relations and wikidata IDs and labels.
    """

    if attributes:
        df = pd.read_csv(path + 'attributes.tsv', sep='\t')
    else:
        df = pd.read_csv(path + 'edges.tsv', sep='\t')

    entities = pd.read_csv(path + 'entities.tsv', sep='\t')
    relations = pd.read_csv(path + 'relations.tsv', sep='\t')

    df = pd.merge(left=df, right=entities[['entityID', 'label']], left_on='headEntity',
                  right_on='entityID')
    df.drop('entityID', axis=1, inplace=True)
    df.columns = list(df.columns[:-1]) + ['headLabel']

    df = pd.merge(left=df, right=entities[['entityID', 'label']], left_on='tailEntity',
                  right_on='entityID')
    df.drop('entityID', axis=1, inplace=True)
    df.columns = list(df.columns[:-1]) + ['tailLabel']

    df = pd.merge(left=df, right=relations[['relationID', 'label']], left_on='relation',
                  right_on='relationID')
    df.drop('relationID', axis=1, inplace=True)
    df.columns = list(df.columns[:-1]) + ['relationLabel']

    if return_dicts:
        return df, entities, relations

    return df
