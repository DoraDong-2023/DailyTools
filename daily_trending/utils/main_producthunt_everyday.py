import requests
import json
from datetime import datetime
import os

def get_product_hunt_posts():
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Host": "api.producthunt.com",
        "Authorization": "Bearer fAQmZObHaIglLCloDm1ZhWu7vwv4YGmyCJUD9YhcWJw",
        "User-Agent": "PostmanRuntime/7.28.4"
    }
    url = "https://api.producthunt.com/v1/posts"
    response = requests.get(url, headers=headers)
    data = response.json()
    data['date'] = datetime.now().strftime('%Y-%m-%d')
    return data

def get_hacker_news():
    url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    response = requests.get(url)
    top_stories = response.json()
    top_stories_info = []
    for story_id in top_stories[:5]:
        story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
        story_info = requests.get(story_url).json()
        story_info['date'] = datetime.now().strftime('%Y-%m-%d')
        top_stories_info.append(story_info)
    return top_stories_info

def get_stack_overflow():
    url = "https://api.stackexchange.com/2.3/questions?order=desc&sort=activity&site=stackoverflow"
    response = requests.get(url)
    data = response.json()['items']
    for item in data:
        item['date'] = datetime.now().strftime('%Y-%m-%d')
    return data

if not os.path.exists('./data/data_trending'):
    os.makedirs('./data/data_trending')

product_hunt_data = get_product_hunt_posts()
with open('./data/data_trending/product_hunt_trending.json', 'w') as f:
    json.dump(product_hunt_data, f, indent=4)

hacker_news_data = get_hacker_news()
with open('./data/data_trending/hacker_news_trending.json', 'w') as f:
    json.dump(hacker_news_data, f, indent=4)

stack_overflow_data = get_stack_overflow()
with open('./data/data_trending/stack_overflow_trending.json', 'w') as f:
    json.dump(stack_overflow_data, f, indent=4)
