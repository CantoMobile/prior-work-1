from app.models.site_model import Site
from app.models.user_model import User

from app.config.database import Database
from app.utils.logger import logger

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
        saved_sites=['Amazon', 'eBay', 'CNN', 'TED']
    ),

    # User 2
    User(
        name="User 2",
        email="user2@example.com",
        password="password2",
        saved_sites=['Facebook', 'Twitter', 'LinkedIn Jobs', 'Indeed']
    ),

    # User 3
    User(
        name="User 3",
        email="user3@example.com",
        password="password3",
        saved_sites=['Coursera', 'edX', 'Codecademy', 'Airbnb']
    ),

    # User 4
    User(
        name="User 4",
        email="user4@example.com",
        password="password4",
        saved_sites=['WebMD', 'Healthline', 'MyFitnessPal', 'Men\'s Health']
    ),

    # User 5
    User(
        name="User 5",
        email="user5@example.com",
        password="password5",
        saved_sites=['Bloomberg', 'Forbes', 'CNBC', 'The Wall Street Journal']
    ),

    # User 6
    User(
        name="User 6",
        email="user6@example.com",
        password="password6",
        saved_sites=['Vogue', 'GQ', 'Refinery29', 'The Cut']
    ),

    # User 7
    User(
        name="User 7",
        email="user7@example.com",
        password="password7",
        saved_sites=['IGN', 'Polygon', 'Kotaku', 'PC Gamer']
    ),

    # User 8
    User(
        name="User 8",
        email="user8@example.com",
        password="password8",
        saved_sites=['Spotify', 'Apple Music', 'Pandora', 'SoundCloud']
    ),

    # User 9
    User(
        name="User 9",
        email="user9@example.com",
        password="password9",
        saved_sites=['Indeed', 'LinkedIn Jobs', 'Glassdoor', 'Monster']
    ),

    # User 10
    User(
        name="User 10",
        email="user10@example.com",
        password="password10",
        saved_sites=['TripAdvisor', 'Expedia', 'Airbnb', 'Lonely Planet']
    ),

    # User 11
    User(
        name="User 11",
        email="user11@example.com",
        password="password11",
        saved_sites=['IMDb', 'Rotten Tomatoes', 'Variety', 'Entertainment Weekly']
    ),

    # User 12
    User(
        name="User 12",
        email="user12@example.com",
        password="password12",
        saved_sites=['TechCrunch', 'The Verge', 'Wired', 'Gizmodo']
    ),

    # User 13
    User(
        name="User 13",
        email="user13@example.com",
        password="password13",
        saved_sites=['AllRecipes', 'Food Network', 'Bon Appétit', 'Epicurious']
    ),

    # User 14
    User(
        name="User 14",
        email="user14@example.com",
        password="password14",
        saved_sites=['ESPN', 'Sports Illustrated', 'Bleacher Report', 'CBS Sports']
    ),

    # User 15
    User(
        name="User 15",
        email="user15@example.com",
        password="password15",
        saved_sites=['CNN', 'BBC News', 'The New York Times', 'Al Jazeera']
    ),

    # User 16
    User(
        name="User 16",
        email="user16@example.com",
        password="password16",
        saved_sites=['Vogue', 'GQ', 'Refinery29', 'The Cut']
    ),

    # User 17
    User(
        name="User 17",
        email="user17@example.com",
        password="password17",
        saved_sites=['IGN', 'Polygon', 'Kotaku', 'PC Gamer']
    ),

    # User 18
    User(
        name="User 18",
        email="user18@example.com",
        password="password18",
        saved_sites=['Spotify', 'Apple Music', 'Pandora', 'SoundCloud']
    ),

    # User 19
    User(
        name="User 19",
        email="user19@example.com",
        password="password19",
        saved_sites=['Indeed', 'LinkedIn Jobs', 'Glassdoor', 'Monster']
    ),

    # User 20
    User(
        name="User 20",
        email="user20@example.com",
        password="password20",
        saved_sites=['TripAdvisor', 'Expedia', 'Airbnb', 'Lonely Planet']
    ),

    # User 21
    User(
        name="User 21",
        email="user21@example.com",
        password="password21",
        saved_sites=['IMDb', 'Rotten Tomatoes', 'Variety', 'Entertainment Weekly']
    ),

    # User 22
    User(
        name="User 22",
        email="user22@example.com",
        password="password22",
        saved_sites=['TechCrunch', 'The Verge', 'Wired', 'Gizmodo']
    ),

    # User 23
    User(
        name="User 23",
        email="user23@example.com",
        password="password23",
        saved_sites=['AllRecipes', 'Food Network', 'Bon Appétit', 'Epicurious']
    ),

    # User 24
    User(
        name="User 24",
        email="user24@example.com",
        password="password24",
        saved_sites=['ESPN', 'Sports Illustrated', 'Bleacher Report', 'CBS Sports']
    ),

    # User 25
    User(
        name="User 25",
        email="user25@example.com",
        password="password25",
        saved_sites=['CNN', 'BBC News', 'The New York Times', 'Al Jazeera']
    ),

    # User 26
    User(
        name="User 26",
        email="user26@example.com",
        password="password26",
        saved_sites=['Amazon', 'eBay', 'Walmart', 'Etsy']
    ),

    # User 27
    User(
        name="User 27",
        email="user27@example.com",
        password="password27",
        saved_sites=['Facebook', 'Twitter', 'Instagram', 'Pinterest']
    ),

    # User 28
    User(
        name="User 28",
        email="user28@example.com",
        password="password28",
        saved_sites=['Khan Academy', 'Coursera', 'edX', 'TED']
    ),

    # User 29
    User(
        name="User 29",
        email="user29@example.com",
        password="password29",
        saved_sites=['WebMD', 'Healthline', 'MyFitnessPal', 'Mayo Clinic']
    ),

    # User 30
    User(
        name="User 30",
        email="user30@example.com",
        password="password30",
        saved_sites=['Forbes', 'Bloomberg', 'CNBC', 'The Wall Street Journal']
    ),

    # User 31
    User(
        name="User 31",
        email="user31@example.com",
        password="password30",
        saved_sites=['IGN', 'Polygon', 'Kotaku', 'PC Gamer']
    )

]

_db = Database()

db = _db.connect()

# Step 4: Access the 'site_test_data' collection and insert the data
site_test_data_collection = db['site_test_data']

site_docs = [site.serialize() for site in site_data]
site_insert_result = site_test_data_collection.insert_many(site_docs)

logger.info(site_insert_result)