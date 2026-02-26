# Dry Run Results (2026 January)

## Comando ejecutado

```bash
./close-month.sh january
```

## Inputs usados

- `example/Commission/Commission/FileFromBusiness/COPS Upload to Shopify Dic - FINAL.csv`
- `example/Points/Points/LoadPointinDB/JAN_Special_Promotion_05_2026_Point_Load.csv`
- `example/Points/Points/LoadVoidPointInDB/Reverse_Points_IN_DB_JAN_05.csv`

## Outputs generados

- `data/2026/january/output/matrixify_commissions.csv`
- `data/2026/january/output/points_load_ready.csv`
- `data/2026/january/output/points_void_ready.csv`
- `data/2026/january/reports/validation_report.md`
- `data/2026/january/reports/validation_report.json`

## Resultado

- Errors: 0
- Warnings: 0
- Estado: listo para uso operativo mensual.

## Nota sobre tags de comisiones

- El sufijo de tag en `matrixify_commissions.csv` ahora es dinámico y depende de `<month>` y `<year>` del comando.
- Formato: `COMM_{commission_percentage}_{MON_YY}` (ejemplo para febrero 2026: `COMM_40_FEB_26`).

