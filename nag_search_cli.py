import requests
import json
import sys
from secrets import KEYS, generateURL

FILE = str(sys.argv[1])


class Search:

    MATCHES = []
    NO_MATHCES = []
    
    """Method that allow user to search for host or service"""

    def search_host(self, search_term_host):
        match_count = 0
        print(f'Searching for {search_term_host}')
        for nag, key in KEYS.items():
            nagios_data = requests.get(
                generateURL(nag) + search_term_host+'&apikey='+key).json()
            hosts_count = nagios_data['recordcount']
            '''
            When more than one result is found, Nagios API returns a list. 
            '''
            if int(hosts_count) == 0:
                pass
            elif type(nagios_data['hoststatus']) == list:
                # Get the initial results
                for host in nagios_data['hoststatus']:
                    # Search through  the initial matches for exact matches
                    if search_term_host in host['display_name']:
                        Search.MATCHES.append({
                            "Host": host['display_name'],
                            "Environment": nag
                        })
                match_count += 1
            else:
                '''
                When just 1 result is found, Nagios API returns a dictionary. 
                '''
                Search.MATCHES.append({
                    "Host": nagios_data['hoststatus']['display_name'],
                    "Environment": nag
                })
                match_count += 1

        if match_count == 0:
            Search.NO_MATHCES.append({
                "Host": search_term_host,
            })
        else:
            pass

        # Write the results to text files
        with open('In_Nagios.txt', 'w') as doc:
            for match in Search.MATCHES:
                doc.write(match['Host'] + "\n")

        with open('Not_In_Nagios.txt', 'w') as doc:
            for hosts in Search.NO_MATHCES:
                doc.write(hosts['Host'] + "\n")


search = Search()


# Run the search_host method on hosts from file that user supplies.
with open(FILE, 'r') as doc:
    for line in doc:
        stripped_line = line.strip()
        search.search_host(stripped_line)
