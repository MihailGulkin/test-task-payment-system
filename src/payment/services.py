from payment.models import Item


def create_stripe_item(
        instance: Item,
        quantity: int
) -> dict:
    stripe_line_items = {
        'price_data': {
            'currency': 'usd',
            'product_data': {
                'name': instance.name,
                'description': instance.description,
            },
            'unit_amount': int(instance.price),

        },
        'quantity': quantity,

    }
    return stripe_line_items
