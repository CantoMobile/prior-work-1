from flask import Blueprint
# Define los blueprints vacíos
user_bp = Blueprint('user', __name__)
auth_bp = Blueprint('auth', __name__)
role_bp = Blueprint('role', __name__)
permissions_bp = Blueprint('permissions', __name__)
site_bp = Blueprint('site', __name__)
search_results_bp = Blueprint('search_results', __name__)
user_sites_bp = Blueprint('user_sites', __name__)
site_stats_bp = Blueprint('site_stats', __name__)


__all__ = [
    'user_bp',
    'auth_bp',
    'role_bp',
    'permissions_bp',
    'site_bp',
    'search_results_bp',
    'user_sites_bp',
    'site_stats_bp'
]


# IMPORT CONTROLLERS FROM CONTROLLERS FILE AND REGISTRATION BLUEPRINT

# USER CONTROLLER
from .user_controller import users, user, set_user_password, add_user_role, remove_user_role, authentication
user_bp.add_url_rule('/users', view_func=users, methods=['GET', 'POST'])
user_bp.add_url_rule('/users/<string:user_id>', view_func=user,
                     methods=['GET', 'PUT', 'DELETE'])
user_bp.add_url_rule('//users/authentication', view_func=authentication,
                     methods=['POST'])
user_bp.add_url_rule('/users/<string:user_id>/set_password',
                     view_func=set_user_password, methods=['PUT'])
user_bp.add_url_rule('/users/<user_id>/add_role/<role_id>',
                     view_func=add_user_role, methods=['PUT'])
user_bp.add_url_rule('/users/<user_id>/remove_role/<role_id>',
                     view_func=remove_user_role, methods=['PUT'])

# USER_SITE CONTROLLER
from .user_site_controller import user_site, user_sites
user_sites_bp.add_url_rule(
    '/user_sites', view_func=user_sites, methods=['GET', 'POST'])
user_sites_bp.add_url_rule(
    '/user_sites/<relationship_id>', view_func=user_site, methods=['GET', 'POST'])

# ROLE CONTROLLER
from .role_controller import role, roles, add_role_permissions, remove_role_permissions
role_bp.add_url_rule('/roles', view_func=roles, methods=['GET', 'POST'])
role_bp.add_url_rule('/roles/<role_id>', view_func=role,
                     methods=['GET', 'PUT', 'DELETE'])
role_bp.add_url_rule('/roles/<role_id>/add_permissions/<permission_id>', 
                     view_func=add_role_permissions, methods=['PUT'])
role_bp.add_url_rule('/roles/<role_id>/remove_permissions/<permission_id>', 
                     view_func=remove_role_permissions, methods=['PUT'])

#PERMISSIONS CONTROLLER 
from .permissions_controller import permissions, permission, permissions_by_group
permissions_bp.add_url_rule('/permissions', view_func=permissions, methods=['GET', 'POST'])
permissions_bp.add_url_rule('/permissions/<string:permission_id>', view_func=permission, methods=['GET', 'PUT', 'DELETE'])
permissions_bp.add_url_rule('/permissions/permissions_by_group', view_func=permissions_by_group, methods=['GET'])
# SEARCH_RESULT CONTROLLER
from .search_result_controller import search_results, search_result
search_results_bp.add_url_rule(
    '/search_results', view_func=search_results, methods=['GET', 'POST'])
search_results_bp.add_url_rule('/search_results/<result_id>',
                               view_func=search_result, methods=['GET', 'PUT', 'DELETE'])

# SITE CONTROLLER
from .site_controller import site_stats, sites, site, search_sites
site_bp.add_url_rule('/sites', view_func=sites, methods=['GET', 'POST'])
site_bp.add_url_rule('/sites/<site_id>', view_func=site,
                     methods=['GET', 'PUT', 'DELETE'])
site_bp.add_url_rule('/sites/<site_id>/stats',
                     view_func=site_stats, methods=['GET'])
user_sites_bp.add_url_rule(
    '/sites/search>', view_func=search_sites, methods=['GET'])

# SITE_STATS CONTROLLER
from .site_stats_controller import site_stat, site_stats
site_stats_bp.add_url_rule(
    '/site_stats', view_func=site_stats, methods=['GET', 'POST'])
site_stats_bp.add_url_rule(
    '/site_stats/<stat_id>', view_func=site_stat, methods=['GET', 'PUT', 'DELETE'])









