from epo_ops import Client
from epo_ops.models import Docdb
import xml.etree.ElementTree as ET
import json
import argparse


def retrieve(client, publication_number,country_code, kind_code):
    response = client.published_data(
        reference_type='publication',  
        input=Docdb(publication_number, country_code, kind_code), 
        endpoint='claims', 
    )
    xml_data = response.text

    root = ET.fromstring(xml_data)
    namespaces = {'ftxt': 'http://www.epo.org/fulltext'} 

    english_claims = root.findall('.//ftxt:claims[@lang="EN"]/ftxt:claim/ftxt:claim-text', namespaces)

    en = ""
    for claim in english_claims:
        en += claim.text + " "
        
    return en


if __name__=='__main__':

    parser = argparse.ArgumentParser(description="retrieve data")
    parser.add_argument("--key", type=str, default=None) 
    parser.add_argument("--secret", type=str, default=None) 
    args = parser.parse_args()
    
    client = Client(
        key=args.key,
        secret=args.secret,

    )
    
    publication_number = "EP3713101"
    country_code = publication_number[:2]
    number = publication_number[2:]
    kind_code = 'B1'
    
    published_claim = retrieve(client, number, country_code, kind_code)
    print(published_claim)
    
    try:
        draft_claim = retrieve(client, number, country_code, 'A1')
    except:
        print("A1 not found")
        try: 
            draft_claim = retrieve(client, number, country_code, 'A2')
        except:
            print("A2 not found")
            print(number)
    print(draft_claim)
    

        
