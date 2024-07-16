from models import Product, db

class ProductService:
    @staticmethod
    def get_all_products():
        return Product.query.all()

    @staticmethod
    def get_all_product_categories():
        return Product.query.with_entities(Product.category).distinct().all()


    @staticmethod
    def get_product_by_id(product_id):
        return Product.query.get(product_id)

    @staticmethod
    def add_product(name, quantity):
        new_product = Product(name=name, quantity=quantity)
        db.session.add(new_product)
        db.session.commit()
        return new_product
