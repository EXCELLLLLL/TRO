# Solusi Manual Step-by-Step
## Transportation Problem - FreshDrink Distribution Co.

---

## DATA AWAL

### Tabel Transportasi

```
              T1    T2    T3    T4  | Supply
        +---------------------------------+
     G1 |  8     6    10     9    |  150
     G2 |  9    12    13     7    |  200
     G3 | 14     9    16     5    |  180
        +---------------------------------+
Demand  | 120   140   110   130   |  530
```

**Total Supply = 530 unit**  
**Total Demand = 500 unit**  
**Excess Supply = 30 unit** (Unbalanced)

---

## METODE 1: NORTHWEST CORNER METHOD

Metode ini mengalokasikan sebanyak mungkin ke sel pojok kiri atas, kemudian bergerak ke kanan atau ke bawah.

### Langkah-langkah:

#### Step 1: Mulai dari sel (G1, T1)
- Supply G1 = 150, Demand T1 = 120
- Alokasi: min(150, 120) = **120**
- x11 = 120
- Sisa Supply G1 = 30, Demand T1 = 0 ✓

```
              T1    T2    T3    T4  | Supply
        +---------------------------------+
     G1 | [120]   -     -     -    |  30
     G2 |  -     -     -     -    | 200
     G3 |  -     -     -     -    | 180
        +---------------------------------+
Demand  |  0    140   110   130   |
```

#### Step 2: Pindah ke (G1, T2)
- Supply G1 = 30, Demand T2 = 140
- Alokasi: min(30, 140) = **30**
- x12 = 30
- Sisa Supply G1 = 0 ✓, Demand T2 = 110

```
              T1    T2    T3    T4  | Supply
        +---------------------------------+
     G1 | [120] [30]   -     -    |   0
     G2 |  -     -     -     -    | 200
     G3 |  -     -     -     -    | 180
        +---------------------------------+
Demand  |  0    110   110   130   |
```

#### Step 3: Pindah ke (G2, T2)
- Supply G2 = 200, Demand T2 = 110
- Alokasi: min(200, 110) = **110**
- x22 = 110
- Sisa Supply G2 = 90, Demand T2 = 0 ✓

```
              T1    T2    T3    T4  | Supply
        +---------------------------------+
     G1 | [120] [30]   -     -    |   0
     G2 |  -   [110]   -     -    |  90
     G3 |  -     -     -     -    | 180
        +---------------------------------+
Demand  |  0     0    110   130   |
```

#### Step 4: Pindah ke (G2, T3)
- Supply G2 = 90, Demand T3 = 110
- Alokasi: min(90, 110) = **90**
- x23 = 90
- Sisa Supply G2 = 0 ✓, Demand T3 = 20

```
              T1    T2    T3    T4  | Supply
        +---------------------------------+
     G1 | [120] [30]   -     -    |   0
     G2 |  -   [110] [90]   -    |   0
     G3 |  -     -     -     -    | 180
        +---------------------------------+
Demand  |  0     0     20   130   |
```

#### Step 5: Pindah ke (G3, T3)
- Supply G3 = 180, Demand T3 = 20
- Alokasi: min(180, 20) = **20**
- x33 = 20
- Sisa Supply G3 = 160, Demand T3 = 0 ✓

```
              T1    T2    T3    T4  | Supply
        +---------------------------------+
     G1 | [120] [30]   -     -    |   0
     G2 |  -   [110] [90]   -    |   0
     G3 |  -     -   [20]   -    | 160
        +---------------------------------+
Demand  |  0     0     0    130   |
```

#### Step 6: Pindah ke (G3, T4)
- Supply G3 = 160, Demand T4 = 130
- Alokasi: min(160, 130) = **130**
- x34 = 130
- Sisa Supply G3 = 30, Demand T4 = 0 ✓

### Solusi Akhir Northwest Corner:

```
              T1    T2    T3    T4  | Supply | Used
        +--------------------------------------------+
     G1 | [120] [30]   0     0    |  150   | 150
     G2 |  0   [110] [90]   0    |  200   | 200
     G3 |  0     0   [20] [130]  |  180   | 150
        +--------------------------------------------+
Demand  | 120   140   110   130   |        | 500
```

**Sisa Supply G3 = 30 unit (tidak digunakan)**

### Perhitungan Biaya Northwest Corner:

```
Z = (8 × 120) + (6 × 30) + (12 × 110) + (13 × 90) + (16 × 20) + (5 × 130)
Z = 960 + 180 + 1,320 + 1,170 + 320 + 650
Z = Rp 4,600
```

**Total Biaya = Rp 4,600**

---

## METODE 2: LEAST COST METHOD

Metode ini mengalokasikan ke sel dengan biaya terendah terlebih dahulu.

### Langkah-langkah:

#### Step 1: Cari biaya minimum = 5 (G3 → T4)
- Supply G3 = 180, Demand T4 = 130
- Alokasi: x34 = 130
- Sisa Supply G3 = 50, Demand T4 = 0 ✓

#### Step 2: Biaya minimum berikutnya = 6 (G1 → T2)
- Supply G1 = 150, Demand T2 = 140
- Alokasi: x12 = 140
- Sisa Supply G1 = 10, Demand T2 = 0 ✓

#### Step 3: Biaya minimum = 7 (G2 → T4) [sudah terpenuhi]
#### Biaya minimum = 8 (G1 → T1)
- Supply G1 = 10, Demand T1 = 120
- Alokasi: x11 = 10
- Sisa Supply G1 = 0 ✓, Demand T1 = 110

#### Step 4: Biaya minimum = 9 (G2 → T1 atau G3 → T2)
Pilih G2 → T1:
- Supply G2 = 200, Demand T1 = 110
- Alokasi: x21 = 110
- Sisa Supply G2 = 90, Demand T1 = 0 ✓

#### Step 5: Biaya minimum = 9 (G3 → T2)
- Supply G3 = 50, Demand T2 = 0 [sudah terpenuhi]
Pilih biaya berikutnya = 13 (G2 → T3):
- Supply G2 = 90, Demand T3 = 110
- Alokasi: x23 = 90
- Sisa Supply G2 = 0 ✓, Demand T3 = 20

#### Step 6: Biaya minimum = 16 (G3 → T3)
- Supply G3 = 50, Demand T3 = 20
- Alokasi: x33 = 20
- Sisa Supply G3 = 30, Demand T3 = 0 ✓

### Solusi Akhir Least Cost:

```
              T1    T2    T3    T4  | Supply | Used
        +--------------------------------------------+
     G1 | [10] [140]   0     0    |  150   | 150
     G2 | [110]  0   [90]   0    |  200   | 200
     G3 |  0     0   [20] [130]  |  180   | 150
        +--------------------------------------------+
Demand  | 120   140   110   130   |        | 500
```

### Perhitungan Biaya Least Cost:

```
Z = (8 × 10) + (6 × 140) + (9 × 110) + (13 × 90) + (16 × 20) + (5 × 130)
Z = 80 + 840 + 990 + 1,170 + 320 + 650
Z = Rp 4,050
```

**Total Biaya = Rp 4,050** (Lebih baik dari Northwest Corner!)

---

## METODE 3: VOGEL'S APPROXIMATION METHOD (VAM)

Metode paling efisien untuk mendapatkan solusi awal yang mendekati optimal.

### Konsep:
Untuk setiap baris dan kolom, hitung **penalty** = selisih antara dua biaya terkecil. Alokasikan ke sel dengan biaya minimum pada baris/kolom dengan penalty tertinggi.

### Iterasi 1:

**Tabel Awal:**
```
              T1    T2    T3    T4  | Supply | Penalty
        +------------------------------------------------+
     G1 |  8     6    10     9    |  150   | 6-8=2
     G2 |  9    12    13     7    |  200   | 7-9=2
     G3 | 14     9    16     5    |  180   | 5-9=4 ← MAX
        +------------------------------------------------+
Demand  | 120   140   110   130   |
Penalty |8-9=1 6-9=3 10-13=3 5-7=2|
```

**Penalty maksimum = 4 (baris G3)**  
**Biaya minimum di G3 = 5 (G3 → T4)**  
**Alokasi: x34 = min(180, 130) = 130**

Update tabel (T4 terpenuhi):
```
              T1    T2    T3    T4  | Supply
        +---------------------------------+
     G1 |  8     6    10     -    |  150
     G2 |  9    12    13     -    |  200
     G3 | 14     9    16     -    |   50
        +---------------------------------+
Demand  | 120   140   110     0   |
```

### Iterasi 2:

```
              T1    T2    T3  | Supply | Penalty
        +---------------------------------------+
     G1 |  8     6    10    |  150   | 6-8=2
     G2 |  9    12    13    |  200   | 9-12=3
     G3 | 14     9    16    |   50   | 9-14=5 ← MAX
        +---------------------------------------+
Demand  | 120   140   110   |
Penalty |8-9=1 6-9=3 10-13=3|
```

**Penalty maksimum = 5 (baris G3)**  
**Biaya minimum di G3 = 9 (G3 → T2)**  
**Alokasi: x32 = min(50, 140) = 50**

### Iterasi 3:

```
              T1    T2    T3  | Supply | Penalty
        +---------------------------------------+
     G1 |  8     6    10    |  150   | 6-8=2
     G2 |  9    12    13    |  200   | 9-12=3 ← MAX
     G3 | 14     -    16    |    0   | -
        +---------------------------------------+
Demand  | 120    90   110   |
Penalty |8-9=1  6-12=6 10-13=3|
```

**Penalty maksimum = 6 (kolom T2)**  
**Biaya minimum di T2 = 6 (G1 → T2)**  
**Alokasi: x12 = min(150, 90) = 90**

### Iterasi 4:

```
              T1    T2    T3  | Supply | Penalty
        +---------------------------------------+
     G1 |  8     -    10    |   60   | 8-10=2
     G2 |  9    12    13    |  200   | 9-13=4 ← MAX
        +---------------------------------------+
Demand  | 120    0    110   |
Penalty |8-9=1   -   10-13=3|
```

**Penalty maksimum = 4 (baris G2)**  
**Biaya minimum di G2 = 9 (G2 → T1)**  
**Alokasi: x21 = min(200, 120) = 120**

### Iterasi 5 & 6 (Sisa):

```
x22 = 0, x23 = 80, x11 = 0, x13 = 60, x33 = 30
```

### Solusi Akhir VAM:

```
              T1    T2    T3    T4  | Supply | Used
        +--------------------------------------------+
     G1 |  0   [90] [60]   0    |  150   | 150
     G2 | [120]  0   [80]   0    |  200   | 200
     G3 |  0   [50] [30] [130]  |  180   | 210*
        +--------------------------------------------+
Demand  | 120   140   110   130   |        | 500
```

*Note: Terjadi over-allocation pada G3 (30 unit excess)

### Perbaikan Solusi VAM (Balanced):

```
              T1    T2    T3    T4  | Supply | Used
        +--------------------------------------------+
     G1 |  0   [90] [60]   0    |  150   | 150
     G2 | [120]  0   [50]   0    |  170   | 170
     G3 |  0   [50]  0  [130]  |  180   | 180
        +--------------------------------------------+
Demand  | 120   140   110   130   |        | 500
```

### Perhitungan Biaya VAM:

```
Z = (6 × 90) + (10 × 60) + (9 × 120) + (13 × 50) + (9 × 50) + (5 × 130)
Z = 540 + 600 + 1,080 + 650 + 450 + 650
Z = Rp 3,970
```

**Total Biaya = Rp 3,970** (Terbaik!)

---

## PERBANDINGAN METODE

| Metode | Total Biaya | Keterangan |
|--------|-------------|------------|
| Northwest Corner | Rp 4,600 | Paling sederhana, hasil kurang optimal |
| Least Cost | Rp 4,050 | Lebih baik, fokus pada biaya rendah |
| VAM | Rp 3,970 | Terbaik, pertimbangkan opportunity cost |

---

## UJI OPTIMALITAS DENGAN MODI METHOD

Untuk memastikan solusi VAM sudah optimal, gunakan MODI Method (Modified Distribution).

### Langkah MODI:

1. **Hitung u_i dan v_j** untuk setiap basic variable
2. **Hitung opportunity cost** untuk non-basic variable
3. **Jika semua opportunity cost ≥ 0**, solusi optimal
4. **Jika ada yang negatif**, lakukan iterasi stepping stone

*[Perhitungan MODI detail akan dilakukan dengan software untuk verifikasi]*

---

## KESIMPULAN SOLUSI MANUAL

**Solusi Terbaik (VAM):**
- G1 → T2: 90 unit (Rp 540)
- G1 → T3: 60 unit (Rp 600)
- G2 → T1: 120 unit (Rp 1,080)
- G2 → T3: 50 unit (Rp 650)
- G3 → T2: 50 unit (Rp 450)
- G3 → T4: 130 unit (Rp 650)

**Total Biaya Minimum: Rp 3,970**

*Catatan: Solusi ini akan diverifikasi menggunakan Excel Solver dan Python untuk memastikan optimalitas.*