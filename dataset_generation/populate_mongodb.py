import json
import lxml.etree as ET
from codecs import open
import argparse
import pymongo
from pymongo import MongoClient

def get_brwac_docs_from_buffer(buffer):
    docs_list = []
    buffer_out = None
    try:
        last_doc_close_pos = buffer.rindex('</doc>')
        buffer_out = buffer[last_doc_close_pos + 6:]
        xml = """<root> """ + buffer[:last_doc_close_pos + 6] + """ </root>"""
        parser = ET.XMLParser(encoding="utf-8", recover='True')
        tree = ET.fromstring(xml.encode('utf-8'), parser=parser)
        docs = tree.findall('doc')
        # print(len(buffer[:last_doc_close_pos + 6].split('<doc ')))
        for doc in docs:
            full_text = ""
            p = doc.findall('p')
            for i in range(len(p)):
                new_para = ET.tostring(p[i], encoding=str).replace('<s>\n', '').replace('</s>\n', '').replace('<g/>\n', '').replace('\n', ' ')[4:-6]
                full_text = full_text + new_para.lower()
                if (i != len(p) - 1):
                    full_text = full_text + '\n'
            url = ''
            try:
                url = doc.attrib['uri']
            except:
                pass
            title = ''
            try:
                title = doc.attrib['title']
            except:
                pass
            new_dict = {'docid': doc.attrib['docid'], 'url' : url, 'title' : title, 'text' : full_text}
            docs_list.append(new_dict)
    except ValueError:
        buffer_out = buffer
    return docs_list, buffer_out

def populate_db(db, brwac_file_path, buffer_size):
    with open(brwac_file_path, 'r', encoding="utf-8") as file:
        total_size = int(22000000000/buffer_size)
        i = 0
        buffer = file.read(buffer_size)
        while(len(buffer) > 5):
            print('{}/{} - buffer size: {}'.format(i, total_size, len(buffer)))
            docs, buffer = get_brwac_docs_from_buffer(buffer)
            if(len(docs) > 0):
                db.brwac.insert_many(docs)
            #print(docs[0])
            #print(len(docs))
            buffer = buffer + file.read(buffer_size)
            i = i + 1

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate Wikisum-pt dataset from Wikipedia articles and BrWac corpus.')
    parser.add_argument('--brwac_file', default='data/brwac/brwac-dec13.vert', type=str)
    parser.add_argument('--buffer_size', default=150000, type=int)
    args = parser.parse_args()
    client = MongoClient()
    db = client.wikisumpt
    populate_db(db, args.brwac_file, args.buffer_size)