import json
from codecs import open
import argparse
import pymongo
from pymongo import MongoClient
import re

def get_wiki_info(path, file_name):
    with open(path+file_name, 'r') as file:
        for line in file:
            content = json.loads(line)
            yield (content['id'], content['title'])

def persist_brwac_ref_urls(to_outs, out_path, wiki_file):
    with open(out_path + wiki_file, 'wb') as out_file:
        for line in to_outs:
            out_file.write('{}\n'.format(json.dumps(line, ensure_ascii=False)).encode('utf-8'))

# try full sentence, if timeout try splited words AND
def query_title_v1(title):
    # remove punctuation
    title = re.sub(r"[^a-zA-ZçÇèéêíáâãõôóúûÉÊÍÁÂÃÕÔÓÚÛöüäëï0-9]+", " ", title)
    print(wiki_id, title)
    # query wiki title on wikisumpt database table brwac, searching on title and text of ref urls
    brwac_docs = None
    to_out = {'wiki_id' : wiki_id, 'wiki_title' : title, 'brwac_urls' : {}}
    try:
        phrase_query = { "$text": { "$search": '\"{}\"'.format(title), "$language": "pt"} }
        brwac_docs = db.brwac.find(phrase_query, max_time_ms=4000).limit(15)
        if(brwac_docs != None):
            for x in brwac_docs:
                to_out['brwac_urls'][x['docid']] = x['text']
    except (pymongo.errors.ExecutionTimeout):
        print("{} falhou".format(phrase_query))
        and_query_words = ''
        for word in title.split(' '):
            and_query_words = and_query_words + '\"{}\" '.format(word)
        and_query = { "$text": { "$search": '{}'.format(and_query_words), "$language": "pt"} }
        print(and_query)
        try:
            brwac_docs = db.brwac.find(and_query, max_time_ms=3000).limit(15)
            if(brwac_docs != None):
                for x in brwac_docs:
                    to_out['brwac_urls'][x['docid']] = x['text']
        except (pymongo.errors.ExecutionTimeout):
            print("{} falhou".format(and_query))
            pass
        #pass
    return to_out

# try full sentence, if timeout try splited words AND
def query_title_v2(title):
    # remove punctuation
    title = re.sub(r"[^a-zA-ZçÇèéêíáâãõôóúûÉÊÍÁÂÃÕÔÓÚÛöüäëï0-9]+", " ", title)
    print(wiki_id, title)
    # query wiki title on wikisumpt database table brwac, searching on title and text of ref urls
    brwac_docs = None
    to_out = {'wiki_id' : wiki_id, 'wiki_title' : title, 'brwac_urls' : {}}
    and_query_words = ''
    for word in title.split(' '):
        and_query_words = and_query_words + '\"{}\" '.format(word)
    and_query = { "$text": { "$search": '{}'.format(and_query_words), "$language": "pt"} }
    brwac_cursor = db.brwac.find(and_query, max_time_ms=2000, batch_size=2)[:15]
    try:
        i = 0
        for x in brwac_cursor:
            #print(x)
            #if(i == 6):
            #    break
            to_out['brwac_urls'][x['docid']] = x['text']
            i = i + 1
    except (pymongo.errors.ExecutionTimeout):
        pass
    print("{} docs".format(len(to_out['brwac_urls'])))
    return to_out

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate Wikisum-pt dataset from Wikipedia articles and BrWac corpus.')
    parser.add_argument('--wiki_file',default='AA/processed_wiki_00.json', type=str)
    parser.add_argument('--wiki_path', default='data/wikipedia_articles_json/', type=str)
    parser.add_argument('--out_path', default='data/brwac_ref_urls_sentences_mongodb_v2/', type=str)
    args = parser.parse_args()
    # connect to mongodb
    client = MongoClient()
    db = client.wikisumpt
    # get wiki titles and ids
    wikis = get_wiki_info(args.wiki_path, args.wiki_file)
    to_outs = []
    for wiki_id, title in wikis:
        to_outs.append(query_title_v2(title))
    persist_brwac_ref_urls(to_outs, args.out_path, args.wiki_file)
