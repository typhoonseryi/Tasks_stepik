import requests
from datetime import datetime as dt

ACCESS_TOKEN = 'f5a1b4f4f5a1b4f4f5a1b4f4ccf5d2ecd7ff5a1f5a1b4f4aa8b186c4ce92adf4fdf4207'
current_date = dt.now()
current_year = current_date.year

def calc_age(uid):
    bdate_list = []
    years = []
    age_list =[]
    age_tuples = []
    payload_user = {'access_token' : ACCESS_TOKEN, 'user_ids' : uid, 'v' : '5.71'}
    res_user = requests.get('https://api.vk.com/method/users.get', params=payload_user)
    data_user = res_user.json()
    user_id = data_user['response'][0]['id']
    payload_friends = {'access_token' : ACCESS_TOKEN, 'user_id' : user_id, 'v' : '5.71', 'fields' : 'bdate'}
    res_friends = requests.get('https://api.vk.com/method/friends.get', params=payload_friends)
    data_friends = res_friends.json()
    friends = data_friends['response']['items']
    for friend in friends:
        try:
            bdate_list.append(friend['bdate'])
        except KeyError:
            pass
    for bdate_str in bdate_list:
        bdate = bdate_str.split('.')
        if len(bdate) == 3:
            years.append(bdate[2])
    for year in years:
        age_list.append(current_year-int(year))
    unique_ages = set(age_list)
    for unique_age in unique_ages:
        count = age_list.count(unique_age)
        age_tuples.append((unique_age, count))
        age_tuples.sort(key=lambda age: age[1], reverse=True)
    return age_tuples


if __name__ == '__main__':
    res = calc_age('shuktomov97')
    print(res)