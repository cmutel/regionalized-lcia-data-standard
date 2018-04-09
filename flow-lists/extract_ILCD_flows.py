from lxml import objectify
import argparse
import csv
import os


_ = lambda x: x if x else ''


def parse_file(dirpath, output_dir):
    data = []
    assert os.path.isdir(dirpath)

    for fp in filter(lambda x: x.endswith(".xml"), os.listdir(dirpath)):
        try:
            root = objectify.parse(open(os.path.join(dirpath, fp), encoding='utf-8')).getroot()
            data.append({
                'id': root.xpath('//*[local-name() = "UUID"]')[0],
                'name': root.flowInformation.dataSetInformation.name.baseName.text,
                'unit': None,
                'compartment': (root.xpath('//*[@level = "1"]') or [None])[0],
                'subcompartment': (root.xpath('//*[@level = "2"]') or [None])[0],
                'CAS number': (root.xpath('//*[local-name() = "CASNumber"]') or [None])[0]
            })
        except:
            print(fp)
            raise

    data.sort(key=lambda x: (x['name'], _(x['compartment']), _(x['subcompartment'])))

    header = ['id', 'name', 'unit', 'compartment', 'subcompartment', 'CAS number']
    with open('elcd-flows.csv', 'w', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header)
        writer.writeheader()
        writer.writerows(data)


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    parser = argparse.ArgumentParser(
        description='Extract flow list from `flows` directory')
    parser.add_argument('dirpath', type=str, help='File path of flows directory')

    args = parser.parse_args()
    parse_file(args.dirpath, here)
