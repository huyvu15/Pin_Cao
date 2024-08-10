import requests
from bs4 import BeautifulSoup

def get_pinterest_links(url):
    headers = {
    'accept': 'application/json, text/javascript, */*, q=0.01',
    'accept-language': 'en-US,en;q=0.9',
    'priority': 'u=1, i',
    'referer': 'https://www.pinterest.com/',
    'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
    'sec-ch-ua-full-version-list': '"Not)A;Brand";v="99.0.0.0", "Google Chrome";v="127.0.6533.89", "Chromium";v="127.0.6533.89"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-platform': '"Windows"',
    'sec-ch-ua-platform-version': '"12.0.0"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    'x-app-version': 'f4e841d',
    'x-pinterest-appstate': 'background',
    'x-pinterest-pws-handler': 'www/pin/[id].js',
    'x-pinterest-source-url': '/pin/1970393580411909/',
    'x-requested-with': 'XMLHttpRequest',
}
    
    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'html5lib')
    
    
    with open('soup.txt', 'w', encoding='utf-8') as f:
        f.write(str(soup))
    

    comment_count = soup.find("h2", {'class': 'lH1 dyH iFc H2s bwj X8m zDA IZT'}).text
    
    
    # author = soup.find('div', {'class': 'tBJ dyH iFc sAJ X8m zDA IZT H2s'}, {'dataset_id': 'creator-profile-name'}).text
    # author = soup.find('div', {'class': 'tBJ dyH iFc j1A X8m zDA IZT H2s'}, {'dataset_id': 'creator-profile-name'}).text
    author = soup.find('div', {'class': 'tBJ dyH iFc sAJ X8m zDA IZT H2s'}, {'dataset_id': 'creator-profile-name'})
    if author is None:
        author = soup.find('div', {'class': 'tBJ dyH iFc j1A X8m zDA IZT H2s'}, {'dataset_id': 'creator-profile-name'})
    if author is not None:
        author = author.text


    # with open('ele.txt', 'w', encoding='utf-8') as f:
    #     f.write(str(elements))
    
    follower = soup.find('div', {'data-test-id': 'user-follower-count'})

    if follower is not None:
        followers = follower.find('div', {'class': 'tBJ dyH iFc sAJ X8m zDA IZT swG'})
        followers_text = followers.get_text(strip=True) if followers else 'Followers not found'
        print(followers_text)  
    else:
        # follower = soup.find('div', {'data-test-id': 'follower-count'}, {'class':'tBJ dyH iFc sAJ X8m zDA IZT swG'}).text.split()[0]
        follower = soup.find('div', {'data-test-id': 'follower-count'})
        follower = follower.find('div', class_='tBJ dyH iFc j1A X8m zDA IZT swG').text.split()[0]
        print(follower)
    

    # follower = soup.find('div', {'data-test-id': 'follower-count'}, {'class':'tBJ dyH iFc sAJ X8m zDA IZT swG'}).text
    # print(follower)
    
    content = soup.find('div', {'class': 'XiG ujU zI7 iyn Hsu'}, {'data-test-id':'truncated-description'}).text
    print(content)

    # print(follow)
    print(comment_count)
    print(author)


# url = 'https://www.pinterest.com/pin/281543723702517/'
# url = 'https://www.pinterest.com/pin/1548181168890509/'
# url = 'https://www.pinterest.com/pin/1759287347092746/'

# url1 = 'https://www.pinterest.com/pin/70437488764288/'

url = 'https://www.pinterest.com/pin/2744449752317432/'
url1 = 'https://www.pinterest.com/pin/347340190028141759/'

pin_links = get_pinterest_links(url1)
# pin_links = get_pinterest_links(url1)


