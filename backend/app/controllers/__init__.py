from .user_controller import user_bp
from .role_controller import role_bp
from .site_controller import site_bp
from .site_stats_controller import site_stats_bp
from .permissions_controller import permissions_bp
from .search_result_controller import search_results_bp
from .user_site_controller import user_sites_bp
from .reviews_controller import reviews_bp
from .admin_controller import admin_bp
from .category_controller import category_bp
from .recommendations_controller import recommendations_bp
from .referrals_controller import referrals_bp
from .points_system_controller import points_system_bp
from .user_action_controller import user_actions_bp

__all__ = [
    'user_bp',
    'role_bp',
    'site_bp',
    'site_stats_bp',
    'permissions_bp',
    'search_results_bp',
    'user_sites_bp',
    'reviews_bp',
    'admin_bp',
    'category_bp',
    'recommendations_bp',
    'referrals_bp',
    'points_system_bp',
    'user_actions_bp'
]
