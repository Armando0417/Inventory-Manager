from models import app, db, Product, ProductVariation

def add_mock_data():
    # Create mock products
    products = [
        {'name': 'T-Shirt', 'category': 'Clothes', 'price': 19.99,'description': 'Comfortable cotton t-shirt'},
        {'name': 'Jeans', 'category': 'Clothes', 'price': 49.99, 'description': 'Stylish blue jeans'},
        {'name': 'Sneakers', 'category': 'Shoes', 'price': 79.99, 'description': 'Comfortable running sneakers'},
        {'name': 'Mug', 'category': 'Accessories', 'price': 9.99, 'quantity': 10, 'description': 'Ceramic coffee mug'},
        {'name': 'Notebook', 'category': 'Stationery', 'price': 4.99, 'description': 'Lined notebook for writing'},
        {'name': 'Dress', 'category': 'Clothes', 'price': 29.99, 'description': 'Elegant evening dress'},
        {'name': 'Boots', 'category': 'Shoes', 'price': 99.99, 'description': 'Leather boots'},
        {'name': 'Hat', 'category': 'Accessories', 'price': 14.99, 'quantity': 10, 'description': 'Stylish sun hat'},
        {'name': 'Pen', 'category': 'Stationery', 'price': 2.99, 'description': 'Smooth writing pen'},
        {'name': 'Bag', 'category': 'Accessories', 'price': 39.99, 'description': 'Leather handbag'}
    ]

    # Insert products and map their names to their generated IDs
    product_name_to_id = {}
    product_objects = [Product(**product_data) for product_data in products]
    db.session.bulk_save_objects(product_objects)
    db.session.commit()

    # Retrieve the generated IDs and update quantities
    for product in Product.query.all():
        product_name_to_id[product.name] = product.id
        product.quantity = product.total_quantity()  # Update product quantity
        db.session.add(product)
    db.session.commit()

    print("Mock products inserted successfully!")
    return product_name_to_id


def add_variation_data(product_name_to_id):
    # Create mock product variations
    product_variations = [
        {'name': 'T-Shirt', 'size': 'S', 'quantity': 10},
        {'name': 'T-Shirt', 'size': 'M', 'quantity': 15},
        {'name': 'T-Shirt', 'size': 'L', 'quantity': 5},
        {'name': 'Jeans', 'size': '32', 'quantity': 20},
        {'name': 'Jeans', 'size': '34', 'quantity': 15},
        {'name': 'Jeans', 'size': '36', 'quantity': 10},
        {'name': 'Sneakers', 'size': '8', 'quantity': 12},
        {'name': 'Sneakers', 'size': '9', 'quantity': 18},
        {'name': 'Sneakers', 'size': '10', 'quantity': 10},
        {'name': 'Dress', 'size': 'S', 'quantity': 7},
        {'name': 'Dress', 'size': 'M', 'quantity': 12},
        {'name': 'Dress', 'size': 'L', 'quantity': 4},
        {'name': 'Boots', 'size': '6', 'quantity': 8},
        {'name': 'Boots', 'size': '7', 'quantity': 14},
        {'name': 'Boots', 'size': '8', 'quantity': 6},
        {'name': 'Boots', 'size': '9', 'quantity': 10},
        {'name': 'Pen', 'size': 'Blue', 'quantity': 50},
        {'name': 'Pen', 'size': 'Black', 'quantity': 30},
        {'name': 'Pen', 'size': 'Red', 'quantity': 20},
        {'name': 'Bag', 'size': 'Small', 'quantity': 5},
        {'name': 'Bag', 'size': 'Medium', 'quantity': 8},
        {'name': 'Bag', 'size': 'Large', 'quantity': 3}
    ]

    # Insert variations using the product name to ID mapping
    variation_objects = [
        ProductVariation(
            product_id=product_name_to_id[variation_data['name']],
            size=variation_data['size'],
            quantity=variation_data['quantity']
        )
        for variation_data in product_variations
    ]
    db.session.bulk_save_objects(variation_objects)
    db.session.commit()

    print("Mock variations added.")
    print("Now run the run.exe file")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        product_name_to_id = add_mock_data()
        add_variation_data(product_name_to_id)
