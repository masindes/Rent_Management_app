from datetime import datetime
from app import app, db
from models import Property, Tenant, Payment

# Initialize the app and database
with app.app_context():
    # Clear existing data
    # db.drop_all()
    # db.create_all()

    # Seed properties
    property1 = Property(name="Sunset Villa", address="123 Sunset Blvd, LA", bedrooms=3, rent=2500)
    property2 = Property(name="Oceanview Apartments", address="456 Ocean Dr, LA", bedrooms=2, rent=1800)

    db.session.add(property1)
    db.session.add(property2)
    db.session.commit()

    # Seed tenants
    tenant1 = Tenant(name="John Doe", phone="1234567890", unit_id=101, email="john@example.com", property_id=property1.id)
    tenant2 = Tenant(name="Jane Smith", phone="9876543210", unit_id=102, email="jane@example.com", property_id=property2.id)

    db.session.add(tenant1)
    db.session.add(tenant2)
    db.session.commit()

    # Seed payments
    payment1 = Payment(payment_type="Rent", status="Paid", amount=2500, payment_date=datetime(2025, 1, 1), tenant_id=tenant1.id)
    payment2 = Payment(payment_type="Rent", status="Pending", amount=1800, payment_date=datetime(2025, 1, 1), tenant_id=tenant2.id)

    db.session.add(payment1)
    db.session.add(payment2)
    db.session.commit()

    print("Database seeded successfully.")
