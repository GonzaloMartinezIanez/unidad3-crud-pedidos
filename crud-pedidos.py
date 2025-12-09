# pip install "fastapi[standard]", pydantic
# fastapi dev .\crud-pedidos.py
import random, os, json, pickle
from fastapi import FastAPI, HTTPException, status
from estructuras_datos import Product, ProductList, OrderList, search, get_all_products
from pydantic import BaseModel
from collections import Counter
from doc import tags_metadata

# Variables globales que guardan las estructuras de datos
products = None
orders = None
# Recuento total de pedidos
total_orders = -1

# Modelo para validar que se ha enviado un producto correctamente
class Product_validation(BaseModel):
    name: str
    description: str
    price: int

# Modelo para validar que se ha enviado un listado de productos correctamente
class Product_list_validation(BaseModel):
    products: list[int]

# Carga los productos con informacion por defecto
def load_default_product():
    global products
    script_path = os.path.dirname(os.path.abspath(__file__))
    data_file_path = os.path.join(script_path, './data/products.json')

    # Cargar los datos de lso productos
    with open(data_file_path, 'r') as file:
        json_data = file.read()
    data = json.loads(json_data)

    # Crear el arbol
    products = Product(4562, "Monitor 27\" 4K", "Pantalla UHD de 27 pulgadas con HDR.", 329)
    for p in data:
        products.insert(p["id_product"], p["name"], p["description"], p["price"])

    # Guardar los productos en un fichero
    with open("./data/products.pkl", "wb") as f:
        pickle.dump(products, f)

# Carga los pedidos con informacion por defecto
def load_default_orders():
    global orders, total_orders
    # Generar los pedidos
    orders = OrderList(1)
    orders.insert_product(1, search(products, 7023))
    orders.insert_product(1, search(products, 6241))
    orders.insert_product(1, search(products, 9978))
    orders.insert_order(2)    
    orders.insert_order(3)
    orders.insert_product(3, search(products, 514))
    orders.insert_product(3, search(products, 6241))
    orders.insert_product(3, search(products, 514))

    # Guardar los pedidos en un fichero pickle
    with open("./data/orders.pkl", "wb") as f:
        pickle.dump(orders, f)
    
    # Se obtiene el id más alto para ir añadiendo respecto a este
    total_orders = orders.get_highest_id_order()

# Carga los productos y pedidos con información por defecto
def load_default_data():
    load_default_product()
    load_default_orders()

# Carga los productos y pedidos desde los ficheros pickle
# De esta forma se simula una base de datos con persistencia
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
    
    # Se obtiene el id más alto para ir añadiendo respecto a este
    total_orders = orders.get_highest_id_order()
   
# Guarda los productos en un fichero pickle
def save_products():
    global products

    with open("./data/products.pkl", "wb") as f:
        pickle.dump(products, f)

# Guarda los pedidos en un fichero pickle
def save_orders():
    global orders

    with open("./data/orders.pkl", "wb") as f:
        pickle.dump(orders, f)

# Si se corrompen los ficheros o se quiere reiniciar los productos y pedidos
# hay que descomentar load_default_data() y comentar load_data_structures()
#load_default_data()
load_data_structures()

# Devuelve el id que debe tener el siguiente pedido
def get_new_order_id():
    global total_orders
    total_orders = total_orders + 1
    return total_orders

# Aplicacion de fastapi
app = FastAPI(
    title="CRUD Pedidos",
    description="Fundamentos de backend con python. Entrega Unidad 3: API para gestionar un sistema de pedidos de una tienda online.",
    openapi_tags=tags_metadata
)

# Endpoint para insertar productos
@app.post("/product", status_code=status.HTTP_201_CREATED, tags=["post_product"])
async def post_products(product: Product_validation):
    global products
    collision = 0
    id = -1
    # Como no puede haber dos productos con el mismo id,
    # se generan ids aleatorios entre 1 y 10000 hasta que no haya colision
    # La estructura de datos donde se guardan los productos es un arbol binario de busqueda
    # por tanto si se van insertando id consecutivos, cada nodo tendria solo un hijo en la derecha
    # y la eficiencia pasaria de O(log(n)) a O(n)
    # Para solucionar esto se deberia de cambiar el BST por un arbol binario balanceado
    while collision is not None:
        id = random.randrange(1, 10000, 1)
        collision = search(products, id)
    products.insert(id, product.name, product.description, product.price)

    save_products()

    return {"message": f"Producto añadido correctamente con id igual a {id}"}

# Endpoint que devuelve la informacion de un producto a partir de su id
@app.get("/product/", status_code=status.HTTP_200_OK, tags=["get_product"])
async def get_product_id(id_product: int):
    global products
    result = search(products, id_product)
    if result is None:
        raise HTTPException(status_code=404, detail=f"No hay ningún producto con id igual a {id_product}")
    else:
        return result.to_json()

# Endpoint que devuelve un lista con todos los productos
@app.get("/all_products/", status_code=status.HTTP_200_OK, tags=["get_all_products"])
async def get_products():
    global products
    # El arbol de productos se recorre en inorden
    result = get_all_products(products)

    return result

# Endpoint para insertar nuevos pedidos
@app.post("/order", status_code=status.HTTP_201_CREATED, tags=["post_order"])
async def post_order(product_list : Product_list_validation):
    global orders, products
    # Comprobar que los productos a insertar existen
    for id in product_list.products:
        if search(products, id) is None:
            raise HTTPException(status_code=404, detail=f"No hay ningún producto con id igual a {id}")
    
    id_order = get_new_order_id()
    # Si se han borrado todos los pedidos, orders sera none
    if orders is None:
        orders = OrderList(id_order)

    # Crear el pedido e insertar todos los productos
    orders.insert_order(id_order)
    for id_product in product_list.products:
        orders.insert_product(id_order, search(products, id_product))

    save_orders()

    return {"message": f"Pedido añadido correctamente con id igual a {id_order}"}

# Enpoint que devuelve un lista con los productos de un pedido
@app.get("/order/", status_code=status.HTTP_200_OK, tags=["get_order"])
async def get_order_id(id_order: int):
    global orders
    if orders is None:
        raise HTTPException(status_code=404, detail=f"No hay ningún pedido en el sistema")
    if not orders.check_if_exists(id_order):
        raise HTTPException(status_code=404, detail=f"No hay ningún pedido con id igual a {id_order}")
    
    result = orders.list_to_json(id_order)

    return result

# Endpoint que modifica la lista de productos de un pedido
@app.put("/order/", status_code=status.HTTP_200_OK, tags=["put_order"])
async def put_order_id(id_order:int, product_list : Product_list_validation):
    global orders, products
    if orders is None:
        raise HTTPException(status_code=404, detail=f"No hay ningún pedido en el sistema")    
    if not orders.check_if_exists(id_order):
        raise HTTPException(status_code=404, detail=f"No hay ningún pedido con id igual a {id_order}")
    
    # Comprobar que existen los productos
    for id in product_list.products:
        if search(products, id) is None:
            raise HTTPException(status_code=404, detail=f"No hay ningún producto con id igual a {id}")
        
    # Se obtiene una lista con los id que tiene la orden a modificar
    # y se compara con la pasada por parametro, con esto se puede saber
    # que producto sobran y cuales faltan
    # Otra alternativa seria borrar el pedido y generar uno nuevo con los nuevos productos
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

# Enpoint que elimina un pedido a partir de su id
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
