# Monthly Close Automation (Shopify JAFRA US)

Automatiza el cierre mensual en un flujo simple:
1) pegas archivos en la carpeta del mes,
2) ejecutas un solo comando,
3) obtienes CSVs listos + reporte.

## Estructura simple

Todo vive por mes en `data/2026/<month>/`:

- `input/commission/` -> 1 archivo CSV de comisiones.
- `input/points_load/` -> 1 archivo CSV de carga de puntos.
- `input/points_void/` -> 1 archivo CSV de void de puntos.
- `output/` -> CSVs generados por el proceso.
- `reports/` -> reporte de validación (`.md` y `.json`).

Meses creados:
- `january` a `december`.

## Comando único

Desde la raíz del proyecto:

```bash
./close-month.sh january
```

## Reglas de uso

- Debe haber **exactamente 1 CSV** en cada carpeta de input:
  - `commission`
  - `points_load`
  - `points_void`
- Si falta alguno o hay más de uno, el script falla con mensaje claro.
- Año default: `2026` (opcional: `./close-month.sh 2026 january`).

## Salidas que genera

En `data/2026/<month>/output/`:
- `matrixify_commissions.csv`
- `points_load_ready.csv`
- `points_void_ready.csv`

En `data/2026/<month>/reports/`:
- `validation_report.md`
- `validation_report.json`

## Notas importantes

- No hace escrituras automáticas a producción.
- `EMAIL` vs `EMAILADDRESS` se reporta como warning (no bloquea).
- Revisa `validation_report.md` antes de cargar en Matrixify/DB.

