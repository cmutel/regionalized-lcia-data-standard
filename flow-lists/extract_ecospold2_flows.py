from lxml import objectify
import argparse
import csv
import os


def get_cas(node):
    try:
        return node.get('casNumber')
    except AttributeError:
        return None


def parse_file(filepath, output_dir):
    data = []
    assert os.path.isfile(filepath)
    root = objectify.parse(open(filepath, encoding='utf-8')).getroot()
    for dataset in root.iterchildren():
        data.append({
            'id': dataset.get('id'),
            'name': dataset.name,
            'unit': dataset.unitName,
            'compartment': dataset.compartment.compartment,
            'subcompartment': dataset.compartment.subcompartment,
            'CAS number': get_cas(dataset)
        })

    data.sort(key=lambda x: (x['name'], x['compartment'], x['subcompartment']))

    header = ['id', 'name', 'unit', 'compartment', 'subcompartment', 'CAS number']
    with open('ecoinvent-flows.csv', 'w', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header)
        writer.writeheader()
        writer.writerows(data)


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    parser = argparse.ArgumentParser(
        description='Extract flow list from ElementaryExchanges.xml` file')
    parser.add_argument('filepath', type=str, help='File path of ElemntaryExchanges file')

    args = parser.parse_args()
    parse_file(args.filepath, here)
