import argparse
from brwac_tools import iterate_over_brwac

parser = argparse.ArgumentParser(description='Transform BrWac vert format to plain text xml: <doc docid=(...)>  (TEXT) </doc>')
parser.add_argument('--brwac_in', default='data/brwac/brwac-dec13.vert', type=str)
parser.add_argument('--brwac_out', default='data/brwac/brwac.plain', type=str)
parser.add_argument('--buffer_size', default=150000, type=int)
args = parser.parse_args()

def write_xml(docs):
    with open(args.brwac_out, 'ab+') as out_file:
        to_out = """"""
        for doc in docs:
            to_out = to_out + """<doc docid="{}" title="{}" url="{}"> \n {} \n </doc> \n""".format(doc["docid"], doc["title"], doc["url"], doc["text"])
        out_file.write(to_out.encode('utf-8'))

iterate_over_brwac(write_xml, args.brwac_in, args.buffer_size)
