# Mars Explorer Lab 🔒

Laboratorio de práctica para aprender y desarrollar una aplicación web de exploración de Marte, inspirada en el desafío de NASA Space Apps Challenge 2026: **Interplanetary Survival Guide: Martian Map**.

> **Importante:** Este repositorio es un laboratorio de aprendizaje independiente. No representa la solución oficial del desafío de NASA Space Apps Challenge.

## 🎯 Objetivo

Crear un prototipo web que permita explorar una zona de Marte mediante un mapa interactivo, visualizar capas de información y calcular rutas entre dos puntos considerando factores como la distancia, la pendiente y las zonas de riesgo.

El proyecto se desarrollará progresivamente, comenzando con datos de prueba y avanzando hacia datos geoespaciales reales cuando estemos preparados para procesarlos.

## 👥 Equipo de trabajo

El laboratorio será desarrollado por dos integrantes:

| Integrante | Responsabilidad principal | Tareas |
|---|---|---|
| **Aldo** | Frontend y apoyo GIS | Desarrollar el mapa interactivo con Leaflet, crear la interfaz, visualizar las capas y representar las rutas. Apoyar la investigación y validación de datos geográficos. |
| **Jesús** | Backend y algoritmos | Desarrollar la API con FastAPI, procesar los datos, implementar el algoritmo A* y calcular los costos de las rutas. |

**Forma de trabajo:** Aldo y Jesús colaborarán en la integración, las pruebas, la documentación y la revisión del código. Cada integrante revisará los cambios del otro mediante Pull Requests cuando corresponda.

## 🧰 Tecnologías previstas

- **Frontend:** HTML, CSS y JavaScript.
- **Mapa interactivo:** Leaflet.
- **Backend:** Python y FastAPI.
- **Algoritmos:** A* para encontrar rutas.
- **Datos geoespaciales:** formatos y herramientas adecuados según los datos seleccionados.
- **Control de versiones:** Git y GitHub.
- **Pruebas:** herramientas de Python y pruebas manuales de la interfaz.

Las tecnologías podrán ajustarse conforme avance el aprendizaje y se conozcan las necesidades reales del proyecto.

## 📁 Estructura del repositorio

```text
mars-explorer-lab/
├── frontend/                 # Interfaz web y mapa (Aldo)
├── backend/                  # API y procesamiento (Jesús)
│   ├── app/
│   │   └── main.py
│   ├── tests/
│   └── requirements.txt
├── algorithms/               # Algoritmo A* y costos de ruta (Jesús)
├── data/
│   ├── raw/                  # Datos originales, no modificados
│   └── processed/            # Datos preparados para la aplicación
├── docs/
│   ├── PLAN_DE_FASES.md
│   ├── ARQUITECTURA.md
│   ├── FUENTES_DE_DATOS.md
│   ├── CONTRATO_DE_DATOS.md
│   ├── FLUJO_GIT.md
│   └── LECCIONES_APRENDIDAS.md
├── tests/                    # Pruebas generales del proyecto
├── .github/
│   └── pull_request_template.md
├── .gitignore
└── README.md
```

Esta estructura es una propuesta inicial. Los archivos y directorios se crearán a medida que sean necesarios.

## 🗺️ Funcionalidades previstas

1. Mostrar una zona de Marte en un mapa interactivo.
2. Permitir activar y desactivar capas de información.
3. Seleccionar un punto de origen y un destino.
4. Calcular una ruta utilizando el algoritmo A*.
5. Considerar costos asociados a distancia, pendiente y zonas de riesgo.
6. Dibujar la ruta calculada sobre el mapa.
7. Mostrar un resumen de la ruta, incluyendo distancia y pendiente máxima cuando los datos lo permitan.

Los riesgos ficticios empleados durante las pruebas estarán identificados claramente como datos simulados y no como riesgos reales de Marte.

## 🛠️ Plan de trabajo

| Fase | Nombre | Responsable | Entregable |
|---|---|---|---|
| 0 | Preparación | Aldo y Jesús | Repositorio organizado, entorno preparado y primer Pull Request. |
| 1 | Datos y mapa inicial | Aldo y Jesús | Zona de prueba seleccionada, datos de prueba disponibles y fuentes documentadas. |
| 2 | Backend básico | Jesús | API inicial que responda correctamente y permita consultar los datos de prueba. |
| 3 | Frontend básico | Aldo | Mapa Leaflet con interfaz y controles iniciales. |
| 4 | Rutas y riesgos | Aldo y Jesús | Algoritmo A*, cálculo de costos y visualización de la ruta. |
| 5 | Pruebas e integración | Aldo y Jesús | Frontend conectado al backend, pruebas y documentación actualizada. |
| 6 | Cierre del laboratorio | Aldo y Jesús | Proyecto documentado y archivo de lecciones aprendidas. |

Las fases podrán modificarse si aparecen dificultades técnicas o si necesitamos aprender alguna tecnología antes de continuar.

## 🚀 Cómo comenzar

### 1. Clonar el repositorio

Cada integrante debe clonar el repositorio en su propio equipo:

```bash
git clone https://github.com/jesusjacintofabian/mars-explorer-lab.git
cd mars-explorer-lab
```

### 2. Crear una rama de trabajo

Aldo puede trabajar inicialmente en:

```bash
git switch -c feature/frontend
```

Jesús puede trabajar inicialmente en:

```bash
git switch -c feature/backend
```

Las ramas se utilizarán para desarrollar funcionalidades sin modificar directamente la rama principal.

### 3. Preparar el backend

Jesús trabajará en el backend con Python y FastAPI.

Desde la raíz del repositorio, cuando exista el directorio `backend/`:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install fastapi uvicorn
```

El entorno virtual permite instalar las dependencias del backend sin mezclarlas con otros proyectos de Python.

Las dependencias utilizadas se registrarán posteriormente en `requirements.txt`.

### 4. Preparar el frontend

Aldo trabajará inicialmente con HTML, CSS, JavaScript y Leaflet.

El frontend comenzará con una página web sencilla y un mapa de prueba. Más adelante se conectará con la API desarrollada por Jesús.

No es necesario instalar todas las herramientas desde el primer día. Se incorporarán conforme las funcionalidades las requieran.

## 🌐 Datos geoespaciales

Antes de utilizar datos reales, debemos:

1. Seleccionar una zona de estudio pequeña.
2. Investigar las fuentes disponibles de datos de Marte.
3. Registrar la fuente, el formato, la fecha de consulta y la licencia o condiciones de uso aplicables.
4. Comprobar que los datos pueden visualizarse o procesarse con nuestras herramientas.
5. Documentar cómo se prepararon para utilizarlos en el proyecto.

Durante las primeras pruebas podremos usar datos sintéticos, como una cuadrícula con costos ficticios, para aprender a implementar el mapa y el algoritmo de rutas.

Los archivos grandes no deben incorporarse al repositorio sin evaluar antes su tamaño y necesidad. Cuando sea posible, se documentará cómo obtenerlos.

## 🔌 Integración entre frontend y backend

El frontend enviará al backend las coordenadas o celdas de origen y destino.

El backend procesará la solicitud y devolverá la información necesaria para dibujar la ruta.

El formato de intercambio se documentará en `docs/CONTRATO_DE_DATOS.md` antes de integrar funcionalidades que dependan de él.

La integración se hará progresivamente: primero una respuesta de prueba, después los datos del mapa y finalmente el cálculo de rutas.

## 🔀 Flujo de trabajo con Git y GitHub

1. Cada integrante trabaja en su propia rama.
2. Realiza cambios pequeños y comprensibles.
3. Comprueba que su código funciona.
4. Guarda los cambios mediante commits con mensajes descriptivos.
5. Abre un Pull Request hacia `main`.
6. El otro integrante revisa los cambios antes de integrarlos.
7. Ambos actualizan su rama local después de integrar los cambios.

La rama `main` debe mantenerse en un estado funcional siempre que sea posible.

## 📋 Reglas del laboratorio

- No subir contraseñas, tokens, claves privadas ni credenciales.
- No subir archivos de datos grandes sin evaluar antes su necesidad.
- Documentar las fuentes de los datos utilizados.
- Identificar claramente los datos sintéticos y los resultados simulados.
- No afirmar que una ruta es segura para una misión real: este prototipo es educativo.
- Mantener actualizada la documentación cuando cambie la arquitectura o el formato de los datos.
- Priorizar el aprendizaje y las pruebas antes de añadir funcionalidades complejas.
- Mantener este laboratorio separado de cualquier entrega oficial de NASA Space Apps Challenge y respetar las reglas aplicables al desafío oficial.

## 📚 Documentación

Los documentos del directorio `docs/` describirán progresivamente:

- **PLAN_DE_FASES.md:** etapas y objetivos del trabajo.
- **ARQUITECTURA.md:** componentes y comunicación entre frontend y backend.
- **FUENTES_DE_DATOS.md:** procedencia y condiciones de uso de los datos.
- **CONTRATO_DE_DATOS.md:** formato de intercambio entre componentes.
- **FLUJO_GIT.md:** ramas, commits y Pull Requests.
- **LECCIONES_APRENDIDAS.md:** dificultades, soluciones y conocimientos adquiridos.

## 🎓 Propósito educativo

Mars Explorer Lab nos permitirá aprender mediante la práctica conceptos de desarrollo web, procesamiento de datos, algoritmos, cartografía digital, pruebas de software y colaboración con GitHub.

**La meta es construirlo paso a paso, comprendiendo cada componente antes de pasar al siguiente.**

---

**Equipo:** Aldo y Jesús  
**Repositorio:** [mars-explorer-lab](https://github.com/jesusjacintofabian/mars-explorer-lab)  
**Estado:** Laboratorio de práctica en desarrollo.
