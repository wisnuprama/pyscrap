import os

from commandlines import Command

from pyscrap import deserialize_cookies, serialize_to_csv
from pyscrap.linkedin import scrap_profile, full_scrap


def getdef(c, key):
    try:
        return c.get_definition(key)
    except Exception:
        return c.get_default(key)


if __name__ == '__main__':
    default_args = {
        'save'   : os.getcwd(),
        'action' : '',
        'url'    : '',
        'cookies': '',
    }

    c = Command()
    c.set_defaults(default_args)

    # scrap action
    action = getdef(c, 'action')
    # url to be scraped
    url = getdef(c, 'url')
    # cookies path
    cookies_path = getdef(c, 'cookies')
    # save path
    save_path = getdef(c, 'save')

    cookies = deserialize_cookies(cookies_path)
    result = None
    if action == 'profile':
        result = scrap_profile(url, cookies)
    elif action == 'full':
        result = full_scrap(url, cookies)

    if result:
        cleaned = dict()
        cleaned['id'] = result['id']
        cleaned['connections'] = result['connections']
        user_fields = ('firstName', 'lastName', 'locationName', 'birthDate', 'skills', 'schools', 'works',)
        for f in user_fields:
            cleaned[f] = result.get('data')[f]
        print(cleaned)
        serialize_to_csv(save_path, cleaned)
