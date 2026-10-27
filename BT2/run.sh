#!/usr/bin/env bash
set -e

echo "======================================================================="
echo "    HE THONG QUAN LY YEU CAU BAO HANH - MEKONG MOBILE (BT2)"
echo "    Sinh vien: Vu The Long - MSSV: 2374802010286"
echo "======================================================================="
echo ""

echo "[BUOC 1/3] Kiem tra va cai dat thu vien tu requirements.txt..."
pip install -r requirements.txt

echo ""
echo "[BUOC 2/3] Chay kiem thu tu dong (29/29 Unit Tests)..."
pytest -v

echo ""
echo "[BUOC 3/3] Khoi chay Web Server..."
echo "(He thong tu dong tao Database va nap du lieu mau, khong can cai MySQL!)"
echo ""
python src/main.py
