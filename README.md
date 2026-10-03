# Mars Explorer Lab 🔒

**Proyecto de práctica del equipo.** No es una solución final ni un proyecto oficial de NASA. Su objetivo es entrenar las habilidades técnicas y el flujo de trabajo del equipo.

## 1. Contexto del reto

Este laboratorio se inspira en el reto de NASA Space Apps 2026 **"Interplanetary Survival Guide: Martian Map"** (Intermedio; temas: Human Exploration, Mars, Planets & Moons, Software, Space Exploration).

Resumen del enunciado: los primeros astronautas en Marte querrán el mejor mapa posible, con detalles de rutas y destinos, actualizaciones de condiciones actuales y los datos necesarios para completar su misión de forma rápida y segura. **El reto consiste en crear una vista integrada y por capas de una ubicación o ruta en la superficie marciana, que reúna datos de varias misiones científicas de NASA y ayude a un explorador humano a planificar y realizar una caminata marciana (Marswalk), haciendo ciencia en el camino.**

Enlace oficial: https://www.spaceappschallenge.org/2026/challenges/interplanetary-survival-guide-martian-map//?tab=teams

> ⚠️ Este repositorio es **práctica independiente**. El proyecto del reto se desarrollará en un repositorio aparte, siguiendo las reglas oficiales del evento. Antes de reutilizar cualquier dato, hay que verificar sus condiciones de uso (ver `docs/FUENTES_DE_DATOS.md`).

## 2. Objetivo de la práctica

Construir un prototipo pequeño que muestre, para **una zona o ruta limitada de Marte**:

1. Un mapa con **varias capas** de datos que se puedan activar y desactivar.
2. Un **cálculo de ruta** entre un origen y un destino con costo por pendiente y zonas de riesgo.
3. Un **resumen** de la ruta (distancia, pendiente máxima).

Así practicamos la idea central del reto: integrar datos de distintas fuentes en una sola vista útil para planificar una caminata.

## 3. Equipo y roles

| Persona | Rol | Responsabilidad |
|---------|-----|-----------------|
| **Aldo** | GIS / Datos de Marte | Investigar, descargar y procesar datos; documentar fuentes y formatos |
| **Jesús** | Backend | API (FastAPI), lectura de datos, pendiente, algoritmo de ruta (A*) |
| **Luis** | Frontend | Mapa Leaflet, capas, interfaz de origen/destino y visualización de la ruta |

Flujo de entrega: **Aldo → Jesús → Luis**. Cada rol documenta lo que entrega al siguiente.

## 4. Estructura del repositorio

```
mars-explorer-lab/
├── frontend/            # Interfaz web (Luis)
├── backend/             # API FastAPI (Jesús)
│   ├── app/
│   │   └── main.py
│   ├── tests/
│   └── requirements.txt
├── algorithms/          # Ruta A* y costos (Jesús)
├── data/
│   ├── raw/             # Datos originales (no se suben a Git)
│   └── processed/       # Datos procesados (no se suben a Git)
├── docs/
│   ├── PLAN_DE_FASES.md
│   ├── ARQUITECTURA.md
│   ├── FUENTES_DE_DATOS.md
│   ├── CONTRATO_DE_DATOS.md
│   └── FLUJO_GIT.md
├── tests/
├── .github/
│   └── pull_request_template.md
├── .gitignore
└── README.md
```

## 5. Fases hasta el armado final

El proyecto tiene **7 fases (0 a 6)**. Detalle completo en [`docs/PLAN_DE_FASES.md`](docs/PLAN_DE_FASES.md).

| Fase | Nombre | Responsable | Entregable |
|------|--------|-------------|------------|
| 0 | Preparación | Los 3 | Repo clonado, entorno funcionando, primer PR |
| 1 | Datos GIS | Aldo | Zona elegida, 2+ capas procesadas, fuentes documentadas |
| 2 | Backend base | Jesús | API sirviendo capas, pendiente calculada |
| 3 | Frontend base | Luis | Mapa Leaflet con capas conmutables |
| 4 | Ruta y riesgo | Jesús + Aldo + Luis | Ruta A* dibujada en el mapa con resumen |
| 5 | Pruebas y documentación | Los 3 | Pruebas pasando, docs al día |
| 6 | Cierre | Los 3 | `docs/LECCIONES_APRENDIDAS.md` |

## 6. Guía paso a paso

### Paso 1. Crear el repositorio (Jesús, una sola vez)
1. En GitHub: **New repository** → nombre `mars-explorer-lab` → **Private**.
2. Subir este contenido (`git init`, `git add .`, `git commit`, `git remote add origin ...`, `git push -u origin main`).
3. En **Settings → Collaborators**, invitar a Aldo y a Luis.
4. (Recomendado) En **Settings → Branches**, proteger `main` exigiendo Pull Request.

### Paso 2. Clonar el repositorio (los 3)
```bash
git clone https://github.com/<usuario>/mars-explorer-lab.git
cd mars-explorer-lab
```

### Paso 3. Preparar el entorno

**Backend (Jesús, y quien quiera probarlo):**
```bash
cd backend
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Abrir http://127.0.0.1:8000/health (debe responder `{"status":"ok"}`) y http://127.0.0.1:8000/docs.

> `rasterio` puede requerir librerías del sistema según tu sistema operativo. Si falla la instalación, avisar al equipo y documentar la solución en `docs/`.

**Pruebas del backend:**
```bash
cd backend
pytest
```

**Frontend (Luis):** se define en la Fase 3. Si se usa Leaflet por CDN, basta un `index.html`; si se usa Node, documentar los comandos en `frontend/README.md`.

### Paso 4. Fase 0: primer Pull Request de práctica (los 3)
Cada persona hace un cambio mínimo (por ejemplo, agregar su nombre a un archivo `docs/EQUIPO.md`) usando el flujo completo de [`docs/FLUJO_GIT.md`](docs/FLUJO_GIT.md): rama → commit → push → PR → revisión cruzada → merge.

### Paso 5. Fase 1: Datos GIS (Aldo)
1. Elegir una **zona de estudio pequeña** (una ubicación o una ruta corta).
2. Investigar productos de datos de misiones NASA para esa zona. Registrar cada uno en [`docs/FUENTES_DE_DATOS.md`](docs/FUENTES_DE_DATOS.md): enlace oficial, licencia/atribución, resolución.
3. Descargar a `data/raw/` y procesar a `data/processed/` (recortar a la zona, unificar sistema de coordenadas).
4. Completar [`docs/CONTRATO_DE_DATOS.md`](docs/CONTRATO_DE_DATOS.md).
5. Compartir los archivos pesados por un medio acordado por el equipo (no por Git) y anotar dónde están.

**Listo cuando:** hay 2+ capas procesadas y el contrato de datos está completo.

### Paso 6. Fase 2: Backend base (Jesús)
1. Leer las capas procesadas según el contrato de datos.
2. Calcular la **pendiente** a partir de la elevación.
3. Crear endpoints para listar y servir capas.
4. Agregar pruebas en `backend/tests/`.

**Listo cuando:** Luis puede consumir las capas desde `/docs` o con una petición de prueba.

### Paso 7. Fase 3: Frontend base (Luis)
1. Crear el mapa Leaflet en `frontend/`.
2. Agregar control para activar/desactivar capas.
3. Permitir seleccionar origen y destino.
4. Conectar con el backend real.

**Listo cuando:** se ven las capas del backend y se pueden alternar.

### Paso 8. Fase 4: Ruta y riesgo (Jesús, con Aldo y Luis)
1. Jesús implementa A* en `algorithms/` sobre una cuadrícula con costo por pendiente.
2. Aldo define con Jesús las **zonas de riesgo de práctica** (derivadas de los datos o ficticias, siempre marcadas como tales).
3. Luis dibuja la ruta y muestra el resumen (distancia, pendiente máxima).

**Listo cuando:** elegir origen y destino devuelve y dibuja una ruta.

### Paso 9. Fase 5: Pruebas y documentación (los 3)
1. Pruebas para backend y algoritmo con casos pequeños.
2. Una persona que no escribió el código sigue este README desde cero para comprobar que se puede levantar el proyecto.
3. Corregir lo que falle y actualizar la documentación.

### Paso 10. Fase 6: Cierre (los 3)
Reunión de retrospectiva y creación de `docs/LECCIONES_APRENDIDAS.md`: qué funcionó, qué tardó más, qué haríamos distinto, qué habilidades ganamos.

## 7. Reglas del equipo

1. `main` siempre estable; todo entra por Pull Request con revisión de otra persona.
2. Ningún dato se usa sin registrarse en `docs/FUENTES_DE_DATOS.md`.
3. No subir datos pesados ni credenciales a Git.
4. Todo lo que sea ficticio (zonas de riesgo, condiciones) se etiqueta como **de práctica**.
5. Esta práctica **no se renombra ni se presenta como el proyecto del reto**.
6. Si algo de este README no coincide con las reglas oficiales del evento, mandan las reglas oficiales.

## 8. Referencias
- Reto: https://www.spaceappschallenge.org/2026/challenges/interplanetary-survival-guide-martian-map//?tab=teams
- Flujo Git: [`docs/FLUJO_GIT.md`](docs/FLUJO_GIT.md)
- Arquitectura: [`docs/ARQUITECTURA.md`](docs/ARQUITECTURA.md)
- Plan de fases: [`docs/PLAN_DE_FASES.md`](docs/PLAN_DE_FASES.md)
