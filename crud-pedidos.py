# pip install "fastapi[standard]", pydantic
# fastapi dev .\crud-pedidos.py
import random, os, json, pickle
from fastapi import FastAPI, HTTPException, status
from estructuras_datos import Product, ProductList, OrderList, search, get_all_products
from pydantic import BaseModel
from collections import Counter
from doc import tags_metadata

products = None
orders = None
total_orders = None

class Product_validation(BaseModel):
    name: str
    description: str
    price: int

class Product_list_validation(BaseModel):
    products: list[int]

def load_default_product():
    global products
    script_path = os.path.dirname(os.path.abspath(__file__))
    data_file_path = os.path.join(script_path, './data/products.json')

    with open(data_file_path, 'r') as file:
        json_data = file.read()
    data = json.loads(json_data)

    products = Product(4562, "Monitor 27\" 4K", "Pantalla UHD de 27 pulgadas con HDR.", 329)
    for p in data:
        products.insert(p["id_product"], p["name"], p["description"], p["price"])

    with open("./data/products.pkl", "wb") as f:
        pickle.dump(products, f)

def load_default_orders():
    global orders
    orders = OrderList(1)
    orders.insert_product(1, search(products, 7023))
    orders.insert_product(1, search(products, 6241))
    orders.insert_product(1, search(products, 9978))
    orders.insert_order(2)    
    orders.insert_order(3)
    orders.insert_product(3, search(products, 514))
    orders.insert_product(3, search(products, 6241))
    orders.insert_product(3, search(products, 514))

    with open("./data/orders.pkl", "wb") as f:
        pickle.dump(orders, f)
    
    total_orders = orders.get_highest_id_order()

def load_default_data():
    load_default_product()
    load_default_orders()

def load_data_structures():
    global products
    global orders
    global total_orders

    with open("./data/products.pkl", "rb") as f:
        products = pickle.load(f)
    if products is None:
        load_default_product()

    with open("./data/orders.pkl", "rb") as f:
        orders = pickle.load(f)

    if orders is None:
        load_default_orders()
    
    

def save_products():
    global products

    with open("./data/products.pkl", "wb") as f:
        pickle.dump(products, f)
    
def save_orders():
    global orders

    with open("./data/orders.pkl", "wb") as f:
        pickle.dump(orders, f)

#load_default_data()
load_data_structures()

def get_new_order_id():
    global total_orders
    total_orders = total_orders + 1
    return total_orders

app = FastAPI(
    title="CRUD Pedidos",
    description="Fundamentos de backend con python. Entrega Unidad 3: API para gestionar un sistema de pedidos de una tienda online.",
    openapi_tags=tags_metadata
)

@app.post("/product", status_code=status.HTTP_201_CREATED, tags=["post_product"])
async def post_products(product: Product_validation):
    global products
    collision = 0
    id = -1
    while collision is not None:
        id = random.randrange(1, 10000, 1)
        collision = search(products, id)
    products.insert(id, product.name, product.description, product.price)

    save_products()

    return {"message": f"Producto añadido correctamente con id igual a {id}"}

@app.get("/product/", status_code=status.HTTP_200_OK, tags=["get_product"])
async def get_product_id(id_product: int):
    global products
    result = search(products, id_product)
    if result is None:
        raise HTTPException(status_code=404, detail=f"No hay ningún producto con id igual a {id_product}")
    else:
        return result.to_json()

@app.get("/all_products/", status_code=status.HTTP_200_OK, tags=["get_all_products"])
async def get_products():
    global products
    result = get_all_products(products)

    return result

@app.post("/order", status_code=status.HTTP_201_CREATED, tags=["post_order"])
async def post_order(product_list : Product_list_validation):
    global orders, products
    for id in product_list.products:
        if search(products, id) is None:
            raise HTTPException(status_code=404, detail=f"No hay ningún producto con id igual a {id}")
    
    id_order = get_new_order_id()
    if orders is None:
        orders = OrderList(id_order)

    orders.insert_order(id_order)
    for id_product in product_list.products:
        orders.insert_product(id_order, search(products, id_product))

    save_orders()

    return {"message": f"Pedido añadido correctamente con id igual a {id_order}"}

@app.get("/order/", status_code=status.HTTP_200_OK, tags=["get_order"])
async def get_order_id(id_order: int):
    global orders
    if orders is None:
        raise HTTPException(status_code=404, detail=f"No hay ningún pedido en el sistema")
    if not orders.check_if_exists(id_order):
        raise HTTPException(status_code=404, detail=f"No hay ningún pedido con id igual a {id_order}")
    
    result = orders.list_to_json(id_order)

    return result

@app.put("/order/", status_code=status.HTTP_200_OK, tags=["put_order"])
async def put_order_id(id_order:int, product_list : Product_list_validation):
    global orders, products
    if orders is None:
        raise HTTPException(status_code=404, detail=f"No hay ningún pedido en el sistema")    
    if not orders.check_if_exists(id_order):
        raise HTTPException(status_code=404, detail=f"No hay ningún pedido con id igual a {id_order}")
    
    for id in product_list.products:
        if search(products, id) is None:
            raise HTTPException(status_code=404, detail=f"No hay ningún producto con id igual a {id}")
        
    ids = orders.get_product_id_in_order(id_order)
    product_list = product_list.products

    counter_ids = Counter(ids)
    counter_product_list = Counter(product_list)

    to_delete = list((counter_ids - counter_product_list).elements())
    to_add = list((counter_product_list - counter_ids).elements())

    for delete_id in to_delete:
        orders.delete_product(id_order, delete_id)
    
    for add_id in to_add:
        orders.insert_product(id_order, search(products, add_id))

    message = {
        "message": f"Pedido con id {id_order} ha sido modificado correctamente.",
        "added": to_add,
        "deleted": to_delete
    }

    save_orders()

    return message

@app.delete("/order/", status_code=status.HTTP_200_OK, tags=["delete_order"])
async def delete_order_id(id_order:int):
    global orders
    if orders is None:
        raise HTTPException(status_code=404, detail=f"No hay ningún pedido con id igual a {id_order}")
    if not orders.check_if_exists(id_order):
        raise HTTPException(status_code=404, detail=f"No hay ningún pedido con id igual a {id_order}")
    else:
        orders = orders.delete_order(id_order)
        save_orders()
        return {"message": f"Pedido con id {id_order} eliminado correctamente"}
