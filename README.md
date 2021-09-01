# BrWac2Wiki
Official repo for the dataset BrWac2Wiki. Contains scripts for the generation of the dataset.

This is a dataset for multi-document summarization in Portuguese, what means that it has examples of multiple documents (input) related to human written summaries (output). In particular, it has entries of __multiple related texts from Brazilian websites__ about a subject, and the summary is the __Portuguese Wikipedia lead section on the same subject__ (_lead_: the first section, i.e., summary, of any Wipedia article).
Input texts were extracted from BrWac corpus, and the output from Brazilian Wikipedia dumps page.

BrWac2Wiki contains __114.652 examples__ of (documents, wikipedia) pairs! So it is suitable for training and validating AI models for the multi-document summarization in Portuguese.
More information on the paper "PLSUM: Generating PT-BR Wikipedia by Summarizing Websites", by André Seidel Oliveira¹ and Anna Helena Reali Costa¹, under review for the conference ENIAC 2021.
Our work is inspired by WikiSum, a similar dataset for the English language.

The dataset can be downloaded here. 

1 - researchers at the Department of Computer Engineering and Digital Systems (PCS) of University of São Paulo (USP)

## Description of data
There are three files on the dataset: _docid.json_, _docs.json_, and _wiki.json_.

### _wiki_docids.json_:

```
{
  "wiki_id": "415", 
  "wiki_title": "Hino da Independência do Brasil", 
  "docids": ["net-6bb71a", "nete-1e5c7d", "neth-1682c"],
  "doc_pos": [1, 5, 99]
}
```
- _wiki_id_: is the Portuguese Wikipedia _entity id_ for "Hino da Independência do Brasil";
- _wiki_title_: is the title of a Wikipedia article;
- _docids_: is a list of document unique ids from BrWac. Each document is the text content from an website;
- _doc_pos_: is a list of document positions on _docs.json_, for fast retrieving.

### _wiki.json_ :
```
{
  "title": "Hino da Independência do Brasil", 
  "id": "415", 
  "sections": ["", "História.", "Letra."],
  "text": ["O Hino da Independência é uma canção patriótica oficial comemorando a declaração da independência do Brasil, composta em 1822 por Dom Pedro I. A letra foi escrita pelo poeta Evaristo da Veiga.", "\nDe acordo com uma versão divulgada por Eugênio Egas em 1909, a música teria sido composta pelo Imperador na tarde do mesmo dia do Grito do Ipiranga, 7 de setembro de 1822 (quando já estava de volta a São Paulo vindo de Santos), tendo sido partiturado às pressas pelo mestre de capela da Catedral de São Paulo, André da Silva Gomes, para execução na noite desse dia, na Casa da Ópera (ao pátio do Palácio do Governo, antigo Colégio dos Jesuítas), por cantores e uma pequena orquestra. A versão de Eugênio Egas, por outro lado, nunca foi referida nos jornais brasileiros de 1822 e nunca foi comprovada com documentação do período, tendo circulado somente a partir do início do século XX.", "\nNormalmente, as estrofes 3, 4, 5, 6, 8 e 10 são hoje omitidas quando o hino da Independência é cantado."]
}
```
- _title_: is the title of a Wikipedia article (same as _wiki_title_ from _docid.json_);
- _id_: is the unique entity id for this article on Brazilian Wikipedia (same as _wiki_id_ from _docid.json_);
- _sections_: a list of section titles for this article (first position is always empty because it is the lead section);
- _text_: a list of the contained text of each section on _sections_.


### _docs.json_:
```
{
  "docid": "net-6bc350",
  "text": "independência do brasil\nseparação política entre a colônia do brasil e a metrópole portuguesa , declarada oficialmente no dia 7 de setembro de 1822 . o processo de independência começa com o agravamento da crise do sistema colonial e se estende até a adoção da primeira constituição brasileira , em 1824 .\nas revoltas do final do século xviii e começo do xix , como a inconfidência mineira , a conjuração baiana e a revolta pernambucana de 1817 , mostram o enfraquecimento do sistema colonial .\n(...)"
}
```
- _docid_: the unique document id for a website text on BrWac (same as _docid_ on the list of _docids_ from _docid.json_);
- _text_: raw text of the document.

## Details
The search for association between BrWac documents and Wikipedia articles was made with the help of a MongoDB database. We populated the database with BrWac documents and them perform a text search for Wikipedia titles. 

For time reasons, the search had the following rule:
- Search for __every word on the article title__ (AND search);
- Limit a maximum of 15 documents per wiki article;
- Search for __2 seconds__ at least __1 document__, if not found, remove wiki article from dataset.

## Dataset generation
Read ```dataset_generation/README.md``` for details on how to generate the dataset.

## Citation
If you use this dataset for your work, please cite:

## Acknowledgements

