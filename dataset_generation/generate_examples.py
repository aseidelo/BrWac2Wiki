import argparse
import json
from os import listdir
from os.path import isfile, join
from codecs import open
import sqlite3
from nltk import word_tokenize 

def detect_clone(text, article_sections):
    text_tokens = word_tokenize(text)
    for section in article_sections:
        if(len(section)>0):
            section_tokens = word_tokenize(section.lower())
            #print(list(section_unigrams))
            count_intersection = len(set(section_tokens) & set(text_tokens))
            clone_prob = float(count_intersection)/len(section_tokens)
            #print(count_intersection, len(section_tokens), len(text_tokens), clone_prob)
            if(clone_prob > 0.5):
                #print(section, text)
                return True
    return False

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

def search_url(db, url):
    cur = db.cursor()
    cur.execute("""select file, pos from pos where docid="{}";""".format(url))
    rows = cur.fetchall()
    if(len(rows) > 0):
        file_name, pos = rows[0]
        #print(pos)
        return file_name, pos
    return None, None

def find_url_content(url, path, db):
    #print(index)
    file_name, pos = search_url(db, url)
    if(file_name is not None):
        with open('{}{}'.format(path,file_name)) as file:
            for position, line in enumerate(file):
                if(position == pos):
                    try:
                        content = json.loads(line)
                        '''
                        print(pos, file_name)
                        print(url)
                        print(content['url'])
                        print('!=---')
                        '''
                        return content['sentences']
                    except:
                        print(line)
                        raise
    return None

def main(args):
    count = 0
    dirs = ['AA/', 'AB/']
    db = create_connection(args.urls_sentences_path + 'urls_pos.db')
    with open(args.out_file_path + 'wiki.json', 'ab+') as out_file1:
        with open(args.out_file_path + 'brwac.json', 'ab+') as out_file2:
            to_out_wiki = b''
            to_out_brwac = b''
            for dir_name in dirs:
                file_names = [f for f in listdir(args.brwac_urls_path + dir_name) if isfile(join(args.brwac_urls_path + dir_name, f))]
                for file_name in file_names:
                    print(file_name)
                    with open(args.brwac_urls_path + dir_name + file_name, 'r') as brwac_wiki_urls_file:
                        with open(args.wiki_path + dir_name + file_name, 'r', encoding="utf-8") as wiki_file:
                            for line in brwac_wiki_urls_file:
                                urls = {}
                                content = json.loads(line)
                                wiki_content = json.loads(wiki_file.readline())
                                for url in content['docids']:
                                    #print(url)
                                    urls[url] = None
                                if(len(urls) >= 1):
                                    to_write_urls = {}
                                    for url in urls:
                                        url_content = find_url_content(url, args.urls_sentences_path, db)
                                        if(url_content is not None):
                                            full_text = ''
                                            for sentence in url_content:
                                                full_text = full_text + sentence
                                            #if(detect_clone(full_text, wiki_content['text'][:1]) is False):
                                            to_write_urls[url] = url_content
                                    if(len(to_write_urls) > 0):
                                        count = count + 1
                                        print(count)
                                        to_out = '{}\n'.format(json.dumps({'wiki_id' : content['id'], 'wiki_title' : wiki_content['title'], 'wiki_sections' : wiki_content['sections'], 'wiki_text' : wiki_content['text']}, ensure_ascii=False)).encode('utf-8')
                                        to_out_wiki = to_out_wiki + to_out
                                        #print(to_out)
                                        #out_file1.write(to_out)
                                        to_out = '{}\n'.format(json.dumps({'wiki_id' : content['id'], 'wiki_title' : wiki_content['title'], 'urls' : to_write_urls}, ensure_ascii=False)).encode('utf-8')
                                        to_out_brwac = to_out_brwac + to_out
                                        #print(to_out)
                                        #out_file2.write(to_out)
                                        if(len(to_out_brwac) > 10000000): # 10M
                                            out_file1.write(to_out_wiki)
                                            out_file2.write(to_out_brwac)
                                            to_out_wiki = b''
                                            to_out_brwac = b''
    print(count)

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Count the number of examples with more then one reference web page.')
	parser.add_argument('--wiki_path', default='data/wikipedia_articles_json/', type=str)
	parser.add_argument('--brwac_urls_path', default='data/wikipedia_ref_urls_brwac_v4/', type=str)
	parser.add_argument('--urls_sentences_path', default='data/brwac_ref_urls_sentences_v4/', type=str)
	parser.add_argument('--out_file_path', default='data/full_examples_v4/', type=str)
	args = parser.parse_args()
	main(args)
