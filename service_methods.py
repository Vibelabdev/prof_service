import vk
import time
import json
from collections import Counter

from config import SERVICE_TOKEN


api = vk.API(access_token=SERVICE_TOKEN, v='5.131')


def get_user_info(link):
    user_id = api.utils.resolveScreenName(screen_name=link.split('/')[-1])['object_id']

    user_groups = api.users.getSubscriptions(user_id=user_id)['groups']['items']

    try:
        groups_info = api.groups.getById(group_ids=user_groups, fields=['activity'])
        groups_type = [el['activity'] for el in groups_info]
    except:
        groups_type = []

    user_interests = api.users.get(user_ids=user_id, fields=['interests'])[0].get('interests')

    time.sleep(1)

    try:
        wall_info = api.wall.get(owner_id=user_id)['items']
        wall_posts = [el['text'] for el in wall_info]
    except:
        wall_posts = None

    return {'user_groups': groups_type, 'user_interests': user_interests, 'wall_posts': wall_posts}


def define_activity_class(user_info):
    with open('group2class.json', 'r') as f:  # на основе нескольких тысяч пользователей составили список групп, которые встречаются чаще всего, но не более, чем у 80% людей
        group2class = json.load(f)

    # в дальнейшем хочется составить список тем групп, которые встречаются у большинства людей - от них избавляемся
    # темы групп будем определять с word2vec и рассчетом косинусного расстояния к группам  ('творчество', 'физическая деятельность', 'умственная деятельность')
    # возможно есть подход лучше


    groups = user_info['user_groups']

    counter = {key: item for key, item in Counter([group2class.get(el) for el in groups]).items() if
               key in ('творчество', 'физическая деятельность', 'умственная деятельность')}

    sum_values = sum([item for _, item in counter.items()])
    procent_counter = [[key, round(item / sum_values * 100, 1)] for key, item in counter.items()]

    class_percents = {key: item for key, item in procent_counter}
    return class_percents


def check_profile(link):
    user_info = get_user_info(link)  # получаем информацию из профиля
    class_percents = define_activity_class(user_info)  # анализируем склонность к видам деятельности

    return class_percents


def recommend_profession(class_percents, activity_level, team, health):
    recommends = []  # подберем то что нам подходит


    with open('professions_dataset.json', 'r') as f:
        professions_data = json.load(f)

    addiction = max(class_percents, key=lambda k: class_percents[k])
    for profession in professions_data.keys():
        if professions_data[profession]['activity_class'] == addiction and professions_data[profession]['activity_level'] == activity_level and professions_data[profession]['team'] == team:
            recommends.append(profession)

    return recommends


def get_recommends(link, activity_level, team, health='ok'):
    class_percents = check_profile(link)  # получаем класс интересов
    recommends = recommend_profession(class_percents, activity_level, team, health)

    return recommends
