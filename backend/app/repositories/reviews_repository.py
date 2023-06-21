from flask import abort, jsonify, request
from app.models.reviews_model import Review
from bson.objectid import ObjectId
from app.repositories.abstract_repository import AbstractRepository


class ReviewsRepository(AbstractRepository[Review]):
    def __init__(self):
        super().__init__()
        
    def averageRating(self, site_id):
        laColeccion = self.db[self.coleccion]
        pipeline = [
            {
                '$match': {
                    'site_id': site_id
                }
            },
            {
                '$group': {
                    '_id': None,
                    'total': {
                        '$sum': {'$toDouble': '$rating'}
                    },
                    'count': {
                        '$sum': 1
                    }
                }
            }
        ]
        result = list(laColeccion.aggregate(pipeline))
        print(result)
        if len(result) > 0:
            average_reviews = result[0]['total'] / result[0]['count']
            return jsonify({'average': average_reviews})
        else:
            return jsonify({'average': 0})
    
