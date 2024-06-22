import sys
import requests
import json
from bs4 import BeautifulSoup

def search_lyrics(query):
    url = "https://m.search.naver.com/p/csearch/content/qapirender.nhn"
    params = {
        "where": "nexearch",
        "key": "LyricsSearchResult",
        "pkid": 519,
        "u1": 1,
        "u2": 5,
        "u3": 0,
        "u4": 0,
        "q": "가사검색 " + query
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        json_data = response.json()
        return json_data
    else:
        print(f"Error fetching data: {response.status_code}")
        return None

def extract_song_titles(json_data):
    if not json_data or 'current' not in json_data or 'html' not in json_data['current']:
        return []

    html_content = json_data['current']['html']
    soup = BeautifulSoup(html_content, 'html.parser')

    song_titles = set()  # 중복 제거를 위한 set 사용
    for strong_tag in soup.find_all('strong', class_='music_title'):
        a_tag = strong_tag.find('a')
        if a_tag:
            song_titles.add(a_tag.text.strip())  # set에 추가

    return list(song_titles)  # 다시 리스트로 변환하여 반환

if __name__ == "__main__":
    if len(sys.argv) > 1:
        query = sys.argv[1]
        json_data = search_lyrics(query)
        if json_data:
            song_titles = extract_song_titles(json_data)
            if song_titles:
                print("Found song titles:")
                for idx, title in enumerate(song_titles, start=1):
                    print(f"#{idx}. {title}")
            else:
                print("No song titles found.")
        else:
            print("No data found for the given query.")
    else:
        print("가사를 문장으로 제공해주세요. 예: 두 눈을 감아도 통 잠은 안오고")
