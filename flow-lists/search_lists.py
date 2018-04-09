import csv
import json
import argparse


def search_list(term, filepath):
    data = []
    with open(filepath, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if term in row['name'].lower():
                data.append({
                    'name': row['name'],
                    'id': row['id'],
                    'archetypes': [row['compartment'], row['subcompartment']],
                    'unit': row['unit'] or None
                })
    return data


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Search flows lists for terms')
    parser.add_argument('term', type=str, help='Term to search for')

    args = parser.parse_args()
    print(json.dumps({
        'ecoinvent': search_list(args.term.lower(), "ecoinvent-flows.csv"),
        'ELCD': search_list(args.term.lower(), "elcd-flows.csv"),
    }, indent=2))
