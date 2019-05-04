'''Client for processing the json file'''

import json
import http.client

PORT = 8000
SERVER = '127.0.0.1'

# PARAMETERS ALREADY ESTABLISHED
endpoints = ['/listSpecies?limit=5&json=1', '/listSpecies?json=1', '/karyotype?specie=mouse&json=1',
             '/chromosomeLength?specie=mouse&chromo=12&json=1', '/geneSeq?gene=frat1&json=1',
             '/geneInfo?gene=frat1&json=1', '/geneCalc?gene=frat1&json=1',
             '/geneList?chromo=1&start=0&end=30000&json=1']


print("\nConnecting to server: \n", 'Server:', SERVER + ', Port:', PORT)
conn = http.client.HTTPConnection(SERVER, PORT)
print('---Information obtained---')

# LOOP FOR OBTAINING EVERY ENDPOINT INCLUDED IN THE LIST
for data in endpoints:
    conn.request("GET", data)
    r1 = conn.getresponse()
    data1 = r1.read().decode("utf-8")
    information = json.loads(data1)
    print(information)
print("Response received: \n", str(r1.status) + ', ', r1.reason)


