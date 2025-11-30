# E-Commerce Application

A full-stack e-commerce application similar to Amazon, built with Vue.js (frontend) and FastAPI (backend), using PostgreSQL as the database.

## Tech Stack

### Frontend
- **Vue.js 3** - Progressive JavaScript framework
- **Vue Router** - Official router for Vue.js
- **Pinia** - State management
- **Tailwind CSS** - Utility-first CSS framework
- **DaisyUI** - Component library for Tailwind CSS
- **Axios** - HTTP client
- **Vite** - Build tool

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - SQL toolkit and ORM
- **PostgreSQL** - Relational database
- **JWT** - Authentication
- **Pydantic** - Data validation

## Project Structure

```
zobot/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── auth.py
│   │   └── routers/
│   │       ├── __init__.py
│   │       ├── auth.py
│   │       ├── products.py
│   │       ├── cart.py
│   │       └── orders.py
│   ├── requirements.txt
│   ├── .env.example
│   └── README.md
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── views/
│   │   ├── stores/
│   │   ├── services/
│   │   ├── router/
│   │   ├── App.vue
│   │   ├── main.js
│   │   └── style.css
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── README.md
└── README.md
```

## Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 16+
- PostgreSQL 12+

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up PostgreSQL database:
   - Create a database named `ecommerce_db`
   - Update the `.env` file with your database credentials

5. Copy `.env.example` to `.env` and update the values:
```bash
cp .env.example .env
```

6. Update `.env` with your PostgreSQL connection string:
```
DATABASE_URL=postgresql://username:password@localhost:5432/ecommerce_db
SECRET_KEY=your-secret-key-here-change-in-production
```

7. Run the application:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`
API documentation: `http://localhost:8000/docs`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:5173`

## Features

### User Features
- User registration and authentication
- Browse products with search and category filters
- View product details
- Add products to shopping cart
- Update cart quantities
- Checkout and place orders
- View order history

### API Endpoints

#### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user

#### Products
- `GET /api/products/` - List products (with search and category filters)
- `GET /api/products/{id}` - Get product details
- `GET /api/products/categories/list` - List all categories
- `POST /api/products/` - Create product (admin)

#### Cart
- `GET /api/cart/` - Get user's cart
- `POST /api/cart/` - Add item to cart
- `PUT /api/cart/{item_id}` - Update cart item quantity
- `DELETE /api/cart/{item_id}` - Remove item from cart
- `DELETE /api/cart/` - Clear cart

#### Orders
- `GET /api/orders/` - Get user's orders
- `GET /api/orders/{id}` - Get order details
- `POST /api/orders/` - Create new order

## Development

### Backend
- The backend uses FastAPI with automatic API documentation
- Database models are defined in `app/models.py`
- API routes are organized in `app/routers/`
- Authentication uses JWT tokens

### Frontend
- Vue 3 with Composition API
- State management with Pinia
- Routing with Vue Router
- Styling with Tailwind CSS and DaisyUI components

## Notes

- Make sure PostgreSQL is running before starting the backend
- Update the CORS origins in `backend/app/main.py` if needed
- Change the SECRET_KEY in production
- The database tables are created automatically on first run

## License

This project is open source and available under the MIT License.

