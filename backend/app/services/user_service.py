import re
from bson import ObjectId
import dns.resolver
from flask import abort, jsonify, request
from app.repositories.user_repository import UserRepository
from app.repositories.role_repository import RoleRepository
from app.services.auth_service import AuthService
from app.repositories.user_site_repository import UserSiteRepository
from app.services.user_site_service import create_relationship, delete_relationship
from app.repositories.site_repository import SiteRepository
from app.models.user_model import User
from app.models.site_model import Site


user_repo = UserRepository()
auth = AuthService()
role_repo = RoleRepository()
site_repo = SiteRepository()
user_site_repo = UserSiteRepository()


def get_all_users(page=None):
    if page is not None:
        users_data = user_repo.findAll(page, 15)
    else:
        users_data = user_repo.findAll()
    return users_data


def get_one_user(user_id):
    user = user_repo.findById(user_id)
    if not user:
        abort(404)
    return user


def create_user(register=False):
    data = request.json
    errors = validate_email_domain(data['email'])
    if errors[0] == False:
        return {"error": errors[1]}, 401

    user = User(
        name=data['name'],
        email=data['email'],
        password=auth.encrypt(data['password'])
    )

    user_data = user_repo.save(user)
    create_relationship(user_data['_id'])
    if register:
        add_user_role(user_data['_id'], "646c0099d72ed166e49c3890")
        return auth.generate_auth_token(user_data, "646c0099d72ed166e49c3890")
    else:
        return jsonify(user_data)


def update_one_user(user_id):
    user_data = get_one_user(user_id)
    data = request.json
    if 'name' in data:
        user_data['name'] = data['name']
    if 'email' in data:
        user_data['email'] = data['email']
    if 'password' in data and user_data['password'] != auth.encrypt(data['password']):
        user_data['password'] = auth.encrypt(data['password'])
    if 'role' in data and role_repo.existsByField('_id', ObjectId(data['role'])):
        user_data['role'] = {'collection': 'role', '_id': data['role']}
    return user_repo.update(user_id, user_data)


def delete_one_user(user_id):
    if user_repo.existsByField('_id', ObjectId(user_id)):
        delete_relationship(user_id)
        return user_repo.delete(user_id)
    else:
        return jsonify({'message': 'This user not exists'}), 304


def add_user_role(user_id, role_id):
    user_data = get_one_user(user_id)
    role_data = role_repo.findById(role_id)
    if user_data['role'] != None:
        if role_id in user_data['role']['_id']:
            return {'Error': 'The user already has the role assigned'}, 304
    else:
        user_data['role'] = {'collection': 'role', '_id': role_data['_id']}
        return user_repo.update(user_id, user_data)


def remove_user_role(user_id, role_id):
    user_data = get_one_user(user_id)
    role_repo.existsByField('_id', ObjectId(role_id))
    if role_repo.existsByField('_id', ObjectId(role_id)) and user_data['role'] != None:
        if role_id in user_data['role']['_id']:
            return user_repo.update(user_id, user_data)
    else:
        return jsonify({"Error": "This role is not associated with this user"}), 304


def add_created_site_user(site_id, user_id):
    user_data = get_one_user(user_id)
    site_data = site_repo.findById(site_id)
    user = User(**user_data)
    site = Site(**site_data)
    validation = any(
        site_item['_id'] == site_id for site_item in user.sites)
    if validation:
        return {'Error': 'The site is already created for this user'}, 404
    else:
        return role_repo.updateArray(site_id, 'sites', site)


def user_authentication():
    data = request.json
    user_data = user_repo.find_by_email(data['email'])
    if not user_data:
        abort(404)
    user = User(**user_data)
    role_id = user_data['role']['_id']
    if user.verify_password(auth.encrypt(data['password'])):
        return auth.generate_auth_token(user_data, role_id)
    else:
        return jsonify({'message': 'Password is incorrect'}), 401


def set_user_password(user_id):
    data = request.json
    user_data = get_one_user(user_id)
    user = User(**user_data)
    response = user.set_password(auth.encrypt(data['password']))
    if response != None and response == True:
        update = user_repo.update(user_id, user)
        return jsonify(update)
    else:
        return {"error": "Failed to update password"}, 304


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
    if exist and email != 'admin@cantonica.com':
        return False, "Email and user all ready exists."

    return True, ""


def save_site_user(user_id, site_id):
    user_data = get_one_user(user_id)
    site_data = site_repo.findById(site_id)
    user = User(**user_data)
    site = Site(**site_data)
    validation = any(
        site_item['_id'] == site_id for site_item in user.sites)
    if validation:
        return {'Error': 'The user already has this site saved'}, 400
    else:
        return user_repo.updateArray(user_id, 'sites', site)


def remove_site_user(site_id, user_id=None):
    if user_id is not None:
        user_data = get_one_user(user_id)
    else:
        user_data = user_repo.findByField('sites._id', ObjectId(site_id))
        if not user_data:
            return None
    site_data = site_repo.findById(site_id)
    user = User(**user_data)
    site = Site(**site_data)
    validation = any(
        site_item['_id'] == site_id for site_item in user.sites)
    if validation:
        return user_repo.deleteFromArray(user_data['_id'], 'sites', site)
    else:
        return {'Error': 'The user not has this site saved'}, 304

def get_created_sites_user(user_id, page=None):
    user_data = user_repo.findById(user_id)
    sites = user_data.get('sites',[])
    created_ids = [site['_id'] for site in sites]

    if page: 
        return site_repo.getReferenced(created_ids, page, 15)
    else:
        return site_repo.getReferenced(created_ids)

