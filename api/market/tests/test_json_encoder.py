import json
from uuid import uuid4
from datetime import date
from decimal import Decimal
from product.models import Product
from utils.json_encoder import CustomJSONEncoder


def test_dumps():
    product_id = uuid4()
    data_to_dump = {
        "date": date(year=2022, month=11, day=14),
        "number": Decimal("10.01"),
        "model": Product(id=product_id),
        "object": { "name": "tradex" }
    }
    expected_dump = json.dumps({
        "date": "2022-11-14",
        "number": "10.01",
        "model": str(product_id),
        "object": { "name": "tradex" }
    })

    dump = json.dumps(data_to_dump, cls=CustomJSONEncoder)

    assert dump == expected_dump
