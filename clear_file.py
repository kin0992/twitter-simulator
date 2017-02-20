# coding=utf-8
import os


def delete_files(directory):
    for file in os.listdir(directory):
        if '.gitkeep' != file:
            os.remove(file)


os.chdir('pycx-0.31/data/csv')
delete_files(os.getcwd())
os.chdir('../gephi')
delete_files(os.getcwd())
os.chdir('../grafici')
delete_files(os.getcwd())
os.chdir('../json')
delete_files(os.getcwd())
os.chdir('../nodi_da_controllare')
delete_files(os.getcwd())
