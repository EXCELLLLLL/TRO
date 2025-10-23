"""
Visualization Script for FreshDrink Distribution Optimization
Membuat grafik dan diagram untuk analisis hasil
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import json

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# ===============================
# LOAD DATA
# ===============================

# Data hasil optimasi
optimal_solution = {
    'G1': {'T1': 0, 'T2': 90, 'T3': 60, 'T4': 0},
    'G2': {'T1': 120, 'T2': 0, 'T3': 50, 'T4': 0},
    'G3': {'T1': 0, 'T2': 50, 'T3': 0, 'T4': 130}
}

costs = {
    'G1': {'T1': 8, 'T2': 6, 'T3': 10, 'T4': 9},
    'G2': {'T1': 9, 'T2': 12, 'T3': 13, 'T4': 7},
    'G3': {'T1': 14, 'T2': 9, 'T3': 16, 'T4': 5}
}

supply = {'G1': 150, 'G2': 200, 'G3': 180}
demand = {'T1': 120, 'T2': 140, 'T3': 110, 'T4': 130}

# Comparison data
comparison_data = {
    'Northwest Corner': 4600,
    'Least Cost': 4050,
    'VAM': 3970,
    'Optimal\n(Software)': 3970
}

# ===============================
# FIGURE 1: COST MATRIX HEATMAP
# ===============================

fig1, ax1 = plt.subplots(figsize=(10, 6))

# Create cost matrix
warehouses = ['G1', 'G2', 'G3']
store_pos = {
    'T1': (4, 3.5),
    'T2': (4, 2.5),
    'T3': (4, 1.5),
    'T4': (4, 0.5)
}

# Draw nodes
for w, pos in warehouse_pos.items():
    circle = plt.Circle(pos, 0.25, color='lightblue', ec='darkblue', linewidth=2, zorder=3)
    ax2.add_patch(circle)
    ax2.text(pos[0], pos[1], w, ha='center', va='center',
             fontweight='bold', fontsize=11, zorder=4)
    # Add supply label
    ax2.text(pos[0] - 0.5, pos[1], f'{supply[w]}u', ha='right', va='center',
             fontsize=9, style='italic')

for s, pos in store_pos.items():
    circle = plt.Circle(pos, 0.25, color='lightcoral', ec='darkred', linewidth=2, zorder=3)
    ax2.add_patch(circle)
    ax2.text(pos[0], pos[1], s, ha='center', va='center',
             fontweight='bold', fontsize=11, zorder=4)
    # Add demand label
    ax2.text(pos[0] + 0.5, pos[1], f'{demand[s]}u', ha='left', va='center',
             fontsize=9, style='italic')

# Draw flows
for flow in flows:
    from_pos = warehouse_pos[flow['from']]
    to_pos = store_pos[flow['to']]

    # Line width proportional to quantity
    linewidth = flow['quantity'] / 30

    # Draw arrow
    ax2.annotate('', xy=to_pos, xytext=from_pos,
                 arrowprops=dict(arrowstyle='->', lw=linewidth,
                                 color='gray', alpha=0.6))

    # Add label
    mid_x = (from_pos[0] + to_pos[0]) / 2
    mid_y = (from_pos[1] + to_pos[1]) / 2
    label = f"{flow['quantity']:.0f}u\nRp{flow['cost']}"
    ax2.text(mid_x, mid_y, label, ha='center', va='center',
             fontsize=8, bbox=dict(boxstyle='round,pad=0.3',
                                   facecolor='yellow', alpha=0.7))

# Labels and legend
ax2.set_xlim(0, 5)
ax2.set_ylim(0, 4)
ax2.set_aspect('equal')
ax2.axis('off')
ax2.set_title('Diagram Alur Distribusi Optimal\nFreshDrink Distribution Co.',
              fontsize=14, fontweight='bold', pad=20)

# Add legend
legend_elements = [
    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='lightblue',
               markersize=10, label='Gudang (Supply)', markeredgecolor='darkblue', markeredgewidth=2),
    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='lightcoral',
               markersize=10, label='Toko (Demand)', markeredgecolor='darkred', markeredgewidth=2),
    plt.Line2D([0], [0], color='gray', linewidth=2, label='Alur Distribusi', alpha=0.6)
]
ax2.legend(handles=legend_elements, loc='upper left', fontsize=10)

# Add total cost
ax2.text(2.5, 3.8, f'Total Biaya: Rp 3,970', ha='center', va='center',
         fontsize=12, fontweight='bold',
         bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgreen', alpha=0.8))

plt.tight_layout()
plt.savefig('solution_flow_diagram.png', dpi=300, bbox_inches='tight')
print("✓ Saved: solution_flow_diagram.png")

# ===============================
# FIGURE 3: METHOD COMPARISON
# ===============================

fig3, ax3 = plt.subplots(figsize=(10, 6))

methods = list(comparison_data.keys())
costs_list = list(comparison_data.values())
colors = ['#ff9999', '#ffcc99', '#ffff99', '#99ff99']

bars = ax3.bar(methods, costs_list, color=colors, edgecolor='black', linewidth=1.5)

# Add value labels on bars
for bar, cost in zip(bars, costs_list):
    height = bar.get_height()
    ax3.text(bar.get_x() + bar.get_width() / 2., height,
             f'Rp {cost:,.0f}',
             ha='center', va='bottom', fontweight='bold', fontsize=10)

# Add gap from optimal
optimal_cost = comparison_data['Optimal\n(Software)']
for i, (method, cost) in enumerate(comparison_data.items()):
    if cost > optimal_cost:
        gap = cost - optimal_cost
        gap_pct = (gap / optimal_cost) * 100
        ax3.text(i, cost + 150, f'+Rp {gap:,.0f}\n(+{gap_pct:.1f}%)',
                 ha='center', va='bottom', fontsize=8, color='red')

# Styling
ax3.set_ylabel('Total Biaya (Rp)', fontsize=12, fontweight='bold')
ax3.set_xlabel('Metode', fontsize=12, fontweight='bold')
ax3.set_title('Perbandingan Metode Penyelesaian\nTransportation Problem',
              fontsize=14, fontweight='bold', pad=20)
ax3.grid(axis='y', alpha=0.3, linestyle='--')
ax3.set_ylim(0, max(costs_list) * 1.15)

# Add horizontal line for optimal
ax3.axhline(y=optimal_cost, color='green', linestyle='--', linewidth=2,
            label='Biaya Optimal', alpha=0.7)
ax3.legend(fontsize=10)

plt.tight_layout()
plt.savefig('method_comparison.png', dpi=300, bbox_inches='tight')
print("✓ Saved: method_comparison.png")

# ===============================
# FIGURE 4: WAREHOUSE UTILIZATION
# ===============================

fig4, ax4 = plt.subplots(figsize=(10, 6))

# Calculate utilization
utilization_data = {}
for w in warehouses:
    used = sum([optimal_solution[w][s] for s in stores])
    utilization_data[w] = {
        'used': used,
        'unused': supply[w] - used,
        'percentage': (used / supply[w]) * 100
    }

# Prepare data for stacked bar
warehouses_list = list(utilization_data.keys())
used = [utilization_data[w]['used'] for w in warehouses_list]
unused = [utilization_data[w]['unused'] for w in warehouses_list]

# Create stacked bar
x = np.arange(len(warehouses_list))
width = 0.5

bars1 = ax4.bar(x, used, width, label='Digunakan', color='#90EE90', edgecolor='black')
bars2 = ax4.bar(x, unused, width, bottom=used, label='Tidak Digunakan',
                color='#FFB6C1', edgecolor='black')

# Add percentage labels
for i, w in enumerate(warehouses_list):
    total = supply[w]
    percentage = utilization_data[w]['percentage']
    ax4.text(i, total + 5, f'{percentage:.1f}%',
             ha='center', va='bottom', fontweight='bold', fontsize=11)

    # Add value labels
    ax4.text(i, used[i] / 2, f'{used[i]:.0f}',
             ha='center', va='center', fontweight='bold', fontsize=10)
    if unused[i] > 0:
        ax4.text(i, used[i] + unused[i] / 2, f'{unused[i]:.0f}',
                 ha='center', va='center', fontweight='bold', fontsize=10)

# Styling
ax4.set_ylabel('Kapasitas (unit)', fontsize=12, fontweight='bold')
ax4.set_xlabel('Gudang', fontsize=12, fontweight='bold')
ax4.set_title('Utilisasi Kapasitas Gudang', fontsize=14, fontweight='bold', pad=20)
ax4.set_xticks(x)
ax4.set_xticklabels(warehouses_list)
ax4.legend(fontsize=11, loc='upper right')
ax4.grid(axis='y', alpha=0.3, linestyle='--')
ax4.set_ylim(0, max(supply.values()) * 1.15)

plt.tight_layout()
plt.savefig('warehouse_utilization.png', dpi=300, bbox_inches='tight')
print("✓ Saved: warehouse_utilization.png")

# ===============================
# FIGURE 5: DEMAND FULFILLMENT
# ===============================

fig5, ax5 = plt.subplots(figsize=(10, 6))

# Calculate actual fulfillment
fulfillment = {}
for s in stores:
    fulfillment[s] = sum([optimal_solution[w][s] for w in warehouses])

stores_list = list(fulfillment.keys())
demand_list = [demand[s] for s in stores_list]
fulfillment_list = [fulfillment[s] for s in stores_list]

x = np.arange(len(stores_list))
width = 0.35

bars1 = ax5.bar(x - width / 2, demand_list, width, label='Permintaan',
                color='#FFB6C1', edgecolor='black')
bars2 = ax5.bar(x + width / 2, fulfillment_list, width, label='Terpenuhi',
                color='#90EE90', edgecolor='black')

# Add value labels
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax5.text(bar.get_x() + bar.get_width() / 2., height,
                 f'{height:.0f}',
                 ha='center', va='bottom', fontweight='bold', fontsize=10)

# Styling
ax5.set_ylabel('Jumlah (unit)', fontsize=12, fontweight='bold')
ax5.set_xlabel('Toko', fontsize=12, fontweight='bold')
ax5.set_title('Pemenuhan Permintaan Toko', fontsize=14, fontweight='bold', pad=20)
ax5.set_xticks(x)
ax5.set_xticklabels(stores_list)
ax5.legend(fontsize=11)
ax5.grid(axis='y', alpha=0.3, linestyle='--')
ax5.set_ylim(0, max(demand_list) * 1.15)

# Add 100% fulfillment note
ax5.text(len(stores_list) / 2 - 0.5, max(demand_list) * 1.05,
         '✓ Semua permintaan terpenuhi 100%',
         ha='center', va='center', fontsize=11, fontweight='bold',
         bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgreen', alpha=0.8))

plt.tight_layout()
plt.savefig('demand_fulfillment.png', dpi=300, bbox_inches='tight')
print("✓ Saved: demand_fulfillment.png")

# ===============================
# FIGURE 6: COST BREAKDOWN BY ROUTE
# ===============================

fig6, ax6 = plt.subplots(figsize=(12, 6))

# Calculate cost for each route
route_costs = []
route_labels = []
for w in warehouses:
    for s in stores:
        if optimal_solution[w][s] > 0:
            cost = optimal_solution[w][s] * costs[w][s]
            route_costs.append(cost)
            route_labels.append(f'{w}→{s}\n{optimal_solution[w][s]:.0f}u×Rp{costs[w][s]}')

# Sort by cost
sorted_indices = np.argsort(route_costs)[::-1]
route_costs = [route_costs[i] for i in sorted_indices]
route_labels = [route_labels[i] for i in sorted_indices]

# Color gradient
colors_gradient = plt.cm.RdYlGn_r(np.linspace(0.3, 0.9, len(route_costs)))

bars = ax6.barh(route_labels, route_costs, color=colors_gradient, edgecolor='black')

# Add value labels
for bar, cost in zip(bars, route_costs):
    width = bar.get_width()
    percentage = (cost / sum(route_costs)) * 100
    ax6.text(width, bar.get_y() + bar.get_height() / 2,
             f' Rp {cost:,.0f} ({percentage:.1f}%)',
             ha='left', va='center', fontweight='bold', fontsize=9)

# Styling
ax6.set_xlabel('Biaya (Rp)', fontsize=12, fontweight='bold')
ax6.set_title('Rincian Biaya Per Rute Distribusi', fontsize=14, fontweight='bold', pad=20)
ax6.grid(axis='x', alpha=0.3, linestyle='--')
ax6.set_xlim(0, max(route_costs) * 1.25)

# Add total
total_cost = sum(route_costs)
ax6.text(max(route_costs) * 0.5, len(route_costs) - 0.3,
         f'Total: Rp {total_cost:,.0f}',
         ha='center', va='center', fontsize=12, fontweight='bold',
         bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.8))

plt.tight_layout()
plt.savefig('cost_breakdown.png', dpi=300, bbox_inches='tight')
print("✓ Saved: cost_breakdown.png")

# ===============================
# SUMMARY STATISTICS
# ===============================

print("\n" + "=" * 60)
print("SUMMARY STATISTICS")
print("=" * 60)

print("\n1. Total Biaya Optimal: Rp 3,970")
print("2. Rata-rata Biaya per Unit: Rp", 3970 / 500)
print("3. Jumlah Rute Aktif:", len([1 for w in warehouses for s in stores if optimal_solution[w][s] > 0]))
print("4. Total Unit Dikirim:", sum([optimal_solution[w][s] for w in warehouses for s in stores]))

print("\n5. Gudang dengan Utilisasi Tertinggi:")
for w in warehouses:
    used = sum([optimal_solution[w][s] for s in stores])
    percentage = (used / supply[w]) * 100
    print(f"   {w}: {percentage:.1f}%")

print("\n6. Rute Termahal:")
max_cost = 0
max_route = None
for w in warehouses:
    for s in stores:
        if optimal_solution[w][s] > 0:
            cost = optimal_solution[w][s] * costs[w][s]
            if cost > max_cost:
                max_cost = cost
                max_route = f"{w}→{s}"
print(f"   {max_route}: Rp {max_cost:,.0f}")

print("\n7. Rute Termurah:")
min_cost = float('inf')
min_route = None
for w in warehouses:
    for s in stores:
        if optimal_solution[w][s] > 0:
            cost = optimal_solution[w][s] * costs[w][s]
            if cost < min_cost:
                min_cost = cost
                min_route = f"{w}→{s}"
print(f"   {min_route}: Rp {min_cost:,.0f}")

print("\n" + "=" * 60)
print("ALL VISUALIZATIONS CREATED SUCCESSFULLY!")
print("=" * 60)
print("\nGenerated files:")
print("  1. cost_matrix_heatmap.png")
print("  2. solution_flow_diagram.png")
print("  3. method_comparison.png")
print("  4. warehouse_utilization.png")
print("  5. demand_fulfillment.png")
print("  6. cost_breakdown.png")
print("\nUse these visualizations in your report!")
print("=" * 60)
s = ['T1', 'T2', 'T3', 'T4']
cost_matrix = np.array([[costs[w][s] for s in stores] for w in warehouses])

# Create heatmap
im = ax1.imshow(cost_matrix, cmap='YlOrRd', aspect='auto')

# Set ticks
ax1.set_xticks(np.arange(len(stores)))
ax1.set_yticks(np.arange(len(warehouses)))
ax1.set_xticklabels(stores)
ax1.set_yticklabels(warehouses)

# Add colorbar
cbar = plt.colorbar(im, ax=ax1)
cbar.set_label('Biaya (Rp/unit)', rotation=270, labelpad=20)

# Add text annotations
for i in range(len(warehouses)):
    for j in range(len(stores)):
        text = ax1.text(j, i, cost_matrix[i, j],
                        ha="center", va="center", color="black", fontweight='bold')

# Labels
ax1.set_title('Matriks Biaya Transportasi\nFreshDrink Distribution Co.',
              fontsize=14, fontweight='bold', pad=20)
ax1.set_xlabel('Toko (Destination)', fontsize=12)
ax1.set_ylabel('Gudang (Source)', fontsize=12)

plt.tight_layout()
plt.savefig('cost_matrix_heatmap.png', dpi=300, bbox_inches='tight')
print("✓ Saved: cost_matrix_heatmap.png")

# ===============================
# FIGURE 2: SOLUTION FLOW DIAGRAM
# ===============================

fig2, ax2 = plt.subplots(figsize=(12, 8))

# Prepare data for flow
flows = []
for w in warehouses:
    for s in stores:
        if optimal_solution[w][s] > 0:
            flows.append({
                'from': w,
                'to': s,
                'quantity': optimal_solution[w][s],
                'cost': costs[w][s]
            })

# Position nodes
warehouse_pos = {
    'G1': (1, 3),
    'G2': (1, 2),
    'G3': (1, 1)
}

store