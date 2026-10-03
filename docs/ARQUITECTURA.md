# Arquitectura (práctica)

```
 Aldo (GIS)            Jesús (Backend)             Luis (Frontend)
 ──────────            ───────────────             ───────────────
 Datos crudos  ──▶  data/processed/  ──▶  API FastAPI  ──▶  Mapa Leaflet
 (data/raw)          (GeoTIFF/GeoJSON)    + algoritmos       capas + ruta
```

## Flujo
1. Aldo descarga y procesa datos, y los deja en `data/processed/` con su documentación.
2. Jesús lee esos datos, calcula pendiente y ruta, y los expone por API.
3. Luis consume la API y los muestra en capas sobre el mapa.

## Contratos entre roles
- **Aldo → Jesús:** `docs/CONTRATO_DE_DATOS.md` (formato, CRS, nombres de capas, unidades).
- **Jesús → Luis:** documentación automática de FastAPI en `/docs` cuando el backend corre.

## Alineación con el reto
El reto pide una **vista integrada y por capas** de una ubicación o ruta en Marte, que combine datos de **varias misiones científicas de NASA** y ayude a planificar una caminata marciana (Marswalk). Esta práctica ejercita esa idea con una zona pequeña y pocas capas.
