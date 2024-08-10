import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

def get_pinterest_links(href):
    url = "https://www.pinterest.com" + href
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
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html5lib')

    # Tìm kiếm comment_count
    comment_count = soup.find("h2", {'class': 'lH1 dyH iFc H2s bwj X8m zDA IZT'})
    comment_count = comment_count.text if comment_count else 'Comments not found'
    
    # Tìm kiếm author
    author = soup.find('div', {'class': 'tBJ dyH iFc sAJ X8m zDA IZT H2s'})
    if author is None:
        author = soup.find('div', {'class': 'tBJ dyH iFc j1A X8m zDA IZT H2s'})
    author = author.text if author else 'Author not found'
    
    # Tìm kiếm follower
    follower = soup.find('div', {'data-test-id': 'user-follower-count'})
    if follower is not None:
        followers = follower.find('div', {'class': 'tBJ dyH iFc sAJ X8m zDA IZT swG'})
        followers_text = followers.get_text(strip=True) if followers else 'Followers not found'
    else:
        follower = soup.find('div', {'data-test-id': 'follower-count'})
        followers_text = follower.find('div', class_='tBJ dyH iFc j1A X8m zDA IZT swG').text.split()[0]
    
    content = soup.find('div', {'class': 'XiG ujU zI7 iyn Hsu'}, {'data-test-id':'truncated-description'})
    if content is None:
        content = "None"
    else:
        content = content.text

    return author, followers_text, comment_count, content

def process_row(row):
    author, follower, comment_count, content = get_pinterest_links(row['href'])
    return {
        'name': row['name'],
        'url': row['url'],
        'href': row['href'],
        'author': author,
        'comment_count': comment_count,
        'follower': follower,
        'content': content 
    }

def main():
    data = pd.read_csv('data.csv', header=None, names=['name', 'url', 'href'])
    results = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(process_row, row) for _, row in data.iterrows()]
        
        for future in tqdm(as_completed(futures), total=len(futures), desc="Processing"):
            try:
                result = future.result()
                if result is not None:
                    results.append(result)
            except Exception as e:
                # print(f"Error processing future: {e}")
                pass
    
    results_df = pd.DataFrame(results)
    file_exists = os.path.isfile('anime2.csv')
    
    results_df.to_csv('anime2.csv', mode='a', index=False, header=not file_exists)

if __name__ == "__main__":
    main()
