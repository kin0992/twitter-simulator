#coding=utf-8

#variabili ausiliarie
retweetted_by_prob_cache = {}

# fermiamo la simulazione dopo 3 mesi
symulation_steps = 360

# probabilità di fare un tweet molto retweettato
prob_tweet_quality = 0.008
bonus_after_quality_tweet = 0.2

lucky_tweet_increment_retw_one_step = 0.75
lucky_tweet_increment_following_one_step = 0.02

#utenti totali della rete
total_users = 1000

#calcolo di un numero di vip nella rete in percentuale
vip_users = int(round(total_users * 0.2 / 100))
common_users = total_users - vip_users

#filtri per "scoraggiare" la creazione di archi durante l'inizializzazione e durante l'update
edge_filter_initialization = 0.1
edge_filter_simulation = 0.05

#numero di interessi che caratterizzano ogni nodo, massimo valore attribuibile ad ogni interessemassimo peso attribuibile a nu interesse
interest_number = 5
max_weight_value = 10

#parametri per il calcolo dei valori di inizializzazione della rete
min_vip_uniform_follow = 0.15
max_vip_uniform_follow = 0.25
min_vip_uniform_following = 0.35
max_vip_uniform_following = 0.55
min_nvip_uniform_follow = 0.3
max_nvip_uniform_follow = 0.5
min_nvip_uniform_following = 0.01
max_nvip_uniform_following = 0.15
min_vip_uniform_retweet = 0.01
max_vip_uniform_retweet = 0.08
min_vip_uniform_retweeted = 0.6
max_vip_uniform_retweeted = 0.7
min_nvip_uniform_retweet = 0.5
max_nvip_uniform_retweet = 0.75
min_nvip_uniform_retweeted = 0.05
max_nvip_uniform_retweeted = 0.15

#parametri per il calcolo del bonus ottenuto quando si è retweettati da un vip o da un non vip
vip_retweet_bonus = 2
nvip_retweet_bonus = 1
max_retweet_bonus = total_users  # vip_retweet_bonus * vip_users + common_users * nvip_retweet_bonus

#variabili lambda per vip e non vip utilizzate nelle distribuzioni poissoniane
tweet_lambda_vip_0 = 1
tweet_lambda_nvip_0 = 0.3
tweet_lambda_vip_1 = 0.5
tweet_lambda_nvip_1 = 0.7
tweet_lambda_vip_2 = 1.5
tweet_lambda_nvip_2 = 0.7
tweet_lambda_vip_3 = 1.7
tweet_lambda_nvip_3 = 1
retweet_lambda_vip_0 = 0.5
retweet_lambda_nvip_0 = 1
retweet_lambda_vip_1 = 0.7
retweet_lambda_nvip_1 = 2
retweet_lambda_vip_2 = 1
retweet_lambda_nvip_2 = 1.7
retweet_lambda_vip_3 = 1.2
retweet_lambda_nvip_3 = 1

penalty_neighbor = 0.08
penalty_not_neighbor = 0.05

time = 0
vip_screen_time = 0
tweet_id = 0
chosen_node_id = 859

tweet_fortunato_path = 'data/nodi_da_controllare/tweet_fortunati.txt'
file_retweet_vip_nvip = 'data/nodi_da_controllare/retweetted_by_vip.txt'
nodo_monitorato_path = 'data/grafici/'
json_path = 'data/json/'
csv_path = "data/csv/"


def nodi_vip_list():
    return None
