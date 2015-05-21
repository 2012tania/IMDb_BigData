# Standard Libs
import os
import json

# Extended Libs
import argparse
from bs4 import BeautifulSoup
import requests
import csv
import time


class IMDBFetcher():
    def __init__(self):
        # Initialization function

        self.imdb_base = "http://www.imdb.com/"
        self.name_id_base = self.imdb_base + "search/name"


    def fetch_name_ids(self):
        """This function fetches all the name ids starting from http://www.imdb.com/search/name?gender=male&start=1
        to http://www.imdb.com/search/name?gender=male&start=50001 for male celebrities
        and from http://www.imdb.com/search/name?gender=female&start=1
        to http://www.imdb.com/search/name?gender=female&start=50001 for female celebrities"""

        ids = []
        for i in range(2001, 2401, 50):
            if self.imdb_base != False:
                # r_url = self.name_id_base + "?gender=male&start=" + str(i)
                r_url = self.name_id_base + "?gender=female&start=" + str(i)
            else:
                print("URL not found! Exiting Program!")
                quit()
            r = requests.get(r_url)
            print(r_url)

            if not r.ok:
                print("Exiting Program!")
                return 0
            else:
                soup = BeautifulSoup(r.text)
                div1 = soup.find("div", {"id": "content-2-wide"})
                div2 = div1.find("div", {"id": "main"})
                table = div2.find("table", {"class": "results"})
                tr_text_divs = table.find_all("tr")

                for row in tr_text_divs[1:]:
                    td = row.find_all("td")[1]
                    ids.append(td.find("a")['href'])

        return ids

    def fetch_celeb_info(self, name_id=False):
        """This function fetches information of all celebrities whose ids have been collected
        It uses the http://www.imdb.com/name/name_id/bio?ref_=nm_ov_bio_sm links for biography
        It uses the http://www.imdb.com/name/name_id/?ref_=nmbio_bio_nm links for filmography"""

        if name_id != False:
            r_url = self.imdb_base + name_id + "bio"
            r_url1 = self.imdb_base + name_id
        else:
            print("URL not found! Exiting Program!")
            quit()
        r = requests.get(r_url)
        r1 = requests.get(r_url1)
        print(r_url)

        if not r.ok or not r1.ok:
            print("Exiting Program!")
            return 0
        else:
            # self.writer = csv.writer(open("male_celebs.txt", "a"), delimiter='\t', lineterminator='\n')
            self.writer = csv.writer(open("female_celebs.txt", "a"), delimiter='\t', lineterminator='\n')

            actors_info = []
            birth_date = ""
            birth_year = ""
            birth_location = ""
            descent = []
            movies = []

            l = len(name_id)

            soup = BeautifulSoup(r.text)

            div_name = soup.find("div", {"class": "parent"})
            name = div_name.find("a").contents
            print(name)

            div_bio = soup.find("div", {"id": "bio_content"})

            table = div_bio.find("table", {"class": "dataTable labelValueTable"})
            if table is not None:        # To handle links which do not have this information
                td_text_divs = table.find_all("tr")[0].find_all("td")[1].contents

                length = len(td_text_divs)
                print(length)
                if length >= 2:          # To handle links which do not have this information
                    birth_date = td_text_divs[1].string
                if length >= 4:         # To handle links which do not have this information
                    birth_year = td_text_divs[3].string
                if length >= 6:         # To handle links which do not have this information
                    birth_location = td_text_divs[5].string

            # Fetching part of the Mini Bio section to look for ethnicity keywords
            para = div_bio.find("p")
            if para is not None:        # To handle links which do not have this information
                para_text = para.text

                if "German" in para_text:
                    descent.append("German")
                if "Italian" in para_text:
                    descent.append("Italian")
                if "Russian" in para_text:
                    descent.append("Russian")
                if "Spanish" in para_text:
                    descent.append("Spanish")
                if "American" in para_text:
                    descent.append("American")
                if "African" in para_text:
                    descent.append("African")
                if "Latino" in para_text or "Latina" in para_text:
                    descent.append("Latino")
                if "Hispanic" in para_text:
                    descent.append("Hispanic")
                if "Indian" in para_text:
                    descent.append("Indian")
                if "Scottish" in para_text:
                    descent.append("Scottish")
                if "English" in para_text:
                    descent.append("English")
                if "Irish" in para_text:
                    descent.append("Irish")

            actors_info.extend([name_id[6:l - 1], str(", ".join(name)), birth_date, birth_year, birth_location,
                                str(", ".join(descent))])

            soup = BeautifulSoup(r1.text)
            div_bio = soup.find("div", {"class": "filmo-category-section"})
            div_titles = div_bio.find_all("div", {"id": True})
            if div_titles is not None:
                for div_title in div_titles:
                    movie = div_title['id']
                    print(movie)
                    movies.append(movie)

            actors_info.extend([str(", ".join(movies))])

            print(actors_info)
            self.writer.writerow(actors_info)
            return True


if __name__ == "__main__":
    # main function

    imdb = IMDBFetcher()
    name_ids = imdb.fetch_name_ids()            # Call to fetch name ids
    for name_id in name_ids:
        imdb.fetch_celeb_info(name_id)         # Call to fetch information for each name id fetched
        time.sleep(1)




    



