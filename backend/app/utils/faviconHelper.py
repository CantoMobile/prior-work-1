import boto3
import requests
from bs4 import BeautifulSoup
import favicon
import urllib.request
import urllib.parse
from dotenv import load_dotenv
from PIL import Image
import io
import os

load_dotenv()

ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
ACCESS_SECRET_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
BUCKET_NAME = os.getenv('BUCKET_NAME')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip',
    'DNT': '1'  # Do Not Track Request Header
}

DEFAULT_FAVICON_LINK = "https://cdn-icons-png.flaticon.com/512/44/44386.png"
FOLDER_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'favicons'))


def getSiteName(url):
    parsed_url = urllib.parse.urlparse(url)

    domain_name = parsed_url.netloc
    split_domain = domain_name.split('.')
    extracted_domain = split_domain[-2]

    return extracted_domain


def uploadFile(link, image_name):
    s3 = boto3.client('s3',
        aws_access_key_id= ACCESS_KEY_ID,
        aws_secret_access_key= ACCESS_SECRET_KEY
    )

    image_data = requests.get(link).content
    image = (io.BytesIO(image_data))
    bucket_name = BUCKET_NAME
    response = s3.upload_fileobj(
        image,
        bucket_name,
        image_name
    )

    return response


def scrapeFavicon(url):
    folder_path = FOLDER_PATH
    image_name = f'{getSiteName(url)}.png'
    filename = os.path.join(folder_path, image_name)
    msg, link = "", ""

    try: 
        page = requests.get(url)

        soup = BeautifulSoup(page.content, 'html.parser')

        favicon_link = soup.find("link", rel="shortcut icon") or soup.find("link", rel="icon")

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
            msg += "Saving file - success \n"
        else:
            link = DEFAULT_FAVICON_LINK
            urllib.request.urlretrieve(link, filename)
            msg += f"Saving file - \n Failure: Couldn't get favicon \n"
    
    except Exception as e:
        msg += f'Error saving file: {e} \n'
    finally:
        upload_status = uploadFile(link, image_name)
        msg += f'Upload to s3 message: {upload_status}'
        return msg


def getFaviconFromURL(url):
    folder_path = FOLDER_PATH
    image_name = f'{getSiteName(url)}.png'
    filename = os.path.join(folder_path, image_name)
    msg, link = "", ""

    try:
        icons = favicon.get(url)
        icon = icons[0]
        for icon in icons:
            if icon.url.endswith("favicon.ico"):
                link = icon.url
        urllib.request.urlretrieve(icon.url, filename)

        msg += "Saving file - success \n"
    except Exception as e:
        link = DEFAULT_FAVICON_LINK
        urllib.request.urlretrieve(link, filename)
        msg += f'Saving file - \n Failure: \n Site - {url} \n Error message - {e} \n'

    finally:
        upload_status = uploadFile(link, image_name)
        public_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{image_name}"
        return public_url
        # msg += f'Upload to s3 message: {upload_status}'
        # return msg




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


