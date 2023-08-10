from app.models.category_model import Category
from app.repositories.abstract_repository import AbstractRepository


class CategoryRepository(AbstractRepository[Category]):
    def __init__(self):
        super().__init__()    
        
    def delete_all_categories(self):
        collection = self.db['category']  # Assuming 'category' is the name of the collection
        result = collection.delete_many({})  # Delete all records in the collection
        return {"deleted count": result.deleted_count}

    
    