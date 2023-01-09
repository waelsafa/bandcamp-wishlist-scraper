from flask import (
    Flask,
    render_template,
    request,
    redirect,
    flash,
    url_for,
    current_app
)
import urllib.request 
from urllib.parse import urlparse,urljoin
from bs4 import BeautifulSoup
import requests,validators,uuid,pathlib,os
from model.WishlistItem import WishlistItem

app = Flask(__name__)
app.secret_key = "secret-key"

    

@app.route("/",methods=("GET", "POST"), strict_slashes=False)
def index():
        if request.method == "POST":

            global requested_url,specific_element,tag
            
            requested_account = request.form.get("accountname")

            wishlist_url = "https://bandcamp.com/" + requested_account + "/wishlist"

            requested_url = requests.get(wishlist_url)

            # parser library?
            soup = BeautifulSoup(requested_url.text, "html.parser")
            
            items = soup.find_all("li", class_="collection-item-container")
                
            WishlistItems = []

            # Loop through each item on the wishlist and extract the data
            for item in items:
                # Get the artist name and album title
                album = item.find("div", class_="collection-item-title").get_text().strip()
                artist = item.find("div", class_="collection-item-artist").get_text().strip()

                # Get the price of the album

                wish_item = WishlistItem(artist, album, 10.0, "https://thebeatles.bandcamp.com/album/abbey-road")
                WishlistItems.append(wish_item)

            return render_template("index.html",
                url = requested_url,
                items = WishlistItems
                )
            
        return render_template("index.html")

