import requests
from bs4 import BeautifulSoup
import os

# Search query

def get_menu(restaurant_name, location):

    query = f"{restaurant_name} {location} menu allmenus"

    # Google search URL
    google_url = f"https://www.google.com/search?q={query}"

    # Send GET request to Google search URL
    response = requests.get(google_url)

    # Parse response HTML with BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the first search result link
    search_results = soup.find_all("a")
    first_link = None
    for link in search_results:
        url = link.get("href")
        if url.startswith("/url?q="):
            first_link = url.split("/url?q=")[1]
            break

    # Send GET request to first search result URL
    if first_link:
        response = requests.get(first_link)

        # Parse response HTML with BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Print the page HTML
        # print(soup.prettify())
        with open('out.text', 'w') as f:
            f.write(soup.prettify())

    menus = "\"@type\": \"Menu\""
    sec = "\"@type\": \"MenuSection\""
    item = "\"@type\": \"MenuItem\""
    description = "\"description\":"
    price = "\"Price\":"

    ct = 0
    menu = dict()
    cursec = []
    cur = ""
    getsec = False
    getitem = False
    curitem = []
    with open('out.text', 'r') as f:
        for l_no, line in enumerate(f):
            # search string

            if menus in line:
                ct = 1
            if ct == 0:
                continue
            if ct<0:
                break
            if '{' in line:
                ct += 1
            if '}' in line:
                ct -= 1
            if getsec:
                # print(line)
                if len(cur) > 1 and len(cursec) > 0:
                    menu[cur] = cursec
                cur = line.split('name": "')[1].split('",')[0]
                cursec = []
                getsec = False
            if sec in line:
                getsec = True
            
            if getitem:
                curitem.append(line.split('name": "')[1].split('",')[0])
                getitem = False
            if item in line:
                if len(curitem) == 3:
                    cursec.append(curitem)
                curitem = []
                getitem = True
            if description in line:
                if len(curitem) ==1:
                    curitem.append(line.split('description": "')[1].split('",')[0])
            if price in line:
                # print(line)
                curitem.append(line.split('Price": "')[1].split('",')[0])
                
            

    os.remove('out.text')
    return menu






