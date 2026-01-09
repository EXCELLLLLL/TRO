"""
Model Formulation Module
PT. MediCare Indonesia - Transportation Problem

This module contains the data structures and model formulation
for the transportation optimization problem.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple


class TransportationData:
    """
    Data structure for transportation problem
    """

    def __init__(self):
        """Initialize transportation problem data"""

        # Warehouse (Supply) data
        self.warehouses = ['Jakarta', 'Tangerang', 'Bekasi', 'Bogor']

        self.supply = {
            'Jakarta': 350,
            'Tangerang': 400,
            'Bekasi': 300,
            'Bogor': 250
        }

        # Destination (Demand) data
        self.destinations = [
            'RS_Jakarta_Pusat',
            'RS_Tangerang',
            'RS_Bekasi',
            'Apotek_Depok',
            'RS_Bogor'
        ]

        self.demand = {
            'RS_Jakarta_Pusat': 250,
            'RS_Tangerang': 300,
            'RS_Bekasi': 200,
            'Apotek_Depok': 280,
            'RS_Bogor': 220
        }

        # Transportation cost matrix (in thousand Rupiah per unit)
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

    def get_total_supply(self) -> int:
        """Calculate total supply capacity"""
        return sum(self.supply.values())

    def get_total_demand(self) -> int:
        """Calculate total demand"""
        return sum(self.demand.values())

    def is_balanced(self) -> bool:
        """Check if the problem is balanced"""
        return self.get_total_supply() == self.get_total_demand()

    def get_cost_matrix(self) -> pd.DataFrame:
        """
        Get cost matrix as DataFrame

        Returns:
            pd.DataFrame: Cost matrix with warehouses as rows and destinations as columns
        """
        data = []
        for warehouse in self.warehouses:
            row = {'Warehouse': warehouse}
            for destination in self.destinations:
                row[destination] = self.costs.get((warehouse, destination), np.inf)
            data.append(row)

        df = pd.DataFrame(data)
        df.set_index('Warehouse', inplace=True)
        return df

    def get_supply_dataframe(self) -> pd.DataFrame:
        """Get supply data as DataFrame"""
        return pd.DataFrame(list(self.supply.items()),
                            columns=['Warehouse', 'Capacity'])

    def get_demand_dataframe(self) -> pd.DataFrame:
        """Get demand data as DataFrame"""
        return pd.DataFrame(list(self.demand.items()),
                            columns=['Destination', 'Demand'])

    def print_problem_summary(self):
        """Print summary of the transportation problem"""
        print("="*70)
        print("TRANSPORTATION PROBLEM - PT. MEDICARE INDONESIA")
        print("="*70)

        print("\n📦 WAREHOUSES (SUPPLY)")
        print("-"*70)
        df_supply = self.get_supply_dataframe()
        print(df_supply.to_string(index=False))
        print(f"\nTotal Supply: {self.get_total_supply()} units")

        print("\n📍 DESTINATIONS (DEMAND)")
        print("-"*70)
        df_demand = self.get_demand_dataframe()
        print(df_demand.to_string(index=False))
        print(f"\nTotal Demand: {self.get_total_demand()} units")

        print("\n💰 TRANSPORTATION COSTS (Rp thousands per unit)")
        print("-"*70)
        df_costs = self.get_cost_matrix()
        print(df_costs.to_string())

        print(f"\n{'='*70}")
        total_supply = self.get_total_supply()
        total_demand = self.get_total_demand()

        if self.is_balanced():
            print("✅ Problem is BALANCED")
            print(f"   Total Supply = Total Demand = {total_supply} units")
        else:
            diff = total_supply - total_demand
            if diff > 0:
                print(f"⚠️  Problem is UNBALANCED (Surplus: {diff} units)")
                print(f"   Total Supply ({total_supply}) > Total Demand ({total_demand})")
                print("   → Need to add dummy destination")
            else:
                print(f"⚠️  Problem is UNBALANCED (Shortage: {-diff} units)")
                print(f"   Total Supply ({total_supply}) < Total Demand ({total_demand})")
                print("   → Need to add dummy warehouse")
        print("="*70)

    def export_to_excel(self, filename='transportation_data.xlsx'):
        """
        Export all data to Excel file

        Args:
            filename (str): Output filename
        """
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # Sheet 1: Cost Matrix
            df_costs = self.get_cost_matrix()
            df_costs.to_excel(writer, sheet_name='Cost Matrix')

            # Sheet 2: Supply
            df_supply = self.get_supply_dataframe()
            df_supply.to_excel(writer, sheet_name='Supply', index=False)

            # Sheet 3: Demand
            df_demand = self.get_demand_dataframe()
            df_demand.to_excel(writer, sheet_name='Demand', index=False)

            # Sheet 4: Summary
            summary_data = {
                'Metric': [
                    'Total Warehouses',
                    'Total Destinations',
                    'Total Supply (units)',
                    'Total Demand (units)',
                    'Balance Status',
                    'Difference (units)'
                ],
                'Value': [
                    len(self.warehouses),
                    len(self.destinations),
                    self.get_total_supply(),
                    self.get_total_demand(),
                    'Balanced' if self.is_balanced() else 'Unbalanced',
                    self.get_total_supply() - self.get_total_demand()
                ]
            }
            df_summary = pd.DataFrame(summary_data)
            df_summary.to_excel(writer, sheet_name='Summary', index=False)

        print(f"\n✓ Data exported to '{filename}'")

    def validate_data(self) -> Tuple[bool, List[str]]:
        """
        Validate the transportation data

        Returns:
            Tuple[bool, List[str]]: (is_valid, list of error messages)
        """
        errors = []

        # Check if all supplies are positive
        for warehouse, capacity in self.supply.items():
            if capacity <= 0:
                errors.append(f"Supply for {warehouse} must be positive")

        # Check if all demands are positive
        for destination, demand in self.demand.items():
            if demand <= 0:
                errors.append(f"Demand for {destination} must be positive")

        # Check if all costs are non-negative
        for (warehouse, destination), cost in self.costs.items():
            if cost < 0:
                errors.append(f"Cost from {warehouse} to {destination} cannot be negative")

        # Check if all routes are defined
        for warehouse in self.warehouses:
            for destination in self.destinations:
                if (warehouse, destination) not in self.costs:
                    errors.append(f"Cost not defined for route {warehouse} → {destination}")

        is_valid = len(errors) == 0
        return is_valid, errors


class ModelFormulation:
    """
    Mathematical formulation of the transportation problem
    """

    def __init__(self, data: TransportationData):
        """
        Initialize model formulation

        Args:
            data: TransportationData object
        """
        self.data = data

    def print_mathematical_formulation(self):
        """Print the mathematical formulation"""
        print("\n" + "="*70)
        print("MATHEMATICAL FORMULATION")
        print("="*70)

        print("\n📊 DECISION VARIABLES:")
        print("-"*70)
        print("x_ij = Amount shipped from warehouse i to destination j")
        print(f"where i ∈ {{{', '.join(self.data.warehouses)}}}")
        print(f"      j ∈ {{{', '.join([d.replace('_', ' ') for d in self.data.destinations])}}}")

        print("\n🎯 OBJECTIVE FUNCTION:")
        print("-"*70)
        print("Minimize Z = Σ Σ c_ij × x_ij")
        print("             i j")
        print("\nExpanded form:")

        obj_terms = []
        for i, warehouse in enumerate(self.data.warehouses, 1):
            for j, destination in enumerate(self.data.destinations, 1):
                cost = self.data.costs[(warehouse, destination)]
                obj_terms.append(f"{cost}x_{i}{j}")

        # Print in chunks of 4 terms per line
        chunk_size = 4
        for i in range(0, len(obj_terms), chunk_size):
            chunk = obj_terms[i:i+chunk_size]
            if i == 0:
                print("Z = " + " + ".join(chunk))
            else:
                print("    + " + " + ".join(chunk))

        print("\n📐 CONSTRAINTS:")
        print("-"*70)

        print("\nA. Supply Constraints (Capacity):")
        for i, warehouse in enumerate(self.data.warehouses, 1):
            capacity = self.data.supply[warehouse]
            terms = [f"x_{i}{j}" for j in range(1, len(self.data.destinations) + 1)]
            print(f"   {' + '.join(terms)} ≤ {capacity}  ({warehouse})")

        print("\nB. Demand Constraints (Requirements):")
        for j, destination in enumerate(self.data.destinations, 1):
            demand = self.data.demand[destination]
            terms = [f"x_{i}{j}" for i in range(1, len(self.data.warehouses) + 1)]
            dest_name = destination.replace('_', ' ')
            print(f"   {' + '.join(terms)} = {demand}  ({dest_name})")

        print("\nC. Non-negativity Constraints:")
        print("   x_ij ≥ 0, for all i and j")

        print("\n" + "="*70)
        print("PROBLEM STATISTICS")
        print("="*70)
        print(f"Number of Variables: {len(self.data.warehouses) * len(self.data.destinations)}")
        print(f"Number of Constraints: {len(self.data.warehouses) + len(self.data.destinations)}")
        print(f"  - Supply Constraints: {len(self.data.warehouses)}")
        print(f"  - Demand Constraints: {len(self.data.destinations)}")
        print("="*70)

    def get_latex_formulation(self) -> str:
        """
        Get LaTeX formatted mathematical formulation

        Returns:
            str: LaTeX code for the formulation
        """
        latex = r"""
\begin{align*}
\text{Minimize: } & Z = \sum_{i=1}^{m} \sum_{j=1}^{n} c_{ij} x_{ij} \\
\text{Subject to: } \\
& \sum_{j=1}^{n} x_{ij} \leq s_i, \quad \forall i = 1, 2, \ldots, m \\
& \sum_{i=1}^{m} x_{ij} = d_j, \quad \forall j = 1, 2, \ldots, n \\
& x_{ij} \geq 0, \quad \forall i, j
\end{align*}
"""
        return latex


# Example usage
if __name__ == "__main__":
    # Create data instance
    data = TransportationData()

    # Print problem summary
    data.print_problem_summary()

    # Validate data
    is_valid, errors = data.validate_data()
    print(f"\n{'='*70}")
    if is_valid:
        print("✅ Data validation PASSED")
    else:
        print("❌ Data validation FAILED")
        for error in errors:
            print(f"   - {error}")
    print("="*70)

    # Print mathematical formulation
    formulation = ModelFormulation(data)
    formulation.print_mathematical_formulation()

    # Export data to Excel
    data.export_to_excel()

    print("\n✓ Model formulation complete!")