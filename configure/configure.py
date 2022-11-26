import os
import yaml
import re


def configure_kube(window, values):
    # disable input on change
    window['-KUBE FOLDER-'].update(disabled=True)
    folder = values['-KUBE FOLDER-']
    # file_list = os.listdir(folder)

    # find the index of the desired file and load it
    # config = file_list.index('config')

    return [] # file_list
    # read the config as a yaml file (apparently they work as yaml files with no extension)
    # with open(folder + "\\" + file_list[config], 'r') as stream:
    #     try:
    #         parsed_yaml = yaml.safe_load(stream)
    #         print(parsed_yaml)
    #     except yaml.YAMLError as exc:
    #         print(exc)
