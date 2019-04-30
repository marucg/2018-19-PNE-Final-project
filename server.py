import http.client
import http.server
import json
import socketserver
import termcolor

PORT = 8000
socketserver.TCPServer.allow_reuse_address = True



class TestHandler(http.server.BaseHTTPRequestHandler):
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

# FUNCTIONS FOR EVERY PARAMETER
    def name_species(self, limit, main_page):
        info_client = self.client('/info/species?content-type=application/json')
        information = json.loads(info_client)
        species_info = information['species']
        content = main_page + "<h2>Species: </h2>"
        count = 0
        try:
            if limit == '' or int(limit) <= 199:
                if limit == '':
                    range_limit = species_info[:]
                else:
                    limit = int(limit)
                    range_limit = species_info[:limit]
                for element in range_limit:
                    count += 1
                    name = element['display_name']
                    name = str(count) + '. ' + name
                    content += "<p>" + name + "</p>"
            elif int(limit) > 199:
                content = content + "<p>The list of species contains only 199 species</p>"
        except ValueError:
            with open('error_parameter.html', 'r') as r:
                content = r.read()
        return content


    def karyotype_species(self, option_specie, main_page):
        info_client = self.client('''/info/assembly/''' + option_specie + '''?content-type=application/json''')
        information = json.loads(info_client)
        if 'karyotype' in information:
            karyotype_info = information['karyotype']
            if karyotype_info == []:
                content = main_page + "<h2>Specie: " + option_specie.capitalize() + "</h2>" + "<p><h2>Karyotype</h2></p>"
                content = content + "<p>Does not exist any karyotype for this specie</p>"
            else:
                content = main_page + "<h2>Specie: " + option_specie.capitalize() + "</h2>" + "<p><h2>Karyotype</h2></p>"
                count = 0
                for element in karyotype_info:
                    count += 1
                    length = len(karyotype_info)
                    if count < length:
                        content += element + ', '
                    else:
                        content += element
        else:
            with open('error_parameter.html', 'r') as r:
                content = r.read()
        return content


    def chromo_length(self, specie, chromo, main_page):
        info_client = self.client('''/info/assembly/''' + specie + '''?content-type=application/json''')
        information = json.loads(info_client)
        if 'top_level_region' in information:
            chromosome_info = information['top_level_region']
            chromo = chromo.upper()
            content = main_page + "<h2>Specie: " + specie.capitalize() + "</h2>" + "<p><h2>Chromosome: " + chromo + '</h2></p>'
            list_names = []
            for element in chromosome_info:
                name = element['name']
                list_names.append(name)
            if chromo in list_names:
                for element in chromosome_info:
                    name = element['name']
                    if name == chromo:
                        length = element['length']
                        content = content + "<p><h3>The length of the chromosome requested is: " + str(length) + "</h3></p>"
            else:
                with open('error_parameter.html', 'r') as r:
                    content = r.read()
        else:
            with open('error_parameter.html', 'r') as r:
                content = r.read()
        return content

# --------- MEDIUM --------------
    def id_genes(self, gene):
        gene = gene.upper()
        gene_id = self.client('''/homology/symbol/human/''' + gene + '''?content-type=application/json''')
        gene_info = json.loads(gene_id)
        data = gene_info['data']
        id = data[0]['id']
        return id

#ARREGLAR
    def gene_sequence(self, gene,  main_page):
        try:
            id = self.id_genes(gene)
            info_client = self.client('''/sequence/id/''' + id + '''?content-type=application/json''')
            information = json.loads(info_client)
            sequence = information['seq']
            content = main_page + "<h2>Sequence of the gene: " + gene.upper() + "</h2>"
            count = 0
            for element in sequence:
                count += 1
                if count == 30:
                    sequence.split('\n')
                    count = 0
                    print('inside')
                content += content + str(sequence)
        except KeyError:
            with open('error_parameter.html', 'r') as r:
                content = r.read()
        return content

    def gene_information(self, gene, main_page):
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

                    content_length = '<p>Length: ' + str(seq_length) + '</p>'
                    content_end = '<p>End: </h4>' + str(end) + '</p>'
                    content_start = '<p>Start: ' + str(start) + '</p>'
                    content_id = '<p>ID: ' + id + '</p>'
                    content_chromo = '<p>Chromosome: ' + chromo + ' ' + 'Region Name: ' + sequence_region + '</p>'

                    content = main_page + "<h2>Information of the gene: " + gene.upper() + "</h2>" + content_id + content_length
                    content = content + content_start + content_end + content_chromo
        except KeyError:
            with open('error_parameter.html', 'r') as r:
                content = r.read()
        return content


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

    def gene_calculations(self, gene, main_page):
        try:
            id = self.id_genes(gene)
            info_client = self.client('''/sequence/id/''' + id + '''?content-type=application/json''')
            information = json.loads(info_client)
            sequence = information['seq']
            length = len(sequence)
            content_length = '<p>Length: ' + str(length) + '</p>'
            calc = self.seq_calculations(sequence)
            content_perc_1 = '<h4>Percentage of bases: </h4>' + '<p>A: ' + str(calc[0]) + '%</p>' + '<p>C: ' + str(calc[1]) + '%</p>'
            content_perc = content_perc_1 + '<p>G: ' + str(calc[2]) + '%</p>' + '<p>T: ' + str(calc[3]) + '%</p>'
            content = main_page + "<h2>Sequence of the gene: " + gene.upper() + "</h2>" + content_length + content_perc
        except KeyError:
            with open('error_parameter.html', 'r') as r:
                content = r.read()
        return content

    def genes_name(self, chromo, start, end, main_page):
        try:
            info_client = self.client('''/overlap/region/human/''' + chromo + ''':''' + start + '''-''' + end + '''?content-type=application/json;feature=gene;feature=transcript;feature=cds;feature=exon''')
            information = json.loads(info_client)
            content = main_page + "<h2>Name of the genes</h2>"
            count = 0
            if information == [] or 'error' in information:
                with open('error_parameter.html', 'r') as r:
                    content = r.read()
            else:
                for key_words in information:
                    count += 1
                    if key_words['feature_type'] == 'gene':
                        names = key_words['external_name']
                        gene_names = str(count) + '. ' + names
                        content += "<p>" + gene_names + "</p>"
        except KeyError:
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

        try:
            if self.path == '/':
                with open('index.html', 'r') as f:
                    contents = f.read()

            elif divide_msg[0] == '/listSpecies?limit':
                limit = divide_msg[1]
                contents = self.name_species(limit, main_page)

            elif divide_msg[0] == '/listSpecies':
                limit = ''
                contents = self.name_species(limit, main_page)

            elif divide_msg[0] == '/karyotype?specie':
                option_specie = divide_msg[1]
                contents = self.karyotype_species(option_specie, main_page)

            elif divide_msg[0] == '/chromosomeLength?specie':
                specie = divide_msg[1][:-7]
                chromo = divide_msg[2]
                contents = self.chromo_length(specie, chromo, main_page)

            elif divide_msg[0] == '/geneSeq?gene':
                gene = divide_msg[1]
                contents = self.gene_sequence(gene, main_page)

            elif divide_msg[0] == '/geneInfo?gene':
                gene = divide_msg[1]
                contents = self.gene_information(gene, main_page)

            elif divide_msg[0] == '/geneCalc?gene':
                gene = divide_msg[1]
                contents = self.gene_calculations(gene, main_page)

            elif divide_msg[0] == '/geneList?chromo':
                chromo = divide_msg[1][:-6]
                start = divide_msg[2][:-4]
                end = divide_msg[3]
                contents = self.genes_name(chromo, start, end, main_page)

            else:
                with open('error.html', 'r') as r:
                    contents = r.read()

        except IndexError:
            with open('error.html', 'r') as r:
                contents = r.read()

        self.send_response(200)
        self.send_header('Content Type', 'text/html')
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

