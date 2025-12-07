from app.core.database import SessionLocal
from app.models.category import Category

class CategoryRepository:

    @staticmethod
    def get_by_id(category_id: int):
        db = SessionLocal()
        return db.query(Category).filter(Category.id == category_id).first()
