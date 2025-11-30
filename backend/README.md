# E-Commerce Backend API

FastAPI backend for the e-commerce application.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up PostgreSQL database:
   - Create a database named `ecommerce_db`
   - Update `.env` file with your database credentials

4. Configure environment variables:
   Create a `.env` file in the backend directory with the following variables:

   **For direct database connection:**
   ```env
   DATABASE_URL=postgresql://user:password@localhost:5432/ecommerce_db
   ```

   **For SSH tunnel connection (AWS):**
   ```env
   # Database settings
   DB_HOST=your-database-host.rds.amazonaws.com
   DB_PORT=5432
   DB_NAME=ecommerce_db
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password

   # SSH Tunnel settings
   SSH_TUNNEL_ENABLED=true
   SSH_HOST=your-ec2-instance.ec2.amazonaws.com
   SSH_PORT=22
   SSH_USERNAME=ec2-user

   # Authentication (use either password OR private key)
   # Option 1: Password
   SSH_PASSWORD=your_ssh_password

   # Option 2: Private key (recommended)
   SSH_PKEY=/path/to/your/private-key.pem
   # If key is encrypted:
   SSH_PKEY_PASSWORD=your_key_password
   ```

5. Run the application:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

API documentation available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

