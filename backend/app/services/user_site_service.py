from flask import abort, jsonify
from app.repositories.user_site_repository import UserSiteRepository
from app.repositories.site_repository import SiteRepository
from app.models.user_site_model import UserSite
from app.models.site_model import Site


site_repo = SiteRepository()
user_site_repo = UserSiteRepository()

def add_site(user_id, site_id):
    site_data = site_repo.findById(site_id)
    user_site_data = user_site_repo.findByField('user_id', user_id)
    if not user_site_data or not site_data:
        abort(404)
    site = Site(**site_data)

    site_stats = site_data.get('site_stats', {})
    site_stats['saves'] = site_stats.get('saves', 0) + 1
    site_data['site_stats'] = site_stats
    site_repo.update(site_id, site_data)

    return user_site_repo.updateArray(user_site_data['_id'],'site', site)

def remove_site(user_id, site_id):
    site_data = site_repo.findById(site_id)
    user_site_data = user_site_repo.findByField('user_id', user_id)
    if not user_site_data or not site_data:
        abort(404)
    user_site = UserSite(**user_site_data)
    site = Site(**site_data)
    validation = any( site_item['_id'] == site_id for site_item in user_site.site)
    if validation:
        site_stats = site_data.get('site_stats', {})
        site_stats['saves'] = max(site_stats.get('saves', 0) - 1, 0)
        site_data['site_stats'] = site_stats
        site_repo.update(site_id, site_data) 
        return user_site_repo.deleteFromArray(user_site_data['_id'],'site', site)
    else: 
        return jsonify({"error":"This user don't have saved this site."})

def create_relationship(id):
    user_site = UserSite(user_id=id)
    user_site_repo.save(user_site)

def delete_relationship(id):
    user_site = user_site_repo.findAllByField('user_id', id)
    user_site_repo.delete(user_site['_id'])

def return_not_referenced(user_id):
    user_site_data = user_site_repo.findByField('user_id', user_id)
    sites = user_site_data.get('site',[])
    referenced_ids = [site['_id'] for site in sites]
    return site_repo.getNotReferenced(referenced_ids)

def return_referenced(user_id):
    user_site_data = user_site_repo.findByField('user_id', user_id)
    sites = user_site_data.get('site', [])
    referenced_ids = [site['_id'] for site in sites]
    return site_repo.getReferenced(referenced_ids)

def query_not_referenced(user_id, query):
    user_site_data = user_site_repo.findByField('user_id', user_id)
    sites = user_site_data.get('site', [])
    referenced_ids = [site['_id'] for site in sites]
    return site_repo.queryNotRefereced(referenced_ids, query)

def query_referenced(user_id, query):
    user_site_data = user_site_repo.findByField('user_id', user_id)
    sites = user_site_data.get('site', [])
    referenced_ids = [site['_id'] for site in sites]
    return site_repo.queryRefereced(referenced_ids, query)

