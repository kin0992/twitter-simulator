# coding=utf-8
import csv
import os
import variabili

# per ogni file presente nella cartella data/csv
taglist = ["id",
           "num_followers",
           "vip",
           "prob_following",
           "num_followee",
           "time",
           "prob_follow",
           "prob_retweet",
           "prob_retweeted_by",
           "n_vip",
           "n_nvip"
           ]
os.chdir('data/csv')
with open('../grafici/nodo_monitorato_%s.csv' % variabili.chosen_node_id, 'w') as csv_file:
    writer = csv.writer(csv_file, delimiter=';')
    writer.writerow(taglist)
    csv_file.close()
for file in os.listdir(os.getcwd()):
    # ignoro il gitkeep
    if '.DS_Store' != file and '.gitkeep' != file:
        print file
        with open(file, 'r') as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            # salto l'intestazione di ogni file, perchè è formattata in maniera sbagliata
            #  es: ['id', 'label', 'timeset', '11', '10', '8', '6', '3', '2', '0', '1', '4', '7', '9', '12', '5']
            next(reader, None)
            for row in reader:
                #  il primo elemento è l'id del nodo
                node_number = row[0]
                if node_number == str(variabili.chosen_node_id):
                    with open('../grafici/nodo_monitorato_%s.csv' % variabili.chosen_node_id, 'a') as grafici_file:
                        writer = csv.writer(grafici_file, delimiter=';')
                        writer.writerow(row)
                        grafici_file.close()
            csv_file.close()
        # os.remove(file)
