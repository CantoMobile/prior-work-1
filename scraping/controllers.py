from flask import request, jsonify, abort
from app import app
from models import User, Authentication, AuthToken, Role, Site, SearchResult, UserSite, SiteStats
from werkzeug.security import check_password_hash


@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        users = User.objects.all()
        return jsonify(users)

    elif request.method == 'POST':
        data = request.json
        roles = data.pop('roles', []) # extract roles from data
        user = User(
            name=data['name'], 
            email=data['email'], 
            password=data['password'], 
            roles=roles
        )
        user.save()
        return jsonify(user)


# Authentication routes
@app.route('/auth', methods=['POST'])
def auth():
    data = request.json
    auth = Authentication.objects(email=data['email']).first()
    if auth and check_password_hash(auth.password_hash, data['password']):
        token = AuthToken(auth.id)
        token.save()
        return jsonify(token)
    else:
        abort(401)


@app.route('/auth/<token>', methods=['DELETE'])
def logout(token):
    token = AuthToken.objects(token=token).first()
    if token:
        token.delete()
        return '', 204
    else:
        abort(404)


@app.route('/roles', methods=['GET'])
def roles():
    roles = Role.objects.all()
    return jsonify(roles)


@app.route('/sites', methods=['GET', 'POST'])
def sites():
    if request.method == 'GET':
        sites = Site.objects.all()
        return jsonify(sites)

    elif request.method == 'POST':
        data = request.json
        site = Site(
            url=data['url'], 
            name=data['name'], 
            description=data['description'], 
            keywords=data['keywords'], 
            media=data['media'], 
            admin_email=data['admin_email']
        )
        site.save()
        return jsonify(site)


@app.route('/search_results', methods=['GET', 'POST'])
def search_results():
    if request.method == 'GET':
        search_results = SearchResult.objects.all()
        return jsonify(search_results)

    elif request.method == 'POST':
        data = request.json
        site = Site.objects.get(id=data['site_id'])
        search_result = SearchResult(query_string=data['query_string'], results=data['results'], site=site)
        search_result.save()
        return jsonify(search_result)


@app.route('/user_sites', methods=['GET', 'POST'])
def user_sites():
    if request.method == 'GET':
        user_sites = UserSite.objects.all()
        return jsonify(user_sites)

    elif request.method == 'POST':
        data = request.json
        user = User.objects.get(id=data['user_id'])
        site = Site.objects.get(id=data['site_id'])
        user_site = UserSite(user=user, site=site)
        user_site.save()
        return jsonify(user_site)


@app.route('/site_stats', methods=['GET', 'POST'])
def site_stats():
    if request.method == 'GET':
        site_stats = SiteStats.objects.all()
        return jsonify(site_stats)

    elif request.method == 'POST':
        data = request.json
        site = Site.objects.get(id=data['site_id'])
        site_stats = SiteStats(site=site, visits=data['visits'], unique_visitors=data['unique_visitors'], last_visit=data['last_visit'])
        site_stats.save()
        return jsonify(site_stats)