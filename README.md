# Project Analisis dan Optimasi Sistem Distribusi
## Teknik Riset Operasi - UTS & UAS

###  Deskripsi Project
Project ini menganalisis dan mengoptimalkan sistem distribusi produk dari gudang ke toko retail menggunakan metode Transportation Problem dan Linear Programming. Studi kasus yang digunakan adalah perusahaan distribusi minuman "FreshDrink Distribution Co."

---

##  Studi Kasus: FreshDrink Distribution Co.

### Konteks Bisnis
FreshDrink Distribution Co. adalah perusahaan distributor minuman ringan yang melayani berbagai toko retail di Jabodetabek. Perusahaan memiliki beberapa gudang distribusi dan harus mengirimkan produk ke berbagai toko dengan biaya transportasi yang berbeda-beda.

### Permasalahan
- Perusahaan memiliki 3 gudang dengan kapasitas berbeda
- Harus melayani 4 toko retail dengan permintaan spesifik
- Biaya transportasi dari setiap gudang ke setiap toko berbeda
- **Tujuan**: Meminimalkan total biaya transportasi

---

##  Data Project

### Kapasitas Gudang (Supply)
| Gudang | Lokasi | Kapasitas (unit) |
|--------|--------|------------------|
| G1 | Bekasi | 150 |
| G2 | Tangerang | 200 |
| G3 | Depok | 180 |
| **Total** | | **530** |

### Permintaan Toko (Demand)
| Toko | Lokasi | Permintaan (unit) |
|------|--------|-------------------|
| T1 | Jakarta Pusat | 120 |
| T2 | Jakarta Utara | 140 |
| T3 | Jakarta Selatan | 110 |
| T4 | Jakarta Timur | 130 |
| **Total** | | **500** |

### Biaya Transportasi (Rp per unit)
| Dari/Ke | T1 | T2 | T3 | T4 |
|---------|----|----|----|----|
| **G1** | 8 | 6 | 10 | 9 |
| **G2** | 9 | 12 | 13 | 7 |
| **G3** | 14 | 9 | 16 | 5 |

---

##  Struktur Project

```
TRO-Project/
├── README.md                          # File ini
├── data/
│   ├── data_input.xlsx               # Data input (Excel)
│   └── data_input.csv                # Data input (CSV)
├── models/
│   ├── model_formulation.md          # Dokumentasi model matematika
│   └── manual_solution.md            # Solusi manual step-by-step
├── solutions/
│   ├── excel_solver/
│   │   ├── solution.xlsx             # Solusi menggunakan Excel Solver
│   │   └── excel_steps.md            # Panduan penggunaan Excel Solver
│   └── python/
│       ├── optimization.py           # Code Python (PuLP/SciPy)
│       ├── requirements.txt          # Dependencies Python
│       └── results.json              # Output hasil optimasi
├── analysis/
│   ├── sensitivity_analysis.md       # Analisis sensitivitas (UAS)
│   └── scenario_exploration.md       # Eksplorasi skenario (UAS)
├── reports/
│   ├── UTS_Report.pdf                # Laporan UTS (Point 1-3)
│   └── UAS_Report.pdf                # Laporan UAS (Point 4-5)
└── visualizations/
    ├── cost_matrix.png               # Visualisasi matriks biaya
    ├── solution_flow.png             # Diagram alur distribusi
    └── comparison_chart.png          # Perbandingan hasil solver
```

---

##  Model Matematika

### Fungsi Tujuan
Minimasi total biaya transportasi:

```
Minimize Z = Σ Σ (cij × xij)
           i=1 j=1
```

Di mana:
- `Z` = Total biaya transportasi
- `cij` = Biaya transportasi dari gudang i ke toko j
- `xij` = Jumlah unit yang dikirim dari gudang i ke toko j
- `i` = 1, 2, 3 (gudang)
- `j` = 1, 2, 3, 4 (toko)

### Kendala (Constraints)

**1. Kendala Kapasitas Gudang (Supply Constraints):**
```
Σ xij ≤ Si  untuk setiap i
j=1
```
- x1j ≤ 150 (Gudang 1)
- x2j ≤ 200 (Gudang 2)
- x3j ≤ 180 (Gudang 3)

**2. Kendala Permintaan Toko (Demand Constraints):**
```
Σ xij = Dj  untuk setiap j
i=1
```
- xi1 = 120 (Toko 1)
- xi2 = 140 (Toko 2)
- xi3 = 110 (Toko 3)
- xi4 = 130 (Toko 4)

**3. Kendala Non-Negatif:**
```
xij ≥ 0  untuk semua i, j
```

---

##  Cara Menjalankan

### Metode 1: Excel Solver
1. Buka file `solutions/excel_solver/solution.xlsx`
2. Pastikan Excel Solver Add-in sudah aktif
3. Ikuti panduan di `excel_steps.md`
4. Klik "Solve" untuk mendapatkan solusi optimal

### Metode 2: Python
```bash
# Install dependencies
pip install -r solutions/python/requirements.txt

# Jalankan optimasi
python solutions/python/optimization.py
```

### Metode 3: Manual
Lihat dokumentasi lengkap di `models/manual_solution.md` untuk solusi step-by-step menggunakan metode:
- Metode Northwest Corner
- Metode Least Cost
- Metode Vogel's Approximation (VAM)
- MODI Method untuk optimalisasi

---

##  Deliverables

### Tugas UTS (Point 1-3)
- ✅ Studi kasus dan data
- ✅ Model matematika lengkap
- ✅ Solusi manual step-by-step
- ✅ Solusi menggunakan Excel Solver
- ✅ Solusi menggunakan Python
- ✅ Perbandingan hasil kedua metode
- ✅ Interpretasi hasil

### Tugas UAS (Point 4-5)
- ⏳ Analisis sensitivitas
- ⏳ Eksplorasi skenario (variasi data)
- ⏳ Visualisasi hasil
- ⏳ Rekomendasi konsultan
- ⏳ Laporan lengkap

---

##  Tim Project
- **Nama Mahasiswa**: Muhammad Arjun Robben
- **NIM**: 231011400740
- **Kelas**: 05TPLM009
- **Mata Kuliah**: Teknik Riset Operasional

---

##  Referensi
1. Hillier, F. S., & Lieberman, G. J. (2020). Introduction to Operations Research
2. Taha, H. A. (2017). Operations Research: An Introduction
3. Winston, W. L. (2022). Operations Research: Applications and Algorithms

---

##  Kontak
Untuk pertanyaan atau diskusi project, silakan hubungi:
- Email: muhammadarjunrobben@gmail.com
- GitHub: EXCELLLLLL

---

**Last Updated**: Oktober 2025