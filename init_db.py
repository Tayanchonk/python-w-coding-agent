"""
Database initialization script with sample data
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from sqlalchemy.orm import Session
    from app.database import SessionLocal, engine, Base
    from app.models import User, Position, Employee
    from app.auth import get_password_hash
except ImportError as e:
    print("Error: Missing required dependencies!")
    print(f"Import error: {e}")
    print("\nPlease install the required dependencies by running:")
    print("pip install -r requirements.txt")
    print("\nOr install individual packages:")
    print("pip install fastapi uvicorn sqlalchemy python-jose[cryptography] passlib[bcrypt] python-multipart")
    sys.exit(1)


def init_db():
    """Initialize database with tables and sample data"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    
    db: Session = SessionLocal()
    
    try:
        # Check if data already exists
        if db.query(User).first():
            print("Database already initialized with data.")
            return
        
        print("Adding sample data...")
        
        # Create sample users
        sample_users = [
            User(
                username="admin",
                email="admin@company.com",
                password_hash=get_password_hash("admin123"),
                is_active=True
            ),
            User(
                username="manager",
                email="manager@company.com",
                password_hash=get_password_hash("manager123"),
                is_active=True
            )
        ]
        
        for user in sample_users:
            db.add(user)
        
        # Create sample positions
        sample_positions = [
            Position(
                name="Software Engineer",
                description="Develops and maintains software applications"
            ),
            Position(
                name="Product Manager",
                description="Manages product development and strategy"
            ),
            Position(
                name="Data Scientist",
                description="Analyzes data and builds predictive models"
            ),
            Position(
                name="DevOps Engineer",
                description="Manages infrastructure and deployment pipelines"
            )
        ]
        
        for position in sample_positions:
            db.add(position)
        
        db.commit()
        
        # Create sample employees
        sample_employees = [
            Employee(
                first_name="John",
                last_name="Doe",
                position_id=1
            ),
            Employee(
                first_name="Jane",
                last_name="Smith",
                position_id=2
            ),
            Employee(
                first_name="Mike",
                last_name="Johnson",
                position_id=1
            ),
            Employee(
                first_name="Sarah",
                last_name="Wilson",
                position_id=3
            )
        ]
        
        for employee in sample_employees:
            db.add(employee)
        
        db.commit()
        print("Sample data added successfully!")
        
        print("\nSample login credentials:")
        print("Username: admin, Password: admin123")
        print("Username: manager, Password: manager123")
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    init_db()