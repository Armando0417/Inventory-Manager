from models import Sale, Product, db

class SalesService:
    @staticmethod
    def record_sale(product_id, quantity, source):
        product = Product.query.get(product_id)
        if product and product.quantity >= quantity:
            sale = Sale(product_id=product_id, quantity=quantity, source=source)
            product.quantity -= quantity
            db.session.add(sale)
            db.session.commit()
            return sale
        return None
