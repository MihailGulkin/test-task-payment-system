import json

import stripe

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views import View

from payment.models import Item
from payment.services import create_stripe_item

stripe.api_key = settings.STRIPE_API_SECRET_KEY

secret_pub = {
    'secret': settings.STRIPE_API_PUB_KEY
}


class BuyView(View):
    def get(self, request, pk, *args, **kwargs):
        instance: Item = get_object_or_404(Item, pk=pk)
        session = stripe.checkout.Session.create(
            line_items=[create_stripe_item(instance, 1)],
            mode='payment',
            success_url=f'http://localhost:8000/item/{pk}',
            cancel_url=f'http://localhost:8000/item/{pk}',
        )
        return JsonResponse(session)


class ItemView(View):
    template = 'payment/item.html'

    def get(self, request, pk, *args, **kwargs):
        item = get_object_or_404(Item, pk=pk)

        return render(
            request,
            self.template,
            context={
                'item': item,
                'stripe': secret_pub
            }
        )


class OrderView(View):
    template = 'payment/order.html'

    def get(self, request, *args, **kwargs):
        items = Item.objects.all()

        return render(
            request,
            self.template,
            context={
                'items': items,
                'stripe': secret_pub
            }
        )

    def post(self, request, *args, **kwargs):
        pk_list = list(map(int, json.loads(request.body)))

        items = Item.objects.filter(pk__in=pk_list)
        line_items = []
        for item in items:
            line_items.append(create_stripe_item(item, 1))

        session = stripe.checkout.Session.create(
            line_items=line_items,
            mode='payment',
            success_url=f'http://localhost:8000/orders',
            cancel_url=f'http://localhost:8000/orders',
        )
        return JsonResponse(session)
