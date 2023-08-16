import socket
from urllib.parse import urlparse
from flask import jsonify,  request, abort
import pymongo
from app.repositories.site_repository import SiteRepository
from app.repositories.user_site_repository import UserSiteRepository
from app.repositories.site_stats_repository import SiteStatsRepository
from app.services.user_site_service import query_referenced, query_not_referenced, get_refereced_ids
from app.models.site_model import Site
from bson.objectid import ObjectId
from app.services.user_service import save_site_user, validate_email_domain, remove_site_user
from app.services.otp_service import add_one_otp, validate_otp_code
from ..utils.s3Upload import uploadFile, uploadFileUrl
from app.services.reviews_service import exists_by_field, delete_review_by_site
from ..utils.faviconHelper import getFaviconFromURL
from app.utils.logger import logger
import json
import concurrent.futures

site_repo = SiteRepository()
user_site_repo = UserSiteRepository()
site_stats_repo = SiteStatsRepository()


def get_all_sites(page=None):
    if page is not None:
        sites_data = site_repo.findAll(page, 15)
    else:
        sites_data = site_repo.findAll()
    return sites_data


def create_site():
    media_links = []
    data = json.loads(request.form['json'])
    change_owner = False

    url = data.get('url')
    admin_email = data.get('admin_email', 'admin@cantonica.com')
    actual_site = site_repo.findByField('url', url)
    print(actual_site)
    if actual_site:
        if actual_site['admin_email'] != 'admin@cantonica.com':
            return jsonify({"error": "This site has already been claimed."}), 400
        if admin_email != 'admin@cantonica.com':
            change_owner = real_site(url, admin_email)
        if not change_owner:
            return jsonify({"error": "Site already exists"}), 400
        else:
            data = {"user_id": data['user_id'],
                    "site_url": data['url'], "email": data["admin_email"]}
            if add_one_otp(data):
                return jsonify({"message": "code sended"})
            else:
                return jsonify({"error":
                                "There was an error sending the confirmation code, please try again later."}), 401

    if admin_email != 'admin@cantonica.com':
        if site_repo.existsByField('admin_email', admin_email):
            return jsonify({"error": "This email is the admin for another site"}), 400

    if 'media' in request.files:
        data_media = request.files.getlist('media')
        media_links = save_data_media(data['name'], data_media)

    site = Site(
        url=url,
        name=data['name'],
        description=data['description'],
        logo=getFaviconFromURL(url),
        keywords=data['keywords'],
        media=media_links,
        admin_email=admin_email
    )

    try:
        site_data = site_repo.save(site)
        if 'user_id' in data:
            return create_site_admin_relationship(data['user_id'], site_data['_id'], True)
        else:
            return site_data
    except Exception as e:
        return jsonify({"error": "Error saving site", "message": str(e)}), 400


def create_site_admin_relationship(user_id, site_id, create=None):
    if create is None:
        remove = remove_site_user(site_id)
        update = save_site_user(user_id, site_id)
        if update['updated_count'] > 0 and (remove != None and remove['updated_count'] > 0):
            return jsonify({"message": "The administration of this site has been successfully changed."})
        else:
            return get_one_site(site_id)
    else:
        save = save_site_user(user_id, site_id)
        if save['updated_count'] > 0:
            return get_one_site(site_id)
        else:
            delete_one_site(site_id)
            return jsonify({"Error": "The site could not be successfully created and assigned your ownership."}), 400


def real_site(url, admin_site):
    domain = validate_domain(url)
    if domain:
        errors = validate_email_domain(admin_site)
        if errors[0] == False:
            return {"error": errors[1]}, 401
        return validate_mail_domain(url, admin_site)
    else:
        return False


def validate_domain(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    try:
        socket.gethostbyname(domain)
        return domain
    except socket.gaierror:
        return None


def validate_mail_domain(url, mail):
    parsed_url = urlparse(url)
    domain_url = parsed_url.netloc.replace("www.", "")
    fields_mail = mail.split('@')

    if len(fields_mail) != 2:
        return False

    domain_email = fields_mail[1].lower()
    return domain_url == domain_email


def update_admin_email(site_id, admin_email):
    site_data = get_one_site(site_id)
    site_data['admin_email'] = admin_email
    update = site_repo.update(site_id, site_data)
    return update['updated_count'] > 0


def save_data_media(namesite, media):
    media_links = []
    if len(media) > 0:
        for file in media:
            image_name = f"{namesite}_{file.filename}"
            try:
                file_data = file.stream.read()
                file_link = uploadFile(file_data, image_name)
                media_links.append(file_link)
            except Exception as e:
                logger.error("Error uploading file " + str(e))
                return jsonify({"error": "Error processing file",
                                "message": str(e)}), 400
        return media_links


def get_one_site(site_id):
    site = site_repo.findById(site_id)
    if not site:
        abort(401)
    return site


def update_one_site(site_id):
    media_links = []
    data = json.loads(request.form['json'])
    site = get_one_site(site_id)

    if 'media' in request.files:
        data_media = request.files.getlist('media')
        media_links = save_data_media(
            data['name'], data_media) if 'name' in data else save_data_media(site['name'], data_media)

    if 'name' in data:
        site['name'] = data['name']
    if 'description' in data:
        site['description'] = data['description']
    if 'keywords' in data:
        site['keywords'] = data['keywords']
    if len(media_links) > 0:
        if 'old_media' in data:
            site['media'] = data['old_media']
            site['media'].extend(media for media in media_links)
        else:
            site['media'] = media_links
    response = site_repo.update(site_id, site)
    if response['updated_count'] > 0 and 'email_admin' not in data:
        return response
    elif response['updated_count'] > 0 and data['admin_email'] != site['admin_email']:
        change_owner = real_site(site['url'], data['admin_email'])
        if not change_owner:
            return jsonify({"error": "Updated information, admin email no."}), 400
        else:
            data = {"user_id": data['user_id'],
                    "site_url": site['url'], "email": data["admin_email"]}
            otp_data = add_one_otp(data)
            if otp_data:
                return jsonify({"message": "code sended"})
            else:
                return jsonify({"error":
                                "There was an error sending the confirmation code, please try again later."}), 401


def delete_one_site(site_id):
    get_one_site(site_id)
    remove_site_user(site_id)
    if user_site_repo.existsByField('site._id', ObjectId(site_id)):
        user_site_repo.deleteAllSitesReferenceds(site_id)
    if exists_by_field('site_id', site_id):
        delete_review_by_site(site_id)
    return site_repo.delete(site_id)


def search_sites_logged(user_id, page=None):
    query = request.args.get('query')
    if not query:
        return jsonify({'error': 'Missing search query'}), 400
    if page is not None:
        return site_repo.query(query_not_referenced(user_id, query), page, 15)
    else:
        return site_repo.query(query_not_referenced(user_id, query))


def search_sites_claimed(page):
    query = request.args.get('query')
    if not query:
        return jsonify({'error': 'Missing search query'}), 400
    if query == 'claimed':
        return site_repo.findAllByField('admin_email', {'$ne': 'admin@cantonica.com'}, page, 15)
    else:
        return site_repo.findAllByField('admin_email', 'admin@cantonica.com', page, 15)


def search_sites_saves_logged(user_id, page=None):
    query = request.args.get('query')
    if not query:
        return jsonify({'error': 'Missing search query'}), 400
    if page is not None:
        return site_repo.query(query_referenced(user_id, query), page, 15)
    else:
        return site_repo.query(query_referenced(user_id, query))


def search_sites_not_logged():
    query = request.args.get('query')
    # Get the search query from the request parameters
    if not query:
        return jsonify({'error': 'Missing search query'}), 400
    sites = site_repo.query({
        '$or': [
            {'url': {'$regex': query, '$options': 'i'}},
            {'name': {'$regex': query, '$options': 'i'}},
            {'description': {'$regex': query, '$options': 'i'}},
            {'keywords': {'$regex': query, '$options': 'i'}}
        ]
    })
    return sites


def search_sites_name_suggested():
    query = request.args.get('query')
    if not query:
        return jsonify({'error': 'Missing search query'}), 400

    pipeline = [
        {
            '$match': {
                '$or': [
                    {'url': {'$regex': query, '$options': 'i'}},
                    {'name': {'$regex': query, '$options': 'i'}}
                ]
            }
        },
        {
            '$sort': {'site_stats.saves': -1}
        },
        {
            '$limit': 10
        },
        {
            '$project': {'_id': 0, 'name': 1}
        }
    ]
    return site_repo.queryAggregation(pipeline)


def get_top_six_saved():
    top6_sites = site_repo.sort('site_stats.saves', pymongo.DESCENDING)[:6]
    return jsonify(top6_sites)


def get_top_six_saved_logged(user_id):
    return site_repo.queryTopSixLogged(get_refereced_ids(user_id))


def stats_by_site(site_id):
    site = site_repo.findById(site_id)

    if not site:
        abort(404)

    if not site['site_stats']:
        abort(404)

    stats = site_stats_repo.findById(site['site_stats'])

    if not stats:
        abort(404)
    return stats


def validate_site_otp():
    data = request.json
    code = validate_otp_code(data['user_id'], data['code'])
    if code:
        site_data = site_repo.findByField('url', data['site_url'])
        print(site_data)
        update_admin_email(site_data['_id'], data['admin_email'])
        return create_site_admin_relationship(data['user_id'], site_data['_id'])
    else:
        return jsonify({"error":
                        "An error occurred while trying to claim the site, please try again later."}), 401


def create_masive_sites(sites):
    media = [
        "https://cantonica-favicons-test.s3.amazonaws.com/default_notfountimagecant (1).png",
        "https://cantonica-favicons-test.s3.amazonaws.com/default_notfountimagecant (2).png",
        "https://cantonica-favicons-test.s3.amazonaws.com/default_notfountimagecant.png"]
    admin_email = "admin@cantonica.com"
    total_sites = len(sites)
    batch_size = 10
    total_batches = total_sites // batch_size + 1

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for batch_index in range(total_batches):
            start_index = batch_index * batch_size
            end_index = start_index + batch_size
            batch_sites = sites[start_index:end_index]
            futures.append(executor.submit(
                process_batch, batch_sites, media, admin_email))

        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
                if result:
                    print("La tarea se completó exitosamente.")
            except Exception as e:
                print({"error": "Error processing batch", "message": str(e)})
                return jsonify({"error": "Error processing batch", "message": str(e)}), 400

    print("Sites created successfully")
    return "Sites created successfully"


def process_batch(batch_sites, media, admin_email):
    site_list = []

    for site_data in batch_sites:
        print("Creando objeto para el sitio: " +
              site_data['name'] + " " + site_data['url'])
        media_links = []
        url = site_data.get('url')

        if 'media' in site_data:
            media = site_data['media']
            i = 1
            if site_repo.existsByField('url', url):
                continue
            for url_media in media:
                image_name = f"{site_data['name']}_screenshot_{i}"
                try:
                    file_link = uploadFileUrl(url_media, image_name)
                    media_links.append(file_link)
                    i += 1
                except Exception as e:
                    logger.error("Error uploading file " + str(e))
                    raise Exception(
                        {"error": "Error processing file", "message": str(e)})
        else:
            media_links = media

        site = Site(
            url=url,
            name=site_data['name'],
            description=site_data['description'],
            logo=getFaviconFromURL(url),
            keywords=site_data['keywords'],
            media=media_links,
            admin_email=[
                'admin_email'] if 'admin_email' in site_data else admin_email
        )

        site_list.append(site)

    try:
        site_data = site_repo.insertMany(site_list)
        if site_data:
            for i, data in enumerate(site_data):
                if 'user_id' in batch_sites[i]:
                    create_site_admin_relationship(
                        batch_sites[i]['user_id'], data['_id'], True)

    except Exception as e:
        print({"error": "Error saving sites", "message": str(e)})
        raise Exception({"error": "Error saving sites", "message": str(e)})

    return True


def delete_site_ownership(site_id):
    response = remove_site_user(site_id)
    if 'updated_count' in response and response['updated_count'] > 0:
        if update_admin_email(site_id, 'admin@cantonica.com'):
            return jsonify({"message": "ownership removed successfully."})
    else:
        return jsonify({"error": "Error deleting site ownership."}), 401


def actualizar_lista_media(media, nuevas_urls):
    if len(nuevas_urls) == 1:
        media.append(nuevas_urls[0])
    elif len(nuevas_urls) >= 2:
        media = media[2:]
        media.extend(nuevas_urls[:2])
        if len(nuevas_urls) > 2:
            media.append(nuevas_urls[2])
    media = media[:4]

    return media


def get_count(query=None):
    if query:
        return site_repo.count(query)
    else:
        return site_repo.count({})


def get_more_saved(limit=None):
    if limit:
        top = site_repo.sort('site_stats.saves', pymongo.DESCENDING)[:limit]
    else:
        top = site_repo.sort('site_stats.saves', pymongo.DESCENDING)[:6]
    top_sites = [
        {
            "name": dic["name"],
            "url": dic["url"],
            "saves": dic["site_stats"]["saves"]
        }
        for dic in top
    ]
    return top_sites
