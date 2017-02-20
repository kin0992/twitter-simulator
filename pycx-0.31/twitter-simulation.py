# coding=utf-8
##========================================
## Section 0: Import e variabili generiche
##========================================
import matplotlib

matplotlib.use('TkAgg')
import random as rd
import numpy as np
import networkx as nx
import pycxsimulator
import json
import variabili
import sys

rd.seed()
network = nx.DiGraph()


##========================================
## Section 1: Funzioni definite
##========================================

# **
# PARAMETRI:
# DESCRIZIONE: Inizializza ogni nodo assegnando ad ognuno dei variabili.max_interest_value interessi,
# identificato con un valore numerico, un peso randomico compreso tra 1 e variabili.max_weight
# RETURNS: interessi, pesi e somma totale di tutti i pesi
# **
def create_interests_and_weights():
    weights_and_interests = {}
    tot_weight = 0
    for i in range(1, variabili.interest_number + 1):
        weights_and_interests[i] = rd.randint(1, variabili.max_weight_value)
        tot_weight += weights_and_interests[i]
    return weights_and_interests, tot_weight


# **
# PARAMETRI:
# DESCRIZIONE: Inizializza i nodi della rete con i relatiivi parametri stabiliti nel file variabili
# RETURNS:
# **
def create_nodes():
    max_node_id = 0
    for i in range(0, variabili.total_users):
        i_and_w = create_interests_and_weights()
        if max_node_id < variabili.vip_users:
            network.add_node(max_node_id, vip=1, node_color='b', interests=i_and_w[0],
                             tot_weight=i_and_w[1],
                             num_followers=0, num_followee=0,
                             prob_follow=rd.uniform(variabili.min_vip_uniform_follow, variabili.max_vip_uniform_follow),
                             prob_following=rd.uniform(variabili.min_vip_uniform_following,
                                                       variabili.max_vip_uniform_following),
                             prob_retweet=rd.uniform(variabili.min_vip_uniform_retweet,
                                                     variabili.max_vip_uniform_retweet),
                             prob_retweeted_by=rd.uniform(variabili.min_vip_uniform_retweeted,
                                                          variabili.max_vip_uniform_retweeted),
                             tweets={}, id_retweeter={}, time=0, n_vip=variabili.vip_users, n_nvip=variabili.common_users)
        else:
            network.add_node(max_node_id, vip=0, node_color='r', interests=i_and_w[0],
                             tot_weight=i_and_w[1],
                             num_followers=0, num_followee=0,
                             prob_follow=rd.uniform(variabili.min_nvip_uniform_follow,
                                                    variabili.max_nvip_uniform_follow),
                             prob_following=rd.uniform(variabili.min_nvip_uniform_following,
                                                       variabili.max_nvip_uniform_following),
                             prob_retweet=rd.uniform(variabili.min_nvip_uniform_retweet,
                                                     variabili.max_nvip_uniform_retweet),
                             prob_retweeted_by=rd.uniform(variabili.min_nvip_uniform_retweeted,
                                                          variabili.max_nvip_uniform_retweeted),
                             tweets={}, id_retweeter={}, time=0)
        max_node_id += 1


# **
# PARAMETRI:
# DESCRIZIONE: Inizializza la rete creando gli archi sulla base dell'omofilia e della probabilità di essere seguito di
# un nodo
# RETURNS:
# **
def create_edges():
    for i in range(0, variabili.total_users):
        for j in range(i + 1, variabili.total_users):
            homophilies = calculate_homophily(i, j)
            if rd.uniform(0, 1) <= variabili.edge_filter_initialization:
                if rd.uniform(0, 1) <= homophilies[0] * network.node[j]['prob_following']:
                    network.add_edge(i, j)
            if rd.uniform(0, 1) <= variabili.edge_filter_initialization:
                if rd.uniform(0, 1) <= homophilies[1] * network.node[i]['prob_following']:
                    network.add_edge(j, i)


# **
# PARAMETRI:
# DESCRIZIONE: Aggiorna il numero di follower e di followee della rete
# RETURNS:
# **
def update_followees_followers():
    for i in range(0, variabili.total_users):
        followers = len(network.in_edges(i))
        followee = len(network.out_edges(i))
        network.node[i]['num_followers'] = followers
        network.node[i]['num_followee'] = followee
        if i in variabili.retweetted_by_prob_cache:
            network.node[i]['prob_retweeted_by'] = variabili.retweetted_by_prob_cache[i] + (variabili.retweetted_by_prob_cache[i] * variabili.bonus_after_quality_tweet)
            if network.node[i]['prob_retweeted_by'] >= 0.9:
                network.node[i]['prob_retweeted_by'] = 0.9
            if network.node[i]['prob_following'] >= 0.9:
                network.node[i]['prob_following'] = 0.9
    variabili.retweetted_by_prob_cache = {}


# **
# PARAMETRI:
# DESCRIZIONE: Aggiunge le etichette al grafo creato (funzione grafica)
# RETURNS: Le etichette
# **
def add_lables_to_edges():
    labels = {}
    for i in range(0, variabili.total_users):
        labels[i] = r'$' + str(i) + '$'
    return labels


# **
# PARAMETRI: Type: tipo del nodo di cui si vogliono contare gli omologhi
# DESCRIZIONE: Conta il numero di nodi dello stesso tipo di quello fornito come parametro e quelli di tipo diverso
# RETURNS: Il numero dei nodi dello stesso tipo ed il numero di nodi di tipo diverso rispetto a type
# **
def same_diff(type):
    same_kind = 0
    diff_kind = 0
    if type:
        agent_type = network.node[type[0]]['vip']
    for n in type:
        if network.out_edges(n):
            for neighbour in network.out_edges(n):
                if network.node[neighbour[1]]['vip'] == agent_type:
                    same_kind += 1
                else:
                    diff_kind += 1
    return same_kind, diff_kind


# **
# PARAMETRI:
# DESCRIZIONE: Calcola l'omofila di gruppo
# RETURNS: Restituisce l'omofilia dei vip e dei non vip
# **
def calculate_group_homophily():
    nvip = []
    vip = []
    for n in network.nodes(data=True):
        if n[1]['vip'] == 0:
            nvip.append(n[0])
        else:
            vip.append(n[0])
    vip_homophily = same_diff(vip)
    nvip_homophily = same_diff(nvip)
    if len(vip) != 0:
        same_kind_vip = float(vip_homophily[0]) / float(len(vip))
        diff_kind_vip = float(vip_homophily[1]) / float(len(vip))
        if same_kind_vip == 0 and diff_kind_vip == 0:
            vip_homophily = 0
        else:
            vip_homophily = float(same_kind_vip) / float(same_kind_vip + diff_kind_vip)
    else:
        vip_homophily = 0
    if len(nvip) != 0:
        same_kind_nvip = float(nvip_homophily[0]) / float(len(nvip))
        diff_kind_nvip = float(nvip_homophily[1]) / float(len(nvip))
        if same_kind_nvip == 0 and diff_kind_nvip == 0:
            n_vip_homophily = 0
        else:
            n_vip_homophily = float(same_kind_nvip) / float(same_kind_nvip + diff_kind_nvip)
    else:
        n_vip_homophily = 0
    return vip_homophily, n_vip_homophily


# **
# PARAMETRI: a_node: nodo A, b_node: nodo B
# DESCRIZIONE: calcola l'omofilia tra A e B e tra B e A
# RETURNS: l'omofilia tra A e B e l'omofilia tra B e A
# **
def calculate_homophily(a_node, b_node):
    # ((max_interest_value + 1) /2) e' il valore medio nel caso di massimo disaccordo su un interesse (1=valore minimo assegnabile)
    # max_eterofily sarebbe varianzamax * interest_number * max_weight / interest_number * max_weight si puo semplificare alla variance
    max_eterofily = ((1 - ((variabili.max_weight_value + 1) / 2)) ** 2 + (
        variabili.max_weight_value - ((variabili.max_weight_value + 1) / 2)) ** 2) / 2
    ab_eterofily = 0
    ba_eterofily = 0
    tot_weights_a = network.node[a_node]['tot_weight']
    tot_weights_b = network.node[b_node]['tot_weight']
    variances_vector = {}
    for i in range(1, variabili.interest_number + 1):
        interest_a = network.node[a_node]['interests'].get(i)
        interest_b = network.node[b_node]['interests'].get(i)
        mean = float(interest_a + interest_b) / 2.0
        variance = ((interest_a - mean) ** 2) + ((interest_b - mean) ** 2)
        variance /= 2
        variances_vector[i] = variance
    for i in range(1, len(variances_vector) + 1):
        ab_eterofily += float(variances_vector[i]) * float(network.node[a_node]["interests"].get(i))
        ba_eterofily += float(variances_vector[i]) * float(network.node[b_node]["interests"].get(i))
    ab_eterofily /= float(tot_weights_a)
    ba_eterofily /= float(tot_weights_b)
    ab_homofily = 1 - (ab_eterofily / max_eterofily)
    ba_homofily = 1 - (ba_eterofily / max_eterofily)
    return ab_homofily, ba_homofily


# **
# PARAMETRI: lambda_vip: parametro lambda per la distribuzione poissoniana dei vip
#            lambda_nvip: parametro lambda per la distribuzione poissoniana dei non vip
# DESCRIZIONE: Funzione che simula la generazione di tweet
# RETURNS:
# **
def generate_tweets(lambda_vip, lambda_nvip):
    for i in range(0, variabili.total_users):
        if network.node[i]['vip'] == 1:
            lambda_to_use = lambda_vip
        else:
            lambda_to_use = lambda_nvip
        number = np.random.poisson(lambda_to_use)
        for j in range(0, number):
            variabili.tweet_id += 1
            network.node[i]['tweets'][i] = variabili.tweet_id
            if rd.uniform(0, 1) < variabili.prob_tweet_quality and i not in variabili.retweetted_by_prob_cache:
                variabili.retweetted_by_prob_cache[i] = network.node[i]['prob_retweeted_by']
                network.node[i]['prob_retweeted_by'] += network.node[i]['prob_retweeted_by'] * variabili.lucky_tweet_increment_retw_one_step
                network.node[i]['prob_following'] += network.node[i]['prob_following'] * variabili.lucky_tweet_increment_following_one_step
                out_file = open(variabili.tweet_fortunato_path, "a")
                out_file.write('il nodo %s ha appena twittato un tweet particolarmente bello al tempo %s \n' % (i, variabili.time))
                out_file.close()
                if network.node[i]['prob_retweeted_by'] >= 1:
                    network.node[i]['prob_retweeted_by'] = 0.9
                if network.node[i]['prob_following'] >= 1:
                    network.node[i]['prob_following'] = 0.9


# **
# PARAMETRI: lambda_vip: parametro lambda per la distribuzione poissoniana dei vip
#            lambda_nvip: parametro lambda per la distribuzione poissoniana dei non vip
# DESCRIZIONE: Funzione che simula la generazione di retweet
# RETURNS:
# **
def generate_retweets(lambda_vip, lambda_nvip):
    node_coin = {}
    nodes = network.nodes()
    nodes_copy = network.nodes()
    for node_i in nodes:
        np.random.shuffle(nodes_copy)
        if network.node[node_i]['vip'] == 1:
            i_vip = True
            node_coin[str(node_i)] = np.random.poisson(lambda_vip)
        else:
            node_coin[str(node_i)] = np.random.poisson(lambda_nvip)
            i_vip = False
        neighbors_list_i = network.neighbors(node_i)
        for node_j in nodes_copy:
            if node_i != node_j:
                if network.node[node_j]['vip'] == 1:
                    j_vip = True
                else:
                    j_vip = False
                tweet_j = network.node[node_j]['tweets']
                if tweet_j:
                    penalty = variabili.penalty_not_neighbor
                    if tweet_j in neighbors_list_i:
                        penalty = variabili.penalty_neighbor
                    prob_retweet = calculate_homophily(node_i, node_j)[0] * network.node[node_j]['prob_retweeted_by'] * network.node[node_i][
                        'prob_retweet'] * penalty
                    if node_coin[str(node_i)] != 0:
                        if rd.uniform(0, 1) < prob_retweet:
                            if not network.node[node_j]['id_retweeter']:
                                network.node[node_j]['id_retweeter'][node_j] = [node_i]
                            else:
                                network.node[node_j]['id_retweeter'][node_j].append(node_i)
                            if i_vip and not j_vip:
                                out_file = open(variabili.file_retweet_vip_nvip, "a")
                                out_file.write('il nodo %s non è vip ed è stato retweettato dal vip %s al tempo %s\n' % (node_j, node_i, variabili.time))
                                out_file.close()
                            node_coin[str(node_i)] -= 1
                    else:
                        break


# **
# PARAMETRI:
# DESCRIZIONE: Aggiorna le probabilità dei nodi della rete in seguito ai tweet e ai retweet
# RETURNS:
# **
# calcola la nuova influenza dei nodi dopo i tweet/retweet
# guarda chi mi retweetta, se mi retweetta un vip, aumenta di un po' la prob di essere retweettato
# e la probabilità di essere seguito
def update_probs():
    for i in range(0, variabili.total_users):
        network.node[i]['time'] = variabili.time
        if (len(network.node[i]['id_retweeter']) != 0) and (len(network.node[i]['id_retweeter'][i]) != 0):
            id_retweetter = network.node[i]['id_retweeter'][i]
            bonus = 0
            for j in range(0, len(id_retweetter)):
                if network.node[id_retweetter[j]]['vip'] == 1:
                    bonus += variabili.vip_retweet_bonus
                else:
                    bonus += variabili.nvip_retweet_bonus
            percentage = float(bonus) / float(variabili.max_retweet_bonus)
            network.node[i]['prob_retweeted_by'] += network.node[i]['prob_retweeted_by'] * percentage
            network.node[i]['prob_following'] += network.node[i]['prob_following'] * percentage
            if network.node[i]['prob_retweeted_by'] >= 0.9:
                network.node[i]['prob_retweeted_by'] = 0.9
            if network.node[i]['prob_following'] >= 0.9:
                network.node[i]['prob_following'] = 0.9
            network.node[i]['id_retweeter'][i] = []


# **
# PARAMETRI:
# DESCRIZIONE: Ricalcola gli archi in seguito alla generazione di tweet/retweet e all'aggiornamento delle probabilità
# RETURNS:
# NOTE: La funzione è stata divisa in due parti per ottimizzare la complesstà del ciclo su tutti i nodi della rete
# **
def update_edges():
    group_homophilies = calculate_group_homophily()
    for i in range(0, variabili.total_users):
        for j in range(i + 1, variabili.total_users):
            homophilies = calculate_homophily(i, j)
            recalculate_edges(i, j, homophilies[0], group_homophilies)
            recalculate_edges(j, i, homophilies[1], group_homophilies)


# **
# PARAMETRI: i: primo nodo, j: secondo nodo, homophily: omofilia da i a j e da j a i, group_homophilies: omofilia di gruppo
# DESCRIZIONE: Ricalcola gli archi in seguito alla generazione di tweet/retweet e all'aggiornamento delle probabilità
# RETURNS:
# NOTE: La funzione è stata divisa in due parti per ottimizzare la complesstà del ciclo su tutti i nodi della rete
# **
def recalculate_edges(i, j, homophily, group_homophilies):
    if network.node[i]["vip"] == 1:
        group_homophily = group_homophilies[0]
    else:
        group_homophily = group_homophilies[1]
    prob_i_follow = network.node[i]['prob_follow']
    prob_j_following = network.node[j]['prob_following']
    if rd.uniform(0, 1) <= variabili.edge_filter_simulation:
        if rd.uniform(0, 1) <= homophily * prob_j_following * prob_i_follow * group_homophily:
            network.add_edge(i, j)


# **
# PARAMETRI:
# DESCRIZIONE: Inserisce tutti i nodi vip in una lista. necessaria per il funzionamento di Gephi
# RETURNS:
# **
def put_all_vip_in_list():
    for i in network.nodes():
        if network.node[i]['vip'] == 1:
            variabili.nodi_vip_list.append(i)


##========================================
## Section 2: Funzioni di default
##========================================

def init():
    variabili.common_users = variabili.total_users - variabili.vip_users
    variabili.nodi_vip_list = []
    variabili.vip_screen_time = 0
    variabili.nodi_vip_list = []
    # plt.clf()
    # plt.figure(1).clear()
    variabili.network = nx.DiGraph()
    create_nodes()
    create_edges()
    update_followees_followers()
    put_all_vip_in_list()
    # pos = nx.spring_layout(network)


def draw():
    print "Percentuale di completamento: %s" % ((float(variabili.time) / float(variabili.symulation_steps)) * 100)
    # plt.figure(1)
    # nx.draw(network, pos)
    # nx.draw_networkx_labels(network, pos, add_lables_to_edges(), font_size=16)
    for i in range(0, variabili.total_users):
        if variabili.time > 20:  # 20 step per stabilizzare la rete
            if network.node[i]['vip'] != 1 and (
                        (network.node[i]['prob_following'] >= variabili.min_vip_uniform_following)
                    and network.node[i]['num_followers'] >= (variabili.total_users * 0.2)):
                network.node[i]['vip'] = 1
                variabili.nodi_vip_list.append(i)
                network.node[i]['node_color'] = 'b'
                variabili.vip_users += 1
                variabili.common_users -= 1
                network.node[0]['n_vip'] = variabili.vip_users
                network.node[0]['n_nvip'] = variabili.common_users
        else:
            if network.node[i]['vip'] != 1 and (network.node[i]['prob_following'] >= variabili.min_vip_uniform_following):
                network.node[i]['vip'] = 1
                variabili.nodi_vip_list.append(i)
                network.node[i]['node_color'] = 'b'
                variabili.vip_users += 1
                variabili.common_users -= 1
                network.node[0]['n_vip'] = variabili.vip_users
                network.node[0]['n_nvip'] = variabili.common_users
                # nx.draw_networkx_nodes(network, pos, nodelist=[i], node_color='b')
                # if network.node[i]['node_color'] == 'b':
                # nx.draw_networkx_nodes(network, pos, nodelist=[i], node_color='b')
    # plt.title('Time: ' + str(time))
    file_name = "data/gephi/network@time%s.gexf" % variabili.time
    nx.write_gexf(network, file_name)
    json_file_name = 'network@time%s.json' % variabili.time
    out_file = open("data/json/%s" % json_file_name, "w")
    out_file.write(json.dumps(network.nodes(data=True)))
    out_file.close()
    if variabili.time == variabili.symulation_steps:
        print "La simulazione è terminata: grazie per aver usato il nostro modello!"
        sys.exit(0)


def step():
    variabili.time += 1
    local_time = 0
    if local_time == 0:
        tweet_lambda_vip = variabili.tweet_lambda_vip_0
        tweet_lambda_nvip = variabili.tweet_lambda_nvip_0
        retweet_lambda_vip = variabili.retweet_lambda_vip_0
        retweet_lambda_nvip = variabili.retweet_lambda_nvip_0
    elif local_time == 1:
        tweet_lambda_vip = variabili.tweet_lambda_vip_1
        tweet_lambda_nvip = variabili.tweet_lambda_nvip_1
        retweet_lambda_vip = variabili.retweet_lambda_vip_1
        retweet_lambda_nvip = variabili.retweet_lambda_nvip_1
    elif local_time == 2:
        tweet_lambda_vip = variabili.tweet_lambda_vip_2
        tweet_lambda_nvip = variabili.tweet_lambda_nvip_2
        retweet_lambda_vip = variabili.retweet_lambda_vip_2
        retweet_lambda_nvip = variabili.retweet_lambda_nvip_2
    else:
        tweet_lambda_vip = variabili.tweet_lambda_vip_3
        tweet_lambda_nvip = variabili.tweet_lambda_nvip_3
        retweet_lambda_vip = variabili.retweet_lambda_vip_3
        retweet_lambda_nvip = variabili.retweet_lambda_nvip_3
        local_time = 0
    generate_tweets(tweet_lambda_vip, tweet_lambda_nvip)
    generate_retweets(retweet_lambda_vip, retweet_lambda_nvip)
    update_probs()
    update_edges()
    update_followees_followers()
    local_time += 1


##=====================================
## Section 3: Import and Run GUI
##=====================================

pycxsimulator.GUI(title='Twitter Simulator', interval=0, parameterSetters=[]).start(func=[init, draw, step])
# 'title', 'interval' and 'parameterSetters' are optional
