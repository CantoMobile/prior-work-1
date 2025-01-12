import boto3
import requests
from bs4 import BeautifulSoup
import favicon
import urllib.request
import urllib.parse
import requests
from io import BytesIO
# from dotenv import load_dotenv
from urllib.parse import urlparse, urlunparse
from PIL import Image
from app.utils.logger import logger
import io
import os
import imghdr

# load_dotenv()

ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
ACCESS_SECRET_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
BUCKET_NAME = os.environ.get('BUCKET_NAME')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip',
    'DNT': '1'  # Do Not Track Request Header
}

DEFAULT_FAVICON_LINK = "https://cdn-icons-png.flaticon.com/512/44/44386.png"
FOLDER_PATH = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', '..', 'favicons'))


# def getSiteName(url):
#     parsed_url = urllib.parse.urlparse(url)

#     domain_name = parsed_url.netloc
#     split_domain = domain_name.split('.')
#     extracted_domain = split_domain[-2]

#     return extracted_domain

import urllib.parse

def getSiteName(url):
    parsed_url = urllib.parse.urlparse(url)
    domain_name = parsed_url.netloc
    split_domain = domain_name.split('.')
    if len(split_domain) > 1:
        extracted_domain = split_domain[-2]
    else:
        extracted_domain = split_domain[0]
    return extracted_domain


def uploadFile(image, image_name):
    s3 = boto3.client('s3',
                      aws_access_key_id=ACCESS_KEY_ID,
                      aws_secret_access_key=ACCESS_SECRET_KEY
                      )

    #image_data = requests.get(link).content
    image = (io.BytesIO(image))
    bucket_name = BUCKET_NAME
    try:
        s3.upload_fileobj(
            image,
            bucket_name,
            image_name
        )
    except Exception as e:
        logger.error("Has error uploading icon ", (str(e)))


def scrapeFavicon(url):
    folder_path = FOLDER_PATH
    image_name = f'{getSiteName(url)}.png'
    filename = os.path.join(folder_path, image_name)
    msg, link = "", ""

    try:
        page = requests.get(url)

        soup = BeautifulSoup(page.content, 'html.parser')

        favicon_link = soup.find(
            "link", rel="shortcut icon") or soup.find("link", rel="icon")

        if favicon_link:
            link = favicon_link.get("href")

            if not link.startswith("https://"):
                if link.startswith("//"):
                    link = "https:" + link
                elif link.startswith("/"):
                    link = "https:/" + link
                else:
                    link = "https://" + link

            image_data = requests.get(link).content
            image = Image.open(io.BytesIO(image_data))
            image.save(filename, "PNG")
            msg += "Saving file - success"
        else:
            link = DEFAULT_FAVICON_LINK
            urllib.request.urlretrieve(link, filename)
            msg += f"Saving file - Failure: Couldn't get favicon"

    except Exception as e:
        msg += f'Error saving file: {e}'
    finally:
        upload_status = uploadFile(link, image_name)
        msg += f'Upload to s3 message: {upload_status}'
        return msg


def getFaviconFromURL(url):
    folder_path = FOLDER_PATH
    image_name = f'{getSiteName(url)}'
    filename = os.path.join(folder_path, image_name)
    msg, link, status = "", "", ""

    try:
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        headers = {'User-Agent': user_agent}

        url = normalize_url(url)
        print("url icon: " + url)
        
        icons = favicon.get(url, headers=headers)
        icon = None
        for ico in icons:
            if ico.url.endswith("favicon.ico"):
                icon = ico
                break
        if icon is not None:
            r = requests.get(icon.url, headers=headers)
            print(is_image(r))
            if is_image(r):
                image_type = imghdr.what(None, r.content)
                print(image_type)
                if image_type:
                    image_name = image_name + f'.{image_type}'
                else:
                    raise ValueError("No valid image found in favicon")
                image = r.content
                msg += "Saving file - success"
                link = icon.url
            else:
                raise Exception
        else:
            raise ValueError("No favicon.ico found in icons")

    except Exception as e:
        print(e)
        link = DEFAULT_FAVICON_LINK
        status = "DEFAULT"
        r = requests.get(link, headers=headers)
        if is_image(r):
            image_type = imghdr.what(None, r.content)
            print(image_type)
            if image_type:
                image_name = image_name + f'.{image_type}'
                image = r.content
        logger.error(
            f'Saving file - Failure:Site - {url}Error message - {e}')

    finally:
        uploadFile(image, image_name)
        public_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{image_name}"
        logger.info(f' Upload icon to s3 successful.')
        return public_url
        # return msg


def normalize_url(url):
    parts = urlparse(url)
    if not parts.scheme:
        parts = parts._replace(scheme='https')
    return urlunparse(parts)


def getFavicon(url):
    url, status = getFaviconFromURL(url)[0], getFaviconFromURL(url)[1]
    if status == "DEFAULT":
        return scrapeFavicon(url)
    else:
        return url


def getUrlFavicon(url, file):
    image_name = f'{getSiteName(url)}.png'
    s3 = boto3.client('s3',
                      aws_access_key_id=ACCESS_KEY_ID,
                      aws_secret_access_key=ACCESS_SECRET_KEY
                      )
    bucket_name = BUCKET_NAME
    with BytesIO(file) as file_stream:
        response = s3.upload_fileobj(
            file_stream,
            bucket_name,
            image_name
        )
    public_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{image_name}"
    return public_url
    
def is_image(response):
    content_type = response.headers.get('Content-Type','')
    if content_type.startswith('image/'):
        return True
    else:
        return False


# TEST_SITES = [
    # "https://www.eventbrite.com",
    # "https://www.amazon.com",
    # "https://www.stackoverflow.com",
    # "https://www.google.com",
    # "https://www.atlassian.com",
    # "https://www.heroku.com",
    # "https://www.railway.com",
    # "https://www.reddit.com",
    # "https://www.mongodb.com",
    # "https://stackoverflow.com/questions/857653/get-a-list-of-urls-from-a-site",
    # "https://www.gmail.com",
    # "https://www.groupon.com",
    # "https://www.ticketmaster.com",
    # "https://www.yelp.com",
    # "https://www.meetup.com",
    # "https://www.github.com",
    # "https://www.smallbizsurvival.com",
    # "https://www.graphql.com",
    # "https://www.ycombinator.com",
    # "https://www.ibm.com",
    # "https://www.huggingface.co",
    # "https://www.apollographql.com",
    # "https://www.rbcroyalbank.com",
    # "https://www.whatsapp.com",
    # "https://www.facebook.com",
    # "https://www.instagram.com",
    # "https://www.twitter.com",
    # "https://www.pinterest.com",
    # "https://www.realpython.com"
    # "https://docs.google.com"
# ]


# try:
#     for site in TEST_SITES:
#         print(getFaviconFromURL(site))
# except Exception as e:
#     print(e)

# try:
#     for site in TEST_SITES:
#         print(scrapeFavicon(site))
# except Exception as e:
#     print(e)
# print(scrapeFavicon("https://www.twitter.com"))
