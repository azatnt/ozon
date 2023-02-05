from shop.models import Product


def perform_data_from_api(data):
    values = {}
    res = []
    data = data['result']['postings']
    if len(data) > 0:
        for i in data:
            values['date'] = i['in_process_at']
            for j in i['products']:
                values['artikul'] = j['offer_id']
                values['name'] = j['name']
                values['quantity'] = j['quantity']
                new_product = Product.objects.filter(name=values['name'], artikul=values['artikul'])
                if not new_product.exists():
                    Product.objects.create(**values)
                values = {}
