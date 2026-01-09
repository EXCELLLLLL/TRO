"""
Transportation Problem Solver - PT. MediCare Indonesia
Menggunakan PuLP untuk Linear Programming
"""

import pulp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class TransportationOptimizer:
    def __init__(self):
        """Inisialisasi data untuk masalah transportasi"""

        # Data Gudang (Supply)
        self.warehouses = ['Jakarta', 'Tangerang', 'Bekasi', 'Bogor']
        self.supply = {
            'Jakarta': 350,
            'Tangerang': 400,
            'Bekasi': 300,
            'Bogor': 250
        }

        # Data Tujuan (Demand)
        self.destinations = ['RS_Jakarta_Pusat', 'RS_Tangerang', 'RS_Bekasi',
                             'Apotek_Depok', 'RS_Bogor']
        self.demand = {
            'RS_Jakarta_Pusat': 250,
            'RS_Tangerang': 300,
            'RS_Bekasi': 200,
            'Apotek_Depok': 280,
            'RS_Bogor': 220
        }

        # Biaya Transportasi (dalam ribu Rupiah per unit)
        self.costs = {
            ('Jakarta', 'RS_Jakarta_Pusat'): 5,
            ('Jakarta', 'RS_Tangerang'): 15,
            ('Jakarta', 'RS_Bekasi'): 12,
            ('Jakarta', 'Apotek_Depok'): 8,
            ('Jakarta', 'RS_Bogor'): 18,

            ('Tangerang', 'RS_Jakarta_Pusat'): 18,
            ('Tangerang', 'RS_Tangerang'): 4,
            ('Tangerang', 'RS_Bekasi'): 20,
            ('Tangerang', 'Apotek_Depok'): 16,
            ('Tangerang', 'RS_Bogor'): 25,

            ('Bekasi', 'RS_Jakarta_Pusat'): 14,
            ('Bekasi', 'RS_Tangerang'): 22,
            ('Bekasi', 'RS_Bekasi'): 6,
            ('Bekasi', 'Apotek_Depok'): 10,
            ('Bekasi', 'RS_Bogor'): 20,

            ('Bogor', 'RS_Jakarta_Pusat'): 16,
            ('Bogor', 'RS_Tangerang'): 24,
            ('Bogor', 'RS_Bekasi'): 18,
            ('Bogor', 'Apotek_Depok'): 7,
            ('Bogor', 'RS_Bogor'): 5
        }

        self.model = None
        self.solution = None

    def build_model(self):
        """Membangun model optimasi"""

        # Inisialisasi model
        self.model = pulp.LpProblem("Transportation_Problem", pulp.LpMinimize)

        # Variabel keputusan
        # x[i,j] = jumlah unit yang dikirim dari gudang i ke tujuan j
        self.x = pulp.LpVariable.dicts("Route",
                                       ((w, d) for w in self.warehouses
                                        for d in self.destinations),
                                       lowBound=0,
                                       cat='Continuous')

        # Fungsi Tujuan: Minimasi total biaya
        self.model += pulp.lpSum([self.costs[(w, d)] * self.x[(w, d)]
                                  for w in self.warehouses
                                  for d in self.destinations]), "Total_Cost"

        # Kendala Kapasitas Gudang (Supply Constraints)
        for w in self.warehouses:
            self.model += (pulp.lpSum([self.x[(w, d)] for d in self.destinations])
                           <= self.supply[w],
                           f"Supply_{w}")

        # Kendala Permintaan Tujuan (Demand Constraints)
        for d in self.destinations:
            self.model += (pulp.lpSum([self.x[(w, d)] for w in self.warehouses])
                           == self.demand[d],
                           f"Demand_{d}")

        print("✓ Model berhasil dibangun!")
        print(f"  - Jumlah variabel: {len(self.x)}")
        print(f"  - Jumlah kendala: {len(self.model.constraints)}")

    def solve(self):
        """Menyelesaikan model optimasi"""

        print("\n" + "="*60)
        print("Memulai proses optimasi...")
        print("="*60)

        # Selesaikan model
        self.model.solve(pulp.PULP_CBC_CMD(msg=1))

        # Status solusi
        status = pulp.LpStatus[self.model.status]
        print(f"\nStatus Solusi: {status}")

        if status == 'Optimal':
            # Ekstrak solusi
            self.solution = {}
            for w in self.warehouses:
                for d in self.destinations:
                    value = self.x[(w, d)].varValue
                    if value > 0:
                        self.solution[(w, d)] = value

            print(f"✓ Solusi optimal ditemukan!")
            print(f"  Total Biaya Minimum: Rp {pulp.value(self.model.objective):,.0f},000")

            return True
        else:
            print("✗ Solusi optimal tidak ditemukan!")
            return False

    def display_results(self):
        """Menampilkan hasil solusi"""

        if not self.solution:
            print("Tidak ada solusi untuk ditampilkan!")
            return

        print("\n" + "="*60)
        print("HASIL OPTIMASI - ALOKASI PENGIRIMAN")
        print("="*60)

        # Tabel alokasi
        print("\nAlokasi Pengiriman (unit):")
        print("-" * 60)

        allocation_matrix = []
        for w in self.warehouses:
            row = [w]
            total_sent = 0
            for d in self.destinations:
                value = self.x[(w, d)].varValue if self.x[(w, d)].varValue else 0
                row.append(value)
                total_sent += value
            row.append(total_sent)
            allocation_matrix.append(row)

        # Tambahkan total permintaan
        total_row = ['TOTAL']
        for d in self.destinations:
            total = sum(self.x[(w, d)].varValue if self.x[(w, d)].varValue else 0
                        for w in self.warehouses)
            total_row.append(total)
        total_row.append(sum([row[-1] for row in allocation_matrix]))
        allocation_matrix.append(total_row)

        # Buat DataFrame
        df_allocation = pd.DataFrame(
            allocation_matrix,
            columns=['Gudang'] + self.destinations + ['Total Dikirim']
        )
        print(df_allocation.to_string(index=False))

        # Ringkasan biaya
        print("\n" + "="*60)
        print("RINGKASAN BIAYA")
        print("="*60)

        total_cost = 0
        cost_breakdown = []

        for (w, d), quantity in self.solution.items():
            cost = self.costs[(w, d)] * quantity
            total_cost += cost
            cost_breakdown.append({
                'Dari': w,
                'Ke': d,
                'Jumlah (unit)': quantity,
                'Biaya/unit (Rp ribuan)': self.costs[(w, d)],
                'Total Biaya (Rp ribuan)': cost
            })

        df_cost = pd.DataFrame(cost_breakdown)
        print(df_cost.to_string(index=False))

        print(f"\n{'='*60}")
        print(f"TOTAL BIAYA TRANSPORTASI: Rp {total_cost:,.0f},000")
        print(f"{'='*60}")

        # Utilisasi kapasitas
        print("\n" + "="*60)
        print("UTILISASI KAPASITAS GUDANG")
        print("="*60)

        utilization = []
        for w in self.warehouses:
            used = sum(self.x[(w, d)].varValue if self.x[(w, d)].varValue else 0
                       for d in self.destinations)
            capacity = self.supply[w]
            util_pct = (used / capacity) * 100
            unused = capacity - used

            utilization.append({
                'Gudang': w,
                'Kapasitas': capacity,
                'Terpakai': used,
                'Sisa': unused,
                'Utilisasi (%)': util_pct
            })

        df_util = pd.DataFrame(utilization)
        print(df_util.to_string(index=False))

        return df_allocation, df_cost, df_util

    def visualize_solution(self):
        """Membuat visualisasi hasil"""

        if not self.solution:
            print("Tidak ada solusi untuk divisualisasikan!")
            return

        # Setup style
        plt.style.use('seaborn-v0_8-darkgrid')
        fig = plt.figure(figsize=(16, 10))

        # 1. Heatmap Alokasi
        ax1 = plt.subplot(2, 2, 1)
        allocation_data = np.zeros((len(self.warehouses), len(self.destinations)))

        for i, w in enumerate(self.warehouses):
            for j, d in enumerate(self.destinations):
                value = self.x[(w, d)].varValue if self.x[(w, d)].varValue else 0
                allocation_data[i, j] = value

        sns.heatmap(allocation_data,
                    annot=True,
                    fmt='.0f',
                    cmap='YlOrRd',
                    xticklabels=[d.replace('_', ' ') for d in self.destinations],
                    yticklabels=self.warehouses,
                    cbar_kws={'label': 'Unit'},
                    ax=ax1)
        ax1.set_title('Heatmap Alokasi Pengiriman (Unit)', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Tujuan', fontsize=11)
        ax1.set_ylabel('Gudang', fontsize=11)
        plt.setp(ax1.get_xticklabels(), rotation=45, ha='right')

        # 2. Utilisasi Kapasitas Gudang
        ax2 = plt.subplot(2, 2, 2)

        warehouses_list = []
        used_list = []
        unused_list = []

        for w in self.warehouses:
            used = sum(self.x[(w, d)].varValue if self.x[(w, d)].varValue else 0
                       for d in self.destinations)
            capacity = self.supply[w]
            unused = capacity - used

            warehouses_list.append(w)
            used_list.append(used)
            unused_list.append(unused)

        x_pos = np.arange(len(warehouses_list))
        ax2.bar(x_pos, used_list, label='Terpakai', color='#2ecc71', alpha=0.8)
        ax2.bar(x_pos, unused_list, bottom=used_list, label='Sisa',
                color='#e74c3c', alpha=0.8)

        ax2.set_xticks(x_pos)
        ax2.set_xticklabels(warehouses_list)
        ax2.set_ylabel('Kapasitas (Unit)', fontsize=11)
        ax2.set_title('Utilisasi Kapasitas Gudang', fontsize=14, fontweight='bold')
        ax2.legend()
        ax2.grid(axis='y', alpha=0.3)

        # Tambahkan persentase utilisasi
        for i, (w, u, un) in enumerate(zip(warehouses_list, used_list, unused_list)):
            total = u + un
            pct = (u / total) * 100
            ax2.text(i, total + 10, f'{pct:.1f}%',
                     ha='center', va='bottom', fontsize=10, fontweight='bold')

        # 3. Distribusi Biaya per Gudang
        ax3 = plt.subplot(2, 2, 3)

        cost_by_warehouse = {}
        for w in self.warehouses:
            cost = 0
            for d in self.destinations:
                quantity = self.x[(w, d)].varValue if self.x[(w, d)].varValue else 0
                cost += self.costs[(w, d)] * quantity
            cost_by_warehouse[w] = cost

        colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12']
        wedges, texts, autotexts = ax3.pie(cost_by_warehouse.values(),
                                           labels=cost_by_warehouse.keys(),
                                           autopct='%1.1f%%',
                                           colors=colors,
                                           startangle=90)

        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(10)
            autotext.set_fontweight('bold')

        ax3.set_title('Distribusi Biaya per Gudang', fontsize=14, fontweight='bold')

        # 4. Perbandingan Supply vs Demand
        ax4 = plt.subplot(2, 2, 4)

        total_supply = sum(self.supply.values())
        total_demand = sum(self.demand.values())
        total_used = sum(used_list)

        categories = ['Total Supply', 'Total Demand', 'Actual Used']
        values = [total_supply, total_demand, total_used]
        colors_bar = ['#3498db', '#e74c3c', '#2ecc71']

        bars = ax4.bar(categories, values, color=colors_bar, alpha=0.8)
        ax4.set_ylabel('Unit', fontsize=11)
        ax4.set_title('Perbandingan Supply, Demand, dan Actual Usage',
                      fontsize=14, fontweight='bold')
        ax4.grid(axis='y', alpha=0.3)

        # Tambahkan nilai di atas bar
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height + 10,
                     f'{int(value)}',
                     ha='center', va='bottom', fontsize=11, fontweight='bold')

        plt.tight_layout()
        plt.savefig('transportation_optimization_results.png', dpi=300, bbox_inches='tight')
        print("\n✓ Visualisasi disimpan sebagai 'transportation_optimization_results.png'")
        plt.show()

    def export_to_excel(self, filename='transportation_solution.xlsx'):
        """Export hasil ke Excel"""

        if not self.solution:
            print("Tidak ada solusi untuk di-export!")
            return

        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # Sheet 1: Alokasi
            allocation_matrix = []
            for w in self.warehouses:
                row = {'Gudang': w}
                for d in self.destinations:
                    value = self.x[(w, d)].varValue if self.x[(w, d)].varValue else 0
                    row[d] = value
                allocation_matrix.append(row)

            df_allocation = pd.DataFrame(allocation_matrix)
            df_allocation.to_excel(writer, sheet_name='Alokasi', index=False)

            # Sheet 2: Biaya Detail
            cost_breakdown = []
            for (w, d), quantity in self.solution.items():
                cost = self.costs[(w, d)] * quantity
                cost_breakdown.append({
                    'Dari': w,
                    'Ke': d,
                    'Jumlah (unit)': quantity,
                    'Biaya/unit (Rp ribuan)': self.costs[(w, d)],
                    'Total Biaya (Rp ribuan)': cost
                })

            df_cost = pd.DataFrame(cost_breakdown)
            df_cost.to_excel(writer, sheet_name='Detail Biaya', index=False)

            # Sheet 3: Ringkasan
            summary = {
                'Metrik': ['Total Biaya (Rp ribuan)',
                           'Total Supply (unit)',
                           'Total Demand (unit)',
                           'Supply Terpakai (unit)',
                           'Supply Tidak Terpakai (unit)'],
                'Nilai': [
                    pulp.value(self.model.objective),
                    sum(self.supply.values()),
                    sum(self.demand.values()),
                    sum(self.x[(w, d)].varValue if self.x[(w, d)].varValue else 0
                        for w in self.warehouses for d in self.destinations),
                    sum(self.supply.values()) - sum(self.x[(w, d)].varValue
                                                    if self.x[(w, d)].varValue else 0
                                                    for w in self.warehouses for d in self.destinations)
                ]
            }

            df_summary = pd.DataFrame(summary)
            df_summary.to_excel(writer, sheet_name='Ringkasan', index=False)

        print(f"\n✓ Hasil berhasil di-export ke '{filename}'")


# Main execution
if __name__ == "__main__":
    print("="*60)
    print("TRANSPORTATION PROBLEM OPTIMIZER")
    print("PT. MediCare Indonesia")
    print("="*60)

    # Inisialisasi optimizer
    optimizer = TransportationOptimizer()

    # Bangun model
    optimizer.build_model()

    # Selesaikan
    if optimizer.solve():
        # Tampilkan hasil
        optimizer.display_results()

        # Visualisasi
        optimizer.visualize_solution()

        # Export ke Excel
        optimizer.export_to_excel()

        print("\n" + "="*60)
        print("PROSES OPTIMASI SELESAI!")
        print("="*60)