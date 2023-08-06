import networkx as nx
import collections
import zipfile
import tarfile
import json
import csv
import os
from . import graphs
from bisect import bisect

TEMPLATE = TEMPLATE2 = None


def write_output_file(outputs, file_name):
    if len(outputs) == 0:
        return
    if not os.path.exists(os.path.dirname(file_name)):
        os.makedirs(os.path.dirname(file_name))
    rows = [['Results'] + [output['name'] for output in outputs]]
    for title in outputs[0]:
        if title != 'name':
            rows.append([title] + [output.get(title, '') for output in outputs])

    with open(file_name, 'w') as f:
        writer = csv.writer(f)
        for row in rows:
            writer.writerow(row)


def find_border(graph):
    best_border = best_score = 0
    for i in range(100):
        honest_score = len([node for node in graph.nodes if node.node_type in (
            'Honest', 'Seed') and node.rank > i])
        sybil_score = len([node for node in graph.nodes if node.node_type in (
            'Sybil', 'Non Bridge Sybil', 'Bridge Sybil') and node.rank < i])
        score = (honest_score * sybil_score)**.5
        if score >= best_score:
            best_border = i
            best_score = score
    return best_border


def calculate_successful_sybils(ranks_dic):
    honests = []
    sybils = []
    attackers = []
    result = {}
    for category in ranks_dic:
        if category in ['Sybil', 'Non Bridge Sybil', 'Bridge Sybil']:
            sybils.extend(ranks_dic[category])
        elif category in ['Seed', 'Honest']:
            honests.extend(ranks_dic[category])
        elif category == 'Attacker':
            attackers.extend(ranks_dic[category])
    honests.sort()
    # for limit in [.8, .9, 1]:
    #     successful_sybils = [rank for rank in sybils if rank >= min(
    #         honests[:int(limit * len(honests))])]
    #     result['successful_sybils_percent_{0}'.format(limit)] = round(
    #         (len(successful_sybils) * 100.0) / max(1, len(sybils)), 2)
    # if len(attackers) != 0:
    #     result['successful_sybils_per_attacker'] = round(
    #         float(len(successful_sybils)) / len(attackers), 2)
    # else:
    #     result['successful_sybils_per_attacker'] = '__'
    result['better_than_pct'] = float(bisect(honests, max(sybils) if sybils else 0)) / len(honests)
    return result


def calculate_successful_honest(ranks_dic):
    honests = []
    attackers = []
    result = {}
    for category in ranks_dic:
        if category in ['Seed', 'Honest']:
            honests.extend(ranks_dic[category])
    honests.sort(reverse=True)
    for limit in [.1, .2]:
        result['min_{0}'.format(limit)] =  min(honests[:int((1 - limit) * len(honests))])
    return result


def generate_output(graph, name=''):
    categories = set([node.node_type for node in graph.nodes])
    ranks_dic = {}
    for category in categories:
        ranks_dic[category] = [
            node.rank if node.rank else 0 for node in graph.nodes if node.node_type == category]
    output = collections.OrderedDict()
    output['name'] = name
    successful_sybils = calculate_successful_sybils(ranks_dic)
    # successful_honests = calculate_successful_honest(ranks_dic)
    # output['Successful Sybils Percentage'] = successful_sybils['successful_sybils_percent_1']
    # output['Successful Sybils Percentage (-10 percent of honests)'] = successful_sybils['successful_sybils_percent_0.9']
    # output['Successful Sybils Percentage (-20 percent of honests)'] = successful_sybils['successful_sybils_percent_0.8']
    # output['Successful Sybils per Attacker'] = successful_sybils['successful_sybils_per_attacker']
    # output['Min 90 Percent'] = successful_honests['min_0.1']
    # output['Min 80 Percent'] = successful_honests['min_0.2']

    output['Sybils scored >= %'] = successful_sybils['better_than_pct']
    output['Avg Honest - Avg Sybil'] = None
    view_order = ('Seed', 'Honest', 'Attacker',
                  'Bridge Sybil', 'Non Bridge Sybil', 'Sybil')
    for category in view_order:
        if category not in categories:
            continue
        for parameter in ['Max', 'Avg', 'Min']:
            if len(ranks_dic[category]) == 0:
                v = '__'
            elif parameter == 'Min':
                v = min(ranks_dic[category])
            elif parameter == 'Avg':
                v = sum(ranks_dic[category]) / len(ranks_dic[category])
            elif parameter == 'Max':
                v = max(ranks_dic[category])
            output['{0} {1}'.format(parameter, category)] = v
    output['Avg Honest - Avg Sybil'] = output['Avg Honest'] - \
        output.get('Avg Sybil', output.get('Avg Bridge Sybil', 0))
    output['Border'] = find_border(graph)
    return output


def save_graph(file_name, graph):
    with open(file_name, 'w') as f:
        f.write(to_json(graph))


def to_json(graph):
    data = {'nodes': [], 'edges': []}
    for node in graph.nodes():
        data['nodes'].append({'name': node.name, 'node_type': node.node_type, 'groups': list(
            node.groups), 'rank': node.rank})
    for edge in graph.edges():
        data['edges'].append((edge[0].name, edge[1].name))
    return json.dumps(data)


def load_graph(file_name):
    with open(file_name, 'r') as f:
        data = f.read()
    return from_json(data)


def from_json(data):
    data = json.loads(data)
    graph = nx.Graph()
    nodes = {}
    for node in data['nodes']:
        groups = set(node['groups']) if node['groups'] else None
        nodes[node['name']] = graphs.node.Node(
            node['name'], node['node_type'], groups, node['rank'])
        graph.add_node(nodes[node['name']])
    graph.add_edges_from([(nodes[edge[0]], nodes[edge[1]])
                          for edge in data['edges']])
    return graph


def zip2dict(f, table):
    zf = zipfile.ZipFile(f)
    fnames = zf.namelist()
    pattern = lambda fname: fname.endswith('.data.json') and fname.count('/{}_'.format(table)) > 0
    fname = list(filter(pattern, fnames))[0]
    content = zf.open(fname).read().decode('utf-8')
    ol = [json.loads(line) for line in content.split('\n') if line.strip()]
    d = {}
    for o in ol:
        if o['type'] == 2300:
            d[o['data']['_key']] = o['data']
        elif o['type'] == 2302 and o['data']['_key'] in d:
            del d[o['data']['_key']]
    return dict((d[k]['_id'].replace(table+'/', ''), d[k]) for k in d)


def from_dump(f):
    user_groups = zip2dict(f, 'usersInGroups')
    users = zip2dict(f, 'users')
    groups = zip2dict(f, 'groups')
    connections = zip2dict(f, 'connections')
    ret = {'nodes': [], 'edges': []}
    buf = {}
    for u in users:
        users[u] = {'node_type': 'Honest', 'rank': 0, 'name': u , 'groups': [], 'createdAt':users[u]['createdAt']}
        ret['nodes'].append(users[u])
    for user_group in user_groups.values():
        u = user_group['_from'].replace('users/', '')
        g = user_group['_to'].replace('groups/', '')
        users[u]['groups'].append(g)
        if groups[g].get('seed', False):
            users[u]['node_type'] = 'Seed'
    for c in connections.values():
        ret['edges'].append([c['_from'].replace('users/', ''), c['_to'].replace('users/', '')])
    ret['nodes'] = sorted(ret['nodes'], key=lambda i: i['name'])
    ret['nodes'] = sorted(ret['nodes'], key=lambda i: i['createdAt'], reverse=True)
    return json.dumps(ret)


def draw_graph(graph, file_name):
    global TEMPLATE
    if not TEMPLATE:
        abspath = os.path.abspath(__file__)
        dname = os.path.dirname(abspath)
        with open(os.path.join(dname, 'template.html')) as f:
            TEMPLATE = f.read()
    dname = os.path.dirname(file_name)
    if dname and not os.path.exists(dname):
        os.makedirs(dname)
    json_dic = to_json(graph)
    edited_string = TEMPLATE.replace('JSON_GRAPH', json_dic)
    with open(file_name, 'w') as output_file:
        output_file.write(edited_string)
    return edited_string


def draw_compare_graph(graph1, graph2, file_name):
    global TEMPLATE2
    if not TEMPLATE2:
        abspath = os.path.abspath(__file__)
        dname = os.path.dirname(abspath)
        with open(os.path.join(dname, 'template2.html')) as f:
            TEMPLATE2 = f.read()
    dname = os.path.dirname(file_name)
    if dname and not os.path.exists(dname):
        os.makedirs(dname)
    for node in graph1.nodes:
        node2 = next(filter(lambda n: n.name == node.name, graph2.nodes))
        node.rank = '{0}-{1}'.format(int(node.rank), int(node2.rank))
    graph_json = to_json(graph1)
    edited_string = TEMPLATE2.replace('JSON_GRAPH', graph_json)
    with open(file_name, 'w') as output_file:
        output_file.write(edited_string)
    return edited_string


def reset_ranks(graph):
    for node in graph.nodes():
        node.rank = 0


def tar_to_zip(fin, fout):
    if os.path.exists(fout):
        os.remove(fout)
    tarf = tarfile.open(fin, mode='r|gz')
    zipf = zipfile.ZipFile(fout, mode='a', compression=zipfile.ZIP_DEFLATED)
    for m in tarf:
        f = tarf.extractfile(m)
        if f:
            zipf.writestr(m.name, f.read())
    tarf.close()
    zipf.close()
