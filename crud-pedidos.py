# pip install "fastapi[standard]", pydantic
# fastapi dev .\crud-pedidos.py
import random
from fastapi import FastAPI, HTTPException, status
from estructuras_datos import Product, ProductList, OrderList, search, get_all_products
from pydantic import BaseModel
from collections import Counter
import os, json

products = None
orders = None
total_orders = 1

class Product_validation(BaseModel):
    name: str
    description: str
    price: int

class Product_list_validation(BaseModel):
    products: list[int]

def load_data_structures():
    global products
    global orders

    script_path = os.path.dirname(os.path.abspath(__file__))
    data_file_path = os.path.join(script_path, 'products.json')

    with open(data_file_path, 'r') as file:
        json_data = file.read()
    data = json.loads(json_data)

    products = Product(4562, "Monitor 27\" 4K", "Pantalla UHD de 27 pulgadas con HDR.", 329)
    for p in data:
        products.insert(p["id_product"], p["name"], p["description"], p["price"])


    orders = OrderList(1)
    orders.insert_product(1, search(products, 7023))
    orders.insert_product(1, search(products, 6241))
    orders.insert_product(1, search(products, 9978))

load_data_structures()

def get_new_order_id():
    global total_orders
    total_orders = total_orders + 1
    return total_orders

app = FastAPI()

@app.post("/product", status_code=status.HTTP_201_CREATED)
async def post_products(product: Product_validation):
    global products
    collision = 0
    id = -1
    while collision is not None:
        id = random.randrange(1, 10000, 1)
        collision = search(products, id)
    products.insert(id, product.name, product.description, product.price)

    return {"message": f"Producto añadido correctamente con id igual a {id}"}

@app.get("/product/", status_code=status.HTTP_200_OK)
async def get_product_id(id_product: int):
    global products
    result = search(products, id_product)
    if result is None:
        raise HTTPException(status_code=404, detail=f"No hay ningún producto con id igual a {id_product}")
    else:
        return result.to_json()

@app.get("/all_products/", status_code=status.HTTP_200_OK)
async def get_products():
    global products
    result = get_all_products(products)

    return result

@app.post("/order", status_code=status.HTTP_201_CREATED)
async def post_order(product_list : Product_list_validation):
    global orders, products
    for id in product_list.products:
        if search(products, id) is None:
            raise HTTPException(status_code=404, detail=f"No hay ningún producto con id igual a {id}")
    
    id_order = get_new_order_id()
    orders.insert_order(id_order)
    for id_product in product_list.products:
        orders.insert_product(id_order, search(products, id_product))

    return {"message": f"Pedido añadido correctamente con id igual a {id_order}"}

@app.get("/order/", status_code=status.HTTP_200_OK)
async def get_order_id(id_order: int):
    global orders
    result = orders.list_to_string(id_order)
    if result is None:
        raise HTTPException(status_code=404, detail=f"No hay ningún pedido con id igual a {id_order}")
    else:
        return {"message": result}

@app.put("/order/", status_code=status.HTTP_200_OK)
async def put_order_id(id_order:int, product_list : Product_list_validation):
    global orders, products
    ids = orders.get_product_id_in_order(id_order)
    product_list = product_list.products

    counter_ids = Counter(ids)
    counter_product_list = Counter(product_list)

    to_delete = list((counter_ids - counter_product_list).elements())
    to_add = list((counter_product_list - counter_ids).elements())

    for delete_id in to_delete:
        orders.delete_product(id_order, delete_id)
    
    for add_id in to_add:
        orders.insert_product(id_order, add_id)

    message = {
        "message": f"Pedido con id {id_order} ha sido modificado correctamente.",
        "added": to_add,
        "deleted": to_delete
    }

    return message

@app.delete("/order/", status_code=status.HTTP_200_OK)
async def delete_order_id(id_order:int):
    global orders
    if not orders.check_if_exists(id_order):
        raise HTTPException(status_code=404, detail=f"No hay ningún pedido con id igual a {id_order}")
    else:
        orders = orders.delete_order(id_order)   
        return {"message": f"Pedido con id {id_order} eliminado correctamente"}
