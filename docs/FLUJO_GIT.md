# Flujo de trabajo con Git

## Ramas
- `main`: siempre estable. Nadie hace push directo.
- Ramas de trabajo con prefijo por tipo y rol:
  - `feature/gis-<tema>` (Aldo)
  - `feature/backend-<tema>` (Jesús)
  - `feature/frontend-<tema>` (Luis)
  - `fix/<tema>` y `docs/<tema>`

## Ciclo de trabajo
```bash
git checkout main
git pull
git checkout -b feature/backend-lectura-geotiff
# ... trabajar ...
git add .
git commit -m "feat(backend): lee GeoTIFF de elevación"
git push -u origin feature/backend-lectura-geotiff
# Abrir Pull Request en GitHub, pedir revisión a otra persona
```

## Mensajes de commit
Formato: `tipo(ámbito): descripción corta`
Tipos: `feat`, `fix`, `docs`, `test`, `refactor`, `chore`.

## Reglas
1. Todo cambio entra por Pull Request.
2. Otra persona del equipo revisa antes de hacer merge.
3. Antes de abrir el PR: `git pull origin main` en tu rama y resolver conflictos.
4. No subir datos pesados ni credenciales (ver `.gitignore`).
