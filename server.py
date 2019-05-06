'''Server for obtaining the requested endpoints, the file contains
    several functions. The information will be sent as html format
    or json format'''

import http.client
import http.server
import json
import socketserver
import termcolor

PORT = 8000
socketserver.TCPServer.allow_reuse_address = True


class TestHandler(http.server.BaseHTTPRequestHandler):
# FUNCTION FOR THE CLIENT
    def client(self, specific_endpoint):
        METHOD = 'GET'
        ENDPOINT = specific_endpoint
        HOSTNAME = 'rest.ensembl.org'
        headers = {'User-Agent': 'http-client'}
        conn = http.client.HTTPConnection(HOSTNAME)
        conn.request(METHOD, ENDPOINT, None, headers)
        r1 = conn.getresponse()
        print()
        data = r1.read().decode("utf-8")
        conn.close()
        return data

# FUNCTION FOR OBTAINING THE LIST OF SPECIES
    def name_species(self, limit, main_page, format):
        try:
            info_client = self.client('/info/species?content-type=application/json')
            information = json.loads(info_client)
            species_info = information['species']
            titles = main_page + "<h2>Species: </h2>"
            count = 0
            species_list = []
            if limit == '' or (0 < int(limit) <= 199):
                if limit == '':
                    range_limit = species_info[:]
                else:
                    limit = int(limit)
                    range_limit = species_info[:limit]
                for element in range_limit:
                    count += 1
                    name = element['display_name']
                    if format == 'json=1':
                        species_list.append(name)
                        content = [{'Species': species_list}]
                    else:
                        name = str(count) + '. ' + name
                        titles += "<p>" + name + "</p>"
                        content = titles
            elif int(limit) > 199:
                if format == 'json=1':
                    content = ["The list of species contains only 199 species"]
                else:
                    content = titles + "<p>The list of species contains only 199 species</p>"
            elif int(limit) == 0:
                if format == 'json=1':
                    content = ['Number of species requested = 0']
                else:
                    content = titles + "<p>The number of species requested = 0</p>"
            elif int(limit) < 0:
                if format == 'json=1':
                    content = ['The number of species requested is negative']
                else:
                    content = titles + "<p>The number of species requested is negative</p>"
        except ValueError:
            if format == 'json=1':
                content = ['-ERROR, invalid parameter-  Please try again.']
            else:
                with open('error_parameter.html', 'r') as r:
                    content = r.read()
        return content

# FUNCTIONS FOR OBTAINING THE KERYOTYPE
    def karyotype_species(self, option_specie, main_page, format):
        try:
            info_client = self.client('''/info/assembly/''' + option_specie + '''?content-type=application/json''')
            information = json.loads(info_client)
            karyotype_info = information['karyotype']
            dict_json = {'Specie': option_specie.capitalize()}
            titles = main_page + "<h2>Specie: " + option_specie.capitalize() + "</h2>" + "<p><h2>Karyotype</h2></p>"
            count = 0
            element_list = []
            if karyotype_info == []:
                if format == 'json=1':
                    dict_json.update({'Karyotype':'Does not exist any karyotype for this specie'})
                    content = [dict_json]
                else:
                    content = titles + "<p>Does not exist any karyotype for this specie</p>"
            else:
                for element in karyotype_info:
                    element_list.append(element)
                    count += 1
                    if format == 'json=1':
                        dict_json.update({'Karyotype': element_list})
                        content = [dict_json]
                    else:
                        length = len(karyotype_info)
                        if count < length:
                            titles += element + ', '
                        else:
                            titles += element
                        content = titles
        except KeyError:
            if format == 'json=1':
                content = ['-ERROR, invalid parameter-  Please try again.']
            else:
                with open('error_parameter.html', 'r') as r:
                    content = r.read()
        return content

# FUNCTIONS FOR OBTAINING THE LENGTH OF THE CHROMOSOME REQUESTED
    def chromo_length(self, specie, chromo, main_page, format):
        try:
            info_client = self.client('''/info/assembly/''' + specie + '''?content-type=application/json''')
            information = json.loads(info_client)
            chromosome_info = information['top_level_region']
            chromo = chromo.upper()
            dict_json = {'Specie': specie.capitalize(), 'Chromosome': chromo}
            titles = main_page + "<h2>Specie: " + specie.capitalize() + "</h2>" + "<p><h2>Chromosome: " + chromo + '</h2></p>'
            list_names = []
            for element in chromosome_info:
                name = element['name']
                list_names.append(name)
            if chromo in list_names:
                for element in chromosome_info:
                    name = element['name']
                    if name == chromo:
                        length = element['length']
                        if format == 'json=1':
                            dict_json.update({'Length_chromosome': str(length)})
                            content = [dict_json]
                        else:
                            content = titles + "<p><h3>The length of the chromosome requested is: " + str(length) + "</h3></p>"
            else:
                if format == 'json=1':
                    content = ['-ERROR, invalid parameter-  Please try again.']
                else:
                    with open('error_parameter.html', 'r') as r:
                        content = r.read()
        except KeyError:
            if format == 'json=1':
                content = ['-ERROR, invalid parameter-  Please try again.']
            else:
                with open('error_parameter.html', 'r') as r:
                    content = r.read()
        return content

# --------- MEDIUM LEVEL --------------
# FUNCTION FOR OBTAINING ID
    def id_genes(self, gene):
        try:
            gene = gene.upper()
            gene_id = self.client('''/homology/symbol/human/''' + gene + '''?content-type=application/json''')
            gene_info = json.loads(gene_id)
            data = gene_info['data']
            content = data[0]['id']
        except KeyError:
            content = 'Error'
        return content

# FUNCTIONS FOR OBTAINING THE SEQUENCE OF THE GENE REQUESTED
    def gene_sequence(self, gene, main_page, format):
        try:
            id = self.id_genes(gene)
            info_client = self.client('''/sequence/id/''' + id + '''?content-type=application/json''')
            information = json.loads(info_client)
            sequence = information['seq']
            if format == 'json=1':
                content = [{'Gene': gene.upper(), 'Sequence': sequence}]
            else:
                content = main_page + "<h2>Sequence of the gene: " + gene.upper() + "</h2>"
                n = 127
                seq_list = [sequence[i:i + n] for i in range(0, len(sequence), n)]
                for element in seq_list:
                    sequence = element + '\n'
                    content = content + sequence
        except KeyError:
            if format == 'json=1':
                content = ['-ERROR, invalid parameter-  Please try again.']
            else:
                with open('error_parameter.html', 'r') as r:
                    content = r.read()
        return content

# FUNCTION FOR OBTAINING THE START, END, ID, LENGTH, AND CHROMOSOME OF THE GENE
    def gene_information(self, gene, main_page, format):
        try:
            id = self.id_genes(gene)
            info_client = self.client('''/overlap/id/''' + id + '''?feature=gene;content-type=application/json''')
            total_info = json.loads(info_client)
            info_client_seq = self.client('''/sequence/id/''' + id + '''?content-type=application/json''')
            info_seq = json.loads(info_client_seq)
            for elements in total_info:
                if elements['external_name'] == gene.upper():
                    start = elements['start']
                    end = elements['end']
                    chromo = elements['assembly_name']
                    sequence_region = elements['seq_region_name']
                    sequence = info_seq['seq']
                    seq_length = len(sequence)

                    if format == 'json=1':
                        content = {'Gene': gene.upper(),'ID': id, 'Length': str(seq_length), 'Start': str(start)}
                        content.update({'End': str(end), 'Chromosome': chromo, 'Region_name': sequence_region})
                        content = [content]
                    else:
                        content_length = '<p>Length: ' + str(seq_length) + '</p>'
                        content_end = '<p>End: </h4>' + str(end) + '</p>'
                        content_start = '<p>Start: ' + str(start) + '</p>'
                        content_id = '<p>ID: ' + id + '</p>'
                        content_chromo = '<p>Chromosome: ' + chromo + ' ' + 'Region Name: ' + sequence_region + '</p>'
                        content = main_page + "<h2>Information of the gene: " + gene.upper() + "</h2>" + content_id + content_length
                        content = content + content_start + content_end + content_chromo
        except TypeError:
            if format == 'json=1':
                content = ['-ERROR, invalid parameter-  Please try again.']
            else:
                with open('error_parameter.html', 'r') as r:
                    content = r.read()
        return content

# FUNCTION FOR CALCULATING THE PERCENTAGES
    def seq_calculations(self, sequence):
        count_a = count_c = count_g = count_t = 0
        for b in sequence:
            if b == 'A':
                count_a += 1
            elif b == 'C':
                count_c += 1
            elif b == 'G':
                count_g += 1
            elif b == 'T':
                count_t += 1
        dictionary = {'A': count_a, 'C': count_c, 'G': count_g, 'T': count_t}
        base_list = ['A', 'C', 'G', 'T']
        perc_list = []
        for base in base_list:
            counter = dictionary.get(base)
            percentage = round(100.0 * counter / len(sequence), 1)
            perc_list.append(percentage)
        return perc_list

# FUNCTION FOR RETURNING THE LENGTH OF THE SEQUENCE AND THE PERCENTAGES REQUESTED
    def gene_calculations(self, gene, main_page, format):
        try:
            id = self.id_genes(gene)
            info_client = self.client('''/sequence/id/''' + id + '''?content-type=application/json''')
            information = json.loads(info_client)
            sequence = information['seq']
            length = len(sequence)
            calc = self.seq_calculations(sequence)
            if format == 'json=1':
                content = {'Gene': gene.upper(), 'Length': str(length)}
                content.update({'Percentages': [{'A': str(calc[0]) + ' %', 'C': str(calc[1]) + ' %', 'G': str(calc[2]) + ' %', 'T': str(calc[3]) + ' %'}]})
                content = [content]
            else:
                content_length = '<p>Length: ' + str(length) + '</p>'
                content_perc_1 = '<h4>Percentage of bases: </h4>' + '<p>A: ' + str(calc[0]) + '%</p>' + '<p>C: ' + str(calc[1]) + '%</p>'
                content_perc = content_perc_1 + '<p>G: ' + str(calc[2]) + '%</p>' + '<p>T: ' + str(calc[3]) + '%</p>'
                content = main_page + "<h2>Sequence of the gene: " + gene.upper() + "</h2>" + content_length + content_perc
        except KeyError:
            if format == 'json=1':
                content = ['-ERROR, invalid parameter-  Please try again.']
            else:
                with open('error_parameter.html', 'r') as r:
                    content = r.read()
        return content

# FUNCTION FOR OBTAINING THE NAMES OF THE GENES
    def genes_name(self, chromo, start, end, main_page, format):
        try:
            info_client = self.client('''/overlap/region/human/''' + chromo + ''':''' + start + '''-''' + end + '''?content-type=application/json;feature=gene;feature=transcript;feature=cds;feature=exon''')
            information = json.loads(info_client)
            if information == [] or 'error' in information:
                if format == 'json=1':
                    content = ['-ERROR, invalid parameter-  Please try again.']
                else:
                    with open('error_parameter.html', 'r') as r:
                        content = r.read()
            else:
                list_names = []
                count = 0
                titles = main_page + "<h2>Name of the genes</h2>"
                for key_words in information:
                    count += 1
                    if key_words['feature_type'] == 'gene':
                        names = key_words['external_name']
                        if format == 'json=1':
                            list_names.append(names)
                            content = [{'Genes': list_names}]
                        else:
                            gene_names = str(count) + '. ' + names
                            titles += "<p>" + gene_names + "</p>"
                            content = titles
        except KeyError:
            if format == 'json=1':
                content = ['-ERROR, invalid parameter-  Please try again.']

            else:
                with open('error_parameter.html', 'r') as r:
                    content = r.read()
        return content


    def do_GET(self):
        termcolor.cprint(self.requestline, 'yellow')
        divide_msg = self.path.split('=')
        main_page = """<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Data</title>
            <h1>Information Requested<h1>
        </head>
        <body style="background-color: orange">
        <h3>---Link for returning to the Main page---</h3>
        <a href="http://localhost:8000/">Main Page</a>"""

# OPTIONS FOR EVERY ENDPOINT
        if self.path == '/':
            with open('index.html', 'r') as f:
                contents = f.read()

        elif divide_msg[0] == '/listSpecies?limit':
            limit = divide_msg[1]
            if 'json=1' in self.path:
                limit = limit[:-5]
                info = self.name_species(limit, main_page, 'json=1')
                contents = json.dumps(info)
            else:
                contents = self.name_species(limit, main_page, 'html')

        elif divide_msg[0] == '/listSpecies' or divide_msg[0] == '/listSpecies?json':
            limit = ''
            if 'json=1' in self.path:
                info = self.name_species(limit, main_page, 'json=1')
                contents = json.dumps(info)
            else:
                contents = self.name_species(limit, main_page, 'html')

        elif divide_msg[0] == '/karyotype?specie':
            option_specie = divide_msg[1]
            if 'json=1' in self.path:
                option_specie = option_specie[:-5]
                info = self.karyotype_species(option_specie, main_page, 'json=1')
                contents = json.dumps(info)
            else:
                contents = self.karyotype_species(option_specie, main_page, 'html')

        elif divide_msg[0] == '/chromosomeLength?specie':
            specie = divide_msg[1][:-7]
            chromo = divide_msg[2]
            if 'json=1' in self.path:
                chromo = chromo[:-5]
                info = self.chromo_length(specie, chromo, main_page, 'json=1')
                contents = json.dumps(info)
            else:
                contents = self.chromo_length(specie, chromo, main_page, 'html')

        elif divide_msg[0] == '/geneSeq?gene':
            gene = divide_msg[1]
            if 'json=1' in self.path:
                gene = gene[:-5]
                info = self.gene_sequence(gene, main_page, 'json=1')
                contents = json.dumps(info)
            else:
                contents = self.gene_sequence(gene, main_page, 'html')

        elif divide_msg[0] == '/geneInfo?gene':
            gene = divide_msg[1]
            if 'json=1' in self.path:
                gene = gene[:-5]
                info = self.gene_information(gene, main_page, 'json=1')
                contents = json.dumps(info)
            else:
                contents = self.gene_information(gene, main_page, 'html')

        elif divide_msg[0] == '/geneCalc?gene':
            gene = divide_msg[1]
            if 'json=1' in self.path:
                gene = gene[:-5]
                info = self.gene_calculations(gene, main_page, 'json=1')
                contents = json.dumps(info)
            else:
                contents = self.gene_calculations(gene, main_page, 'html')

        elif divide_msg[0] == '/geneList?chromo':
            chromo = divide_msg[1][:-6]
            start = divide_msg[2][:-4]
            end = divide_msg[3]
            if 'json=1' in self.path:
                end = end[:-5]
                info = self.genes_name(chromo, start, end, main_page, 'json=1')
                contents = json.dumps(info)
            else:
                contents = self.genes_name(chromo, start, end, main_page, 'html')
# ERRORS
        else:
            if 'json=1' in self.path:
                info = ['-ERROR- You have introduced an invalid ENDPOINT']
                contents = json.dumps(info)
            else:
                with open('error.html', 'r') as r:
                    contents = r.read()

# possibilities: API or REST API
        self.send_response(200)

        if 'json=1' in self.path:
            self.send_header('Content-Type', 'application/json')
        else:
            self.send_header('Content-Type', 'text/html')

        self.send_header('Content-Length', len(str.encode(contents)))
        self.end_headers()
        self.wfile.write(str.encode(contents))


# ------MAIN PROGRAM------
with socketserver.TCPServer(('', PORT), TestHandler) as httpd:
    print('Serving at PORT', PORT)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()
print('Sever stopped')

