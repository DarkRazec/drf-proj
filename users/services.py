import stripe
from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def create_stripe_product(instance):
    title = f'{instance.course}' if instance.course else f'{instance.lesson}'
    stripe_product = stripe.Product.create(name=f"{title}")
    return stripe_product.get('id')


def create_stripe_price(amount):
    return stripe.Price.create(
        currency="usd",
        unit_amount=amount,
        product_data={"name": "Payment"},
    )


def create_stripe_session(price):
    session = stripe.checkout.Session.create(
        success_url="https://127.0.0.1:8000/",
        line_items=[{"price": price.get('id'), "quantity": 1}],
        mode="payment",
    )
    return session.get('id'), session.get('url')
