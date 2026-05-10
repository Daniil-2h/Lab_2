from sqlalchemy.orm import Session
from app.models.item import ItemOrm
from app.schemas.item import ItemCreate, ItemUpdate
from datetime import datetime, timezone
from typing import Optional, Tuple

class ItemRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, item_id: int) -> Optional[ItemOrm]:
        return self.db.query(ItemOrm).filter(
            ItemOrm.id == item_id,
            ItemOrm.deleted_at.is_(None)
        ).first()

    def get_multi(self, skip: int = 0, limit: int = 100) -> Tuple[list[ItemOrm], int]:
        query = self.db.query(ItemOrm).filter(ItemOrm.deleted_at.is_(None))
        total = query.count()
        items = query.offset(skip).limit(limit).all()
        return items, total

    def create(self, item_data: ItemCreate) -> ItemOrm:
        db_item = ItemOrm(**item_data.model_dump())
        self.db.add(db_item)
        self.db.commit()
        self.db.refresh(db_item)
        return db_item

    def update(self, db_item: ItemOrm, item_data: ItemUpdate) -> ItemOrm:
        for field, value in item_data.model_dump(exclude_unset=True).items():
            setattr(db_item, field, value)
        self.db.commit()
        self.db.refresh(db_item)
        return db_item

    def soft_delete(self, db_item: ItemOrm) -> ItemOrm:
        db_item.deleted_at = datetime.now(timezone.utc)
        self.db.commit()
        self.db.refresh(db_item)
        return db_item

    def restore(self, db_item: ItemOrm) -> ItemOrm:
        db_item.deleted_at = None
        self.db.commit()
        self.db.refresh(db_item)
        return db_item