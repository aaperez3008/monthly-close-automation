# Runbook Simple de Cierre de Mes

## Qué haces cada mes

1. Pegar archivos de negocio en la carpeta del mes.
2. Ejecutar un solo comando.
3. Revisar reporte.
4. Si no hay errores, cargar outputs en Matrixify/DB.

## Dónde pegar archivos

Ruta base:

`data/2026/<month>/input/`

Carpetas:
- `commission/` -> 1 CSV de comisiones.
- `points_load/` -> 1 CSV de puntos (carga positiva).
- `points_void/` -> 1 CSV de puntos (void/negativos).

## Comando único

```bash
./close-month.sh january
```

Reemplaza `january` por el mes que corresponda.
Opcional con año explícito:

```bash
./close-month.sh 2026 february
```

## Qué genera

En `data/2026/<month>/output/`:
- `matrixify_commissions.csv`
- `points_load_ready.csv`
- `points_void_ready.csv`

Para comisiones (`matrixify_commissions.csv`) se genera formato Matrixify Customer update:
- `EMAIL` (identificador)
- `COMMAND` = `UPDATE`
- `Metafield: custom.commission_percentage[number_integer]`
- `CONSID` (si existe en el input)
- `Tags Command` = `MERGE`
- `Tags` = `COMM_{commission_percentage}_{MON_YY}` (según mes/año del comando)

En `data/2026/<month>/reports/`:
- `validation_report.md`
- `validation_report.json`

## Regla para decidir

- Si `validation_report.md` tiene errores: no cargar.
- Si tiene solo warnings: revisar y decidir.
- Si está limpio: proceder con carga.

## Operación de cierre fuera del script

- Limpieza de tags: se mantiene en Arigato.
- Página de mantenimiento: se mantiene en Launchpad.
- Validación funcional final: checkout, enrollment, impuestos, comisiones.

