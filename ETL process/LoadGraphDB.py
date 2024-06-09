import glob
import requests

#Import files from folder RDF
rdf_files = glob.glob("C:/Users/bruna/OneDrive/Documentos/Ellas/Secondary Data/RDF/*")
#Execute load for all the files
for file in rdf_files:
    print("From file ",file)
    data=open(file, 'r')
    for d in data:
        if ('SecondaryData' in d):
            d_end = d.split(' ')
            named_graph = d_end[0]
            print("Named graph", named_graph)
            break
    url = 'http://localhost:7200/repositories/ELLAS-Ontology-Inep/statements'
    headers = {
        'Content-Type': 'text/turtle',
    }
    data.close()
    data = open(file, 'rb').read()

    # Formatando o URI do Named Graph corretamente
    context_uri = named_graph
    response = requests.post(url, headers=headers, data=data, params={'context': context_uri})

    if response.status_code == 204:
        print('Arquivo Turtle importado com sucesso para o Named Graph:', context_uri)
    else:
        print('Erro ao importar o arquivo Turtle:', response.text)