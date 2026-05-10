from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.schemas.item import ItemCreate, ItemUpdate, ItemResponse, PaginatedItemResponse
from app.services.item_service import ItemService
from app.database import get_db
from app.config import settings

router = APIRouter(prefix="/items", tags=["items"])

@router.get("/", response_model=PaginatedItemResponse)
def get_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(settings.DEFAULT_PAGE_SIZE, ge=1, le=settings.MAX_PAGE_SIZE),
    db: Session = Depends(get_db)
):
    service = ItemService(db)
    items, total = service.get_items(skip, limit)
    return {"total": total, "skip": skip, "limit": limit, "items": items}

@router.get("/{item_id}", response_model=ItemResponse)
def get_item(item_id: int, db: Session = Depends(get_db)):
    return ItemService(db).get_item(item_id)

@router.post("/", response_model=ItemResponse, status_code=201)
def create_item(item_data: ItemCreate, db: Session = Depends(get_db)):
    return ItemService(db).create_item(item_data)

@router.put("/{item_id}", response_model=ItemResponse)
def update_item(item_id: int, item_data: ItemUpdate, db: Session = Depends(get_db)):
    return ItemService(db).update_item(item_id, item_data)

@router.patch("/{item_id}", response_model=ItemResponse)
def patch_item(item_id: int, item_data: ItemUpdate, db: Session = Depends(get_db)):
    return ItemService(db).update_item(item_id, item_data)

@router.delete("/{item_id}", response_model=ItemResponse)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    return ItemService(db).delete_item(item_id)

@router.post("/{item_id}/restore", response_model=ItemResponse)
def restore_item(item_id: int, db: Session = Depends(get_db)):
    return ItemService(db).restore_item(item_id)