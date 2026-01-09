# Formulasi Model Matematika
## Transportation Problem - PT. MediCare Indonesia

### 1. DEFINISI MASALAH

PT. MediCare Indonesia perlu mendistribusikan produk farmasi dari 4 gudang ke 5 lokasi tujuan dengan biaya seminimal mungkin, sambil memenuhi semua permintaan dan tidak melebihi kapasitas gudang.

### 2. PARAMETER DAN VARIABEL

#### Parameter:
- **m** = 4 (jumlah gudang)
- **n** = 5 (jumlah tujuan)
- **s_i** = kapasitas gudang i (dalam unit)
- **d_j** = permintaan tujuan j (dalam unit)
- **c_{ij}** = biaya transportasi per unit dari gudang i ke tujuan j (dalam ribu Rupiah)

#### Variabel Keputusan:
- **x_{ij}** = jumlah unit yang dikirim dari gudang i ke tujuan j
- i ∈ {1, 2, 3, 4} (Jakarta, Tangerang, Bekasi, Bogor)
- j ∈ {1, 2, 3, 4, 5} (RS Jakarta Pusat, RS Tangerang, RS Bekasi, Apotek Depok, RS Bogor)

### 3. DATA KASUS

#### Kapasitas Gudang (s_i):
| Gudang | Lokasi | Kapasitas (unit) |
|--------|--------|------------------|
| 1 | Jakarta | 350 |
| 2 | Tangerang | 400 |
| 3 | Bekasi | 300 |
| 4 | Bogor | 250 |
| **Total** | | **1,300** |

#### Permintaan Tujuan (d_j):
| Tujuan | Lokasi | Permintaan (unit) |
|--------|--------|-------------------|
| 1 | RS Jakarta Pusat | 250 |
| 2 | RS Tangerang | 300 |
| 3 | RS Bekasi | 200 |
| 4 | Apotek Depok | 280 |
| 5 | RS Bogor | 220 |
| **Total** | | **1,250** |

**Catatan:** Total kapasitas (1,300) > Total permintaan (1,250), sehingga masalah ini balanced setelah ditambah dummy destination.

#### Biaya Transportasi (c_{ij}) dalam ribu Rupiah per unit:
|  | RS Jkt Pusat (1) | RS Tangerang (2) | RS Bekasi (3) | Apotek Depok (4) | RS Bogor (5) |
|---|---|---|---|---|---|
| **Jakarta (1)** | 5 | 15 | 12 | 8 | 18 |
| **Tangerang (2)** | 18 | 4 | 20 | 16 | 25 |
| **Bekasi (3)** | 14 | 22 | 6 | 10 | 20 |
| **Bogor (4)** | 16 | 24 | 18 | 7 | 5 |

### 4. FORMULASI MODEL

#### Fungsi Tujuan (Objective Function):
**Minimisasi Total Biaya Transportasi**

```
Minimize Z = Σ Σ c_{ij} × x_{ij}
            i j
```

**Secara eksplisit:**
```
Minimize Z = 5x₁₁ + 15x₁₂ + 12x₁₃ + 8x₁₄ + 18x₁₅
           + 18x₂₁ + 4x₂₂ + 20x₂₃ + 16x₂₄ + 25x₂₅
           + 14x₃₁ + 22x₃₂ + 6x₃₃ + 10x₃₄ + 20x₃₅
           + 16x₄₁ + 24x₄₂ + 18x₄₃ + 7x₄₄ + 5x₄₅
```

#### Kendala (Constraints):

**A. Kendala Kapasitas Gudang (Supply Constraints):**
```
x₁₁ + x₁₂ + x₁₃ + x₁₄ + x₁₅ ≤ 350  (Gudang Jakarta)
x₂₁ + x₂₂ + x₂₃ + x₂₄ + x₂₅ ≤ 400  (Gudang Tangerang)
x₃₁ + x₃₂ + x₃₃ + x₃₄ + x₃₅ ≤ 300  (Gudang Bekasi)
x₄₁ + x₄₂ + x₄₃ + x₄₄ + x₄₅ ≤ 250  (Gudang Bogor)
```

**B. Kendala Permintaan Tujuan (Demand Constraints):**
```
x₁₁ + x₂₁ + x₃₁ + x₄₁ = 250  (RS Jakarta Pusat)
x₁₂ + x₂₂ + x₃₂ + x₄₂ = 300  (RS Tangerang)
x₁₃ + x₂₃ + x₃₃ + x₄₃ = 200  (RS Bekasi)
x₁₄ + x₂₄ + x₃₄ + x₄₄ = 280  (Apotek Depok)
x₁₅ + x₂₅ + x₃₅ + x₄₅ = 220  (RS Bogor)
```

**C. Kendala Non-Negativitas:**
```
x_{ij} ≥ 0, untuk semua i dan j
```

### 5. BENTUK STANDAR LINEAR PROGRAMMING

**Model dalam bentuk matriks:**

```
Minimize: c^T x

Subject to:
Ax ≤ b  (kapasitas)
Bx = d  (permintaan)
x ≥ 0
```

Dimana:
- **c** = vektor biaya (20 elemen untuk 4×5 rute)
- **x** = vektor variabel keputusan (20 elemen)
- **A** = matriks koefisien kapasitas (4×20)
- **b** = vektor kapasitas gudang (4 elemen)
- **B** = matriks koefisien permintaan (5×20)
- **d** = vektor permintaan tujuan (5 elemen)

### 6. TIPE MODEL

**Klasifikasi:**
- **Linear Programming Problem (LPP)**
- **Transportation Problem** - kasus khusus dari network flow problem
- **Balanced Transportation Problem** (setelah penyesuaian)

### 7. ASUMSI MODEL

1. Biaya transportasi proporsional terhadap jumlah unit yang dikirim
2. Tidak ada diskon volume atau biaya tetap
3. Semua pengiriman dapat dipecah (divisible)
4. Kapasitas dan permintaan deterministik (pasti)
5. Tidak ada kendala waktu atau prioritas
6. Produk homogen dan dapat dikirim dari gudang mana saja ke tujuan mana saja

### 8. METODE PENYELESAIAN

Model ini dapat diselesaikan dengan:
1. **Metode Manual**: Vogel's Approximation Method (VAM), Northwest Corner, Least Cost
2. **Excel Solver**: Add-in Solver dengan Simplex LP
3. **Python**: Library PuLP, SciPy.optimize
4. **Software Komersial**: LINGO, GAMS, CPLEX

### 9. OUTPUT YANG DIHARAPKAN

1. Nilai optimal fungsi tujuan (Z*) = Total biaya minimum
2. Nilai optimal variabel keputusan (x*_{ij}) = Alokasi pengiriman optimal
3. Status kendala (binding/non-binding)
4. Slack/surplus untuk setiap kendala
5. Shadow price untuk analisis sensitivitas