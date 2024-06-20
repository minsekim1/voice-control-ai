import sys
import webbrowser

if len(sys.argv) > 1:  # 명령 줄 인자가 제공되었는지 확인
		search_query = sys.argv[1]  # 첫 번째 인자를 검색 쿼리로 사용
		base_url = "https://www.youtube.com/results?search_query="
		search_url = f"{base_url}{search_query}"
		webbrowser.open(search_url)
else:
		print("Please provide a search term. Usage: python 유튜브/검색.py \"search term\"")
