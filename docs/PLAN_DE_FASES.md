# Plan de fases

> Este plan es una **propuesta interna del equipo** para el proyecto de práctica.
> No es un requisito de NASA. Se puede ajustar.

**Total: 7 fases (0 a 6).** Cada fase termina con una entrega verificable.

| Fase | Nombre | Responsable principal | Entregable verificable |
|------|--------|-----------------------|------------------------|
| 0 | Preparación | Los 3 | Repo privado clonado por los 3, entorno funcionando, primer PR aprobado |
| 1 | Datos GIS | Aldo | Zona de estudio elegida y al menos 2 capas procesadas en `data/processed/`, documentadas |
| 2 | Backend base | Jesús | API que sirve las capas y responde `/health` y consultas de capas |
| 3 | Frontend base | Luis | Mapa Leaflet que muestra las capas con control para activarlas/desactivarlas |
| 4 | Ruta y riesgo | Jesús (+ Aldo datos, Luis visualización) | Ruta origen→destino con costo por pendiente/riesgo, dibujada en el mapa |
| 5 | Pruebas y documentación | Los 3 | Pruebas básicas pasando, README y docs actualizados |
| 6 | Cierre y lecciones aprendidas | Los 3 | Documento `docs/LECCIONES_APRENDIDAS.md` para llegar preparados al reto real |

## Detalle por fase

### Fase 0: Preparación
- Crear repositorio privado y agregar a Aldo y Luis como colaboradores.
- Cada uno clona, crea su entorno y corre el proyecto vacío.
- Practicar el flujo: rama → commit → push → Pull Request → revisión → merge.

### Fase 1: Datos GIS (Aldo)
- Elegir una zona de estudio pequeña (una ubicación o una ruta, como pide el reto).
- Investigar qué productos de datos de misiones NASA existen para esa zona y anotarlos en `docs/FUENTES_DE_DATOS.md` con enlace oficial, licencia/atribución y resolución.
- Procesar al menos dos capas (por ejemplo elevación y una imagen) a un formato acordado con el equipo.
- Entregar a Jesús y Luis un archivo `docs/CONTRATO_DE_DATOS.md` con formato, sistema de coordenadas y nombres de capas.

### Fase 2: Backend base (Jesús)
- Estructura FastAPI, endpoints para listar y servir capas, lectura de GeoTIFF.
- Calcular pendiente a partir de la elevación.

### Fase 3: Frontend base (Luis)
- Mapa Leaflet, selector de capas, marcadores de origen y destino.
- Consumir los endpoints reales del backend.

### Fase 4: Ruta y riesgo
- A* sobre una cuadrícula con costo por pendiente y zonas de riesgo.
- Zonas de riesgo **ficticias o derivadas de los datos de práctica**, claramente marcadas como tales.
- Mostrar la ruta y su resumen (distancia, pendiente máxima) en el mapa.

### Fase 5: Pruebas y documentación
- Pruebas del backend y del algoritmo con casos pequeños.
- Revisar que cualquier persona nueva pueda levantar el proyecto solo con el README.

### Fase 6: Cierre
- Retrospectiva: qué funcionó, qué tardó más, qué haríamos distinto.
- Lista de habilidades y patrones aprendidos (no de código final) para el reto real.
