from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from app.database import get_db
from app import models, schemas

router = APIRouter()

# Get user orders by user_id, email, or username
@router.get("/orders/user/{identifier}", response_model=List[schemas.OrderResponse])
def get_user_orders_by_identifier(
    identifier: str,
    identifier_type: str = Query("auto", description="Type: 'id', 'email', 'username', or 'auto'"),
    db: Session = Depends(get_db)
):
    """
    Get orders for a user by user_id, email, or username.
    If identifier_type is 'auto', it will try to detect the type.
    """
    user = None
    
    if identifier_type == "auto":
        # Try to detect type
        if identifier.isdigit():
            user = db.query(models.User).filter(models.User.id == int(identifier)).first()
        else:
            # Try email first, then username
            user = db.query(models.User).filter(models.User.email == identifier).first()
            if not user:
                user = db.query(models.User).filter(models.User.username == identifier).first()
    elif identifier_type == "id":
        user = db.query(models.User).filter(models.User.id == int(identifier)).first()
    elif identifier_type == "email":
        user = db.query(models.User).filter(models.User.email == identifier).first()
    elif identifier_type == "username":
        user = db.query(models.User).filter(models.User.username == identifier).first()
    else:
        raise HTTPException(status_code=400, detail="Invalid identifier_type. Use 'id', 'email', 'username', or 'auto'")
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    orders = db.query(models.Order).options(
        joinedload(models.Order.order_items).joinedload(models.OrderItem.product)
    ).filter(models.Order.user_id == user.id).order_by(models.Order.created_at.desc()).all()
    
    return orders

# Get specific order by order_id
@router.get("/orders/{order_id}", response_model=schemas.OrderResponse)
def get_order_by_id(order_id: int, db: Session = Depends(get_db)):
    """Get order details by order ID"""
    order = db.query(models.Order).options(
        joinedload(models.Order.order_items).joinedload(models.OrderItem.product),
        joinedload(models.Order.user)
    ).filter(models.Order.id == order_id).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    return order

# Get orders by status
@router.get("/orders/status/{status}", response_model=List[schemas.OrderResponse])
def get_orders_by_status(
    status: str,
    user_identifier: Optional[str] = Query(None, description="Optional: filter by user (id, email, or username)"),
    db: Session = Depends(get_db)
):
    """Get orders by status, optionally filtered by user"""
    query = db.query(models.Order).options(
        joinedload(models.Order.order_items).joinedload(models.OrderItem.product)
    )
    
    query = query.filter(models.Order.status == status)
    
    if user_identifier:
        user = None
        if user_identifier.isdigit():
            user = db.query(models.User).filter(models.User.id == int(user_identifier)).first()
        else:
            user = db.query(models.User).filter(models.User.email == user_identifier).first()
            if not user:
                user = db.query(models.User).filter(models.User.username == user_identifier).first()
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        query = query.filter(models.Order.user_id == user.id)
    
    orders = query.order_by(models.Order.created_at.desc()).all()
    return orders

# Get product details
@router.get("/products/{product_id}", response_model=schemas.ProductResponse)
def get_product_details(product_id: int, db: Session = Depends(get_db)):
    """Get detailed product information"""
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# Search products
@router.get("/products/search", response_model=List[schemas.ProductResponse])
def search_products(
    q: str = Query(..., description="Search query"),
    category: Optional[str] = Query(None, description="Filter by category"),
    limit: int = Query(20, ge=1, le=100, description="Maximum number of results"),
    db: Session = Depends(get_db)
):
    """Search products by name or description"""
    query = db.query(models.Product).filter(
        models.Product.name.ilike(f"%{q}%") |
        models.Product.description.ilike(f"%{q}%")
    )
    
    if category:
        query = query.filter(models.Product.category == category)
    
    products = query.limit(limit).all()
    return products

# Get products by category
@router.get("/products/category/{category}", response_model=List[schemas.ProductResponse])
def get_products_by_category(
    category: str,
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get all products in a specific category"""
    products = db.query(models.Product).filter(
        models.Product.category == category
    ).limit(limit).all()
    return products

# Get all categories
@router.get("/products/categories", response_model=List[str])
def get_all_categories(db: Session = Depends(get_db)):
    """Get list of all product categories"""
    categories = db.query(models.Product.category).distinct().all()
    return [cat[0] for cat in categories if cat[0]]

# Get user information
@router.get("/users/{identifier}", response_model=schemas.UserResponse)
def get_user_info(
    identifier: str,
    identifier_type: str = Query("auto", description="Type: 'id', 'email', 'username', or 'auto'"),
    db: Session = Depends(get_db)
):
    """Get user information by user_id, email, or username"""
    user = None
    
    if identifier_type == "auto":
        if identifier.isdigit():
            user = db.query(models.User).filter(models.User.id == int(identifier)).first()
        else:
            user = db.query(models.User).filter(models.User.email == identifier).first()
            if not user:
                user = db.query(models.User).filter(models.User.username == identifier).first()
    elif identifier_type == "id":
        user = db.query(models.User).filter(models.User.id == int(identifier)).first()
    elif identifier_type == "email":
        user = db.query(models.User).filter(models.User.email == identifier).first()
    elif identifier_type == "username":
        user = db.query(models.User).filter(models.User.username == identifier).first()
    else:
        raise HTTPException(status_code=400, detail="Invalid identifier_type. Use 'id', 'email', 'username', or 'auto'")
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

# Get user's cart items
@router.get("/cart/{identifier}", response_model=List[schemas.CartItemResponse])
def get_user_cart(
    identifier: str,
    identifier_type: str = Query("auto", description="Type: 'id', 'email', 'username', or 'auto'"),
    db: Session = Depends(get_db)
):
    """Get user's cart items by user_id, email, or username"""
    user = None
    
    if identifier_type == "auto":
        if identifier.isdigit():
            user = db.query(models.User).filter(models.User.id == int(identifier)).first()
        else:
            user = db.query(models.User).filter(models.User.email == identifier).first()
            if not user:
                user = db.query(models.User).filter(models.User.username == identifier).first()
    elif identifier_type == "id":
        user = db.query(models.User).filter(models.User.id == int(identifier)).first()
    elif identifier_type == "email":
        user = db.query(models.User).filter(models.User.email == identifier).first()
    elif identifier_type == "username":
        user = db.query(models.User).filter(models.User.username == identifier).first()
    else:
        raise HTTPException(status_code=400, detail="Invalid identifier_type. Use 'id', 'email', 'username', or 'auto'")
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    cart_items = db.query(models.CartItem).options(
        joinedload(models.CartItem.product)
    ).filter(models.CartItem.user_id == user.id).all()
    
    return cart_items

# Get order statistics for a user
@router.get("/orders/stats/{identifier}")
def get_user_order_stats(
    identifier: str,
    identifier_type: str = Query("auto", description="Type: 'id', 'email', 'username', or 'auto'"),
    db: Session = Depends(get_db)
):
    """Get order statistics for a user"""
    user = None
    
    if identifier_type == "auto":
        if identifier.isdigit():
            user = db.query(models.User).filter(models.User.id == int(identifier)).first()
        else:
            user = db.query(models.User).filter(models.User.email == identifier).first()
            if not user:
                user = db.query(models.User).filter(models.User.username == identifier).first()
    elif identifier_type == "id":
        user = db.query(models.User).filter(models.User.id == int(identifier)).first()
    elif identifier_type == "email":
        user = db.query(models.User).filter(models.User.email == identifier).first()
    elif identifier_type == "username":
        user = db.query(models.User).filter(models.User.username == identifier).first()
    else:
        raise HTTPException(status_code=400, detail="Invalid identifier_type. Use 'id', 'email', 'username', or 'auto'")
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    orders = db.query(models.Order).filter(models.Order.user_id == user.id).all()
    
    total_orders = len(orders)
    total_spent = sum(order.total_amount for order in orders)
    status_counts = {}
    for order in orders:
        status_counts[order.status] = status_counts.get(order.status, 0) + 1
    
    return {
        "user_id": user.id,
        "username": user.username,
        "email": user.email,
        "total_orders": total_orders,
        "total_spent": total_spent,
        "status_breakdown": status_counts
    }

# Cancel an order
@router.post("/orders/{order_id}/cancel", response_model=schemas.OrderResponse)
def cancel_order(
    order_id: int,
    user_identifier: Optional[str] = Query(None, description="Optional: verify ownership by user (id, email, or username)"),
    db: Session = Depends(get_db)
):
    """
    Cancel an order by order ID.
    Optionally verify ownership by providing user_identifier.
    """
    # Get the order
    order = db.query(models.Order).options(
        joinedload(models.Order.order_items).joinedload(models.OrderItem.product),
        joinedload(models.Order.user)
    ).filter(models.Order.id == order_id).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Verify ownership if user_identifier is provided
    if user_identifier:
        user = None
        if user_identifier.isdigit():
            user = db.query(models.User).filter(models.User.id == int(user_identifier)).first()
        else:
            user = db.query(models.User).filter(models.User.email == user_identifier).first()
            if not user:
                user = db.query(models.User).filter(models.User.username == user_identifier).first()
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        if order.user_id != user.id:
            raise HTTPException(status_code=403, detail="Order does not belong to this user")
    
    # Check if order can be cancelled
    non_cancellable_statuses = ["delivered", "cancelled"]
    if order.status in non_cancellable_statuses:
        raise HTTPException(
            status_code=400, 
            detail=f"Cannot cancel order with status '{order.status}'. Only orders that are not delivered or already cancelled can be cancelled."
        )
    
    # Update order status to cancelled
    order.status = "cancelled"
    db.commit()
    db.refresh(order)
    
    return order

# Download invoice for an order
@router.get("/orders/{order_id}/invoice")
def download_invoice(
    order_id: int,
    user_identifier: Optional[str] = Query(None, description="Optional: verify ownership by user (id, email, or username)"),
    db: Session = Depends(get_db)
):
    """
    Get invoice data for an order by order ID.
    Optionally verify ownership by providing user_identifier.
    Returns invoice information in JSON format.
    """
    # Get the order with all relationships
    order = db.query(models.Order).options(
        joinedload(models.Order.order_items).joinedload(models.OrderItem.product),
        joinedload(models.Order.user)
    ).filter(models.Order.id == order_id).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Verify ownership if user_identifier is provided
    if user_identifier:
        user = None
        if user_identifier.isdigit():
            user = db.query(models.User).filter(models.User.id == int(user_identifier)).first()
        else:
            user = db.query(models.User).filter(models.User.email == user_identifier).first()
            if not user:
                user = db.query(models.User).filter(models.User.username == user_identifier).first()
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        if order.user_id != user.id:
            raise HTTPException(status_code=403, detail="Order does not belong to this user")
    
    # Build invoice data
    invoice_items = []
    for item in order.order_items:
        invoice_items.append({
            "product_id": item.product_id,
            "product_name": item.product.name,
            "quantity": item.quantity,
            "unit_price": item.price,
            "subtotal": item.price * item.quantity
        })
    
    invoice_data = {
        "invoice_number": f"INV-{order.id:06d}",
        "order_id": order.id,
        "invoice_date": order.created_at.isoformat(),
        "order_date": order.created_at.isoformat(),
        "status": order.status,
        "customer": {
            "user_id": order.user.id,
            "name": order.user.full_name or order.user.username,
            "email": order.user.email,
            "username": order.user.username
        },
        "shipping_address": order.shipping_address,
        "items": invoice_items,
        "subtotal": order.total_amount,
        "tax": 0.0,  # Can be calculated if tax is implemented
        "shipping": 0.0,  # Can be calculated if shipping fees are implemented
        "total": order.total_amount,
        "currency": "USD"  # Can be made configurable
    }
    
    return invoice_data

