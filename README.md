# BrWac2Wiki
Official repo for the dataset BrWac2Wiki.

__The challenge: Generate Brazilian Wikipedia articles from multiple website texts!__

This is a dataset for multi-document summarization in Portuguese, what means that it has examples of multiple documents (input) related to human-written summaries (output). In particular, it has entries of __multiple related texts from Brazilian websites__ about a subject, and the summary is the __Portuguese Wikipedia lead section on the same subject__ (_lead_: the first section, i.e., summary, of any Wipedia article).
Input texts were extracted from BrWac corpus, and the output from Brazilian Wikipedia dumps page.

BrWac2Wiki contains __114.652 examples__ of (documents, wikipedia) pairs! So it is suitable for training and validating AI models for multi-document summarization in Portuguese.
More information on the paper "PLSUM: Generating PT-BR Wikipedia by Summarizing Websites", by André Seidel Oliveira¹ and Anna Helena Reali Costa¹, that is going to be presented at ENIAC 2021.
Our work is inspired by WikiSum, a similar dataset for the English language.

The full dataset can be downloaded [here](https://drive.google.com/drive/folders/1JLlnk-H4YtBuCmilktdrnA9qZGbX1DmQ?usp=sharing). 

1 - researchers at the Department of Computer Engineering and Digital Systems (PCS) of University of São Paulo (USP)

## Description of data
There are three files on the dataset: _docids.json_, _input.csv_, and _output.csv_.

### _docids.json_:
Shows the BrWac docs related to each Wikipedia article. Each line is a json entry relating a unique Wikipedia article identifier, _wiki_id_, to several BrWac unique identifiers for documents, _docids_. Each BrWac document cite all the words from the Wikipedia article title, _wiki_title_, at least once. 
Example:
```json
{
  "wiki_id": "415", 
  "wiki_title": "Hino da Independência do Brasil", 
  "docids": ["net-6bb71a", "nete-1e5c7d", "neth-1682c"],
}
```
- _wiki_id_: is the Portuguese Wikipedia _entity id_ for "Hino da Independência do Brasil";
- _wiki_title_: is the title of a Wikipedia article;
- _docids_: is a list of document unique ids from BrWac. Each document is the text content from an website;

### _input.csv_:
Each line has the title for a wiki article and the __sentences__ (document's extracts with a maximum of 100 words) from the BrWac documents associated to the article, separated by the symbol _</s>_. __Lines in the same order as docids.json__.
Example:
```
1  astronomia </s> veja nesta página do site - busca relacionada a astronomico com a seguinte descrição - astronomico </s> astronômico dicionário informal significado de astronômico o que é astronômico substivo masculino referente a corpos celestes como estrelas planetas satélites. </s> (...)
2  (...)
```

### _output.csv_ :
Each line contains the __lead section__ for a Wikipedia article, __also in the same order as docids.json__.
Example:
```
1  O Hino da Independência é uma canção patriótica oficial comemorando a declaração da independência do Brasil, composta em 1822 por Dom Pedro I. A letra foi escrita pelo poeta Evaristo da Veiga.
2  (...)
```

## Details
The search for association between BrWac documents and Wikipedia articles was made with the help of a MongoDB database. We populated the database with BrWac documents and them perform a text search for Wikipedia titles. 

For time reasons, the search had the following rule:
- Search for __every word on the article title__ (AND search);
- Limit a maximum of 15 documents per wiki article;
- Search for __2 seconds__ at least __1 document__, if not found, remove wiki article from dataset.

## Acknowledgements
This research was supported by _Itaú Unibanco S.A._, with the scholarship program of _Programa de Bolsas Itaú_ (PBI), and partially financed by the Coordenação de Aperfeiçoamento de Pessoal de Nível Superior (CAPES), Finance Code 001, and CNPQ (grant 310085/2020-9), Brazil.
Any opinions, findings, and conclusions expressed in this manuscript are those of the authors and do not necessarily reflect the views, official policy or position of the Itaú-Unibanco, CAPES and CNPq.

