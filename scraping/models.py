from database import db


class User(db.Document):
    name = db.StringField(required=True)
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True)
    auth_id = db.ReferenceField(Authentication)
    auth_provider = db.StringField()
    sites = db.ListField(db.ReferenceField('Site'))
    roles = db.ListField(db.ReferenceField('Role'))
    created_at = db.DateTimeField(default=datetime.now)

    def __repr__(self):
        return f"User(name='{self.name}', email='{self.email}')"
    

class Authentication(db.Document):
    email = db.StringField(required=True, unique=True)
    password_hash = db.StringField(required=True)


class Authorization(db.Document):
    user_id = db.ReferenceField(User)
    role_id = db.ReferenceField(Role)
    permission_id = db.ReferenceField(Permission)


class AuthToken(db.Document):
    user = db.ReferenceField('User', required=True)
    token = db.StringField(required=True)
    created_at = db.DateTimeField(default=datetime.now)

    def __repr__(self):
        return f"AuthToken(user='{self.user.email}', token='{self.token}')"

    

class Role(db.Document):
    name = db.StringField(required=True)
    description = db.StringField()
    permissions = db.ListField(db.StringField())

    def __repr__(self):
        return f"Role(name='{self.name}')"


class Site(db.Document):
    url = db.URLField(required=True, unique=True)
    name = db.StringField(required=True)
    description = db.StringField()
    keywords = db.ListField(db.StringField())
    media = db.ListField(db.URLField())
    admin_email = db.EmailField()
    site_stats = db.ReferenceField('SiteStats')

    def __repr__(self):
        return f"Site(name='{self.name}', url='{self.url}')"

    def serialize(self):
        return {
            'id': str(self.id),
            'url': self.url,
            'name': self.name,
            'description': self.description,
            'keywords': self.keywords,
            'media': self.media,
            'admin_email': self.admin_email,
            'site_stats': str(self.site_stats.id) if self.site_stats else None
        }


class SearchResult(db.Document):
    query_string = db.StringField(required=True)
    results = db.ListField(db.StringField())
    site = db.ReferenceField('Site')

    def __repr__(self):
        return f"SearchResult(query_string='{self.query_string}')"


class UserSite(db.Document):
    user = db.ReferenceField('User', required=True)
    site = db.ReferenceField('Site', required=True)

    def __repr__(self):
        return f"UserSite(user='{self.user.name}', site='{self.site.name}')"


class SiteStats(db.Document):
    site = db.ReferenceField('Site', required=True)
    visits = db.IntField(default=0)
    unique_visitors = db.IntField(default=0)
    last_visit = db.DateTimeField()

    def __repr__(self):
        return f"SiteStats(site='{self.site.name}')"


