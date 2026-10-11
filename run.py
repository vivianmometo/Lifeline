# import os
# from app import create_app

# app = create_app()

# @app.cli.command("init-db")
# def init_db_command():
#     """Initialize the database with tables and sample data"""
#     from setup_database import create_database, init_database
#     create_database()
#     init_database()
#     print("Database initialized successfully!")

# @app.cli.command("create-db")
# def create_db_command():
#     """Create the database only"""
#     from setup_database import create_database
#     create_database()
#     print("Database created successfully!")

# @app.cli.command("drop-db")
# def drop_db_command():
#     """Drop the database (use with caution)"""
#     try:
#         import pyodbc
#         conn = pyodbc.connect(
#             'Driver={ODBC Driver 17 for SQL Server};'
#             'Server=Safa and Salsabel-PC;'
#             'Database=master;'
#             'Trusted_Connection=yes;'
#         )
#         conn.autocommit = True
#         cursor = conn.cursor()
        
#         # Set database to single user mode first
#         cursor.execute("ALTER DATABASE pharmacy_db SET SINGLE_USER WITH ROLLBACK IMMEDIATE")
#         cursor.execute("DROP DATABASE pharmacy_db")
#         print("Database dropped successfully.")
        
#         cursor.close()
#         conn.close()
#     except Exception as e:
#         print(f"Error dropping database: {e}")

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=5000)
import os
from app import create_app
from config import DevelopmentConfig

app = create_app(DevelopmentConfig)  # Explicitly use DevelopmentConfig

@app.cli.command("init-db")
def init_db_command():
    """Initialize the database with tables and sample data"""
    from setup_database import create_database, init_database
    create_database()
    init_database()
    print("Database initialized successfully!")

@app.cli.command("create-db")
def create_db_command():
    """Create the database only (SQL Server)"""
    from setup_database import create_database
    create_database()
    print("Database created successfully!")

@app.cli.command("drop-db")
def drop_db_command():
    """Drop the database (use with caution)"""
    try:
        import pyodbc
        conn = pyodbc.connect(
            'Driver={ODBC Driver 17 for SQL Server};'
            'Server=.;'
            'Database=master;'
            'Trusted_Connection=yes;'
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Set database to single user mode first
        cursor.execute("ALTER DATABASE pharmacy_db SET SINGLE_USER WITH ROLLBACK IMMEDIATE")
        cursor.execute("DROP DATABASE pharmacy_db")
        print("Database dropped successfully.")
        
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error dropping database: {e}")
        
@app.cli.command("add-sample-notifications")

def add_sample_notifications():
    """Add sample notifications to the database"""
    from setup_database import create_sample_notifications
    from app import create_app, db
    
    app = create_app()
    
    with app.app_context():
        try:
            create_sample_notifications()
            print("✅ Sample notifications added successfully!")
        except Exception as e:
            print(f"❌ Error adding sample notifications: {e}")

@app.cli.command("test-notifications")
def test_notifications():
    """Test notifications functionality"""
    from app import create_app, db
    from app.models import Notification
    
    app = create_app()
    
    with app.app_context():
        try:
            # Count notifications
            count = Notification.query.count()
            print(f"Total notifications in database: {count}")
            
            # Show all notifications
            notifications = Notification.query.all()
            for notification in notifications:
                status = "📧 UNREAD" if not notification.is_read else "📭 READ"
                print(f"- {status} {notification.medicine.name}: {notification.status} - {notification.message}")
            
            if count == 0:
                print("No notifications found. Run 'flask add-sample-notifications' to create sample data.")
            else:
                print(f"\n✅ Notifications are working! Found {count} notifications.")
                
        except Exception as e:
            print(f"❌ Error testing notifications: {e}")

@app.cli.command("test-connection")
def test_connection():
    """Test SQL Server connection"""
    from app import db
    try:
        with app.app_context():
            db.session.execute('SELECT 1')
            print("✅ Successfully connected to SQL Server!")
    except Exception as e:
        print(f"❌ Connection failed: {e}")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)