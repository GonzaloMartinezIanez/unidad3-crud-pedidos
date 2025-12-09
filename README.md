# CRUD de pedidos con estructuras de datos avanzadas
Universidad Europea\
Fundamendos de backend con python\
Ejercicio entregable de la Unidad 3\
Gonzalo Martínez Iáñez

## Instalación
Crear el entorno virtual
```
py -m venv venv
```
Activar el entorno (Windows, para linux o mac usar su forma para ejecutar programas)
```
.\venv\Scripts\activate
```
Instalar la librerias necesarias
```
pip install "fastapi[standard]", pydantic
```

## Ejecución
Lanzar la API y dejar ejecutando para poder recibir peticiones http (la ruta será http://127.0.0.1:8000/docs)
```
fastapi dev .\crud-pedidos.py
```

## Memoria
### Funcionamiento
Esta aplicación te permite crear productos con nombre, descripción, precio (y un id que genera el sistema). Además se pueden generar pedidos que constan de un listado de productos y un id generado automáticamente.\
A continuación se enumeran todas las peticiones http disponibles en el sistema.
1. Products
    - GET /product/?id_product=int : Devuelve la información de un producto mediante su id, si no existe ningún producto con esta id se devuelve error 404.
    - GET /all_products : Devuelve la información de todos los productos.
    - POST /product : Añade un producto al sistema, en el cuerpo de la petición hay que enviar un json con los atributos "name" (str), "description" (str) y "price" (int). El sistema generará un id nuevo y lo devolverá junto a un mensaje de éxito.
2. Orders
    - GET /order/?id_order=int : Devuelve un listado con los productos que hay en el pedido con id_order pasado como parámetro.
    - GET /all_orders : Devuelve un listado con todos los pedidos
    - POST /order : Añade un pedido al sistema, este puede traer un listado ids de productos con o sin productos. Devuelve el id_order generado junto a un mensaje de éxito.
    - PUT /order/?id_order=int : Modifica el pedido con id_order pasado como parámetro. En el body se pasa el nuevo listado con los productos que deberá contener este pedido y devolverá un mensaje con los productos que se han insertado, los que se han eliminado y un mensaje de éxito.
    - DELETE /order/?id_order=int : Elimina el pedido con id_order pasado como parámetro.
3. Documentación
    - GET /docs : Devuelve una interfaz gráfica para el navegador que sirve para probar los disintos métodos.
![Interfaz visual para probar las peticiones](img/swagger.png)

Esta aplicación guarda los productos y pedidos en un fichero pickle, pero si se quiere reiniciar el sistema con valores por defecto hay que descomentar la función load_default_data() y comentar load_data_structures(). Viceversa para volver a usar los datos que persisten entre reinicios.

### Conclusión
En este ejercicio he decidido usar fastAPI ya que en el anterior usé Flask y así puedo practicar ambos frameworks. Además en fastAPI, la documentación de swagger se genera automáticamente y también gestiona la validación de datos con pydantic. Además en el ejercicio anterior, en las rutas se pasaba el id de esta forma /product/{id_product}, en esta he usado esta otra /product/?id_product={id} para prácticar ambas.\
He usado un arbol binario de búsqueda para almacenar los productos programado por mi. Para este caso de uso, que no va a producción ni va a escalar mucho, esta estructura de datos es válida. Pero he decidido que a la hora de insertar los productos, el id se elija aleatoriamente entre el 1 y el 10000. De no ser así y los ids van incrementando de uno en uno, el árbol solo tendría ramas derechas y perdería su ventaja a la hora de hacer búsquedas ya que pasa de una eficiencia de O(log(n)) a O(n). La alternativa más razonable es sustituir este BST por uno que se autobalancee con cada insercción y así todas las hojas tendrán una profundidad similar.\
Para simular el almacenamiento en una base de datos, he decidido serializar las estructuras de datos de los productos y los pedidos en un fichero de tipo pickle, de esta forma, cada vez que se inserta un nuevo item en el sistema, se sobreescriben estos datos y perduran entre reinicios del sistema. Es una solución fácil y rápida de programar, pero muy poco eficiente en tiempo ya que si se modifica un solo pedido o se inserta un producto, hay que volver a volcar toda la información.\