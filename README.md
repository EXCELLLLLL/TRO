# Project Analisis dan Optimasi Sistem Distribusi
## Studi Kasus: Optimasi Distribusi Produk Farmasi PT. MediCare Indonesia

### 📋 Deskripsi Project
Project ini menganalisis dan mengoptimalkan sistem distribusi produk farmasi dari beberapa pusat distribusi (gudang) ke berbagai rumah sakit dan apotek di Indonesia. Tujuan utama adalah meminimalkan biaya transportasi sambil memenuhi permintaan semua lokasi tujuan.

### 🎯 Objektif
- Meminimalkan total biaya distribusi
- Memenuhi semua permintaan pelanggan
- Tidak melebihi kapasitas gudang
- Membandingkan solusi dari berbagai metode/software
- Melakukan analisis sensitivitas terhadap perubahan parameter

### 📊 Studi Kasus
**Konteks Bisnis:**
PT. MediCare Indonesia adalah distributor produk farmasi yang melayani rumah sakit dan apotek di wilayah Jabodetabek dan Jawa Barat. Perusahaan memiliki 4 pusat distribusi dan harus melayani 5 lokasi tujuan dengan biaya transportasi yang bervariasi berdasarkan jarak dan kondisi jalan.

**Data Kasus:**
- 4 Gudang (Warehouse): Jakarta, Tangerang, Bekasi, Bogor
- 5 Tujuan (Destination): RS Jakarta Pusat, RS Tangerang, RS Bekasi, Apotek Depok, RS Bogor
- Kapasitas gudang berbeda-beda
- Permintaan setiap tujuan berbeda-beda
- Biaya transportasi per unit berbeda untuk setiap rute

### 📁 Struktur Folder

```
TRO_Project/
│
├── README.md
├── requirements.txt
│
├── data/
│   ├── input_data.xlsx
│   ├── warehouse_capacity.csv
│   ├── destination_demand.csv
│   └── transportation_cost.csv
│
├── src/
│   ├── __init__.py
│   ├── model_formulation.py
│   ├── excel_solver.py
│   ├── python_solver.py
│   └── visualization.py
│
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_manual_solution.ipynb
│   ├── 03_excel_solver_solution.ipynb
│   ├── 04_python_optimization.ipynb
│   └── 05_sensitivity_analysis.ipynb
│
├── results/
│   ├── UTS/
│   │   ├── manual_solution.xlsx
│   │   ├── excel_solver_solution.xlsx
│   │   ├── python_solution.csv
│   │   └── comparison_table.xlsx
│   │
│   └── UAS/
│       ├── sensitivity_analysis.xlsx
│       ├── scenario_comparison.xlsx
│       └── visualizations/
│
├── docs/
│   ├── UTS_Report.pdf
│   ├── UAS_Report.pdf
│   ├── model_formulation.md
│   └── methodology.md
│
└── presentation/
    ├── UTS_Presentation.pptx
    └── UAS_Presentation.pptx
```

### 🔧 Teknologi yang Digunakan
- **Python 3.8+**
    - PuLP (Linear Programming)
    - SciPy (Optimization)
    - Pandas (Data manipulation)
    - Matplotlib & Seaborn (Visualisasi)
    - NumPy (Numerical computation)
- **Microsoft Excel** dengan Solver Add-in
- **Jupyter Notebook** untuk analisis interaktif

### 📦 Instalasi

```bash
# Clone repository
git clone https://github.com/username/TRO_Project.git
cd TRO_Project

# Install dependencies
pip install -r requirements.txt

# Untuk Excel Solver, aktifkan Add-in Solver di Excel
```

### 🚀 Cara Menjalankan

#### 1. Tugas UTS (Point 1-3)
```bash
# Jalankan analisis manual
python src/manual_solution.py

# Jalankan solver Python
python src/python_solver.py

# Untuk Excel Solver, buka file:
# data/input_data.xlsx dan jalankan Solver
```

#### 2. Tugas UAS (Point 4-5)
```bash
# Jalankan analisis sensitivitas
python src/sensitivity_analysis.py

# Generate laporan lengkap
python src/generate_report.py
```

### 📈 Hasil yang Diharapkan

**UTS:**
1. Model matematika yang terformulasi dengan jelas
2. Solusi optimal dari metode manual
3. Solusi dari Excel Solver
4. Solusi dari Python (PuLP/SciPy)
5. Tabel perbandingan hasil

**UAS:**
4. Analisis sensitivitas terhadap:
    - Perubahan kapasitas gudang
    - Perubahan biaya transportasi
    - Penambahan gudang/tujuan baru
    - Perubahan permintaan
5. Laporan lengkap dengan:
    - Executive summary
    - Visualisasi hasil
    - Rekomendasi strategis
    - Analisis cost-benefit

### 👥 Tim Project
- Nama Mahasiswa: Muhammad Arjun Robben
- NIM: 231011400740
- Kelas: 05TLPM009
- Mata Kuliah: Teknik Riset Operasional (TRO)

### 📝 Lisensi
Project ini dibuat untuk keperluan akademik.

### 📧 Kontak
Untuk pertanyaan lebih lanjut, hubungi: muhammadarjunrobben@gmail.com

---
**Last Updated:** Januari 2026