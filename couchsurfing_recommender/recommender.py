from couchsurfing import *
import json
import time


def get_place_options(destination):
    path = f'/api/v4/autocomplete?type=place&search_text={destination}'
    response = json.loads(make_request(path).decode('utf-8'))

    for r in response:
        r['hosts_url'] = f'/api/v4/users/search?bbox={r["coordinates"]["bbox"]}&latLng={r["coordinates"]["lat"]},{r["coordinates"]["lng"]}&radius=10&couchStatus=yes,maybe,hang&minGuestsWelcome=1'

    places = []
    for i,r in enumerate(response):
        place = {}
        place['id'] = i+1
        place['name'] = r['name']
        place['url'] = r['hosts_url']
        places.append(place)

    return places


def scrape_profile_ids(destination, amount, url, per_page=50, min_age=None, max_age=None, keyword=None):
    profile_counter = 0
    page_counter = 1
    
    while True:
        time.sleep(4)
        print(f'Downloading page {page_counter}...')
        page_path = url + f'&perPage={per_page}&page={page_counter}'
        
        if min_age != None:
            page_path += f'&minAge={min_age}'
        if max_age != None:
            page_path += f'&maxAge={max_age}'
        if keyword != None:
            page_path += f'&keyword={keyword}'
        
        data = make_request(page_path)
        jdata = json.loads(data)

        hosts = jdata['results']
        for host in hosts:
            with open(f'./data/{destination}_ids.txt', 'a') as f:
                f.write(host['id'])
                f.write('\n')
                
                profile_counter += 1
                if profile_counter == amount:
                    return
                
        if len(hosts) < per_page:
            return
        
        else:
            page_counter += 1


def get_profile_media(user_id):
    jdata = get_profile_data(user_id)
    
    details = {}
    details['id'] = jdata['id']
    # details['publicName'] = jdata['publicName']
    # details['city'] = jdata['publicAddress']['description']
    details['media'] = jdata['about']['media']

    return details


def already_downloaded(data_file, id):
    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            file_data = json.load(f)
        
        for person in file_data:
            if id == person['id']:
                return True
            
        return False
    
    except FileNotFoundError:
        return False


def scrape_profiles(destination):
    id_file = f'./data/{destination}_ids.txt'
    data_file = f'./data/{destination}_data.json'
    error_file = './errors.txt'

    with open(id_file, 'r') as f:
        for id in f.read().splitlines():
            if already_downloaded(data_file, id):
                print(f'Already downloaded {id}')
                continue

            else:
                time.sleep(1)
                print(f'Downloading {id}...')

                try:
                    with open(data_file, 'r', encoding='utf-8') as f:
                        file_data = json.load(f)
                except FileNotFoundError:
                    file_data = []

                try:
                    user_data = get_profile_media(id)
                    if user_data['media'] == None or user_data['media'] == "":
                        continue
                    file_data.append(user_data)
                    
                    with open(data_file, 'w', encoding='utf-8') as f:
                        file_data = json.dump(file_data, f, ensure_ascii=False)

                except:
                    with open(error_file, 'a') as f:
                        f.write(id)
                        f.write('\n')
                    print(f'[!] Error: {id}')


def main():
    destination = input('Enter city: ')
    amount_to_scrape = 50

    options = get_place_options(destination)
    for option in options:
        print(f"{option['id']} - {option['name']}")

    user_option = int(input('Enter option: '))
    url = [o['url'] for o in options if o['id'] == user_option][0]

    min_age = None
    max_age = None
    keyword = None

    destination = destination.replace(' ', '_')
    scrape_profile_ids(destination, amount_to_scrape, url, min_age=min_age, max_age=max_age, keyword=keyword)
    scrape_profiles(destination)


main()
