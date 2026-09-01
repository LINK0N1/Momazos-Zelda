# Momazos-Zelda

## Integrantes del Equipo

* **Amaury Alí Tristán Córdova** — [@LINK0N1] https://github.com/LINK0N1

---

## Descripción

**Meme Generator App** 
Es una aplicación de escritorio desarrollada en Python que permite a los usuarios y creadores de contenido digital generar memes de manera rápida, intuitiva y local. El proyecto resuelve la necesidad frecuente de editar imágenes para la creación de memes sin depender de software de diseño pesado (como Adobe Photoshop) ni de herramientas web de terceros que a menudo imponen marcas de agua, limitan la calidad de salida o comprometen la privacidad del usuario al subir archivos a servidores externos. A través de una interfaz gráfica ligera, la aplicación facilita la carga de plantillas mediante URL o almacenamiento local, permitiendo superponer y estilizar texto superior e inferior de forma inmediata.

## Justificación 

En la actualidad, la creación y difusión de memes forma parte fundamental de la comunicación en redes sociales y medios digitales. Sin embargo, los creadores de contenido y usuarios convencionales enfrentan problemas recurrentes al utilizar herramientas existentes:
* **Marcas de agua y pagos:** Las plataformas web gratuitas suelen incrustar marcas de agua molestas o restringir la descarga en alta calidad bajo esquemas de suscripción.
* **Privacidad y dependencia de red:** Subir imágenes a servidores de terceros compromete la privacidad de los archivos personales y requiere una conexión a Internet constante para editar.
* **Software complejo:** Las herramientas avanzadas de edición (como Adobe Photoshop o GIMP) representan una curva de aprendizaje elevada y consumen demasiados recursos de hardware para una tarea rápida.

---

## Historias de Usuario (User Stories)

Las historias de usuario definidas para la planificación y validación de las funcionalidades del sistema son las siguientes:

- [ ]* **US1:** Como usuario, quiero ingresar una URL de imagen para usarla como plantilla del meme.
- [ ] **US1: ** Como usuario, quiero ingresar texto para la parte superior de la imagen para contextualizar el meme.
- [ ] **US3:** Como usuario, quiero ingresar texto para la parte inferior de la imagen para complementar el mensaje.
- [ ] **US4:** Como usuario, quiero hacer clic en un botón de "Generar" para renderizar y visualizar la imagen con el texto superpuesto.
- [ ] **US5:** Como usuario, quiero exportar/descargar el meme generado en formato PNG o JPG en mi almacenamiento local.
- [ ] **US6:** Como usuario, quiero poder cargar una imagen local desde mi computadora además de usar URLs.
- [ ] **US7:** Como usuario, quiero personalizar el tamaño y color del texto/borde para darle mejor estética al meme.

> **Origen del Proyecto:** Idea adaptada del banco de proyectos comunitarios [App Ideas (Tier 2 - Intermediate)](https://github.com/florinpop17/app-ideas/blob/master/Projects/2-Intermediate/Meme-Generator-App.md).

---

## Metodología de Trabajo

### Enfoque Ágil (Kanban con GitHub Projects)

Para el desarrollo del proyecto se seleccionó una metodología de trabajo **Ágil basada en Kanban**, gestionada de forma centralizada mediante **GitHub Projects**.

### Justificación
Se eligió el enfoque ágil/Kanban debido al tamaño reducido del equipo (3 a 4 integrantes) y al marco de tiempo acotado disponible para la realización de la práctica. Esta metodología nos permite gestionar un *backlog* cambiante de forma flexible, descomponer las historias de usuario (*User Stories*) en *Issues* iterativos y asignables, y visibilizar en tiempo real el flujo de trabajo (columnas: *Backlog*, *In Progress*, *Review*, *Done*) en el tablero de GitHub Projects para asegurar entregas continuas e incrementos funcionales rápidos.

---

## Herramientas CASE y Tecnologías Utilizadas

### Lenguaje y Librerías de Desarrollo
* **Lenguaje de Programación:** [Python](https://www.python.org/)
* **Interfaz Gráfica de Usuario (GUI):** [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) / [Tkinter](https://docs.python.org/3/library/tkinter.html) para la construcción de una interfaz visual moderna, limpia y responsive.
* **Procesamiento de Imágenes:** [Pillow (PIL)](https://python-pillow.org/) para la manipulación, renderizado dinámico de tipografía con contorno (*stroke*), redimensionado y exportación de imágenes.

### Herramientas CASE (Computer-Aided Software Engineering)
* **Gestión del Proyecto:** [GitHub Projects](https://github.com/features/projects) para el seguimiento de tareas con el tablero Kanban y la vinculación automática de *Issues* y *Pull Requests*.
* **Modelado y Diagramado:** [draw.io (diagrams.net)](https://app.diagrams.net/) para el diseño de diagramas estructurales, casos de uso y diagramas de flujo de la arquitectura del software.

---

