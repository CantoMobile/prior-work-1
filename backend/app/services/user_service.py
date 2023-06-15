import re
import dns.resolver
from flask import abort
from app.repositories.user_repository import UserRepository
from app.repositories.role_repository import RoleRepository
from app.services.auth_service import AuthService
from app.repositories.user_site_repository import UserSiteRepository
from app.repositories.site_repository import SiteRepository


user_repo = UserRepository()
auth = AuthService()
role_repo = RoleRepository()
site_repo = SiteRepository()
user_site_repo = UserSiteRepository()

def validate_email_domain(email):
    # Validate email structure using a regular expression
    email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if not re.match(email_pattern, email):
        return False, "Invalid email format."

    # Check if the domain exists using DNS resolution
    domain = email.split('@')[1]
    try:
        dns.resolver.resolve(domain, 'MX')
    except dns.resolver.NXDOMAIN:
        return False, "Invalid domain."
    
    exist = user_repo.existsByField('email', email)
    if exist:
        return False, "Email and user all ready exists."

    return True, ""

def add_site(user_id, site_id):
    site_data = site_repo.findById(site_id)
    user_site_data = user_site_repo.findByField('user_id', user_id)
    if not user_site_data or not site_data:
        abort(404)
    return role_repo.updateArray(user_site_data['_id'],'site', site_data)

