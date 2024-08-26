from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Material, Warehouse, ProductMaterials


class DistributeMaterialsView(APIView):

    def post(self, request, *args, **kwargs):
        products_data = request.data.get('products', [])
        result = []

        warehouse_remaining = {w.id: w.remainder for w in Warehouse.objects.all()}

        for product_data in products_data:
            product_name = product_data['product_name']
            product_qty = product_data['product_qty']

            product = Product.objects.get(name=product_name)
            product_materials = ProductMaterials.objects.filter(product=product)

            materials_list = []
            material_needed = {}
            for pm in product_materials:
                if pm.material.name not in material_needed:
                    material_needed[pm.material.name] = 0
                material_needed[pm.material.name] += pm.quantity * product_qty

            for material_name, needed_qty in material_needed.items():
                warehouses = Warehouse.objects.filter(material__name=material_name).order_by('id')
                for warehouse in warehouses:
                    if needed_qty <= 0:
                        break

                    available_qty = min(needed_qty, warehouse_remaining.get(warehouse.id, 0))
                    warehouse_remaining[warehouse.id] = max(0, warehouse_remaining.get(warehouse.id, 0) - available_qty)
                    needed_qty -= available_qty

                    materials_list.append({
                        "warehouse_id": warehouse.id if available_qty > 0 else None,
                        "material_name": material_name,
                        "qty": available_qty,
                        "price": warehouse.price if available_qty > 0 else None,
                    })

                if needed_qty > 0:
                    materials_list.append({
                        "warehouse_id": None,
                        "material_name": material_name,
                        "qty": needed_qty,
                        "price": None,
                    })

            result.append({
                "product_name": product_name,
                "product_qty": product_qty,
                "product_materials": materials_list
            })

        return Response({"result": result}, status=status.HTTP_200_OK)
