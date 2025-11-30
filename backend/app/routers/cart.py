from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List
from app.database import get_db
from app import models, schemas, auth

router = APIRouter()

@router.get("/", response_model=List[schemas.CartItemResponse])
def get_cart(current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    cart_items = db.query(models.CartItem).options(
        joinedload(models.CartItem.product)
    ).filter(models.CartItem.user_id == current_user.id).all()
    return cart_items

@router.post("/", response_model=schemas.CartItemResponse)
def add_to_cart(
    item: schemas.CartItemCreate,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    # Check if product exists
    product = db.query(models.Product).filter(models.Product.id == item.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Check if item already in cart
    existing_item = db.query(models.CartItem).filter(
        models.CartItem.user_id == current_user.id,
        models.CartItem.product_id == item.product_id
    ).first()
    
    if existing_item:
        existing_item.quantity += item.quantity
        db.commit()
        # Reload with product relationship
        existing_item = db.query(models.CartItem).options(
            joinedload(models.CartItem.product)
        ).filter(models.CartItem.id == existing_item.id).first()
        return existing_item
    
    cart_item = models.CartItem(
        user_id=current_user.id,
        product_id=item.product_id,
        quantity=item.quantity
    )
    db.add(cart_item)
    db.commit()
    # Reload with product relationship
    cart_item = db.query(models.CartItem).options(
        joinedload(models.CartItem.product)
    ).filter(models.CartItem.id == cart_item.id).first()
    return cart_item

@router.put("/{item_id}", response_model=schemas.CartItemResponse)
def update_cart_item(
    item_id: int,
    quantity: int,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    cart_item = db.query(models.CartItem).filter(
        models.CartItem.id == item_id,
        models.CartItem.user_id == current_user.id
    ).first()
    
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    
    cart_item.quantity = quantity
    db.commit()
    # Reload with product relationship
    cart_item = db.query(models.CartItem).options(
        joinedload(models.CartItem.product)
    ).filter(models.CartItem.id == cart_item.id).first()
    return cart_item

@router.delete("/{item_id}")
def remove_from_cart(
    item_id: int,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    cart_item = db.query(models.CartItem).filter(
        models.CartItem.id == item_id,
        models.CartItem.user_id == current_user.id
    ).first()
    
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    
    db.delete(cart_item)
    db.commit()
    return {"message": "Item removed from cart"}

@router.delete("/")
def clear_cart(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    db.query(models.CartItem).filter(models.CartItem.user_id == current_user.id).delete()
    db.commit()
    return {"message": "Cart cleared"}

