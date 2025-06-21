"""
Database migration script to convert integer IDs to UUIDs
"""
import os
import sys
import uuid
import sqlite3
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models import User, Position, Employee
from app.utils import generate_uuid


def migrate_to_uuid():
    """Migrate all integer IDs to UUIDs while preserving relationships"""
    
    # Create a mapping for ID conversions
    user_id_mapping = {}
    position_id_mapping = {}
    employee_id_mapping = {}
    
    db: Session = SessionLocal()
    
    try:
        print("Starting migration to UUID...")
        
        # Check if we're already using UUIDs (if any record has string ID)
        sample_user = db.query(User).first()
        if sample_user and isinstance(sample_user.user_id, str):
            print("Database already appears to use UUIDs. Migration not needed.")
            return
        
        # Step 1: Create backup tables with UUID columns
        print("Creating backup tables with UUID structure...")
        
        # Use raw SQL to create backup tables
        db.execute("""
            CREATE TABLE IF NOT EXISTS users_backup (
                user_id TEXT PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                is_active BOOLEAN DEFAULT 1
            )
        """)
        
        db.execute("""
            CREATE TABLE IF NOT EXISTS positions_backup (
                position_id TEXT PRIMARY KEY,
                position_name TEXT NOT NULL,
                description TEXT
            )
        """)
        
        db.execute("""
            CREATE TABLE IF NOT EXISTS employees_backup (
                emp_id TEXT PRIMARY KEY,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                position_id TEXT NOT NULL,
                FOREIGN KEY (position_id) REFERENCES positions_backup (position_id)
            )
        """)
        
        # Step 2: Migrate users
        print("Migrating users...")
        users = db.query(User).all()
        for user in users:
            new_uuid = generate_uuid()
            user_id_mapping[user.user_id] = new_uuid
            
            db.execute("""
                INSERT INTO users_backup (user_id, username, email, password, is_active)
                VALUES (?, ?, ?, ?, ?)
            """, (new_uuid, user.username, user.email, user.password, user.is_active))
        
        # Step 3: Migrate positions
        print("Migrating positions...")
        positions = db.query(Position).all()
        for position in positions:
            new_uuid = generate_uuid()
            position_id_mapping[position.position_id] = new_uuid
            
            db.execute("""
                INSERT INTO positions_backup (position_id, position_name, description)
                VALUES (?, ?, ?)
            """, (new_uuid, position.position_name, position.description))
        
        # Step 4: Migrate employees
        print("Migrating employees...")
        employees = db.query(Employee).all()
        for employee in employees:
            new_uuid = generate_uuid()
            employee_id_mapping[employee.emp_id] = new_uuid
            new_position_id = position_id_mapping[employee.position_id]
            
            db.execute("""
                INSERT INTO employees_backup (emp_id, first_name, last_name, position_id)
                VALUES (?, ?, ?, ?)
            """, (new_uuid, employee.first_name, employee.last_name, new_position_id))
        
        db.commit()
        
        # Step 5: Drop original tables and rename backup tables
        print("Replacing original tables...")
        
        db.execute("DROP TABLE employees")
        db.execute("DROP TABLE positions")
        db.execute("DROP TABLE users")
        
        db.execute("ALTER TABLE users_backup RENAME TO users")
        db.execute("ALTER TABLE positions_backup RENAME TO positions")
        db.execute("ALTER TABLE employees_backup RENAME TO employees")
        
        # Step 6: Recreate indexes
        print("Recreating indexes...")
        db.execute("CREATE INDEX ix_users_user_id ON users (user_id)")
        db.execute("CREATE INDEX ix_users_username ON users (username)")
        db.execute("CREATE INDEX ix_users_email ON users (email)")
        db.execute("CREATE INDEX ix_positions_position_id ON positions (position_id)")
        db.execute("CREATE INDEX ix_employees_emp_id ON employees (emp_id)")
        
        db.commit()
        
        print("Migration completed successfully!")
        print(f"Migrated {len(user_id_mapping)} users")
        print(f"Migrated {len(position_id_mapping)} positions")
        print(f"Migrated {len(employee_id_mapping)} employees")
        
        # Print sample ID mappings for verification
        if user_id_mapping:
            sample_old_id = list(user_id_mapping.keys())[0]
            sample_new_id = user_id_mapping[sample_old_id]
            print(f"Sample user ID mapping: {sample_old_id} -> {sample_new_id}")
        
    except Exception as e:
        print(f"Error during migration: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    migrate_to_uuid()