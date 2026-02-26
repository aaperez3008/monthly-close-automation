#!/usr/bin/env bash
set -euo pipefail

if [[ $# -eq 1 ]]; then
  YEAR="2026"
  MONTH="$1"
elif [[ $# -eq 2 ]]; then
  YEAR="$1"
  MONTH="$2"
else
  echo "Uso: ./close-month.sh <month>"
  echo "Ejemplo: ./close-month.sh january"
  echo "Opcional: ./close-month.sh <year> <month>"
  exit 1
fi

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MONTH_DIR="$BASE_DIR/data/$YEAR/$MONTH"

COMMISSION_DIR="$MONTH_DIR/input/commission"
POINTS_LOAD_DIR="$MONTH_DIR/input/points_load"
POINTS_VOID_DIR="$MONTH_DIR/input/points_void"
OUTPUT_DIR="$MONTH_DIR/output"
REPORTS_DIR="$MONTH_DIR/reports"

if [[ ! -d "$COMMISSION_DIR" || ! -d "$POINTS_LOAD_DIR" || ! -d "$POINTS_VOID_DIR" ]]; then
  echo "No existe la estructura para $YEAR/$MONTH."
  echo "Esperado: data/$YEAR/$MONTH/input/{commission,points_load,points_void}"
  exit 1
fi

shopt -s nullglob
commission_files=("$COMMISSION_DIR"/*.csv)
points_load_files=("$POINTS_LOAD_DIR"/*.csv)
points_void_files=("$POINTS_VOID_DIR"/*.csv)
shopt -u nullglob

if [[ ${#commission_files[@]} -ne 1 ]]; then
  echo "Debe existir exactamente 1 CSV en $COMMISSION_DIR"
  exit 1
fi
if [[ ${#points_load_files[@]} -ne 1 ]]; then
  echo "Debe existir exactamente 1 CSV en $POINTS_LOAD_DIR"
  exit 1
fi
if [[ ${#points_void_files[@]} -ne 1 ]]; then
  echo "Debe existir exactamente 1 CSV en $POINTS_VOID_DIR"
  exit 1
fi

mkdir -p "$OUTPUT_DIR" "$REPORTS_DIR"

echo "Ejecutando cierre para $YEAR/$MONTH..."
python3 -m monthly_close_automation.cli run \
  --commission-file "${commission_files[0]}" \
  --points-load-file "${points_load_files[0]}" \
  --points-void-file "${points_void_files[0]}" \
  --output-dir "$OUTPUT_DIR" \
  --reports-dir "$REPORTS_DIR" \
  --month "$MONTH" \
  --year "$YEAR"

echo ""
echo "Listo."
echo "Outputs: $OUTPUT_DIR"
echo "Reportes: $REPORTS_DIR"

