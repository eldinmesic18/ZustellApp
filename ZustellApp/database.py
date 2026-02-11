import sqlite3

class Database:
    def __init__(self, db_name="zustellapp.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        # Create Packages table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS packages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                address TEXT NOT NULL,
                status TEXT DEFAULT 'pending', -- pending, delivered, skipped
                type TEXT DEFAULT 'package', -- package, letter
                notes TEXT,
                latitude REAL,
                longitude REAL,
                delivery_order INTEGER DEFAULT 0,
                area_id INTEGER,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (area_id) REFERENCES delivery_areas(id)
            )
        """)
        
        # Check if area_id column exists (migration)
        try:
            self.cursor.execute("SELECT area_id FROM packages LIMIT 1")
        except sqlite3.OperationalError:
            self.cursor.execute("ALTER TABLE packages ADD COLUMN area_id INTEGER")
        
        # Create Delivery Areas table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS delivery_areas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
        """)

        # Create Master Routes table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS area_master_routes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                area_id INTEGER,
                address TEXT NOT NULL,
                sequence_index INTEGER NOT NULL,
                FOREIGN KEY (area_id) REFERENCES delivery_areas(id)
            )
        """)
        
        # Create Routes table (stores order of delivery)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS routes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create Notes table for address-specific notes
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS address_notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                address TEXT NOT NULL,
                note TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        self.conn.commit()

    def add_package(self, address, type='package', notes=None):
        # Automatic area and order lookup
        self.cursor.execute("SELECT area_id, sequence_index FROM area_master_routes WHERE ? LIKE '%' || address || '%'", (address,))
        match = self.cursor.fetchone()
        
        area_id = None
        delivery_order = 0
        
        if match:
            area_id, delivery_order = match
        else:
            # Fallback: Find next delivery order
            self.cursor.execute("SELECT MAX(delivery_order) FROM packages")
            max_order = self.cursor.fetchone()[0]
            delivery_order = (max_order + 1) if max_order is not None else 1
        
        self.cursor.execute("INSERT INTO packages (address, type, notes, delivery_order, area_id) VALUES (?, ?, ?, ?, ?)", 
                          (address, type, notes, delivery_order, area_id))
        self.conn.commit()
        return self.cursor.lastrowid

    def add_delivery_area(self, name):
        self.cursor.execute("INSERT OR IGNORE INTO delivery_areas (name) VALUES (?)", (name,))
        self.conn.commit()
        self.cursor.execute("SELECT id FROM delivery_areas WHERE name = ?", (name,))
        return self.cursor.fetchone()[0]

    def add_master_route_entry(self, area_id, address, sequence_index):
        self.cursor.execute("INSERT INTO area_master_routes (area_id, address, sequence_index) VALUES (?, ?, ?)",
                          (area_id, address, sequence_index))
        self.conn.commit()

    def clear_all_data(self):
        """Reset the entire delivery database state (not the masters)"""
        self.cursor.execute("DELETE FROM packages")
        self.conn.commit()

    def get_packages(self, status=None):
        query = """
            SELECT p.*, a.name as area_name 
            FROM packages p 
            LEFT JOIN delivery_areas a ON p.area_id = a.id
        """
        if status:
            self.cursor.execute(query + " WHERE p.status = ? ORDER BY p.delivery_order ASC", (status,))
        else:
            self.cursor.execute(query + " ORDER BY p.delivery_order ASC")
        return self.cursor.fetchall()
    
    def get_packages_with_coordinates(self):
        """Get packages that have been geocoded"""
        self.cursor.execute("SELECT * FROM packages WHERE latitude IS NOT NULL AND longitude IS NOT NULL ORDER BY delivery_order ASC")
        return self.cursor.fetchall()
    
    def update_package_coordinates(self, package_id, latitude, longitude):
        """Update the coordinates for a package"""
        self.cursor.execute("UPDATE packages SET latitude = ?, longitude = ? WHERE id = ?", 
                          (latitude, longitude, package_id))
        self.conn.commit()
    
    def update_package(self, package_id, address, notes):
        """Update the address and notes for a package"""
        self.cursor.execute("UPDATE packages SET address = ?, notes = ? WHERE id = ?", 
                          (address, notes, package_id))
        self.conn.commit()

    def update_delivery_order(self, package_id, order_index):
        """Update the delivery order for a package"""
        self.cursor.execute("UPDATE packages SET delivery_order = ? WHERE id = ?", 
                          (order_index, package_id))
        self.conn.commit()
    
    def update_package_status(self, package_id, status):
        """Update the status of a package"""
        self.cursor.execute("UPDATE packages SET status = ? WHERE id = ?", (status, package_id))
        self.conn.commit()
    
    def add_address_note(self, address, note):
        """Add a note for a specific address"""
        self.cursor.execute("INSERT INTO address_notes (address, note) VALUES (?, ?)", (address, note))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def get_address_notes(self, address):
        """Get all notes for a specific address"""
        self.cursor.execute("SELECT note, created_at FROM address_notes WHERE address = ?", (address,))
        return self.cursor.fetchall()
    
    def delete_package(self, package_id):
        """Delete a package"""
        self.cursor.execute("DELETE FROM packages WHERE id = ?", (package_id,))
        self.conn.commit()

    def close(self):
        self.conn.close()

