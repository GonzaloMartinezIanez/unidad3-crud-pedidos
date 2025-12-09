tags_metadata = [
    {
        "name": "post_product",
        "description": "Inserta un nuevo producto en el sistema."
    },
    {
        "name": "get_product",
        "description": "Obtiene la información de un producto mediante su id."
    },
    {
        "name": "get_all_products",
        "description": "Obtiene todos los productos del sistema."
    },
    {
        "name": "post_order",
        "description": "Crea un pedido nuevo. Este puede tener cero o mas productos, pero estos deben existir en el sistema."
    },
    {
        "name": "get_order",
        "description": "Obtiene el listado de los productos que tiene un pedido mediante su id."
    },
    {
        "name": "put_order",
        "description": "Modifica la lista de productos de un pedido. Se tienen que pasar todos los productos que se quieren en el pedido. Algunos se eliminaran y otros se insertaran."
    },
    {
        "name": "delete_order",
        "description": "Elimina un pedido del sistema mediante su id."
    },
    {
        "name": "get_all_orders",
        "description": "Obtiene un listado de todos los pedidos del sistema"
    }
]