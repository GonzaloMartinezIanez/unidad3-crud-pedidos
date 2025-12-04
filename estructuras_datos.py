class Product:
    def __init__(self, id_product, name, description, price):
        self.id_product = id_product
        self.name = name
        self.description = description
        self.price = price
        self.left = None
        self.right = None
    
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

class Product_list:
    def __init__(self, product):
        self.product = product
        self.next = None

    def insert(self, product):
        if self.next is None:
            self.next = Product_list(product)
        else:
            self.next.insert(product)

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
      

    def to_string(self):
        this_product = f"[id: {self.product.id_product} - nombre: {self.product.name} - descripcion: {self.product.description} - precio: {self.product.price}]"
        if self.next is None:
            return this_product
        else:
            return this_product + self.next.to_string()

class Order:
    def __init__(self, id_order):
        self.id_order = id_order
        self.orders = None

    def insert(self, new_product):
        # La lista esta vacia
        if self.orders is None:
            self.orders = Product_list(new_product)
        # Delegar la inserccion al primero de la lista
        else:
            self.orders.insert(new_product)

    def delete(self, id_product):
        if self.orders is not None:
            self.orders = self.orders.delete(id_product)

    def list_to_string(self):
        return self.orders.to_string()

products = Product(24, "Tornillo", "descripcion tornillo", 6)
products.insert(10, "Tuerca", "descripcion tuerca", 5)
products.insert(43, "Destornillador", "descripcion destronillador", 49)
products.insert(20, "LLave inglesa", "descripcion llave inglesa", 123)

print(search(products, 10).description)

order_1 = Order(1)
order_1.insert(search(products, 43))
order_1.insert(search(products, 10))
order_1.insert(search(products, 20))
print(order_1.list_to_string())
order_1.delete(20)
print(order_1.list_to_string())