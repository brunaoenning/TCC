#!/usr/bin/env python
# coding: utf-8

import os
import re
import pandas as pd

#use common path to easily change the main path
common_path = "C:/Users/bruna/OneDrive/Documentos/Ellas/Secondary Data"

# read the files in the folder
path = common_path + "/Data"
files = os.listdir(path)
print(files)

#create folder with all the links triple files
folder = common_path + "/RDF"
os.makedirs(folder, exist_ok=True)

# for each file in the folder
for file in files:
    final_path = path + "/" + file
    print(final_path)
    df = pd.read_csv(final_path, index_col=None, encoding='latin-1', low_memory=False)
    
    #add secondary data id INEP2020 and source INEP
    df['FONTE'] = "INEP"
    df['SECONDARY_DATA_ID'] = "INEP"+str(df['NU_ANO_CENSO'][0])
    df.to_csv(final_path) #replace the original file
    
    #create
    pipe_path="ontorefine-cli.cmd create \""+final_path+"\" -u http://localhost:7333"
    os.chdir(r'C:/Users/bruna/AppData/Local/Ontotext Refine/app/bin/')
    pipe = os.popen(pipe_path)
    result = pipe.read()
    pipe.close()
    print(result)
    id_project = re.findall("\d+", result) #finding the numbers into result variable
    
    #apply operations
    pipe_path="ontorefine-cli.cmd apply \""+common_path+"/mapping.json\" "+id_project[0]+" -u http://localhost:7333"
    pipe = os.popen(pipe_path)
    result = pipe.read()
    print(result)
    pipe.close()
    
    #RDF export
    pipe_path="ontorefine-cli.cmd rdf "+id_project[0]+" -m \""+common_path+"/mapping.json\" -u http://localhost:7333"
    pipe_path
    pipe = os.popen(pipe_path)
    result = pipe.read()
    pipe.close()
    
    #download triples as ttl file
    download_path = ""+folder+"/triples_"+id_project[0]+".ttl"
    file = open(download_path, "w")
    a = file.write(result)
    file.close()

    #add year to secondary data controll file
    controll_file = pd.read_csv(""+common_path+"/secondarydata_uploaded.csv", index_col=None, encoding='latin-1', low_memory=False)
    controll_file = controll_file['year']
    controll_file.loc[len(controll_file.index)] = str(df['NU_ANO_CENSO'][0])
    controll_file.to_csv(""+common_path+"/secondarydata_uploaded.csv")
