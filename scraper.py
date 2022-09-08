import requests
from bs4 import BeautifulSoup as bs

base_url = "https://clutch.co/directory/mobile-application-developers"



with requests.session() as s:
    soup = bs(s.post(base_url).content, "html.parser")
    links = soup.find_all("li", attrs={"class": "provider provider-row sponsor"})
    for link in links:
        name = link.find("a", attrs={"data-link_text": "Profile Title"})
    print(name.text.strip())