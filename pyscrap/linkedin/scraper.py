import json

import requests
from bs4 import BeautifulSoup

from pyscrap import settings


def extracting_user_connection(connections: list) -> list:
    # somehow the first index is not the user connection so we start from index 1
    extraced = []
    for i in range(1, len(connections)):
        conn = connections[i]
        temp_data = {
            settings.MEMBER_DISTANCE  : conn.get(settings.MEMBER_DISTANCE).get(settings.MEMBER_DISTANCE_VALUE),
            settings.PUBLIC_IDENTIFIER: conn.get(settings.PUBLIC_IDENTIFIER),
            settings.FULL_NAME        : conn.get(settings.TITLE).get(settings.TITLE_USER_FULL_NAME),
        }
        extraced.append(temp_data)
    return extraced


def extracting_user_skills(included: list) -> list:
    # it is pretty weird actually
    skills = []
    for p in included:
        # criteria is based on organization
        if settings.SKILL_KEY in p and settings.SKILL_NAME:
            skills.append(p.get(settings.SKILL_NAME))
    return skills


def extracting_user_workplaces(included: list) -> list:
    # it is pretty weird actually
    workplaces = []
    for p in included:
        # criteria is based on organization
        if settings.COMPANY_NAME in p and settings.COMPANY:
            workplaces.append({
                settings.COMPANY     : p.get(settings.COMPANY),
                settings.COMPANY_NAME: p.get(settings.COMPANY_NAME),
                settings.TIME_PERIOD : p.get(settings.TIME_PERIOD),
            })
    return workplaces


def extracting_user_schools(included: list) -> list:
    # it is pretty weird actually
    schools = []
    for p in included:
        # criteria is based on organization
        if settings.SCHOOL_NAME in p and settings.FIELD_OF_STUDY:
            schools.append({
                settings.SCHOOL_NAME   : p.get(settings.SCHOOL_NAME),
                settings.FIELD_OF_STUDY: p.get(settings.FIELD_OF_STUDY),
                settings.DEGREE_NAME   : p.get(settings.DEGREE_NAME),
                settings.TIME_PERIOD   : p.get(settings.TIME_PERIOD),
            })
    return schools


def extracting_user_profile(included) -> dict:
    # it is pretty weird actually
    for p in included:
        # criteria is based on user profile
        if settings.FIRST_NAME in p and settings.LAST_NAME in p and settings.SUMMARY in p:
            return p


def get_target_user(code_tags: list) -> tuple:
    user_target = None
    profile_key = None
    for c in code_tags:
        try:
            deserialized = json.loads(c.string)
            data = deserialized.get(settings.DATA)
            included = deserialized.get(settings.INCLUDED)

            if included:
                user_target = extracting_user_profile(included)
                user_target[settings.SKILLS] = extracting_user_skills(included)
                user_target[settings.SCHOOLS] = extracting_user_schools(included)
                user_target[settings.WORKS] = extracting_user_workplaces(included)

            if data is not None and settings.PROFILE_KEY in data:
                profile_key = get_profile_key(data.get(settings.PROFILE_KEY))

            if user_target is not None and profile_key is not None:
                break
        except:
            pass

    return user_target, profile_key


def get_profile_key(profile: str) -> str:
    return profile.split(':')[3]


def find_connection_data(code_tags):
    for c in code_tags:
        try:
            deserialized = json.loads(c.string)
            data = deserialized.get(settings.DATA)
            if 'metadata' in data:
                return data
        except:
            pass


def scrap_connection(user_key: str, cookies: dict) -> list or None:
    current_page = 1
    full_connection = []
    for i in range(current_page, settings.MAX_PAGE):
        url = settings.SEARCH_URL.format(user_key=user_key, page=current_page)
        response = requests.get(url, cookies=cookies)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            code_tags = soup.find_all('code')
            data = find_connection_data(code_tags)
            try:
                el_lvl0 = data.get(settings.ELEMENTS)[1]
                full_connection += extracting_user_connection(el_lvl0.get(settings.ELEMENTS))
            except:
                pass
    return full_connection


def scrap_profile(linkedin_profile_url: str, cookies: dict) -> dict or None:
    response = requests.get(linkedin_profile_url, cookies=cookies)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        code_tags = soup.find_all('code')
        user_target, user_key = get_target_user(code_tags)
        return {
            'id'  : user_key,
            'data': user_target,
        }

    return None


def full_scrap(linkedin_profile_url: str, cookies: dict):
    userdata = scrap_profile(linkedin_profile_url, cookies)

    if userdata is None:
        raise Exception('404')
    userdata['connections'] = scrap_connection(userdata.get('id'), cookies)
    return userdata
