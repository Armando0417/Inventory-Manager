from flask import Flask, render_template, jsonify, request
from models import ProductVariation, app, db, Product, Sale, SyncLog
from product_service import ProductService
from sales_service import SalesService

# Ensure the app context is properly set
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')



# ========= Product routes =========

@app.route('/products', methods=['GET'])
def get_products():
    products = ProductService.get_all_products()
    categories = ProductService.get_all_product_categories()
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        return jsonify([
            {"id": p.id, "name": p.name,"category": p.category, "price": p.price} 
            for p in products
        ])
    else:
        return render_template('products.html', products=products, categories=categories)
    
    
@app.route('/product/<int:product_id>/variations', methods=['GET'])
def get_product_variations(product_id):
  try:
    # Fetch product using Session.get
    product = db.session.get(Product, product_id)
    if product is None:
      return jsonify({'message': 'Product not found'}), 404
    print(product.name)
    
    # Access variations using the relationship attribute
    variations = product.variations  # No need for .all()

    variations_data = [{'size': variation.size, 'quantity': variation.quantity} for variation in variations]
    print(variations_data)
    return jsonify(variations_data), 200

  except Exception as e:
    # Handle any errors during database interaction
    print(f"Error fetching product variations: {e}")
    return jsonify({'message': 'Internal server error'}), 500



# ========== Transaction Section ==========

@app.route('/process-transaction', methods=['GET'])
def process_transaction():
    products = ProductService.get_all_products()  # Example function to fetch products from the database
    items = []
    
    for product in products:
        if len(product.variations) == 0:
            items.append({
                'id': product.id,
                'name': product.name,
                'category': product.category,
                'price': product.price,
                'quantity': product.quantity
            })
        else:
            for variation in product.variations:
                items.append({
                    'id': variation.id,
                    'name': product.name,
                    'category': product.category,
                    'price': product.price,
                    'size': variation.size,
                    'quantity': variation.quantity  # Ensure variations have 'quantity' if needed
                })
    
    return render_template('process_transaction.html', items=items)




@app.route('/finish-transaction', methods=['POST'])
def finish_transaction():
    cart = request.json.get('cart')
    if not cart:
        return jsonify({'success': False, 'error': 'No items in cart'})

    try:
        for item in cart:
            item_id = item['id']
            isVariation = item['isVariation']
            # print(f"Item ID: {item_id}, Name: {item['name']}, Is Variation: {isVariation}, Size: {size}")
            print(str(item_id) + " is " + item['name'] + " and is Variation: " + str(isVariation) + " size: " + str(item.get('size')))
            
            model = ProductVariation if isVariation else Product
            productFound = db.session.get(model, item_id)
            
            if productFound:
                print(f"Found product: {item['name']}, Current quantity: {productFound.quantity}")
                
                if productFound.quantity > 0:
                    productFound.quantity -= 1
                    print(f"Updated product quantity: {productFound.quantity}")
                else:
                    productFound.quantity = 0
                    return jsonify({'success': False, 'error': f'Insufficient stock for product ID {item_id}'})
            
            else:
                print(f"Product not found for ID={item_id}")
            

        db.session.commit()
        print("Transaction committed successfully.")
        return jsonify({'success': True})

    except Exception as e:
        db.session.rollback()
        print(f"Transaction failed: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 400





# ========== Add Product Section ==========
@app.route('/modify-inventory', methods=['GET'])
def modify_inventory():
    products = ProductService.get_all_products() 
    items = []
    
    for product in products:
        if len(product.variations) == 0:
            items.append({
                'id': product.id,
                'name': product.name,
                'category': product.category,
                'price': product.price,
                'quantity': product.quantity
            })
        else:
            for variation in product.variations:
                items.append({
                    'id': variation.id,
                    'name': product.name,
                    'category': product.category,
                    'price': product.price,
                    'size': variation.size,
                    'quantity': variation.quantity  
                })
    
    return render_template('new-item-form.html', items=items)



@app.route('/add-product', methods=['POST'])
def add_product():
    try:
        data = request.json

        name = data.get('name')
        category = data.get('category')
        price = data.get('price')
        quantity = data.get('quantity', 0)
        size = data.get('size')
        description = data.get('description')

        if not name or not category or not price or not quantity:
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400
    
    
        existing_product = Product.query.filter_by(name=name).first()
        if existing_product:
            return jsonify({'success': False, 'error': 'Product with this name already exists'}), 400

        # Create a new product instance
        new_product = Product(name=name, category=category, price=price, quantity=quantity, size=size, description=description)
        db.session.add(new_product)
        db.session.commit()
    
        return jsonify({'success': True, 'message': 'Product added successfully', 'product_id': new_product.id}), 201
    
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")  # Print the error message to the console
        return jsonify({'success': False, 'error': str(e)}), 500
    
    

@app.route('/update-product/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.json
    name = data.get('name')
    category = data.get('category')
    price = data.get('price')
    quantity = data.get('quantity', 0)
    size = data.get('size')
    description = data.get('description')

    try:
        # Retrieve the product to update
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'success': False, 'error': 'Product not found'}), 404
        
        # Update the product fields
        product.name = name
        product.category = category
        product.price = price
        product.quantity = quantity
        product.size = size
        product.description = description

        db.session.commit()
        return jsonify({'success': True, 'message': 'Product updated successfully'}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
