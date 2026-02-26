# Contratos de Datos (Formato Real)

## 1) Commission input

Carpeta: `data/2026/<month>/input/commission/`

CSV esperado (columnas):
- `EMAIL`
- `Metafield: custom.commission_percentage[number_integer]`
- `CONSID` (opcional)

Output:
- `data/2026/<month>/output/matrixify_commissions.csv`

Reglas:
- Se conserva una sola columna identificadora: `EMAIL`.
- `COMMAND` se fuerza a `UPDATE` (uppercase).
- El metafield se exporta exactamente como `Metafield: custom.commission_percentage[number_integer]`.
- `CONSID` se conserva solo si existe en el input.
- Se agregan columnas de tags para Matrixify:
  - `Tags Command` = `MERGE`
  - `Tags` = `COMM_{commission_percentage}_{MON_YY}` (ejemplo: `COMM_40_FEB_26`)
- Se conservan todas las filas del input.

## 2) Points load input

Carpeta: `data/2026/<month>/input/points_load/`

CSV esperado (columnas):
- `consultant_id`
- `original`
- `current`
- `earns_at`
- `expires_at`
- `description`

Output:
- `data/2026/<month>/output/points_load_ready.csv`

Reglas:
- `consultant_id` se normaliza quitando ceros a la izquierda.
- `original` y `current` deben ser numéricos.
- Si `original != current`, se reporta warning.

## 3) Points void input

Carpeta: `data/2026/<month>/input/points_void/`

CSV esperado (columnas):
- `consultant_id`
- `original`
- `current`
- `earns_at`
- `expires_at`
- `description`

Output:
- `data/2026/<month>/output/points_void_ready.csv`

Reglas:
- `consultant_id` se normaliza.
- `original` y `current` deben ser numéricos.
- Valores positivos en void se reportan como warning.

## 4) Reportes

El script siempre genera:
- `data/2026/<month>/reports/validation_report.md`
- `data/2026/<month>/reports/validation_report.json`

