"""
CSV Optimizer - FreshDrink Distribution Co.
Membaca data dari CSV dan menjalankan optimasi otomatis
"""

import csv
from pulp import *
import json


def read_csv_data(filename='data_input.csv'):
    """Read data from CSV file"""

    supply = {}
    demand = {}
    costs = {}

    with open(filename, 'r') as file:
        lines = file.readlines()

        current_section = None

        for line in lines:
            line = line.strip()

            # Skip comments and empty lines
            if not line or line.startswith('#'):
                continue

            # Detect section headers
            if line == 'SUPPLY':
                current_section = 'SUPPLY'
                continue
            elif line == 'DEMAND':
                current_section = 'DEMAND'
                continue
            elif line == 'COSTS':
                current_section = 'COSTS'
                continue
            elif line == 'SOLUTION':
                current_section = 'SOLUTION'
                continue
            elif line == 'METADATA':
                break

            # Parse data based on current section
            if current_section == 'SUPPLY':
                parts = line.split(',')
                if len(parts) == 3:
                    warehouse = parts[0]
                    capacity = int(parts[2])
                    supply[warehouse] = capacity

            elif current_section == 'DEMAND':
                parts = line.split(',')
                if len(parts) == 3:
                    store = parts[0]
                    demand_val = int(parts[2])
                    demand[store] = demand_val

            elif current_section == 'COSTS':
                parts = line.split(',')
                if len(parts) == 5:
                    warehouse = parts[0]
                    costs[warehouse] = {
                        'T1': int(parts[1]),
                        'T2': int(parts[2]),
                        'T3': int(parts[3]),
                        'T4': int(parts[4])
                    }

    return supply, demand, costs


def optimize_transportation(supply, demand, costs):
    """Solve transportation problem using PuLP"""

    warehouses = list(supply.keys())
    stores = list(demand.keys())

    # Create problem
    prob = LpProblem("Transportation_CSV", LpMinimize)

    # Decision variables
    x = LpVariable.dicts("Ship",
                         [(i, j) for i in warehouses for j in stores],
                         lowBound=0,
                         cat='Continuous')

    # Objective function
    prob += lpSum([costs[i][j] * x[(i, j)]
                   for i in warehouses for j in stores])

    # Supply constraints
    for i in warehouses:
        prob += lpSum([x[(i, j)] for j in stores]) <= supply[i]

    # Demand constraints
    for j in stores:
        prob += lpSum([x[(i, j)] for i in warehouses]) == demand[j]

    # Solve
    prob.solve(PULP_CBC_CMD(msg=0))

    return prob, x, warehouses, stores


def display_results(prob, x, warehouses, stores, supply, demand, costs):
    """Display optimization results"""

    print("=" * 70)
    print("TRANSPORTATION PROBLEM OPTIMIZER - FROM CSV")
    print("=" * 70)

    print(f"\nStatus: {LpStatus[prob.status]}")

    if LpStatus[prob.status] == "Optimal":
        print("\nOPTIMAL SOLUTION FOUND!\n")

        print("SHIPMENT ALLOCATION:")
        print("-" * 70)
        total_cost = 0
        shipments = []

        for i in warehouses:
            for j in stores:
                qty = x[(i, j)].varValue
                if qty > 0:
                    cost = costs[i][j] * qty
                    total_cost += cost
                    shipments.append({
                        'from': i,
                        'to': j,
                        'quantity': qty,
                        'unit_cost': costs[i][j],
                        'total_cost': cost
                    })
                    print(f"{i} → {j}: {qty:>6.0f} units × Rp {costs[i][j]:>4} = Rp {cost:>8,.0f}")

        print("-" * 70)
        print(f"TOTAL COST: Rp {total_cost:,.0f}")
        print("=" * 70)

        # Distribution table
        print("\nDISTRIBUTION TABLE:")
        print("-" * 70)
        print(f"{'':8}", end="")
        for j in stores:
            print(f"{j:>10}", end="")
        print(f"{'Supply':>10}{'Used':>10}")

        for i in warehouses:
            print(f"{i:8}", end="")
            row_total = 0
            for j in stores:
                qty = x[(i, j)].varValue
                print(f"{qty:>10.0f}", end="")
                row_total += qty
            print(f"{supply[i]:>10}{row_total:>10.0f}")

        print(f"{'Demand':8}", end="")
        for j in stores:
            col_total = sum([x[(i, j)].varValue for i in warehouses])
            print(f"{col_total:>10.0f}", end="")
        print()

        # Warehouse utilization
        print("\nWAREHOUSE UTILIZATION:")
        print("-" * 70)
        for i in warehouses:
            used = sum([x[(i, j)].varValue for j in stores])
            unused = supply[i] - used
            util = (used / supply[i]) * 100
            print(f"{i}: {used:>6.0f}/{supply[i]:>6.0f} units ({util:>5.1f}%) | Unused: {unused:>6.0f}")

        # Save to JSON
        results = {
            'status': 'Optimal',
            'total_cost': total_cost,
            'shipments': shipments,
            'utilization': {
                i: {
                    'capacity': supply[i],
                    'used': sum([x[(i, j)].varValue for j in stores]),
                    'unused': supply[i] - sum([x[(i, j)].varValue for j in stores])
                }
                for i in warehouses
            }
        }

        with open('results_from_csv.json', 'w') as f:
            json.dump(results, f, indent=4)

        print("\nResults saved to: results_from_csv.json")
        print("=" * 70)

    else:
        print(f"\nNo optimal solution found. Status: {LpStatus[prob.status]}")


def main():
    """Main function"""

    print("\nReading data from CSV...")

    try:
        supply, demand, costs = read_csv_data('data_input.csv')

        print("Data loaded successfully!\n")
        print(f"Warehouses: {len(supply)}")
        print(f"Stores: {len(demand)}")
        print(f"Total Supply: {sum(supply.values())}")
        print(f"Total Demand: {sum(demand.values())}")

        balance = sum(supply.values()) - sum(demand.values())
        if balance > 0:
            print(f"Balance: Unbalanced (Excess supply = {balance})")
        elif balance < 0:
            print(f"Balance: Unbalanced (Shortage = {abs(balance)})")
        else:
            print("Balance: Balanced")

        print("\nRunning optimization...\n")

        prob, x, warehouses, stores = optimize_transportation(supply, demand, costs)

        display_results(prob, x, warehouses, stores, supply, demand, costs)

    except FileNotFoundError:
        print("Error: data_input.csv not found!")
        print("Please make sure the CSV file is in the same directory.")
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()