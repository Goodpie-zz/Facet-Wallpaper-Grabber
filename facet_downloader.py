import os
import queue
import threading
from urllib.error import URLError

from urllib.request import urlopen, urlretrieve

import time
from bs4 import BeautifulSoup


class FacetDownloader:

    def __init__(self, attempts=10, threaded=True):

        # Amount of attempts to make before giving up the download
        self.attempts = attempts

        # Whether to use threads or not (may be faster)
        self.threaded = threaded

        # Available images per year
        self.MAX_IMAGES = 365

        # Current year
        self.year = 2013

        # Directory to store images
        self.output_folder = "facets/"

    # Gets a directory to store the facets in
    def get_output_folder(self):
        # Get Output dir from user
        output_folder = input("Please enter the directory where you would like to save the Facets: ")
        self.output_folder = os.path.join(output_folder)

        # If the dir doesn't exist, attempt to create it
        if not os.path.isdir(self.output_folder):
            print("Creating new directory: {}".format(self.output_folder))
            os.mkdir(self.output_folder)

    def start(self):

        self.get_output_folder()

        threads = []

        for i in range(self.MAX_IMAGES * 2):

            # Ensure we don't exceed the max amount of images for 2013
            if i > self.MAX_IMAGES:
                self.year = 2014
                i -= self.MAX_IMAGES

            # Generate URL

            url = "http://facets.la/{0}/{1}/wallpaper/".format(str(self.year), str(i))

            # Create threads if needed
            if self.threaded:
                download_thread = threading.Thread(target=self.init_downlaod, args=(url, i,))
                download_thread.start()
                threads.append(download_thread)
            else:
                self.init_downlaod(url, i)

        # Join all threads
        if self.threaded:
            for t in threads:
                t.join()

    # Downloads the image from the HTML fetched
    def init_downlaod(self, url, index, attempts=0):

        print("checking {} ".format(url))

        # Create soup
        try:
            html = urlopen(url).read()
            soup = BeautifulSoup(html, 'lxml')

            # We know the image is in the third image element of the page
            img_parent = soup.find(id="facet-wallpaper")
            if img_parent is not None:
                img_source = img_parent.img['src']

                # Ensure URL is valid
                if img_source != "http://www.facets.la/wallpaper/" and img_source is not None:
                    # Attempt to download the image
                    out_dir = os.path.join(self.output_folder + str(index) + ".jpg")
                    self.download_image(img_source, out_dir)
            else:
                print("failed {} ".format(url))
        except:
            if attempts <= 20:
                time.sleep(1 + attempts)
                self.init_downlaod(url, index, attempts + 1)
            else:
                print("failed {} ".format(url))
                return

    def download_image(self, url, out_dir, attempts=0):

        print("Downloading image from {}".format(url))

        try:
            urlretrieve(url, out_dir)
            print("Downloaded image from {}".format(url))
        except:
            if attempts <= self.attempts:
                time.sleep(1)
                self.download_image(url, out_dir, attempts + 1)
            else:
                print("There was an error downloading the image from {}".format(url))
                return

if __name__ == "__main__":
    downloader = FacetDownloader(attempts=5)
    downloader.start()
