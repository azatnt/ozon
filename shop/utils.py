from shop.models import Product


def perform_data_from_api(data):
    values = {}
    res = []
    data = data['result']['postings']
    if len(data) > 0:
        for i in data:
            values['date'] = i['in_process_at']
            values['posting_number'] = i['posting_number']
            for j in i['products']:
                values['artikul'] = j['offer_id']
                values['name'] = j['name']
                values['quantity'] = j['quantity']
                product = Product.objects.filter(posting_number=values['posting_number'])
                if not product.exists():
                    Product.objects.create(**values)
                values = {}
