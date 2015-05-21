# IMDb_Project
Project for IMDb Data Scraping


The code has been written in Python 3.0. I have used the Python package BeautifulSoup which parses XML and HTML data in order to facilitate data extraction.


Function init
This function initializes the following
•	IMDb base URL to http://www.imdb.com/
•	Name ID base URL to http://www.imdb.com/search/name


Function fetch_name_ids
This function fetches all the name ids starting from
•	http://www.imdb.com/search/name?gender=male&start=1 to http://www.imdb.com/search/name?gender=male&start=10001 for male celebrities
•	http://www.imdb.com/search/name?gender=female&start=1 to http://www.imdb.com/search/name?gender=female&start=10001 for female celebrities

To avoid any forced closing of connection from IMDb, we need to execute in slots. Rather than fetching all name ids and then the respective celebrities’ information at once, I executed the code in slots of 1000 extractions each time.
This can be done by changing the for loop as following-
•	First Run-
for i in range(1, 1001, 50):
    if self.imdb_base != False:
        # r_url = self.name_id_base + "?gender=male&start=" + str(i)
        r_url = self.name_id_base + "?gender=female&start=" + str(i)
•	Second Run-
for i in range(1001, 2001, 50):
    if self.imdb_base != False:
        # r_url = self.name_id_base + "?gender=male&start=" + str(i)
        r_url = self.name_id_base + "?gender=female&start=" + str(i)
•	And so on



Note – The links used for fetching name ids contain as many as 2,494,770 name ids for male celebrities and 1,331,009 name ids for female celebrities. Based on our requirements, using the links we can expand our data collection upto these many celebrities.

Function fetch_celeb_info
This function fetches information of all celebrities whose ids have been collected
 It uses the following links-
•	http://www.imdb.com/name/name_id/bio?ref_=nm_ov_bio_sm link for biography, that is, name, birth date, birth year, birth location, ethnicity.
•	http://www.imdb.com/name/name_id/?ref_=nmbio_bio_nm links for filmography, that is, the list of titles/soundtracks they are associated with.

For extracting a celebrity’s ethnicity, I am using the Mini Bio section of his/her IMDb biography page. I have fetched initial part of the Mini Bio which usually mentions the descent. I then search for matches of various ethnicities in it.

 
Function main
This function creates an object of the class. This automatically calls the init function and the IMDb and Name ID base URLs get initialized.
It then calls the fetch_name_ids function to fetch the name ids of celebrities.
Finally, it iterates through the name ids and calls the fetch_celeb_info function for each iteration.


To properly view the resultant files male_celebs.txt and female_celebs.txt
•	Open the files using Excel.
•	Under the ‘Data’ tab in Excel, click on ‘Text to Columns’.
•	Select the ‘Delimiter’ radio button and click Next.
•	Check the ‘Tab’ option and click Next.  
•	In Destination select the whole sheet (or manually enter $A$1).

