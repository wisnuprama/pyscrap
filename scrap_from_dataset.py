import json
from time import sleep
from csv import DictReader
from pyscrap import deserialize_cookies, serialize_to_csv
from pyscrap.linkedin import full_scrap

NPM = 'NPM'
NAMA = 'Nama'
USERNAME = 'Username'


if __name__ == '__main__':
    cookies = deserialize_cookies('../cookies.json')
    total = 1
    list_scraped = []
    with open('../dataset.csv') as dataset:
        input_file = DictReader(f=dataset, fieldnames=(NPM, NAMA, USERNAME))

        for mhs in input_file:
            mhs_data = f'{mhs.get(NPM)} {mhs.get(NAMA)}'
            try:
                if mhs.get(USERNAME):
                    mhs_username = str(mhs.get(USERNAME)).strip()
                    url = f'https://www.linkedin.com/in/{mhs_username}/'
                    result = full_scrap(url, cookies)
                    if result:
                        cleaned = dict()
                        cleaned['publicIdentifier'] = mhs_username
                        cleaned['id'] = result['id']
                        cleaned['connections'] = result['connections']
                        user_fields = ('firstName', 'lastName', 'locationName',
                                    'birthDate', 'skills', 'schools', 'works',)
                        for f in user_fields:
                            cleaned[f] = result.get('data')[f]
                        list_scraped.append(cleaned)
                        print('(Success)', total, mhs_data)
                        total += 1
                else:
                    print('(Skip)', total, mhs_data)
            except Exception as e:
                print('(Failed)', total, mhs_data, e)
                continue

    with open('../result.json', 'w') as json_file:
        json.dump(list_scraped, fp=json_file)
        print('Complete!', total)