FacetWallpaperGrabber
=====================

Grabs all the Facet Wallpapers created by Justin Maller from his website Http://Facets.la. 

I do not own the facet wallpapers nor the website in which the wallpapers are extracted from. They belong respectfully to Justin Maller. If there is an issue with this script, please contact me at Brandynbb96@gmail.com

This script will run throguh all 365 images that Justin Maller has created on his website using the link http://facets.la/[YEAR]/[IMAGE No]/wallpaper. From here, the BeautifulSoup4 module will find and extract the image source from the image tag that is displaying the wallpaper. Using the urllib module, we can then fetch the image and store it in the desired location.
