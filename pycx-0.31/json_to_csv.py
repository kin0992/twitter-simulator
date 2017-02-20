import json
import csv
import os
from os import listdir
from os.path import isfile, join
import variabili

all_files = [f for f in listdir(variabili.json_path) if isfile(join(variabili.json_path, f))]

for file in all_files:
    if file != ".gitkeep" and file != ".DS_Store":
        taglist = ["id",
                   # "interests",
                   # "tweets",
                   # "id_retweeter",
                   # "tot_weight",
                   "num_followers",
                   "vip",
                   "prob_following",
                   # "weights",
                   "num_followee",
                   "time",
                   "prob_follow",
                   "prob_retweet",
                   "prob_retweeted_by",
                   "n_vip",
                   "n_nvip"
                   # "node_color"
                   ]

        source_path = "%s%s" % (variabili.json_path, file)
        print source_path
        json_source = open(source_path, "r")
        json_data = json_source.read()
        json_parsed = json.loads(json_data)

        at_char = file.find('@')
        dot_char = file.find('.')

        dest_file_name = "csv_network%s" % (file[at_char:dot_char])
        destination_path = "%s%s.csv" % (variabili.csv_path, dest_file_name)
        print destination_path
        csv_destination = open(destination_path, 'w')
        csvwriter = csv.writer(csv_destination)


        #imposta l'header del cs con le colonne corrispondenti ai tag
        csvwriter.writerow(taglist)
        # print os.stat(destination_path).st_size
        # if os.stat(destination_path).st_size == 0:
        #     with open(variabili.nodo_monitorato_path, 'w') as csv_file:
        #         writer = csv.writer(csv_file)
        #         writer.writerow(taglist)
        #         csv_file.close()
        # #elimina "id" dai tag
        taglist.pop(0)

        for i in range (0, len(json_parsed)):
            csv_text =  []
            csv_text.append(i)
            for tag in taglist:
                #metti nella colonna successiva json_parsed[i][1][tag]
                if tag == 'n_vip' or tag == 'n_nvip':
                    if tag in json_parsed[i][1]:
                        csv_text.append(json_parsed[i][1][tag])
                    else:
                        csv_text.append('null')
                else:
                    csv_text.append(json_parsed[i][1][tag])
            csvwriter.writerow(csv_text)

