from bs4 import BeautifulSoup
import requests

l = ['https://tlgrm.ru/channels/news', 'https://tlgrm.ru/channels/blogs', 'https://tlgrm.ru/channels/tech', 'https://tlgrm.ru/channels/entertainment', 'https://tlgrm.ru/channels/economics', 'https://tlgrm.ru/channels/finance', 'https://tlgrm.ru/channels/crypto', 'https://tlgrm.ru/channels/education', 'https://tlgrm.ru/channels/music', 'https://tlgrm.ru/channels/language', 'https://tlgrm.ru/channels/business', 'https://tlgrm.ru/channels/psychology', 'https://tlgrm.ru/channels/video', 'https://tlgrm.ru/channels/books', 'https://tlgrm.ru/channels/fitness', 'https://tlgrm.ru/channels/travel', 'https://tlgrm.ru/channels/art', 'https://tlgrm.ru/channels/beauty', 'https://tlgrm.ru/channels/health', 'https://tlgrm.ru/channels/gaming', 'https://tlgrm.ru/channels/food', 'https://tlgrm.ru/channels/quotes', 'https://tlgrm.ru/channels/handicraft', 'https://tlgrm.ru/channels/adult', 'https://tlgrm.ru/channels/other']

for j in l:
    print(j)
    url = j
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "lxml")
    str_1 = soup.find_all('div', class_='channel-card')
    for i in str_1:
        file = open('channels.txt', 'a')
        str_2 = i.find('div', class_='channel-card__meta')
        str_3 = str_2.find('a', class_='channel-card__username')
        file.write(str_3.get('href') + '\n')
        file.close
