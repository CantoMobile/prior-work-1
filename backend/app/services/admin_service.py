from flask import jsonify
from app.services.user_service import get_count as user_count
from app.services.site_service import get_count as site_count, get_more_saved


def get_admin_information():
    user_total = user_count()
    print(user_total)
    claimed_count = site_count({'admin_email': {'$ne': 'admin@cantonica.com'}})
    print(claimed_count)
    site_total = site_count()
    print(site_total)
    more_saved = get_more_saved(10)
    print(more_saved)
    response = {
        'created_users': user_total,
        'claimed_sites': claimed_count,
        'total_sites': site_total,
        'more_saved_sites': more_saved
    }
    return jsonify(response)