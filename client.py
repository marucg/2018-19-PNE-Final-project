'''Client for processing the json file'''

import json
import http.client

PORT = 8000
SERVER = '127.0.0.1'

# INTRODUCING THE PARAMETERS

limit = input('Introduce the limit parameter for obtaining species: ')
specie = input('Introduce a specie for obtaining the karyotype: ')
specie_chromo = input('Introduce a specie for obtaining the length of its chromosome: ')
chromo = input('Introduce the chromosome for obtaining length: ')
seq = input('Introduce a gene for obtaining its sequence: ')
info = input('Introduce a gene for obtaining information: ')
calc = input('Introduce a gene for some calculations: ')
gene_chromo = input('Introduce a chromosome for obtaining its genes names: ')
start = input('Introduce the start position: ')
end = input('Introduce the end position: ')

endpoints = ['/listSpecies?limit=' + limit + '&json=1', '/listSpecies?json=1', '/karyotype?specie=' + specie + '&json=1',
            '/chromosomeLength?specie=' + specie_chromo + '&chromo=' + chromo + '&json=1', '/geneSeq?gene=' + seq + '&json=1',
            '/geneInfo?gene=' + info + '&json=1', '/geneCalc?gene=' + calc + '&json=1',
            '/geneList?chromo=' + gene_chromo + '&start=' + start + '&end=' + end + '&json=1']



print("\nConnecting to server: \n", 'Server:', SERVER + ', Port:', PORT)
conn = http.client.HTTPConnection(SERVER, PORT)
print('\n---Information obtained---\n')

# LOOP FOR OBTAINING EVERY ENDPOINT INCLUDED IN THE LIST
for data in endpoints:
    conn.request("GET", data)
    r1 = conn.getresponse()
    data1 = r1.read().decode("utf-8")
    information = json.loads(data1)
    print(information)
print("Response received: \n", str(r1.status) + ', ', r1.reason)


