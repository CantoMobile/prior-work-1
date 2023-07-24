import datetime
from bson import ObjectId
from flask import abort, request
import pymongo
from app.models import SiteStats
from app.repositories.site_stats_repository import SiteStatsRepository
from app.repositories.site_repository import SiteRepository

site_stats_repo = SiteStatsRepository()
site_repo = SiteRepository()


def get_all_site_stats(page=None):
    if page is not None:
        site_stats_data = site_stats_repo.findAll(page, 15)
    else:
        site_stats_data = site_stats_repo.findAll()
    return site_stats_data


def add_stats():
    data = request.json
    if 'site' in data:
        site_stats = SiteStats(
            site=data['site']
        )
        stats = site_stats_repo.save(site_stats)
        return stats
    else: 
        abort(401)


def search_top_six():
    top6_sites = site_stats_repo.sort('saves', pymongo.DESCENDING)[:6]
    return top6_sites


def get_one_site_stats(stat_id):
    site_stats = site_stats_repo.findById(stat_id)
    if not site_stats:
        abort(404)
    return site_stats


def update_one_site_stats(stat_id):
    site_stats = site_stats_repo.findById(stat_id)
    data = request.json
    if 'site' in data:
        site = site_repo.findAllByField('url', data['site'])
        if not site:
            abort(404)
        if site_stats['site']['_id'] != site['_id']:
            abort(404)
    if 'visits' in data:
        site_stats['visits'] += data['visits']
    if 'unique_visitors' in data:
        site_stats['unique_visitors'] += data['unique_visitors']
        site_stats['last_visit'] = datetime.now()
    return site_stats_repo.update(stat_id, site_stats)


def delete_one_site_stats(stat_id):
    if site_stats_repo.existsByField('_id', ObjectId(stat_id)):
        site = site_repo.findByField('site_stats._id', stat_id)
        site['site_stats'] = None
        site_repo.update(site['_id'], site)
        return site_stats_repo.delete(stat_id)
    else:
        abort(404)
