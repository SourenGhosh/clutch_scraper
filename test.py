
# import requests
# import pandas as pd
# from operator import itemgetter
# from bs4 import BeautifulSoup as bs
# with requests.session() as s:
#     soup = bs(s.post(base_url).content, "html.parser")
#     links = soup.find_all("li", attrs={"class": "provider provider-row sponsor"})
#     for link in links:
#         name = link.find("a", attrs={"data-link_text": "Profile Title"})
#         company_url = link.find("a", attrs={"class": "website-link__item"})
#         locality = link.find("span", attrs={"class": "locality"})
#         rating = link.find("span", attrs={"class": "rating sg-rating__number"})
#         rating_count = link.find('a', attrs={'data-link_text': "Reviews Count"})
#         hourly_rate = link.find('div', attrs={'data-content': "<i>Avg. hourly rate</i>"}).find('span')
#         min_project_size = link.find('div', attrs={'data-content': "<i>Min. project size</i>"}).find('span')
#         employee_size = link.find('div', attrs={'data-content': "<i>Employees</i>"}).find('span')
#         details_url = f"https://clutch.co/profile/{name.text.strip().lower()}/#summary"
#         company_dt_soup = bs(s.post(details_url).content, "html.parser")
        
#         contact = company_dt_soup.find_all("h3", attrs={"class": "error-type"})

    
#     print(name.text.strip())
#     print(company_url['href'])
#     print(locality.text.strip())
#     print(rating.text.strip())
#     print(rating_count.text.strip())
#     print(hourly_rate.text.strip())
#     print(min_project_size.text.strip())
#     print(employee_size.text.strip())
#     print(details_url)
#     print(contact)