#Copyright 2014 ReallyGoodPie
#All imagess extraced from this program belong respectfully to Justin Maller. Http://facet.la also belongs to Justin Maller
#If there is an issue with this program, please contact me at Brandynbb96@gmail.com

from urllib.request import urlopen, urlretrieve
from bs4 import BeautifulSoup

def make_soup(url):

        #Making some dank soup using BS4 module
        html = urlopen(url).read()
        return BeautifulSoup(html)

def sep_list(html_elements):

    #All wallpapers are stored in the third <img> element of the webpage
    try:
        new_soup = BeautifulSoup(str(html_elements[2]))
        return new_soup.find('img')['src']
    #If failed, return defaul URL
    except IndexError:
        return "http://www.facets.la/wallpaper/"
        
def get_image():

    #Setting some defaults    
    output_folder = input("Please enter the directory you would like to store the Facets: ")
    failed_images, success_images = 0, 0

    #Vars extracted from website
    """Earliest Year = 2013
    Amount of images for 2013: 330
    Current max images: 360
    All images home pages (where Justin Maller showcases his images) are located at the following address:
    http://facets.la/[YEAR]/[IMAGE No.]/wallpaper/
    """
    max_images = 365
    year = 2013
    max_2013 = 330

    #Runs through a loop of all images, get's the image and stores it
    for i in range(max_images):
        i = i+1
        if i > max_2013:
            year = 2014
        urlpath = "http://facets.la/%s/%s/wallpaper/" % (str(year), str(i))
        print("Checking: %s" % (urlpath))
        soup = make_soup(urlpath)
        
        #Gets a list of all image elements
        images = [img for img in soup.findAll('img')]
        actual_image = sep_list(images)

        #Some images fail to download or are no longer avaialble. If this happens, don't do anything
        if(actual_image != "http://www.facets.la/wallpaper/"):
            print("Downloading: %s" % (actual_image))
            output_file = (output_folder + str(i) + ".jpg")
            try:
                urlretrieve(actual_image, output_file)
                success_images += 1
            except:
                print("Failed to store image in %s directory" % (output_file))
                failed_images += 1
        else:
            print("Failed to download: %s" % (urlpath))
            failed_images += 1

    #Returning user feedback
    print("Downloaded: %s\nFailed:%s" % (str(success_images), str(failed_images)))
    
if __name__ == "__main__":
    get_image()
