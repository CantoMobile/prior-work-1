from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from app.utils.logger import logger
import heapq
import uuid
import datetime


def generate_random_id():
    return str(uuid.uuid4())


class Site:

    def __init__(self, url, name, description=None, logo=None, keywords=None, media=None, admin_email=None, site_stats=None, _id=generate_random_id()):
        self.url = url
        self.name = name
        self.description = description
        self.logo = logo
        self.keywords = keywords or []
        self.media = media or []
        self.admin_email = admin_email
        self.site_stats = site_stats if site_stats is not None else {"saves": 0}
        if _id is not None:
            if isinstance(_id, str):
                self._id = _id
            else:
                self._id = _id

    def serialize(self):
        return {
            'id': str(self.id),
            'url': self.url,
            'name': self.name,
            'description': self.description,
            'logo': self.logo,
            'keywords': self.keywords,
            'media': self.media,
            'admin_email': self.admin_email,
            'site_stats': self.site_stats
        }

class User:
    def __init__(self, name, email, password, auth_provider=None, sites=None, role=None, created_at=None, _id=generate_random_id()):
        self.name = name
        self.email = email
        self.password = password
        self.auth_provider = auth_provider
        self.sites = sites or {}
        self.role = role  # or []
        if created_at is None:
            self.created_at = datetime.datetime.now()
        else:
            self.created_at = created_at

        if _id is not None:
            if isinstance(_id, str):
                self._id = _id
            else:
                self._id = _id

    def verify_password(self, password):
        return self.password == password

    def set_password(self, password):
        if self.password == password:
            return None
        elif len(password) > 10:
            self.password = password
            return True
        else:
            return False

    # def serialize(self):
    #     return {
    #         'name': self.name,
    #         'email': self.email,
    #         'password': self.password,
    #         'sites': self.sites,
    #         'created_at': self.created_at
    # }





site_data = [
    # News Websites
    Site(
        url="https://www.cnn.com",
        name="CNN",
        description="News and Information",
        keywords=["news", "current events", "politics", "world", "opinions"]
    ),
    Site(
        url="https://www.bbc.com/news",
        name="BBC News",
        description="UK and World News",
        keywords=["news", "world events", "international", "business", "sports"]
    ),
    Site(
        url="https://www.nytimes.com",
        name="The New York Times",
        description="Newspaper",
        keywords=["news", "politics", "culture", "science", "technology"]
    ),
    Site(
        url="https://www.aljazeera.com",
        name="Al Jazeera",
        description="Media Network",
        keywords=["news", "world news", "opinions", "analysis", "investigations"]
    ),
    Site(
        url="https://www.reuters.com",
        name="Reuters",
        description="International News Agency",
        keywords=["news", "business", "finance", "politics", "technology"]
    ),

    # E-commerce Stores
    Site(
        url="https://www.amazon.com",
        name="Amazon",
        description="Online Shopping",
        keywords=["e-commerce", "online store", "shopping", "products", "electronics"]
    ),
    Site(
        url="https://www.ebay.com",
        name="eBay",
        description="Online Marketplace",
        keywords=["e-commerce", "auction", "buy", "sell", "bidding"]
    ),
    Site(
        url="https://www.walmart.com",
        name="Walmart",
        description="Retail Company",
        keywords=["e-commerce", "shopping", "retail", "discounts", "groceries"]
    ),
    Site(
        url="https://www.etsy.com",
        name="Etsy",
        description="Handmade and Vintage Items",
        keywords=["e-commerce", "handmade", "crafts", "vintage", "art"]
    ),
    Site(
        url="https://www.target.com",
        name="Target",
        description="Retail Chain",
        keywords=["e-commerce", "shopping", "retail", "clothing", "home"]
    ),

    # Social Media Platforms
    Site(
        url="https://www.facebook.com",
        name="Facebook",
        description="Social Networking",
        keywords=["social media", "social networking", "friends", "posts", "communication"]
    ),
    Site(
        url="https://twitter.com",
        name="Twitter",
        description="Social Media and Microblogging",
        keywords=["social media", "tweets", "microblogging", "news", "communication"]
    ),
    Site(
        url="https://www.instagram.com",
        name="Instagram",
        description="Photo and Video Sharing",
        keywords=["social media", "photos", "videos", "sharing", "visuals"]
    ),
    Site(
        url="https://www.linkedin.com",
        name="LinkedIn",
        description="Professional Network",
        keywords=["social media", "professional networking", "jobs", "career", "business"]
    ),
    Site(
        url="https://www.pinterest.com",
        name="Pinterest",
        description="Visual Discovery",
        keywords=["social media", "visual discovery", "inspiration", "ideas", "crafts"]
    ),
    # Educational Resources
    Site(
        url="https://www.khanacademy.org",
        name="Khan Academy",
        description="Online Learning Platform",
        keywords=["education", "learning", "courses", "videos", "mathematics"]
    ),
    Site(
        url="https://www.coursera.org",
        name="Coursera",
        description="Online Education Platform",
        keywords=["education", "online courses", "certificates", "degrees", "universities"]
    ),
    Site(
        url="https://www.edx.org",
        name="edX",
        description="Online Learning Platform",
        keywords=["education", "courses", "online learning", "universities", "certifications"]
    ),
    Site(
        url="https://www.ted.com",
        name="TED",
        description="Ideas Worth Spreading",
        keywords=["education", "TED Talks", "inspirational", "ideas", "knowledge"]
    ),
    Site(
        url="https://www.codecademy.com",
        name="Codecademy",
        description="Interactive Learning Platform",
        keywords=["education", "coding", "programming", "web development", "data science"]
    ),

    # Travel and Tourism Websites
    Site(
        url="https://www.tripadvisor.com",
        name="TripAdvisor",
        description="Travel Platform",
        keywords=["travel", "hotels", "restaurants", "reviews", "destinations"]
    ),
    Site(
        url="https://www.expedia.com",
        name="Expedia",
        description="Travel Booking Site",
        keywords=["travel", "flights", "hotels", "vacations", "packages"]
    ),
    Site(
        url="https://www.airbnb.com",
        name="Airbnb",
        description="Short-term Accommodations",
        keywords=["travel", "accommodations", "rentals", "vacation homes", "experiences"]
    ),
    Site(
        url="https://www.lonelyplanet.com",
        name="Lonely Planet",
        description="Travel Guides and Tips",
        keywords=["travel", "destination guides", "tips", "adventures", "exploration"]
    ),
    Site(
        url="https://www.booking.com",
        name="Booking.com",
        description="Travel Accommodations",
        keywords=["travel", "hotels", "accommodations", "booking", "reservations"]
    ),

    # Health and Fitness Websites
    Site(
        url="https://www.webmd.com",
        name="WebMD",
        description="Health Information",
        keywords=["health", "medical information", "symptoms", "conditions", "wellness"]
    ),
    Site(
        url="https://www.healthline.com",
        name="Healthline",
        description="Health and Wellness",
        keywords=["health", "wellness", "nutrition", "fitness", "medical information"]
    ),
    Site(
        url="https://www.myfitnesspal.com",
        name="MyFitnessPal",
        description="Health and Fitness App",
        keywords=["health", "fitness", "nutrition", "calorie counter", "exercise tracking"]
    ),
    Site(
        url="https://www.mayoclinic.org",
        name="Mayo Clinic",
        description="Medical Care and Research",
        keywords=["health", "medical care", "research", "patient care", "diseases"]
    ),
    Site(
        url="https://www.menshealth.com",
        name="Men's Health",
        description="Men's Lifestyle and Fitness",
        keywords=["health", "fitness", "nutrition", "workouts", "lifestyle"]
    ),

    # Entertainment Portals
    Site(
        url="https://www.imdb.com",
        name="IMDb",
        description="Movies and TV Shows",
        keywords=["entertainment", "movies", "TV shows", "actors", "reviews"]
    ),
    Site(
        url="https://www.rottentomatoes.com",
        name="Rotten Tomatoes",
        description="Movie Reviews and Ratings",
        keywords=["entertainment", "movie reviews", "film ratings", "critics", "audience"]
    ),
    Site(
        url="https://variety.com",
        name="Variety",
        description="Entertainment News",
        keywords=["entertainment", "film", "TV", "celebrities", "industry news"]
    ),
    Site(
        url="https://ew.com",
        name="Entertainment Weekly",
        description="Entertainment News",
        keywords=["entertainment", "movies", "TV shows", "celebrities", "pop culture"]
    ),
    Site(
        url="https://www.vulture.com",
        name="Vulture",
        description="Entertainment News and Features",
        keywords=["entertainment", "pop culture", "TV", "movies", "celebrities"]
    ),

    # Technology Blogs
    Site(
        url="https://techcrunch.com",
        name="TechCrunch",
        description="Technology News and Reviews",
        keywords=["technology", "startups", "gadgets", "apps", "innovation"]
    ),
    Site(
        url="https://www.theverge.com",
        name="The Verge",
        description="Technology News and Media Network",
        keywords=["technology", "gadgets", "reviews", "science", "innovation"]
    ),
    Site(
        url="https://www.wired.com",
        name="Wired",
        description="Technology Magazine and Website",
        keywords=["technology", "science", "gadgets", "culture", "innovation"]
    ),
    Site(
        url="https://gizmodo.com",
        name="Gizmodo",
        description="Technology and Gadget Blog",
        keywords=["technology", "gadgets", "reviews", "science", "innovation"]
    ),
    Site(
        url="https://mashable.com",
        name="Mashable",
        description="Digital Media Website",
        keywords=["technology", "digital culture", "entertainment", "tech news", "social media"]
    ),

    # Food and Recipe Websites
    Site(
        url="https://www.allrecipes.com",
        name="AllRecipes",
        description="Recipes and Cooking",
        keywords=["food", "recipes", "cooking", "baking", "meal ideas"]
    ),
    Site(
        url="https://www.foodnetwork.com",
        name="Food Network",
        description="Food and Cooking Shows",
        keywords=["food", "cooking shows", "recipes", "chefs", "restaurants"]
    ),
    Site(
        url="https://www.bonappetit.com",
        name="Bon Appétit",
        description="Food and Cooking Magazine",
        keywords=["food", "cooking", "recipes", "restaurants", "entertaining"]
    ),
    Site(
        url="https://www.epicurious.com",
        name="Epicurious",
        description="Recipes and Cooking",
        keywords=["food", "recipes", "cooking", "ingredients", "entertaining"]
    ),
    Site(
        url="https://www.seriouseats.com",
        name="Serious Eats",
        description="Food and Cooking Blog",
        keywords=["food", "cooking", "recipes", "techniques", "entertaining"]
    ),

    # Sports News Sites
    Site(
        url="https://www.espn.com",
        name="ESPN",
        description="Sports News and Scores",
        keywords=["sports", "sports news", "scores", "athletes", "events"]
    ),
    Site(
        url="https://www.si.com",
        name="Sports Illustrated",
        description="Sports News and Magazine",
        keywords=["sports", "sports news", "scores", "athletes", "events"]
    ),
    Site(
        url="https://bleacherreport.com",
        name="Bleacher Report",
        description="Sports News and Highlights",
        keywords=["sports", "sports news", "highlights", "athletes", "teams"]
    ),
    Site(
        url="https://www.cbssports.com",
        name="CBS Sports",
        description="Sports News and Scores",
        keywords=["sports", "sports news", "scores", "athletes", "events"]
    ),
    Site(
        url="https://theathletic.com",
        name="The Athletic",
        description="Sports News and Analysis",
        keywords=["sports", "sports news", "analysis", "athletes", "teams"]
    ),

    # Fashion and Lifestyle Blogs
    Site(
        url="https://www.vogue.com",
        name="Vogue",
        description="Fashion and Lifestyle Magazine",
        keywords=["fashion", "style", "designers", "celebrities", "runway"]
    ),
    Site(
        url="https://www.gq.com",
        name="GQ",
        description="Men's Fashion and Style",
        keywords=["fashion", "men's style", "grooming", "celebrities", "culture"]
    ),
    Site(
        url="https://www.refinery29.com",
        name="Refinery29",
        description="Women's Lifestyle and Fashion",
        keywords=["fashion", "women's style", "beauty", "wellness", "culture"]
    ),
    Site(
        url="https://www.thecut.com",
        name="The Cut",
        description="Fashion and Style",
        keywords=["fashion", "style", "beauty", "culture", "celebrities"]
    ),
    Site(
        url="https://www.manrepeller.com",
        name="Man Repeller",
        description="Fashion and Lifestyle Blog",
        keywords=["fashion", "style", "lifestyle", "culture", "trends"]
    ),

    # Business and Finance Websites
    Site(
        url="https://www.forbes.com",
        name="Forbes",
        description="Business News and Financial Information",
        keywords=["business", "finance", "entrepreneurs", "investing", "wealth"]
    ),
    Site(
        url="https://www.bloomberg.com",
        name="Bloomberg",
        description="Financial News and Data",
        keywords=["business", "finance", "markets", "economy", "technology"]
    ),
    Site(
        url="https://www.cnbc.com",
        name="CNBC",
        description="Business News and Financial Information",
        keywords=["business", "finance", "stock market", "investing", "economy"]
    ),
    Site(
        url="https://www.wsj.com",
        name="The Wall Street Journal",
        description="Business and Financial News",
        keywords=["business", "finance", "news", "economy", "investing"]
    ),
    Site(
        url="https://www.ft.com",
        name="Financial Times",
        description="Business and Financial News",
        keywords=["business", "finance", "markets", "economy", "global news"]
    ),

    # Gaming Portals
    Site(
        url="https://www.ign.com",
        name="IGN",
        description="Gaming News and Reviews",
        keywords=["gaming", "video games", "reviews", "previews", "gamer"]
    ),
    Site(
        url="https://www.polygon.com",
        name="Polygon",
        description="Gaming News and Reviews",
        keywords=["gaming", "video games", "reviews", "news", "culture"]
    ),
    Site(
        url="https://kotaku.com",
        name="Kotaku",
        description="Gaming News and Features",
        keywords=["gaming", "video games", "news", "culture", "features"]
    ),
    Site(
        url="https://www.pcgamer.com",
        name="PC Gamer",
        description="PC Gaming News and Reviews",
        keywords=["gaming", "PC games", "reviews", "hardware", "enthusiast"]
    ),
    Site(
        url="https://www.gamespot.com",
        name="GameSpot",
        description="Gaming News and Reviews",
        keywords=["gaming", "video games", "reviews", "news", "trailers"]
    ),

    # Music Streaming Platforms
    Site(
        url="https://www.spotify.com",
        name="Spotify",
        description="Music Streaming Service",
        keywords=["music", "streaming", "playlists", "artists", "genres"]
    ),
    Site(
        url="https://www.apple.com/apple-music",
        name="Apple Music",
        description="Music Streaming Service",
        keywords=["music", "streaming", "playlists", "artists", "genres"]
    ),
    Site(
        url="https://www.pandora.com",
        name="Pandora",
        description="Music Streaming and Internet Radio",
        keywords=["music", "streaming", "internet radio", "playlists", "genres"]
    ),
    Site(
        url="https://soundcloud.com",
        name="SoundCloud",
        description="Music and Audio Streaming Platform",
        keywords=["music", "streaming", "audio", "artists", "genres"]
    ),
    Site(
        url="https://tidal.com",
        name="Tidal",
        description="Music Streaming Service",
        keywords=["music", "streaming", "playlists", "artists", "genres"]
    ),

    # Job Search Portals
    Site(
        url="https://www.indeed.com",
        name="Indeed",
        description="Job Search Engine",
        keywords=["jobs", "job search", "employment", "resumes", "career"]
    ),
    Site(
        url="https://www.linkedin.com/jobs",
        name="LinkedIn Jobs",
        description="Job Search and Networking",
        keywords=["jobs", "job search", "networking", "employment", "career"]
    ),
    Site(
        url="https://www.glassdoor.com",
        name="Glassdoor",
        description="Job Search and Company Reviews",
        keywords=["jobs", "job search", "company reviews", "employment", "career"]
    ),
    Site(
        url="https://www.monster.com",
        name="Monster",
        description="Job Search Engine",
        keywords=["jobs", "job search", "employment", "resumes", "career"]
    ),
    Site(
        url="https://www.ziprecruiter.com",
        name="ZipRecruiter",
        description="Job Search and Employment",
        keywords=["jobs", "job search", "employment", "resumes", "career"]
    ),
]

user_data = [
    # User 1
    User(
        name="User 1",
        email="user1@example.com",
        password="password1",
        sites=['Amazon', 'eBay', 'CNN', 'TED']
    ),

    # User 2
    User(
        name="User 2",
        email="user2@example.com",
        password="password2",
        sites=['Facebook', 'Twitter', 'LinkedIn Jobs', 'Indeed']
    ),

    # User 3
    User(
        name="User 3",
        email="user3@example.com",
        password="password3",
        sites=['Coursera', 'edX', 'Codecademy', 'Airbnb']
    ),

    # User 4
    User(
        name="User 4",
        email="user4@example.com",
        password="password4",
        sites=['WebMD', 'Healthline', 'MyFitnessPal', 'Men\'s Health']
    ),

    # User 5
    User(
        name="User 5",
        email="user5@example.com",
        password="password5",
        sites=['Bloomberg', 'Forbes', 'CNBC', 'The Wall Street Journal']
    ),

    # User 6
    User(
        name="User 6",
        email="user6@example.com",
        password="password6",
        sites=['Vogue', 'GQ', 'Refinery29', 'The Cut']
    ),

    # User 7
    User(
        name="User 7",
        email="user7@example.com",
        password="password7",
        sites=['IGN', 'Polygon', 'Kotaku', 'PC Gamer']
    ),

    # User 8
    User(
        name="User 8",
        email="user8@example.com",
        password="password8",
        sites=['Spotify', 'Apple Music', 'Pandora', 'SoundCloud']
    ),

    # User 9
    User(
        name="User 9",
        email="user9@example.com",
        password="password9",
        sites=['Indeed', 'LinkedIn Jobs', 'Glassdoor', 'Monster']
    ),

    # User 10
    User(
        name="User 10",
        email="user10@example.com",
        password="password10",
        sites=['TripAdvisor', 'Expedia', 'Airbnb', 'Lonely Planet']
    ),

    # User 11
    User(
        name="User 11",
        email="user11@example.com",
        password="password11",
        sites=['IMDb', 'Rotten Tomatoes', 'Variety', 'Entertainment Weekly']
    ),

    # User 12
    User(
        name="User 12",
        email="user12@example.com",
        password="password12",
        sites=['TechCrunch', 'The Verge', 'Wired', 'Gizmodo']
    ),

    # User 13
    User(
        name="User 13",
        email="user13@example.com",
        password="password13",
        sites=['AllRecipes', 'Food Network', 'Bon Appétit', 'Epicurious']
    ),

    # User 14
    User(
        name="User 14",
        email="user14@example.com",
        password="password14",
        sites=['ESPN', 'Sports Illustrated', 'Bleacher Report', 'CBS Sports']
    ),

    # User 15
    User(
        name="User 15",
        email="user15@example.com",
        password="password15",
        sites=['CNN', 'BBC News', 'The New York Times', 'Al Jazeera']
    ),

    # User 16
    User(
        name="User 16",
        email="user16@example.com",
        password="password16",
        sites=['Vogue', 'GQ', 'Refinery29', 'The Cut']
    ),

    # User 17
    User(
        name="User 17",
        email="user17@example.com",
        password="password17",
        sites=['IGN', 'Polygon', 'Kotaku', 'PC Gamer']
    ),

    # User 18
    User(
        name="User 18",
        email="user18@example.com",
        password="password18",
        sites=['Spotify', 'Apple Music', 'Pandora', 'SoundCloud']
    ),

    # User 19
    User(
        name="User 19",
        email="user19@example.com",
        password="password19",
        sites=['Indeed', 'LinkedIn Jobs', 'Glassdoor', 'Monster']
    ),

    # User 20
    User(
        name="User 20",
        email="user20@example.com",
        password="password20",
        sites=['TripAdvisor', 'Expedia', 'Airbnb', 'Lonely Planet']
    ),

    # User 21
    User(
        name="User 21",
        email="user21@example.com",
        password="password21",
        sites=['IMDb', 'Rotten Tomatoes', 'Variety', 'Entertainment Weekly']
    ),

    # User 22
    User(
        name="User 22",
        email="user22@example.com",
        password="password22",
        sites=['TechCrunch', 'The Verge', 'Wired', 'Gizmodo']
    ),

    # User 23
    User(
        name="User 23",
        email="user23@example.com",
        password="password23",
        sites=['AllRecipes', 'Food Network', 'Bon Appétit', 'Epicurious']
    ),

    # User 24
    User(
        name="User 24",
        email="user24@example.com",
        password="password24",
        sites=['ESPN', 'Sports Illustrated', 'Bleacher Report', 'CBS Sports']
    ),

    # User 25
    User(
        name="User 25",
        email="user25@example.com",
        password="password25",
        sites=['CNN', 'BBC News', 'The New York Times', 'Al Jazeera']
    ),

    # User 26
    User(
        name="User 26",
        email="user26@example.com",
        password="password26",
        sites=['Amazon', 'eBay', 'Walmart', 'Etsy']
    ),

    # User 27
    User(
        name="User 27",
        email="user27@example.com",
        password="password27",
        sites=['Facebook', 'Twitter', 'Instagram', 'Pinterest']
    ),

    # User 28
    User(
        name="User 28",
        email="user28@example.com",
        password="password28",
        sites=['Khan Academy', 'Coursera', 'edX', 'TED']
    ),

    # User 29
    User(
        name="User 29",
        email="user29@example.com",
        password="password29",
        sites=['WebMD', 'Healthline', 'MyFitnessPal', 'Mayo Clinic']
    ),

    # User 30
    User(
        name="User 30",
        email="user30@example.com",
        password="password30",
        sites=['Forbes', 'Bloomberg', 'CNBC', 'The Wall Street Journal']
    ),

    # User 31
    User(
        name="User 31",
        email="user31@example.com",
        password="password30",
        sites=['IGN', 'Polygon', 'Kotaku', 'PC Gamer']
    )

]




# Assuming the following data is already available
# user_data: List of User objects
# site_data: List of Site objects

class HybridModel:
    def __init__(self, user_data, site_data, user_similarity_weight=0.5, site_similarity_weight=0.5):
        self.user_data = user_data
        self.site_data = site_data
        self.user_similarity_weight = user_similarity_weight
        self.site_similarity_weight = site_similarity_weight
        self.user_site_matrix = self.build_user_site_matrix()
        self.site_keyword_matrix = self.build_site_keyword_matrix()

    def build_user_site_matrix(self):
        user_site_matrix = defaultdict(dict)
        for user in self.user_data:
            for site in user['sites']:
                user_name = user['name']
                user_site_matrix[user_name][site['name']] = 1
        return user_site_matrix

    def build_site_keyword_matrix(self):
        site_names = [site['name'] for site in self.site_data]
        keywords = [' '.join(site['keywords']) for site in self.site_data]
        vectorizer = TfidfVectorizer()
        site_keyword_matrix = vectorizer.fit_transform(keywords)
        return dict(zip(site_names, site_keyword_matrix))

    def compute_user_similarity_scores(self, user_name, user_id):
        user_sites = self.user_site_matrix[user_name]
        user_sites_set = set(user_sites.keys())
        similarity_scores = defaultdict(int)
        for user in self.user_data:
            if user['name'] != user_name:
                other_user_sites = self.user_site_matrix[user['name']]
                other_user_sites_set = set(other_user_sites.keys())
                common_sites = user_sites_set.intersection(other_user_sites_set)
                if len(common_sites) > 0:
                    similarity_scores[user['name']] = len(common_sites) / (len(user_sites_set) + len(other_user_sites_set))
                else:
                    similarity_scores[user['name']] = 0.0  # Set default similarity score to 0.0
        return similarity_scores

    def compute_site_similarity_scores(self, user_name):
        user_sites = self.user_site_matrix[user_name]
        user_sites_set = set(user_sites.keys())
        user_keywords = ' '.join([site.keywords for site in self.site_data if site.name in user_sites_set])
        vectorizer = TfidfVectorizer()
        user_keywords_matrix = vectorizer.fit_transform([user_keywords])
        site_similarity_scores = defaultdict(int)
        for site in self.site_data:
            if site['name'] not in user_sites_set:
                site_keywords_matrix = self.site_keyword_matrix[site['name']]
                cosine_sim = linear_kernel(user_keywords_matrix, site_keywords_matrix).flatten()[0]
                site_similarity_scores[site['name']] = cosine_sim
        return site_similarity_scores

    def get_user_sites(self, user_name):
        user_sites = []
        for user in self.user_data:
            if user['name'] == user_name:
                user_sites = [site['name'] for site in user['sites'] or []]
        return user_sites

    def get_similar_users(self, user_id, user_name, num_users=5):
        user_similarity_scores = self.compute_user_similarity_scores(user_name, user_id)
        similar_users = dict(sorted(user_similarity_scores.items(), key=lambda x: x[1], reverse=True)[:num_users])
        print(f'similar users 1 {similar_users}')
        return similar_users

    def get_similar_sites(self, user_sites, num_sites=10):
        combined_keywords = set()
        for site in user_sites:
            site = self.get_site_by_name(site)
            combined_keywords.update(site['keywords'])
        user_keywords = ' '.join(combined_keywords)
        vectorizer = TfidfVectorizer()
        user_keywords_matrix = vectorizer.fit_transform([user_keywords])

        site_similarity_scores = {}
        for site in self.site_data:
            if site not in user_sites:
                site_keywords = ' '.join(site['keywords'])
                site_keywords_matrix = vectorizer.transform([site_keywords])
                cosine_sim = linear_kernel(user_keywords_matrix, site_keywords_matrix).flatten()[0]
                site_similarity_scores[site['name']] = cosine_sim

        similar_sites = heapq.nlargest(num_sites, site_similarity_scores.items(), key=lambda x: x[1])
        return [site for site, _ in similar_sites]


    def get_user_by_id(self, user_id):
        for user in self.user_data:
            if user['_id'] == user_id:
                return user

    def get_user_by_name(self, user_name):
        for user in self.user_data:
            if user['name'] == user_name:
                return user['_id']

    def get_site_by_name(self, site_name):
        for site in self.site_data:
            if site['name'] ==site_name:
                return site

    def normalize_scores(self, scores):
        if not scores:
            return scores
        max_score = max(scores.values())
        min_score = min(scores.values())
        if max_score == min_score:
            return {item_id: 1.0 for item_id in scores}
        normalized_scores = {
            item_id: (score - min_score) / (max_score - min_score)
            for item_id, score in scores.items()
        }
        return normalized_scores

    def get_user_hybrid_recommendations(self, user_id, user_name):
        user_sites = self.get_user_sites(user_name)
        if not user_sites:
            return {"message": "User has no saved sites."}  # Or you can return some default recommendations here

        similar_sites = self.get_similar_sites(user_sites)
        similar_users = self.get_similar_users(user_id, user_name)

        # Combine the keywords from user's saved sites and similar sites
        combined_keywords = set()
        for site in user_sites:
            site = self.get_site_by_name(site)
            combined_keywords.update(site['keywords'])
        for site in similar_sites:
            site = self.get_site_by_name(site)
            combined_keywords.update(site['keywords'])

        # Convert the set of keywords to a single string for vectorization
        user_keywords = ' '.join(combined_keywords)

        # Compute the user and site keyword matrices using the same vectorizer and set of keywords
        vectorizer = TfidfVectorizer()
        combined_keywords_matrix = vectorizer.fit_transform([user_keywords] + [' '.join(self.get_site_by_name(site)['keywords']) for site in similar_sites])
        # Split the combined keywords matrix back into user_keywords_matrix and site_keywords_matrix
        num_similar_sites = len(similar_sites)
        user_keywords_matrix = combined_keywords_matrix[:1]
        site_keywords_matrix = combined_keywords_matrix[1:num_similar_sites + 1]

        # Compute the user and site similarity scores
        user_similarity_scores = self.compute_user_similarity_scores(user_name, user_id)
        site_similarity_scores = {}
        for site, site_keywords_vector in zip(similar_sites, site_keywords_matrix):
            cosine_sim = linear_kernel(user_keywords_matrix, site_keywords_vector).flatten()[0]
            site_similarity_scores[self.get_site_by_name(site)['name']] = cosine_sim
        

        print("User Similarity Scores:", user_similarity_scores)
        print("Site Similarity Scores:", site_similarity_scores)

        # user_similarity_scores = self.normalize_scores(user_similarity_scores)
        # site_similarity_scores = self.normalize_scores(site_similarity_scores)


        # Combine the two approaches to get hybrid recommendations
        hybrid_recommendations = {}
        print(f'similar users: {similar_users}')
        for user in similar_users:
            user_saved_sites = self.get_user_sites(user)
            for site_name in user_saved_sites:
                if site_name not in user_sites:
                    score = user_similarity_scores[user]
                    hybrid_recommendations[site_name] = hybrid_recommendations.get(site_name, 0) + score

        for site in similar_sites:
            site_name = self.get_site_by_name(site)['name']
            if site_name not in user_sites:
                score = site_similarity_scores[site_name]
                hybrid_recommendations[site_name] = hybrid_recommendations.get(site_name, 0) + score

        # Sort the recommendations based on scores in descending order
        sorted_recommendations = dict(sorted(hybrid_recommendations.items(), key=lambda x: x[1], reverse=True))
        return sorted_recommendations


# # Usage example:
# hybrid_model = HybridModel(user_data, site_data)
# user_name = "User 2"
# user_id = hybrid_model.get_user_by_name(user_name)
# # print(hybrid_model.user_site_matrix)
# recommendations = hybrid_model.get_user_hybrid_recommendations(user_id, user_name)
# print(recommendations)
