from sqlalchemy.orm import Session
from app.repositories.item_repository import ItemRepository
from app.schemas.item import ItemCreate, ItemUpdate
from app.models.item import ItemOrm
from typing import Tuple
from fastapi import HTTPException

class ItemService:
    def __init__(self, db: Session):
        self.repo = ItemRepository(db)

    def get_item(self, item_id: int) -> ItemOrm:
        item = self.repo.get(item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        return item

    def get_items(self, skip: int, limit: int) -> Tuple[list[ItemOrm], int]:
        return self.repo.get_multi(skip=skip, limit=limit)

    def create_item(self, item_data: ItemCreate) -> ItemOrm:
        # Здесь можно добавить бизнес-логику, например, проверку уникальности имени
        return self.repo.create(item_data)

    def update_item(self, item_id: int, item_data: ItemUpdate) -> ItemOrm:
        item = self.get_item(item_id)
        return self.repo.update(item, item_data)

    def delete_item(self, item_id: int) -> ItemOrm:
        item = self.get_item(item_id)
        return self.repo.soft_delete(item)

    def restore_item(self, item_id: int) -> ItemOrm:
        # Поиск среди удалённых
        db_item = self.repo.db.query(ItemOrm).filter(ItemOrm.id == item_id).first()
        if not db_item or db_item.deleted_at is None:
            raise HTTPException(status_code=404, detail="Deleted item not found")
        return self.repo.restore(db_item)