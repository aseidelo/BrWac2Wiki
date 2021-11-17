import json
from codecs import open
import argparse
from os import listdir
from os.path import isfile, join

'''


'''

def check_url(url):
    to_filter = [
        "www.acervoamador.com.br/", 
        "www.brasileirinhas.com.br/", 
        "xvideos",
        "wikipedia"
    ]
    filter_out = False
    for domain in to_filter:
        if(domain in url):
            filter_out = True
            break
    return filter_out