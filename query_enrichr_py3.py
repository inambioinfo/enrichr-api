#!/usr/bin/env python

# python 3
# Author: Stephen Newhouse <stephen.j.newhouse@gmail.com>
# Date: June 2016
# see: http://amp.pharm.mssm.edu/Enrichr/help#api for API docs
#
# Usage: python query_enrichr_v0.1.py <genelist> <listdesrciption> <enrichr_library> <enrichr_results>

import json
import requests
import sys

print("Enrichr API : Start")
print("Enrichr API : Reading Command Options")
## get command line args
genelist = sys.argv[1]
listdesrciption = sys.argv[2]
enrichr_library = sys.argv[3]
enrichr_results = sys.argv[4]

# testing
# genelist = "gene_list.txt"
# enrichr_library = "KEGG_2016"
# listdesrciption = "TEST"
# enrichr_results = "example_enrichment_KEGG_2016"

## Print options
print('Enrichr API : Input file is:', genelist)
print('Enrichr API : Analysis name: ', listdesrciption)
print('Enrichr API : Enrichr Library: ', enrichr_library)
print('Enrichr API : Enrichr Results File: ', enrichr_results)

# get gene lits
print("Enrichr API : Reading:",genelist)
f = open(genelist)
genes = f.read()

## enrichr url
ENRICHR_URL = 'http://amp.pharm.mssm.edu/Enrichr/addList'

# stick gene list here
genes_str = str(genes)

# name of analysis or list
description = str(listdesrciption)

# payload
payload = {
  'list': (None, genes_str),
  'description': (None, description)
}

# response
print("Enrichr API : requests.post")
response = requests.post(ENRICHR_URL, files=payload)

if not response.ok:
  raise Exception('Error analyzing gene list')

job_id = json.loads(response.text)

print('Enrichr API : Job ID:', job_id)

################################################################################
# View added gene list
#
ENRICHR_URL_A = 'http://amp.pharm.mssm.edu/Enrichr/view?userListId=%s'

user_list_id = job_id['userListId']
#print(user_list_id)

response_gene_list = requests.get(ENRICHR_URL_A % str(user_list_id))

if not response_gene_list.ok:
    raise Exception('Error getting gene list')

print('Enrichr API : View added gene list:', job_id)
added_gene_list = json.loads(response_gene_list.text)
print(added_gene_list)

################################################################################
# Get enrichment results
#
ENRICHR_URL = 'http://amp.pharm.mssm.edu/Enrichr/enrich'
query_string = '?userListId=%s&backgroundType=%s'

## get id data
user_list_id = job_id['userListId']

## Libraray
gene_set_library = str(enrichr_library)

response = requests.get(
    ENRICHR_URL + query_string % (str(user_list_id), gene_set_library)
 )
if not response.ok:
    raise Exception('Error fetching enrichment results')

print('Enrichr API : Get enrichment results: Job Id:', job_id)
data = json.loads(response.text)
print(data)

################################################################################
## Download file of enrichment results
#
ENRICHR_URL = 'http://amp.pharm.mssm.edu/Enrichr/export'

query_string = '?userListId=%s&filename=%s&backgroundType=%s'

user_list_id = str(job_id['userListId'])

filename = enrichr_results

gene_set_library = str(enrichr_library)

url = ENRICHR_URL + query_string % (user_list_id, filename, gene_set_library)

response = requests.get(url, stream=True)

print('Enrichr API : Downloading file of enrichment results: Job Id:', job_id)
with open(filename + '.txt', 'wb') as f:
    for chunk in response.iter_content(chunk_size=1024):
        if chunk:
            f.write(chunk)
################################################
print('Enrichr API : Results written to:', enrichr_results + ".txt")
print("Enrichr API : Done")
