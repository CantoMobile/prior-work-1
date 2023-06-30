from locust import HttpUser, task, between
class WebsiteTestUser(HttpUser):
    wait_time = between(0.5, 3.0)

    def on_start(self):
        pass

    def on_stop(self):
        pass

    # @task(1)
    # def hello_world(self):
    #     self.client.get("http://127.0.0.1:5000/site_stats/top6_saved")

    
    # @task(2)
    # def test_sites(self):
    #     self.client.get("http://127.0.0.1:5000/sites/")

    # @task(3)
    # def test_site_update(self):
    #     self.client.put("http://127.0.0.1:5000/sites/64968b73ca090471568569e2/64968a1dd7d93fbf1791db2c", 
    #                     json={"url": "https://www.linkedin.com", "name": "linkedin",  "description": "professional social media site for job searchers and employers alike", "keywords": ["networking", "job searching", "social media"], "admin_email": "admin@linkedin.com"})

    @task(4)
    def test_adding_sites(self):
        self.client.post("http://127.0.0.1:5000/sites/add_site",
                        json={"url": "https://www.samsung.com", "name": "samsung",  "description": "technology manufacturer and distributor", "keywords": ["technology", "devices", "software"], "admin_email": "admin@samsung.com"})
        
    @task(5)
    def test_adding_reviews(self):
        self.client.post("http://127.0.0.1:5000/sites/add_site",
                        json={"url": "https://www.samsung.com", "name": "samsung",  "description": "technology manufacturer and distributor", "keywords": ["technology", "devices", "software"], "admin_email": "admin@samsung.com"})