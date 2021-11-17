import json
import lxml.etree as ET
#import xml.etree.ElementTree as ET
from codecs import open
import argparse
from os import listdir
from os.path import isfile, join
from nltk import word_tokenize 
from hash_tools import HashTable
from filter_urls import check_url
import re

def read_brwac_docs(buffer, wiki_titles, n, titles_pos):
    #print(buffer)
    docs_list = []
    buffer_out = None
    try:
        last_doc_close_pos = buffer.rindex('</doc>')
        buffer_out = buffer[last_doc_close_pos + 6:]
        #print(buffer_out)
        xml = """<root> """ + buffer[:last_doc_close_pos + 6] + """ </root>"""
        parser = ET.XMLParser(encoding="utf-8", recover='True')
        tree = ET.fromstring(xml.encode('utf-8'), parser=parser)
        docs = tree.findall('doc')
        i = 0
        #print(len(docs))
        #print(len(buffer[:last_doc_close_pos + 6].split('<doc ')))
        for doc in docs:
            pos = i + n
            s = []
            p = doc.findall('p')
            for para in p:
                new_para = ET.tostring(para, encoding=str).replace('<s>\n', '').replace('</s>\n', '').replace('<g/>\n', '')[3:-5]
                #print(new_para)
                s.append(new_para.lower())
            sentences = []
            to_save = False
            for sentence in s:
                words = sentence.split('\n')
                for word in words:
                    #if word == 'anno' or word == 'domini':
                    #    print(word, i)
                    #print(word)
                    if word in titles_pos:
                        to_save = True
                        try:
                            if titles_pos[word][-1] != pos:
                                titles_pos[word].append(pos)
                        except:
                            titles_pos[word].append(pos)
                full_sentence = sentence.replace('\n', ' ')
                sentences.append(full_sentence)
            #try:
            #    if('http://ocatequista.com.br/archives/5281' in doc.attrib['uri']):
            #        print(sentences)
            #        #http://ocatequista.com.br/archives/5281
            #except:
            #    pass
            #print(sentences)
            if(to_save):
                url = None
                try:
                    url = doc.attrib['uri']
                except:
                    pass
                title = None
                try:
                    title = doc.attrib['title']
                except:
                    pass
                new_dict = {'docid': doc.attrib['docid'], 'url' : url, 'title' : title, 'text' : sentences}
                #print(new_dict)
                docs_list.append(new_dict)
                i = i + 1
        #print(titles_pos)
        n = n + i
    except:
        buffer_out = buffer
    finally:
        return docs_list, titles_pos, buffer_out, n

'''
def read_brwac_docs(buffer):
    #print(buffer)
    last_doc_close_pos = buffer.rindex('</doc>')
    buffer_out = buffer[last_doc_close_pos + 6:]
    xml = '<root> ' + buffer[:last_doc_close_pos + 6] + ' </root>'
    parser = ET.XMLParser(encoding="utf-8", recover='True')
    tree = ET.fromstring(xml.encode('utf-8'), parser=parser)
    docs = tree.findall('doc')
    docs_list = []
    unique_words = {}
    i = 0
    for doc in docs:
        s = []
        p = doc.findall('p')
        for para in p:
            new_sent = ''
            for sent in para.findall('s'):
                new_sent = new_sent + sent.text.lower()
            s.append(new_sent)
        sentences = []
        for sentence in s:
            words = sentence.split('\n')
            for word in words:
                if word in unique_words:
                    if i not in unique_words[word]:
                        unique_words[word].append(i)
                else:
                    unique_words[word] = [i]
            sentences.append(sentence.replace('\n', ' '))
        #print(sentences)
        url = None
        try:
            url = doc.attrib['uri']
        except:
            pass
        title = None
        try:
            title = doc.attrib['title']
        except:
            pass
        new_dict = {'url' : url, 'title' : title, 'text' : sentences}
        #print(new_dict)
        docs_list.append(new_dict)
        i = i + 1
    #print(unique_words)
    return docs_list, unique_words, buffer_out
'''

def search_on_docs(text, words_dict):
    text_words = word_tokenize(re.sub(r"[^a-zA-ZçÇéêíáâãõôóúûÉÊÍÁÂÃÕÔÓÚÛ]+", " ", text).lower())
    #print(text_words)
    inds = None
    for word in text_words:
        try:
            new_inds = words_dict[word]
            #print(word)
            if(inds == None):
                inds = new_inds.copy()
            else:
                #inds = [value for value in new_inds if value in inds]
                #print('old inds', inds)
                inds = list(set(inds).intersection(new_inds))
                #print('new inds', new_inds)
                #print('intersection', inds)
        except:
            inds = []
            break
    if(inds==None):
        inds = []
    #if(len(inds) > 0 and text=='Anno Domini'):
    #    #print('achou')
    #    print(text)
    return inds

def update_unique_words(new_unique_words, unique_words):
    for word in new_unique_words:
        if(word in unique_words):
            if(len(unique_words[word]) < 50):
                for ind in new_unique_words[word]:
                    if(ind not in unique_words[word]):
                        unique_words[word].append(ind)
        else:
            unique_words[word] = new_unique_words[word]
    return unique_words

def search_on_brwac(wiki_ids, wiki_titles, brwac_file_path):
    unique_words = {}
    for title in wiki_titles:
        title = re.sub(r"[^a-zA-ZçÇéêíáâãõôóúûÉÊÍÁÂÃÕÔÓÚÛ]+", " ", title).lower()
        title_words = word_tokenize(title)
        for word in title_words:
            unique_words[word] = []
    hash_table = HashTable(200)
    wiki_urls = []
    for wiki_id in wiki_ids:
        wiki_urls.append({'id' : wiki_id, 'docids' : []})
    buffer_size = 150000
    total_size = int(22000000000/buffer_size)
    with open(brwac_file_path, 'r', encoding="utf-8") as file:
        i = 0
        buffer = file.read(buffer_size)
        docs = []
        n = 0
        while(len(buffer) > 5):
            new_docs, unique_words, buffer, n = read_brwac_docs(buffer, wiki_titles, n, unique_words)
            docs = docs + new_docs
            #unique_words = update_unique_words(new_unique_words, unique_words)
            buffer = buffer + file.read(buffer_size)
            print('{}/{} - buffer size: {}'.format(i, total_size, len(buffer)))
            if(i == 50000):
                break
            i = i + 1
        #print(unique_words['astronomia'], unique_words['domini'])
        if(len(docs) > 0):
            for j in range(len(wiki_ids)):
                if(len(wiki_urls[j]['docids']) < 50):
                    docs_inds = search_on_docs(wiki_titles[j], unique_words)
                    for ind in docs_inds:
                        doc = docs[ind]
                        #check if field exists
                        is_offensive = False
                        # check if uri is one to filter (known offensive websites or wikipedia)
                        if('url' in doc):
                            is_offensive = check_url(doc['url'])
                        #wiki_urls[j]['urls'].append(doc.attrib['uri'])
                        hash_table.set_val(doc['docid'], doc['text'])
                        #print(ss)
                        wiki_urls[j]['docids'].append(doc['docid'])
                        #wiki_urls[j]['texts'].append(doc.text)
                print(j, len(wiki_ids))
        else:
            print('buffer sem docs!', len(buffer))
            print(buffer[:10], buffer[-10:])
        buffer = buffer + file.read(buffer_size)
        #if(i==5):
        #    break
    return wiki_urls, hash_table

def main(args):
    wiki_titles = []
    wiki_ids = []
    dir_name = 'AA/'
    #file_names = [f for f in listdir(args.wiki_path + dir_name) if isfile(join(args.wiki_path + dir_name, f))]
    file_names = ['processed_wiki_{:02d}.json'.format(i) for i in range(0, 1)]
    for file_name in file_names:
        print(file_name)
        with open(args.wiki_path + dir_name + file_name, 'r', encoding="utf-8") as file:
            for line in file:
                content = json.loads(line)
                wiki_titles.append(content['title'])
                wiki_ids.append(content['id'])
    brwac_wiki_urls_dicts, hash_table = search_on_brwac(wiki_ids, wiki_titles, args.brwac_file)
    with open(args.wiki_urls_output_path + dir_name + 'wiki_docids.json', 'wb') as out_file:
        for wiki in brwac_wiki_urls_dicts:
            out_file.write('{}\n'.format(json.dumps(wiki, ensure_ascii=False)).encode('utf-8'))
    serialized_urls = []
    try:
        with open("{}serialized_urls_list.txt".format(args.urls_sentences_output_path), 'r') as file:
            for line in file:
                serialized_urls.append(line.replace('\n', ''))
    except:
        pass
    new_urls = []
    for i in range(len(hash_table.hash_table)):
        with open("{}{:03d}.json".format(args.urls_sentences_output_path, i), 'ab+') as out_file:
            for docid, sentences in hash_table.hash_table[i]:
                if(docid not in serialized_urls):
                    new_urls.append(docid)
                    url_dict = {'docid' : docid, 'sentences' : sentences}
                    out_file.write('{}\n'.format(json.dumps(url_dict, ensure_ascii=False)).encode('utf-8'))
    with open("{}serialized_urls_list.txt".format(args.urls_sentences_output_path), 'a+') as file:
        for docid in new_urls:
            file.write('{}\n'.format(docid))

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Generate Wikisum-pt dataset from Wikipedia articles and BrWac corpus.')
	parser.add_argument('--brwac_file', default='data/brwac/brwac-dec13.vert', type=str)
	parser.add_argument('--wiki_path', default='data/wikipedia_articles_json/', type=str)
	parser.add_argument('--wiki_file', default='AA/processed_wiki_00.json', type=str)
	parser.add_argument('--wiki_urls_output_path', default='data/wikipedia_ref_urls_brwac_v4/', type=str)
	parser.add_argument('--urls_sentences_output_path', default='data/brwac_ref_urls_sentences_v4/', type=str)
	args = parser.parse_args()
	# turn-on the worker thread
	#for i in range(args.workers):
	#	threading.Thread(target=worker, daemon=True).start()
	main(args)
