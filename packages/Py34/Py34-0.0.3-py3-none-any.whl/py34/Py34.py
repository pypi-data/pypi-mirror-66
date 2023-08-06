import  os,\
        math, \
        random, \
        json, \
        urllib.request

import requests
from fake_useragent import UserAgent

ua = UserAgent()

class PIDTooBigError(Exception):
    pass

class LimitTooBigError(Exception):
    pass

class Py34:
    def __init__(self):
        pass

    def downloadURL(self, url, path):
        """
            :param url: The url of the file you want to download
            :param path: The path where you want your file to be downloaded in + it's file name
        """
        r = requests.get(url, allow_redirects=True) 
        open(path, 'wb').write(r.content) # write the content of the file in the specified path
    
    def generateUserAgent(self):
        """
            :return: String User Agent (ex: Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36)
        """
        return ua['google chrome']

    def generateURL(self, tags=None, limit=None, PID=None):
        """
            :param tags: str ||The tags to search for. Any tag combination that works on the web site will work here. This includes all the meta-tags
            :param limit: str ||How many posts you want to retrieve
            :param PID: int ||The page number.

            :return: URL String or None
        """
        baseURL = 'https://r34-json.herokuapp.com/posts?tags'

        if tags != None:
            tags = tags.replace(' ', '+')
            baseURL += '={}'.format(tags)

        if limit != None: # if the user wants to download more or less than the default result number (100)
            if limit > 1000:
                raise LimitTooBigError('You cannot have more than a thousand results per page.')

            baseURL += '&limit={}'.format(limit)

        if PID != None: # if the user wants to look for a specific page
            if PID > 2000: # R34 does not allow more than 2000 pid
                raise PIDTooBigError('Page ID is more than 2000')
            baseURL += '&pid={}'.format(PID)

        return baseURL

    def getTotalImages(self, tags):
        """
            :param tags: String || The user tag we want to check

            :return: int || The amount of results that can be retrieved
        """
        data = self._retrieve_url_data(self.generateURL(tags=tags))
        try:
            return int(data['count'])
        except:
            return False

    def getImagesURLs(self, tags, singlePage=True, pageResultAmount=100, randomPage=False, PID=None, Videos=True, Gifs=True, Images=True):
        """
            :param tags: The tag we want to retrieve the results from
            :param singlePage: If you want to retrieve more than 100 results
            :param limit: How many results you want to retrieve
            :param pageResultAmount: The amount of results per page
            :param randomPage: If you want the results from a random page
            :param PID: The page number the user wants to be in
            :param Videos: If you want to retrieve videos
            :param Gifs: If you want to retrieve gifs
            :param Images: If you want to retrieve images

            :return: list of urls or []
        """
        num = self.getTotalImages(tags=tags) # the total amount of images
        urls = [] # the urls will be stored in this list

        if pageResultAmount > 1000:
            raise LimitTooBigError('You cannot have more than a thousand results per page')

        if randomPage == True and PID != None: # if we want a random page but the page ID was already given
            PID=None

        if randomPage == True and singlePage == False: # if we want a random page but all the pages will be retrieved anyway
            randomPage = False

        if randomPage == True: # if we want a random page
            maxPID = self._get_max_page_id(num, pageResultAmount) # we will guess the max amount of pages using maths
            PID = random.randint(0, maxPID) # will give a random page ID 

        if singlePage == False: # if we want to retrieve all the results
            pageResultAmount = 1000 # we will put the page result number to 1000 since it does not matter if we are gonna retrieve all the data
            maxPID = self._get_max_page_id(num, pageResultAmount) # we will guess the max amount of pages using maths

            for x in range(maxPID+1): # we will start to go through all the pages
                PID = x # the page number
                url = self.generateURL(tags=tags, limit=pageResultAmount, PID=PID)

                urls.append(self._get_url_from_posts(url))
        else: # if the user only wants to retireve the results from one page
            url = self.generateURL(tags=tags, limit=pageResultAmount, PID=PID)

            urls = self._get_url_from_posts(url)
        try:
            urls = sum(urls, [])
        except:
            pass

        urls = self._filter_urls(urls, downloadImages=Images, downloadGifs=Gifs, downloadVideos=Videos)

        return [x.split('?url=')[-1] for x in urls]

    #############################################################################################################################################################
  
    def _filter_urls(self, urls, downloadImages=True, downloadGifs=True, downloadVideos=True):
        """
            :param urls: List of urls gathered using the getImageURLs function
            :param downloadImages: Boolean if the user wants to download images
            :param downloadGifs: Boolean if the user wants to download gifs
            :param downloadVideos: Boolean if the user wants to download videos

            :return: List of filtered urls
        """
        all_urls = []
        videos = []
        gifs = []
        images = []

        for url in urls:
            if url.lower().endswith('.webm') and downloadVideos: # if the file is a webm, add it to the videos list
                videos.append(url)
            elif url.lower().endswith('.gif') and downloadGifs: # if the file is a gif, add it to the gifs list
                gifs.append(url)
            if url.lower().endswith(('.png', '.jpg', '.jpeg')) and downloadImages: # if the file is a picture, add it to the images list
                images.append(url)

        # we want to put the pictures in the list first, then we can add the videos and the gifs

        for url in images: 
            all_urls.append(url)

        for url in gifs:
            all_urls.append(url)

        for url in videos:
            all_urls.append(url)

        return all_urls

    def _get_max_page_id(self, num, resultsPerPage):
        maxPID = 2000 # 2000 is the max amount of page possible 

        if math.floor(num/resultsPerPage) < maxPID:
                return math.floor(num/resultsPerPage)

    def _get_url_from_posts(self, url):
        """
            :param url: The url of the post

            :return: The url of the file from the post
        """
        urls = []
        data = self._retrieve_url_data(url)
        posts = data['posts']

        for y in range(len(posts)):
            result_url = posts[y]['file_url'] # Needs to be put in a method but i manage to make this return 227 everytime
            urls.append(result_url)

        return urls

    def _retrieve_url_data(self, url, useragent=''):
        """
            :param url: The url where all the data is stored
            :param useragent: The user agent you want to use to make the request

            :return: Dictionnary
        """
        if useragent != '': # if the user wants to use a useragent
            headers = {
                'UserAgent':self.generateUserAgent()
            }
        else: # if the user does not want to user a useragent
            headers = {}
        try: # here we try to open the url and convert it into a json
            response = requests.get(url, headers=headers)

            return response.json()
        except: # if an error occured, return False
            return False