from django.db import models
import pgtrigger
from product.models import BaseModel, Product

class ProductCost(BaseModel):
    product = models.ForeignKey(Product, blank=False, null=False, on_delete=models.CASCADE)
    cost = models.DecimalField(max_digits=8, decimal_places=2, blank=False, null=False)
    date = models.DateField(blank=False, null=False)

    class Meta:
        triggers = [
            pgtrigger.Trigger(
                name="cost__gte_min_cost_and__lte_max_cost",
                level=pgtrigger.Row,
                when=pgtrigger.Before,
                operation=pgtrigger.Insert | pgtrigger.Update,
                declare=[('product_min_cost', 'NUMERIC(8,2)'), ('product_max_cost', 'NUMERIC(8,2)')],
                func=f"""
                    IF (new.cost IS NULL) THEN
                        RETURN NEW;
                    END IF;

                    SELECT min_cost, max_cost INTO product_min_cost, product_max_cost FROM {Product._meta.db_table} WHERE id = NEW.product_id;

                    IF (NOT FOUND) THEN
                        SELECT min_cost, max_cost INTO product_min_cost, product_max_cost FROM {Product._meta.db_table} WHERE id = OLD.product_id;
                    END IF;

                    IF (NEW.cost >= product_min_cost AND  NEW.cost <= product_max_cost) THEN
                        RETURN NEW;
                    ELSE
                        RAISE 'Cost must be greater than % and less than %.', product_min_cost, product_max_cost USING ERRCODE = 'check_violation';
                    END IF;
                """
            )
        ]
