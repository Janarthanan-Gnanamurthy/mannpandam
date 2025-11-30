from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.database import engine, Base, close_ssh_tunnel
from app.routers import products, auth, cart, orders, chatbot

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    # Create database tables
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown
    close_ssh_tunnel()

app = FastAPI(title="E-Commerce API", version="1.0.0", lifespan=lifespan)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(products.router, prefix="/api/products", tags=["products"])
app.include_router(cart.router, prefix="/api/cart", tags=["cart"])
app.include_router(orders.router, prefix="/api/orders", tags=["orders"])
app.include_router(chatbot.router, prefix="/api/chatbot", tags=["chatbot"])

@app.get("/")
async def root():
    return {"message": "E-Commerce API"}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

