# Pregunta 1

##### Intente usar el script que inventó ahora con IPv6: ¿Cuánto se debe modificar lo hecho? ¿Por qué?

Para poder utilizar el script usando IPv6 habría que ccambiar algunas cosas, por ejemplo, el formato es distinto, ya que en IPv4 se utilizan 4 bytes para representar la dirección IP, mientras que en IPv6 se utilizan 16 bytes, por lo que habría que cambiar el código para usar este formato. Por otro lado también habría que tener en cuenta que el formato de los paquetes es distinto, así que para hacer un paquete falso habría que cambiar los campos que se modifican en el código. Finalemente también habría que tener en cuenta que en IPv6 existen métodos de seguridad extra que no existen en IPv4, por lo que habría que tener en cuenta esto para poder inyectar paquetes.

# Pregunta 2

##### Este ejercicio muestra lo trivial que es la seguridad en UDP. Si uno quisiera tener un sistema seguro en UDP, ¿cómo podrı́amos protegernos de este tipo de falsificaciones?

Para tener un sistema más seguro en UDP se podría utilizar un sistema de autenticación, por ejemplo, utilizando un hash de la información que se envía en el paquete, de esta forma, si alguien quisiera falsificar un paquete, tendría que conocer el hash de la información que se envía, lo que es muy poco probable. Otra forma de hacerlo sería utilizando un sistema de encriptación, de esta forma, si alguien quisiera falsificar un paquete, tendría que conocer la llave de encriptación, lo que es muy poco probable.

# Pregunta 3

##### 3. En TCP, ¿serı́a igual de trivial inyectar un paquete de datos?

No, ya que en TCP hay un mayor control de la conexión entre el cliente y el servidor, por lo que es más difícil falsificar un paquete de datos (3-way handshake, etc). También habría que saber adaptarse al control de flujo que se esté usando (ventana deslizante, etc), lo cual es mucho más complejo que en UDP. Y finalemente, TCP también suele usar métodos de autenticación y encriptación, lo que hace aún más difícil falsificar un paquete de datos.

# Pregunta 4

##### Si ahora queremos que el pirata esté en otro computador que el cliente ¿se podrı́a hacer lo mismo con scapy? ¿Cómo?

Si, se podría hacer lo mismo con scapy, ya que scapy permite modificar los paquetes que se envían, por lo que se podría modificar la dirección IP del cliente para que sea la del pirata, y luego modificar la dirección IP del servidor para que sea la del cliente. De esta forma, el servidor recibiría el paquete del pirata, pero creería que lo está recibiendo del cliente. Pero también habría que tener en cuenta que para hacer funcionar este código se requirió de permisos de administrador, por lo que para hacerlo funcionar en otro computador habría que de alguna forma conseguir cambiar las configuraciones de red del computador para que permita inyectar paquetes.
