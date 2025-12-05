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

class ProductList:
    def __init__(self, product):
        self.product = product
        self.next = None

    def insert(self, product):
        if self.next is None:
            self.next = ProductList(product)
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

class OrderList:
    def __init__(self, id_order):
        self.id_order = id_order
        self.orders = None
        self.next = None

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
        # Si no hay siguiente, no existe una orden con este id

    def insert_order(self, id_order):
        if self.next is None:
              self.next = OrderList(id_order)
        else:
            self.next.insert_order(id_order)

    def delete_product(self, id_order, id_product):
        if self.id_order == id_order:
            self.orders = self.orders.delete(id_product)
        elif self.next is not None:
            self.next.delete_product(id_order, id_product)
        
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

    def list_to_string(self, id_order):
        if id_order == self.id_order:
            return self.orders.to_string()
        elif self.next is not None:
            return self.next.list_to_string(id_order)





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
print(orders.list_to_string(2))