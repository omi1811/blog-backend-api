from sqlalchemy import create_engine, text

# Use the EXACT same URL as alembic.ini
engine = create_engine("postgresql://blog_user:secure_password_123@127.0.0.1:5434/blog_db")

try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("Connection successful!")
except Exception as e:
    print(f"Connection failed: {e}")
