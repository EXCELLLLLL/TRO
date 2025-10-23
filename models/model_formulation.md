# Formulasi Model Matematika
## Transportation Problem - FreshDrink Distribution Co.

---

## 1. DEFINISI MASALAH

FreshDrink Distribution Co. menghadapi masalah optimasi distribusi klasik (Transportation Problem) di mana perusahaan harus menentukan jumlah unit produk yang harus dikirim dari setiap gudang ke setiap toko untuk meminimalkan total biaya transportasi sambil memenuhi semua permintaan dan tidak melebihi kapasitas gudang.

---

## 2. VARIABEL KEPUTUSAN

Didefinisikan variabel keputusan xij sebagai:

**xij** = Jumlah unit produk yang dikirim dari Gudang i ke Toko j

Di mana:
- i ∈ {1, 2, 3} adalah indeks gudang
- j ∈ {1, 2, 3, 4} adalah indeks toko

Sehingga terdapat 3 × 4 = **12 variabel keputusan**:

| Variabel | Deskripsi |
|----------|-----------|
| x11 | Unit dari Gudang 1 (Bekasi) ke Toko 1 (Jakarta Pusat) |
| x12 | Unit dari Gudang 1 (Bekasi) ke Toko 2 (Jakarta Utara) |
| x13 | Unit dari Gudang 1 (Bekasi) ke Toko 3 (Jakarta Selatan) |
| x14 | Unit dari Gudang 1 (Bekasi) ke Toko 4 (Jakarta Timur) |
| x21 | Unit dari Gudang 2 (Tangerang) ke Toko 1 (Jakarta Pusat) |
| x22 | Unit dari Gudang 2 (Tangerang) ke Toko 2 (Jakarta Utara) |
| x23 | Unit dari Gudang 2 (Tangerang) ke Toko 3 (Jakarta Selatan) |
| x24 | Unit dari Gudang 2 (Tangerang) ke Toko 4 (Jakarta Timur) |
| x31 | Unit dari Gudang 3 (Depok) ke Toko 1 (Jakarta Pusat) |
| x32 | Unit dari Gudang 3 (Depok) ke Toko 2 (Jakarta Utara) |
| x33 | Unit dari Gudang 3 (Depok) ke Toko 3 (Jakarta Selatan) |
| x34 | Unit dari Gudang 3 (Depok) ke Toko 4 (Jakarta Timur) |

---

## 3. FUNGSI TUJUAN

**Tujuan**: Meminimalkan total biaya transportasi

### Formulasi Matematika:

```
Minimize Z = 8x11 + 6x12 + 10x13 + 9x14 +
             9x21 + 12x22 + 13x23 + 7x24 +
             14x31 + 9x32 + 16x33 + 5x34
```

### Dalam Bentuk Umum:

```
         3   4
Minimize Z = Σ   Σ  cij × xij
        i=1 j=1
```

### Matriks Biaya (cij):

```
        T1   T2   T3   T4
G1  [   8    6   10    9  ]
G2  [   9   12   13    7  ]
G3  [  14    9   16    5  ]
```

### Interpretasi:
Fungsi tujuan ini menghitung total biaya transportasi dengan mengalikan jumlah unit yang dikirim (xij) dengan biaya transportasi per unit (cij) untuk setiap rute, kemudian menjumlahkan semua biaya tersebut.

---

## 4. KENDALA (CONSTRAINTS)

### 4.1 Kendala Kapasitas Gudang (Supply Constraints)

Total pengiriman dari setiap gudang tidak boleh melebihi kapasitasnya.

**Kendala Gudang 1 (Bekasi - Kapasitas 150 unit):**
```
x11 + x12 + x13 + x14 ≤ 150
```

**Kendala Gudang 2 (Tangerang - Kapasitas 200 unit):**
```
x21 + x22 + x23 + x24 ≤ 200
```

**Kendala Gudang 3 (Depok - Kapasitas 180 unit):**
```
x31 + x32 + x33 + x34 ≤ 180
```

**Bentuk Umum:**
```
  4
  Σ  xij ≤ Si    untuk i = 1, 2, 3
j=1
```
Di mana Si adalah kapasitas gudang i.

---

### 4.2 Kendala Permintaan Toko (Demand Constraints)

Total pengiriman ke setiap toko harus memenuhi permintaannya secara tepat.

**Kendala Toko 1 (Jakarta Pusat - Permintaan 120 unit):**
```
x11 + x21 + x31 = 120
```

**Kendala Toko 2 (Jakarta Utara - Permintaan 140 unit):**
```
x12 + x22 + x32 = 140
```

**Kendala Toko 3 (Jakarta Selatan - Permintaan 110 unit):**
```
x13 + x23 + x33 = 110
```

**Kendala Toko 4 (Jakarta Timur - Permintaan 130 unit):**
```
x14 + x24 + x34 = 130
```

**Bentuk Umum:**
```
  3
  Σ  xij = Dj    untuk j = 1, 2, 3, 4
i=1
```
Di mana Dj adalah permintaan toko j.

---

### 4.3 Kendala Non-Negatif

Jumlah unit yang dikirim tidak boleh negatif.

```
xij ≥ 0    untuk semua i ∈ {1, 2, 3} dan j ∈ {1, 2, 3, 4}
```

---

## 5. MODEL LENGKAP

### Formulasi Standar Linear Programming:

```
Minimize:
    Z = 8x11 + 6x12 + 10x13 + 9x14 + 9x21 + 12x22 + 13x23 + 7x24 + 14x31 + 9x32 + 16x33 + 5x34

Subject to:
    Supply Constraints:
        x11 + x12 + x13 + x14 ≤ 150                    (Gudang 1)
        x21 + x22 + x23 + x24 ≤ 200                    (Gudang 2)
        x31 + x32 + x33 + x34 ≤ 180                    (Gudang 3)
    
    Demand Constraints:
        x11 + x21 + x31 = 120                           (Toko 1)
        x12 + x22 + x32 = 140                           (Toko 2)
        x13 + x23 + x33 = 110                           (Toko 3)
        x14 + x24 + x34 = 130                           (Toko 4)
    
    Non-Negativity:
        xij ≥ 0  untuk semua i, j
```

---

## 6. VERIFIKASI KELAYAKAN (FEASIBILITY CHECK)

### Cek Total Supply vs Total Demand:

**Total Supply:**
```
S_total = 150 + 200 + 180 = 530 unit
```

**Total Demand:**
```
D_total = 120 + 140 + 110 + 130 = 500 unit
```

**Kesimpulan:**
```
S_total (530) > D_total (500)
```

**Masalah FEASIBLE** - Total supply melebihi total demand sebesar 30 unit, sehingga semua permintaan dapat dipenuhi. Ini adalah **Unbalanced Transportation Problem** dengan excess supply.

---

## 7. KARAKTERISTIK MODEL

| Karakteristik | Nilai | Keterangan |
|---------------|-------|------------|
| Tipe Masalah | Transportation Problem | Linear Programming khusus |
| Jumlah Sumber (m) | 3 | Gudang |
| Jumlah Tujuan (n) | 4 | Toko |
| Jumlah Variabel | 12 | m × n |
| Jumlah Kendala | 7 | m + n |
| Balanced/Unbalanced | Unbalanced | Supply > Demand |
| Excess Supply | 30 unit | 530 - 500 |
| Tujuan | Minimasi | Biaya transportasi |

---

## 8. SOLUSI METODE

Model ini dapat diselesaikan menggunakan:

1. **Metode Manual:**
   - Northwest Corner Method (Initial Basic Feasible Solution)
   - Least Cost Method (Initial BFS)
   - Vogel's Approximation Method/VAM (Initial BFS)
   - MODI Method / Stepping Stone (Optimality Test)

2. **Software/Tools:**
   - Excel Solver (Simplex LP)
   - Python (PuLP, SciPy Optimize)
   - LINGO
   - MATLAB

---

## 9. EXPECTED OUTPUT

Solusi optimal akan memberikan:

1. **Nilai xij optimal** - Jumlah unit yang harus dikirim dari setiap gudang ke setiap toko
2. **Nilai Z optimal** - Total biaya transportasi minimum
3. **Shadow Price** - Nilai marginal dari kendala (sensitivitas)
4. **Slack Variables** - Kelebihan kapasitas gudang yang tidak digunakan
5. **Reduced Cost** - Biaya untuk memaksa variabel non-basic menjadi basic

---

## 10. ASUMSI MODEL

1. Biaya transportasi bersifat linear (proporsional dengan jumlah unit)
2. Tidak ada diskon volume atau biaya tetap
3. Semua gudang dapat mengirim ke semua toko
4. Tidak ada batasan waktu atau jadwal pengiriman
5. Tidak ada kendala kapasitas kendaraan
6. Produk bersifat homogen (identik dari semua gudang)
7. Biaya transportasi sudah mencakup semua biaya terkait

---

**Catatan**: Model ini merupakan formulasi dasar untuk Tugas UTS. Pada Tugas UAS, model dapat diperluas dengan menambahkan:
- Gudang atau toko tambahan
- Kendala kapasitas kendaraan
- Kendala time window
- Multiple product types
- Biaya tetap (fixed cost)
- Dan skenario lainnya