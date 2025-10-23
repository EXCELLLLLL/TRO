"""
FreshDrink Distribution Co. - Transportation Problem Optimization
Menggunakan PuLP untuk Linear Programming
"""

from pulp import *
import numpy as np
import json
from datetime import datetime

# ===============================
# DATA INPUT
# ===============================

# Kapasitas Gudang (Supply)
supply = {
    'G1': 150,  # Bekasi
    'G2': 200,  # Tangerang
    'G3': 180   # Depok
}

# Permintaan Toko (Demand)
demand = {
    'T1': 120,  # Jakarta Pusat
    'T2': 140,  # Jakarta Utara
    'T3': 110,  # Jakarta Selatan
    'T4': 130   # Jakarta Timur
}

# Biaya Transportasi (Rp per unit)
costs = {
    'G1': {'T1': 8, 'T2': 6, 'T3': 10, 'T4': 9},
    'G2': {'T1': 9, 'T2': 12, 'T3': 13, 'T4': 7},
    'G3': {'T1': 14, 'T2': 9, 'T3': 16, 'T4': 5}
}

# Daftar gudang dan toko
warehouses = list(supply.keys())
stores = list(demand.keys())

print("="*60)
print("FRESHDRINK DISTRIBUTION CO. - OPTIMIZATION SOLVER")
print("Transportation Problem using PuLP")
print("="*60)
print()

# ===============================
# DISPLAY INPUT DATA
# ===============================

print("DATA INPUT")
print("-" * 60)
print("\n1. KAPASITAS GUDANG (Supply):")
for warehouse, cap in supply.items():
    print(f"   {warehouse}: {cap} unit")
print(f"   Total Supply: {sum(supply.values())} unit")

print("\n2. PERMINTAAN TOKO (Demand):")
for store, dem in demand.items():
    print(f"   {store}: {dem} unit")
print(f"   Total Demand: {sum(demand.values())} unit")

print("\n3. MATRIKS BIAYA TRANSPORTASI (Rp/unit):")
print(f"   {'':6}", end="")
for store in stores:
    print(f"{store:>8}", end="")
print()
for warehouse in warehouses:
    print(f"   {warehouse:6}", end="")
    for store in stores:
        print(f"{costs[warehouse][store]:>8}", end="")
    print()

# Check balance
total_supply = sum(supply.values())
total_demand = sum(demand.values())
print(f"\n  Balance Check: Supply={total_supply}, Demand={total_demand}")
if total_supply > total_demand:
    print(f"     UNBALANCED: Excess supply = {total_supply - total_demand} unit")
elif total_supply < total_demand:
    print(f"     UNBALANCED: Shortage = {total_demand - total_supply} unit")
else:
    print("   BALANCED")

print("\n" + "="*60)

# ===============================
# BUILD OPTIMIZATION MODEL
# ===============================

print("\nBUILDING OPTIMIZATION MODEL...")
print("-" * 60)

# Create the LP problem
prob = LpProblem("FreshDrink_Distribution", LpMinimize)

# Decision Variables: x[i,j] = units shipped from warehouse i to store j
x = LpVariable.dicts("Route",
                     [(i, j) for i in warehouses for j in stores],
                     lowBound=0,
                     cat='Continuous')

print(f"✓ Created {len(x)} decision variables (xij)")

# Objective Function: Minimize total transportation cost
prob += lpSum([costs[i][j] * x[(i, j)]
               for i in warehouses for j in stores]), "Total_Cost"

print("✓ Set objective function: Minimize total cost")

# Constraints
constraint_count = 0

# Supply Constraints: Sum of shipments from each warehouse <= capacity
for i in warehouses:
    prob += lpSum([x[(i, j)] for j in stores]) <= supply[i], f"Supply_{i}"
    constraint_count += 1

print(f"✓ Added {len(warehouses)} supply constraints")

# Demand Constraints: Sum of shipments to each store = demand
for j in stores:
    prob += lpSum([x[(i, j)] for i in warehouses]) == demand[j], f"Demand_{j}"
    constraint_count += 1

print(f"✓ Added {len(stores)} demand constraints")
print(f"✓ Total constraints: {constraint_count}")

# ===============================
# SOLVE THE PROBLEM
# ===============================

print("\nSOLVING THE PROBLEM...")
print("-" * 60)

# Solve
prob.solve(PULP_CBC_CMD(msg=0))

# Check status
status = LpStatus[prob.status]
print(f"Status: {status}")

if status == "Optimal":
    print("Optimal solution found!")
else:
    print(f"Solution status: {status}")

print("\n" + "="*60)

# ===============================
# DISPLAY RESULTS
# ===============================

print("\nHASIL OPTIMASI")
print("="*60)

# Optimal shipments
print("\n1. ALOKASI PENGIRIMAN OPTIMAL:")
print("-" * 60)

shipment_table = []
total_cost = 0

for i in warehouses:
    for j in stores:
        quantity = x[(i, j)].varValue
        if quantity > 0:
            cost = costs[i][j] * quantity
            total_cost += cost
            shipment_table.append({
                'from': i,
                'to': j,
                'quantity': quantity,
                'unit_cost': costs[i][j],
                'total_cost': cost
            })
            print(f"   {i} → {j}: {quantity:>6.0f} unit × Rp {costs[i][j]:>4} = Rp {cost:>8,.0f}")

# Summary table
print("\n2. TABEL DISTRIBUSI:")
print("-" * 60)
print(f"   {'':6}", end="")
for store in stores:
    print(f"{store:>10}", end="")
print(f"{'Supply':>10}{'Used':>10}")

for warehouse in warehouses:
    print(f"   {warehouse:6}", end="")
    row_total = 0
    for store in stores:
        quantity = x[(warehouse, store)].varValue
        if quantity > 0:
            print(f"{quantity:>10.0f}", end="")
        else:
            print(f"{'0':>10}", end="")
        row_total += quantity
    print(f"{supply[warehouse]:>10}{row_total:>10.0f}")

# Demand fulfillment
print(f"   {'Demand':6}", end="")
for store in stores:
    col_total = sum([x[(warehouse, store)].varValue for warehouse in warehouses])
    print(f"{col_total:>10.0f}", end="")
print()

# Warehouse utilization
print("\n3. UTILISASI GUDANG:")
print("-" * 60)
for warehouse in warehouses:
    used = sum([x[(warehouse, store)].varValue for store in stores])
    capacity = supply[warehouse]
    unused = capacity - used
    utilization = (used / capacity) * 100
    print(f"   {warehouse}: {used:>6.0f}/{capacity:>6.0f} unit used ({utilization:>5.1f}%) | Unused: {unused:>6.0f} unit")

# Cost breakdown
print("\n4. RINCIAN BIAYA:")
print("-" * 60)
print(f"   Total Biaya Transportasi: Rp {value(prob.objective):>10,.0f}")
print(f"   Rata-rata Biaya per Unit: Rp {value(prob.objective)/sum(demand.values()):>10,.2f}")

# Shadow prices (dual values)
print("\n5. SHADOW PRICES (NILAI DUAL):")
print("-" * 60)
print("   Supply Constraints:")
for i in warehouses:
    constraint = prob.constraints[f"Supply_{i}"]
    shadow_price = constraint.pi if constraint.pi is not None else 0
    print(f"   {i}: {shadow_price:>10.4f}")

print("\n   Demand Constraints:")
for j in stores:
    constraint = prob.constraints[f"Demand_{j}"]
    shadow_price = constraint.pi if constraint.pi is not None else 0
    print(f"   {j}: {shadow_price:>10.4f}")

# Reduced costs
print("\n6. REDUCED COSTS (Non-Basic Variables):")
print("-" * 60)
non_basic_count = 0
for i in warehouses:
    for j in stores:
        if x[(i, j)].varValue == 0:
            reduced_cost = x[(i, j)].dj if hasattr(x[(i, j)], 'dj') else 0
            if reduced_cost != 0:
                print(f"   {i} → {j}: {reduced_cost:>10.4f}")
                non_basic_count += 1

if non_basic_count == 0:
    print("   (Semua reduced costs = 0 atau tidak tersedia)")

print("\n" + "="*60)

# ===============================
# SAVE RESULTS TO JSON
# ===============================

results = {
    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'status': status,
    'optimal_cost': value(prob.objective),
    'shipments': shipment_table,
    'warehouse_utilization': {
        warehouse: {
            'capacity': supply[warehouse],
            'used': sum([x[(warehouse, store)].varValue for store in stores]),
            'unused': supply[warehouse] - sum([x[(warehouse, store)].varValue for store in stores])
        }
        for warehouse in warehouses
    },
    'demand_fulfillment': {
        store: sum([x[(warehouse, store)].varValue for warehouse in warehouses])
        for store in stores
    }
}

# Save to JSON file
with open('results.json', 'w') as f:
    json.dump(results, f, indent=4)

print("\nResults saved to: results.json")

# ===============================
# COMPARISON WITH MANUAL METHODS
# ===============================

print("\n" + "="*60)
print("PERBANDINGAN DENGAN METODE MANUAL")
print("="*60)

manual_results = {
    'Northwest Corner': 4600,
    'Least Cost': 4050,
    'VAM': 3970,
    'Optimal (Software)': value(prob.objective)
}

print("\n   Method                    | Total Cost (Rp) | Gap from Optimal")
print("   " + "-"*60)
for method, cost in manual_results.items():
    gap = cost - manual_results['Optimal (Software)']
    gap_pct = (gap / manual_results['Optimal (Software)']) * 100
    if gap == 0:
        print(f"   {method:25} | {cost:>15,.0f} | OPTIMAL")
    else:
        print(f"   {method:25} | {cost:>15,.0f} | +Rp {gap:>,.0f} (+{gap_pct:.2f}%)")

print("\n" + "="*60)
print("OPTIMIZATION COMPLETE!")
print("="*60)