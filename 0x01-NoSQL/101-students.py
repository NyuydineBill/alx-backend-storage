#!/usr/bin/env python3
"""
Function to return all students sorted by average score
"""

from pymongo import MongoClient

def top_students(mongo_collection):
    """
    Returns all students sorted by average score.
    
    Parameters:
    - mongo_collection: the pymongo collection object

    Returns:
    - List of students sorted by average score with key = averageScore
    """
    pipeline = [
        {
            "$project": {
                "name": 1,
                "averageScore": {"$avg": "$scores.score"}
            }
        },
        {
            "$sort": {"averageScore": -1}
        }
    ]
    return list(mongo_collection.aggregate(pipeline))

if __name__ == "__main__":
    client = MongoClient('mongodb://localhost:27017/')
    db = client.school
    collection = db.students
    for student in top_students(collection):
        print(student)

