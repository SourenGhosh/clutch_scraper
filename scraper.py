import requests
import pandas as pd
from operator import itemgetter
from bs4 import BeautifulSoup as bs
from webdriver import get_service_location, find_firm_contact


BASE_URL = "https://clutch.co"
base_url = "https://clutch.co/directory/mobile-application-developers?page=1"

class BaseScraper(object):
    def __init__(self, base_url, *args, **kwargs):
        self.base_url = base_url

    def soup_base_session(self, url):
        with requests.session() as s:
            soup = bs(s.post(url).content, "html.parser")
        return soup

    @property
    def clutch_list_of_services(self):
        services = list()
        soup_obj = self.soup_base_session(self.base_url)
        links = soup_obj.find_all("a", attrs={"class": "facets_list__item"})
        for link in links:
            service = link.find("span", attrs={"class": "facets_list__item__name"}).find('span', attrs={
                "class": "name"
            })
            service_data_url = link.find("input")
            services.append(
                {
                    'service_name': service.text.strip(),
                    'data_url': service_data_url['data-url']
                } 
            )
        df = pd.DataFrame.from_dict(services)
        df.to_csv('clutch_services.csv')
        return services
    
    

    def get_last_page(self, data_url):
        url = "%s%s" %(self.base_url, data_url)
        soup_obj = self.soup_base_session(url)
        link = soup_obj.find("li", attrs={"class": "page-item last"}).find('a')
        last_data_page = link['data-page']
        return last_data_page

    def get_available_location(self, service):
        return get_service_location(self.base_url, service)
    

    def dump_availale_service_location(self):
        data_list = dict()
        for service in self.clutch_list_of_services:
            data_list.update(
                {
                    service['service_name']: list( map(itemgetter(0), self.get_available_location(service['service_name']) ))
                }
            )
            print(data_list)
        df = pd.DataFrame(data_list)
        df.to_csv('service_with_available.csv')
        print(data_list)         
    
    def find_service_data_url(self, service_name):
        service_data_url = None
        for service in self.clutch_list_of_services:
            if service['service_name'] == service_name:
                service_data_url = service['data_url']
        return service_data_url

    def get_location_id_from_name(self, location_name, service_name):
        data = self.get_available_location(service_name)
        loc_id=None
        print(".................", list(data))
        datas=list(data)
        for d in datas:
            print(d)
            if location_name in d[0]:
                loc_id = d[1]
        print(loc_id)
        return loc_id




    def scrape_data(self, service_name, location=None, page_no=False):
        service_data_url = self.find_service_data_url(service_name)
        service_last_page = self.get_last_page(service_data_url)
        dump_file = f"{service_name}.csv"

        if service_data_url is None:
            raise Exception("No data Url found for the service name")
        base_service_url = f"{self.base_url}{service_data_url}"

        if location is not None:
            #loc_id = self.get_location_id_from_name(location[1])
            base_service_url = f"{self.base_service_url}{service_data_url}?geona_id={location[1]}"
            dump_file = f"{dump_file}_{location[0].split(',')[0]}"

        if page_no:
            last_page=service_last_page
        else:
            last_page=4
        data_list = list()
        for page in range(last_page):
            service_url = f"{base_service_url}?page={page}"
            soup_obj = self.soup_base_session(service_url)
            links = soup_obj.find_all("li", attrs={"class": "provider provider-row sponsor"})
            for link in links:
                name = link.find("a", attrs={"data-link_text": "Profile Title"})
                company_url = link.find("a", attrs={"class": "website-link__item"})
                locality = link.find("span", attrs={"class": "locality"})
                rating = link.find("span", attrs={"class": "rating sg-rating__number"})
                rating_count = link.find('a', attrs={'data-link_text': "Reviews Count"})
                hourly_rate = link.find('div', attrs={'data-content': "<i>Avg. hourly rate</i>"}).find('span')
                min_project_size = link.find('div', attrs={'data-content': "<i>Min. project size</i>"}).find('span')
                employee_size = link.find('div', attrs={'data-content': "<i>Employees</i>"}).find('span')
                company_data_url = name['href']
                profile_url = f"{self.base_url}{company_data_url}#summary"
                print(profile_url)
                contact_no = find_firm_contact(profile_url)

                print(contact_no)

                data_list.append(
                    {
                        "name": name.text.strip(),
                        "company_url": company_url['href'],
                        "locality": locality.text.strip(),
                        "rating": rating.text.strip(),
                        "hourly_rate": hourly_rate.text.strip(),
                        "min_project_size": min_project_size.text.strip(),
                        "employee_size": employee_size.text.strip(),
                        "contact": contact_no
                    }
                )
        df = pd.DataFrame.from_dict(data_list)
        df.to_csv(dump_file)









if __name__=="__main__":
    base_obj = BaseScraper(BASE_URL)
    services = base_obj.clutch_list_of_services
    #base_obj.dump_availale_service_location()
    
    for service in services[:2]:
        last_page = base_obj.get_last_page(service['data_url'])
        base_obj.scrape_data(service['service_name'])
        #Scrape data location wise and page_wise
        '''
        for service in services:
            last_page = base_obj.get_last_page(service['data_url'])
            base_obj.scrape_data(service['service_name'])
            available_locs = base_obj.get_available_location(service)
            for location in available_locs:
                base_obj.scrape_data(service['service_name'], location, last_page)
        '''

    #base_obj.scrape_data('Mobile App Development')
