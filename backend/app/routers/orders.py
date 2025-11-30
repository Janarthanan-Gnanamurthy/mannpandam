from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List
from app.database import get_db
from app import models, schemas, auth

router = APIRouter()

@router.post("/", response_model=schemas.OrderResponse)
def create_order(
    order: schemas.OrderCreate,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    # Get cart items with product relationship
    cart_items = db.query(models.CartItem).options(
        joinedload(models.CartItem.product)
    ).filter(models.CartItem.user_id == current_user.id).all()
    
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")
    
    # Calculate total
    total_amount = sum(item.product.price * item.quantity for item in cart_items)
    
    # Create order
    db_order = models.Order(
        user_id=current_user.id,
        total_amount=total_amount,
        shipping_address=order.shipping_address,
        status="pending"
    )
    db.add(db_order)
    db.flush()
    
    # Create order items
    for cart_item in cart_items:
        order_item = models.OrderItem(
            order_id=db_order.id,
            product_id=cart_item.product_id,
            quantity=cart_item.quantity,
            price=cart_item.product.price
        )
        db.add(order_item)
    
    # Clear cart
    db.query(models.CartItem).filter(models.CartItem.user_id == current_user.id).delete()
    
    db.commit()
    # Reload with relationships
    db_order = db.query(models.Order).options(
        joinedload(models.Order.order_items).joinedload(models.OrderItem.product)
    ).filter(models.Order.id == db_order.id).first()
    return db_order

@router.get("/", response_model=List[schemas.OrderResponse])
def get_orders(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    orders = db.query(models.Order).options(
        joinedload(models.Order.order_items).joinedload(models.OrderItem.product)
    ).filter(models.Order.user_id == current_user.id).all()
    return orders

@router.get("/{order_id}", response_model=schemas.OrderResponse)
def get_order(
    order_id: int,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    order = db.query(models.Order).options(
        joinedload(models.Order.order_items).joinedload(models.OrderItem.product)
    ).filter(
        models.Order.id == order_id,
        models.Order.user_id == current_user.id
    ).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    return order

