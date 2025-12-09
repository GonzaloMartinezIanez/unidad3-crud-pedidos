# Arbol binario para almacenar los productos
class Product:
    def __init__(self, id_product: int, name: str, description: str, price: int):
        self.id_product = id_product
        self.name = name
        self.description = description
        self.price = price
        self.left = None
        self.right = None
    
    # Añade un nuevo nodo al arbol
    def insert(root, id_product, name, description, price):
        # El padre de este nodo
        if root is None:
            return Product(id_product, name, description, price)
        # Guarda los nuevos productos con id menor que el actual en la izquierda
        # y los mayores en la derecha
        if id_product < root.id_product:
            root.left = Product.insert(root.left, id_product, name, description, price)
        else:
            root.right = Product.insert(root.right, id_product, name, description, price)
        
        return root
    
    # Devuelve la informacion del producto en formato json
    def to_json(self):
        return {            
                "id_product": self.id_product,
                "name": self.name,
                "description": self.description,
                "price": self.price
        }
    
    # Funcion auxiliar
    def get_data(self):
        return (self.id_product, self.name, self.description, self.price)

# Funcion que devuelve el nodo del producto con este id
def search(root : Product, id_product):
    if root is None or root.id_product == id_product:
        return root
    if root.id_product > id_product:
        if root.left is None:
            return None
        else:
            return search(root.left, id_product)
    else:
        if root.right is None:
            return None
        else:
            return search(root.right, id_product)

# Recorre todo el arbol de productos en inorder y devuelve
# los productos en formato json
def inorder(root: Product):
    if root is None:
        return []
    
    result = []

    
    if root.left is not None:
        result.extend(inorder(root.left))

    result.append(root.to_json())

    if root.right is not None:
        result.extend(inorder(root.right))


    return result

# Devuelve un json con la lista de productos del arbol
def get_all_products(root: Product):
    result = {
        "products": inorder(root)
    }    
    return result

# Lista enlazada que guarda una lista de productos
class ProductList:
    def __init__(self, product : Product):
        self.product = product
        self.next = None

    # Añade un nuevo nodo al final de la lista
    def insert(self, product):
        if self.next is None:
            self.next = ProductList(product)
        else:
            self.next.insert(product)

    # Elimina un nodo de la lista y devuelve el puntero del primer nodo
    def delete(self, id_product):
        # Hay que borrar el primero
        if self.product.id_product == id_product:
            # Se devuelve el segundo de la lista (None si no hay segundo)
            return self.next
        
        aux = self
        found = False
        while not found:
            # No se ha encontrado
            if aux.next is None:
                found = True
            else:
                # Hay que eliminar el siguiente producto
                if aux.next.product.id_product == id_product:
                    aux.next = aux.next.next
                    found = True

            aux = aux.next
        
        # Se devuelve el primer producto de la lista
        return self
    
    # Recorre recursivamente la lista y devuelve un listado
    # con el id de los productos en la lista
    def get_ids(self):
        if self.next is None:
            ids = [self.product.id_product]
            return ids
        else:
            ids = [self.product.id_product]
            ids.extend(self.next.get_ids())
            return ids

    # Metodo auxiliar para probar el contenido de una lista
    def to_string(self):
        this_product = f"[id: {self.product.id_product} - nombre: {self.product.name} - descripcion: {self.product.description} - precio: {self.product.price}]"
        if self.next is None:
            return this_product
        else:
            return this_product + self.next.to_string()
    
    # Metodo que devuelve un array con todos los productos que tiene la lista
    def to_json(self):
        if self.next is None:
            return [self.product.get_data()]
        else:
            data = [self.product.get_data()]
            data.extend(self.next.to_json())
            return data

        
# Lista enlazada que guarda una lista de pedidos que a su vez guardan otra
# lista enlazada de productos
class OrderList:
    def __init__(self, id_order: int):
        self.id_order = id_order
        self.orders = None
        self.next = None

    # Añade un nuevo producto al pedido con este id
    def insert_product(self, id_order, new_product):
        if self.id_order == id_order:
            # La lista esta vacia
            if self.orders is None:
                self.orders = ProductList(new_product)
            # Delegar la inserccion al primero de la lista
            else:
                self.orders.insert(new_product)
        elif self.next is not None:
            self.next.insert_product(id_order, new_product)
        # Si no hay siguiente, no existe un pedido con este id

    # Crea un nodo en la lista con un pedido vacio
    def insert_order(self, id_order):
        if self.next is None:
              self.next = OrderList(id_order)
        else:
            self.next.insert_order(id_order)

    # Elimina un producto de la lista de productos del pedido con este id
    def delete_product(self, id_order, id_product):
        if self.id_order == id_order:
            self.orders = self.orders.delete(id_product)
        elif self.next is not None:
            self.next.delete_product(id_order, id_product)
        
    # Elimina un pedido y devuelve el primer nodo de la lista de pedidos
    def delete_order(self, id_order):
        # Hay que borrar el primero
        if self.id_order == id_order:
            return self.next
        
        aux = self
        found = False
        while not found:
            # No se ha encontrado
            if aux.next is None:
                found = True
            else:
                # Hay que eliminar el siguiente producto
                if aux.next.id_order == id_order:
                    aux.next = aux.next.next
                    found = True

            aux = aux.next

        # Se devuelve el primer producto de la lista
        return self
    
    # Recorre la lista de pedidos y devuelve los ids de los productos que tiene
    # el pedido con el id pasado
    def get_product_id_in_order(self, id_order):
        if self.id_order == id_order:
            if self.orders is None:
                return []
            else:
                return self.orders.get_ids()
        elif self.next is not None:
            return self.next.get_product_id_in_order(id_order)

    # Comprueba que exista un pedido con este id
    # Si se intenta hacer uso de un pedido que no existe, la aplicacion
    # generara un error de tipo 500
    def check_if_exists(self, id_order):
        if self.id_order == id_order:
            return True
        elif self.next is not None:
            return self.next.check_if_exists(id_order)
        else:
            return False

    # Recorre todos los pedidos y devuelve el que tenga el mayor id utilizado
    # para insertar nuevos pedidos
    def get_highest_id_order(self):
        if self.next is None:
            return self.id_order
        else:
            next_highest = self.next.get_highest_id_order()
            if self.id_order > next_highest:
                return self.id_order
            else:
                return next_highest

    # Metodo auxilair para probar el contenido de los pedidos
    def list_to_string(self, id_order):
        if id_order == self.id_order:
            return self.orders.to_string()
        elif self.next is not None:
            return self.next.list_to_string(id_order)
    
    # Devuelve un json que tiene un listado con todos los productos que tiene
    # el pedido con este id
    def list_to_json(self, id_order):
        if id_order == self.id_order:
            # No tiene productos
            if self.orders is None:
                return {
                    "products": []
                }
            else:
                # Generar el json con todos los productos
                data = self.orders.to_json()
                result = {
                    "products": []
                }
                for p in data:
                    result['products'].append({
                        "id_product": p[0],
                        "name": p[1],
                        "description": p[2],
                        "price": p[3]
                    })

                return result
        elif self.next is not None:
            # Buscar en el siguiente pedido
            return self.next.list_to_json(id_order)

    # Devuelve todos los pedidos con su productos
    def all_orders_to_json(self):
        # Es el ultimo
        if self.next is None:
            return [{
                "id_order" : self.id_order,
                "products": self.list_to_json(self.id_order)["products"]
            }]
        else:
            this_order = []
            # Pedido sin productos
            if self.orders is None:
                this_order = [{
                    "id_order" : self.id_order,
                    "products": []
                }] 
            else:
                # Buscar los productos del pedido actual
                this_order = [{
                    "id_order" : self.id_order,
                    "products": self.list_to_json(self.id_order)["products"]
                }]  
            # Devolver el resto de forma recursiva           
            return this_order + (self.next.all_orders_to_json())

# Devuelve todos los pedidos en formato json
def get_all_orders(orders : OrderList):
    result = {
        "orders": orders.all_orders_to_json()
    }

    return result


""" 
# Pruebas
products = Product(24, "Tornillo", "descripcion tornillo", 6)
products.insert(10, "Tuerca", "descripcion tuerca", 5)
products.insert(43, "Destornillador", "descripcion destronillador", 49)
products.insert(20, "LLave inglesa", "descripcion llave inglesa", 123)

#print(search(products, 10).description)

orders = OrderList(1)
orders.insert_product(1, search(products, 10))
orders.insert_product(1, search(products, 43))
#print(orders.list_to_string(1))
orders.delete_product(1, 10)
#print(orders.list_to_string(1))
orders.insert_order(2)
orders.insert_product(2, search(products, 24))
orders.insert_product(2, search(products, 20))
orders.delete_product(2, 24)
#print(orders.list_to_string(2))
orders = orders.delete_order(2)
print(orders.list_to_string(2)) """