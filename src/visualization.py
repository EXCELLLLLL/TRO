"""
Visualization Module
PT. MediCare Indonesia - Transportation Problem

This module contains all visualization functions for the optimization results.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots


class TransportationVisualizer:
    """
    Visualization class for transportation optimization results
    """

    def __init__(self, optimizer):
        """
        Initialize visualizer

        Args:
            optimizer: TransportationOptimizer instance with solved solution
        """
        self.optimizer = optimizer
        self.setup_style()

    def setup_style(self):
        """Setup matplotlib style"""
        plt.style.use('seaborn-v0_8-darkgrid')
        sns.set_palette("husl")

        # Custom color palette
        self.colors = {
            'primary': '#2E86AB',
            'secondary': '#A23B72',
            'success': '#06A77D',
            'warning': '#F18F01',
            'danger': '#C73E1D',
            'info': '#6A4C93'
        }

    def plot_allocation_heatmap(self, save_path=None):
        """
        Create heatmap of allocation matrix

        Args:
            save_path: Path to save the figure
        """
        if not self.optimizer.solution:
            print("No solution available to visualize!")
            return

        # Create allocation matrix
        allocation_data = np.zeros((len(self.optimizer.warehouses),
                                    len(self.optimizer.destinations)))

        for i, w in enumerate(self.optimizer.warehouses):
            for j, d in enumerate(self.optimizer.destinations):
                value = self.optimizer.x[(w, d)].varValue if self.optimizer.x[(w, d)].varValue else 0
                allocation_data[i, j] = value

        # Create figure
        fig, ax = plt.subplots(figsize=(12, 8))

        # Create heatmap
        im = ax.imshow(allocation_data, cmap='YlOrRd', aspect='auto')

        # Set ticks
        ax.set_xticks(np.arange(len(self.optimizer.destinations)))
        ax.set_yticks(np.arange(len(self.optimizer.warehouses)))

        # Set tick labels
        ax.set_xticklabels([d.replace('_', '\n') for d in self.optimizer.destinations])
        ax.set_yticklabels(self.optimizer.warehouses)

        # Rotate the tick labels for better readability
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

        # Add text annotations
        for i in range(len(self.optimizer.warehouses)):
            for j in range(len(self.optimizer.destinations)):
                value = allocation_data[i, j]
                text = ax.text(j, i, f'{int(value)}' if value > 0 else '',
                               ha="center", va="center", color="black", fontsize=12, fontweight='bold')

        # Add colorbar
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('Units Shipped', rotation=270, labelpad=20, fontsize=12)

        ax.set_title('Allocation Heatmap: Units Shipped from Each Warehouse to Each Destination',
                     fontsize=14, fontweight='bold', pad=20)
        ax.set_xlabel('Destination', fontsize=12, fontweight='bold')
        ax.set_ylabel('Warehouse', fontsize=12, fontweight='bold')

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Heatmap saved to {save_path}")

        plt.show()

    def plot_utilization(self, save_path=None):
        """
        Create utilization chart for warehouses

        Args:
            save_path: Path to save the figure
        """
        if not self.optimizer.solution:
            print("No solution available to visualize!")
            return

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

        # Calculate utilization
        warehouses_list = []
        used_list = []
        unused_list = []
        utilization_pct = []

        for w in self.optimizer.warehouses:
            used = sum(self.optimizer.x[(w, d)].varValue if self.optimizer.x[(w, d)].varValue else 0
                       for d in self.optimizer.destinations)
            capacity = self.optimizer.supply[w]
            unused = capacity - used
            util_pct = (used / capacity) * 100

            warehouses_list.append(w)
            used_list.append(used)
            unused_list.append(unused)
            utilization_pct.append(util_pct)

        # Plot 1: Stacked bar chart
        x_pos = np.arange(len(warehouses_list))

        bars1 = ax1.bar(x_pos, used_list, label='Used', color=self.colors['success'], alpha=0.8)
        bars2 = ax1.bar(x_pos, unused_list, bottom=used_list, label='Unused',
                        color=self.colors['danger'], alpha=0.6)

        ax1.set_xticks(x_pos)
        ax1.set_xticklabels(warehouses_list)
        ax1.set_ylabel('Capacity (Units)', fontsize=11, fontweight='bold')
        ax1.set_title('Warehouse Capacity Utilization', fontsize=13, fontweight='bold')
        ax1.legend(loc='upper right')
        ax1.grid(axis='y', alpha=0.3)

        # Add percentage labels
        for i, (w, u, un, pct) in enumerate(zip(warehouses_list, used_list, unused_list, utilization_pct)):
            total = u + un
            ax1.text(i, total + 10, f'{pct:.1f}%',
                     ha='center', va='bottom', fontsize=11, fontweight='bold')

        # Plot 2: Horizontal bar chart with percentages
        colors_gradient = [self.colors['success'] if x >= 90 else
                           self.colors['warning'] if x >= 70 else
                           self.colors['danger'] for x in utilization_pct]

        y_pos = np.arange(len(warehouses_list))
        bars = ax2.barh(y_pos, utilization_pct, color=colors_gradient, alpha=0.8)

        ax2.set_yticks(y_pos)
        ax2.set_yticklabels(warehouses_list)
        ax2.set_xlabel('Utilization (%)', fontsize=11, fontweight='bold')
        ax2.set_title('Capacity Utilization Percentage', fontsize=13, fontweight='bold')
        ax2.set_xlim(0, 110)
        ax2.grid(axis='x', alpha=0.3)

        # Add value labels
        for i, (bar, pct) in enumerate(zip(bars, utilization_pct)):
            width = bar.get_width()
            ax2.text(width + 2, bar.get_y() + bar.get_height()/2,
                     f'{pct:.1f}%',
                     ha='left', va='center', fontsize=10, fontweight='bold')

        # Add reference line at 100%
        ax2.axvline(x=100, color='red', linestyle='--', linewidth=2, alpha=0.5, label='Full Capacity')
        ax2.legend()

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Utilization chart saved to {save_path}")

        plt.show()

    def plot_cost_breakdown(self, save_path=None):
        """
        Create cost breakdown visualization

        Args:
            save_path: Path to save the figure
        """
        if not self.optimizer.solution:
            print("No solution available to visualize!")
            return

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

        # Calculate cost by warehouse
        cost_by_warehouse = {}
        for w in self.optimizer.warehouses:
            cost = 0
            for d in self.optimizer.destinations:
                quantity = self.optimizer.x[(w, d)].varValue if self.optimizer.x[(w, d)].varValue else 0
                cost += self.optimizer.costs[(w, d)] * quantity
            cost_by_warehouse[w] = cost

        # Plot 1: Pie chart
        colors = [self.colors['primary'], self.colors['danger'],
                  self.colors['success'], self.colors['warning']]

        wedges, texts, autotexts = ax1.pie(cost_by_warehouse.values(),
                                           labels=cost_by_warehouse.keys(),
                                           autopct='%1.1f%%',
                                           colors=colors,
                                           startangle=90,
                                           explode=[0.05, 0, 0, 0])

        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(11)
            autotext.set_fontweight('bold')

        for text in texts:
            text.set_fontsize(12)
            text.set_fontweight('bold')

        ax1.set_title('Cost Distribution by Warehouse', fontsize=13, fontweight='bold')

        # Plot 2: Bar chart with details
        warehouses = list(cost_by_warehouse.keys())
        costs = list(cost_by_warehouse.values())

        bars = ax2.bar(warehouses, costs, color=colors, alpha=0.8)
        ax2.set_ylabel('Total Cost (Rp thousands)', fontsize=11, fontweight='bold')
        ax2.set_title('Total Cost per Warehouse', fontsize=13, fontweight='bold')
        ax2.grid(axis='y', alpha=0.3)

        # Add value labels on bars
        for bar, cost in zip(bars, costs):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                     f'Rp {cost:,.0f}k',
                     ha='center', va='bottom', fontsize=10, fontweight='bold')

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Cost breakdown saved to {save_path}")

        plt.show()

    def plot_network_flow(self, save_path=None):
        """
        Create network flow diagram using plotly

        Args:
            save_path: Path to save the figure
        """
        if not self.optimizer.solution:
            print("No solution available to visualize!")
            return

        # Prepare data for Sankey diagram
        labels = self.optimizer.warehouses + self.optimizer.destinations

        sources = []
        targets = []
        values = []
        colors_links = []

        for (w, d), quantity in self.optimizer.solution.items():
            source_idx = self.optimizer.warehouses.index(w)
            target_idx = len(self.optimizer.warehouses) + self.optimizer.destinations.index(d)

            sources.append(source_idx)
            targets.append(target_idx)
            values.append(quantity)

            # Color based on cost
            cost = self.optimizer.costs[(w, d)]
            if cost <= 7:
                colors_links.append('rgba(46, 134, 171, 0.4)')  # Blue - low cost
            elif cost <= 15:
                colors_links.append('rgba(241, 143, 1, 0.4)')   # Orange - medium cost
            else:
                colors_links.append('rgba(199, 62, 29, 0.4)')   # Red - high cost

        # Create Sankey diagram
        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=labels,
                color=["#2E86AB", "#2E86AB", "#2E86AB", "#2E86AB",
                       "#06A77D", "#06A77D", "#06A77D", "#06A77D", "#06A77D"]
            ),
            link=dict(
                source=sources,
                target=targets,
                value=values,
                color=colors_links
            )
        )])

        fig.update_layout(
            title="Transportation Network Flow Diagram",
            font=dict(size=12, family="Arial"),
            height=600
        )

        if save_path:
            fig.write_html(save_path)
            print(f"✓ Network flow diagram saved to {save_path}")

        fig.show()

    def plot_comparison_chart(self, results_dict: Dict[str, float], save_path=None):
        """
        Create comparison chart for different methods

        Args:
            results_dict: Dictionary with method names and their costs
            save_path: Path to save the figure
        """
        fig, ax = plt.subplots(figsize=(10, 6))

        methods = list(results_dict.keys())
        costs = list(results_dict.values())

        colors_bars = [self.colors['primary'] if i == costs.index(min(costs))
                       else self.colors['secondary'] for i in range(len(costs))]

        bars = ax.bar(methods, costs, color=colors_bars, alpha=0.8)

        ax.set_ylabel('Total Cost (Rp thousands)', fontsize=12, fontweight='bold')
        ax.set_title('Method Comparison: Total Cost', fontsize=14, fontweight='bold')
        ax.grid(axis='y', alpha=0.3)

        # Add value labels
        for bar, cost in zip(bars, costs):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'Rp {cost:,.0f}k',
                    ha='center', va='bottom', fontsize=11, fontweight='bold')

        # Add optimal marker
        min_cost = min(costs)
        for i, cost in enumerate(costs):
            if cost == min_cost:
                ax.text(i, cost + max(costs)*0.02, '★ OPTIMAL',
                        ha='center', va='bottom', fontsize=10,
                        color=self.colors['success'], fontweight='bold')

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Comparison chart saved to {save_path}")

        plt.show()

    def create_dashboard(self, save_path=None):
        """
        Create comprehensive dashboard with all visualizations

        Args:
            save_path: Path to save the figure
        """
        if not self.optimizer.solution:
            print("No solution available to visualize!")
            return

        fig = plt.figure(figsize=(20, 12))
        gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

        # 1. Allocation Heatmap
        ax1 = fig.add_subplot(gs[0:2, 0:2])
        allocation_data = np.zeros((len(self.optimizer.warehouses),
                                    len(self.optimizer.destinations)))

        for i, w in enumerate(self.optimizer.warehouses):
            for j, d in enumerate(self.optimizer.destinations):
                value = self.optimizer.x[(w, d)].varValue if self.optimizer.x[(w, d)].varValue else 0
                allocation_data[i, j] = value

        im = ax1.imshow(allocation_data, cmap='YlOrRd', aspect='auto')
        ax1.set_xticks(np.arange(len(self.optimizer.destinations)))
        ax1.set_yticks(np.arange(len(self.optimizer.warehouses)))
        ax1.set_xticklabels([d.replace('_', '\n') for d in self.optimizer.destinations], fontsize=9)
        ax1.set_yticklabels(self.optimizer.warehouses, fontsize=10)

        for i in range(len(self.optimizer.warehouses)):
            for j in range(len(self.optimizer.destinations)):
                value = allocation_data[i, j]
                if value > 0:
                    ax1.text(j, i, f'{int(value)}', ha="center", va="center",
                             color="black", fontsize=10, fontweight='bold')

        plt.colorbar(im, ax=ax1, label='Units')
        ax1.set_title('Allocation Matrix', fontsize=13, fontweight='bold')

        # 2. Utilization
        ax2 = fig.add_subplot(gs[0, 2])
        warehouses_list = []
        utilization_pct = []

        for w in self.optimizer.warehouses:
            used = sum(self.optimizer.x[(w, d)].varValue if self.optimizer.x[(w, d)].varValue else 0
                       for d in self.optimizer.destinations)
            capacity = self.optimizer.supply[w]
            util_pct = (used / capacity) * 100

            warehouses_list.append(w)
            utilization_pct.append(util_pct)

        colors_util = [self.colors['success'] if x >= 90 else
                       self.colors['warning'] if x >= 70 else
                       self.colors['danger'] for x in utilization_pct]

        ax2.barh(warehouses_list, utilization_pct, color=colors_util, alpha=0.8)
        ax2.set_xlabel('Utilization (%)', fontsize=10)
        ax2.set_title('Capacity Utilization', fontsize=12, fontweight='bold')
        ax2.grid(axis='x', alpha=0.3)

        for i, pct in enumerate(utilization_pct):
            ax2.text(pct + 2, i, f'{pct:.1f}%', va='center', fontsize=9, fontweight='bold')

        # 3. Cost Distribution
        ax3 = fig.add_subplot(gs[1, 2])
        cost_by_warehouse = {}
        for w in self.optimizer.warehouses:
            cost = 0
            for d in self.optimizer.destinations:
                quantity = self.optimizer.x[(w, d)].varValue if self.optimizer.x[(w, d)].varValue else 0
                cost += self.optimizer.costs[(w, d)] * quantity
            cost_by_warehouse[w] = cost

        colors_pie = [self.colors['primary'], self.colors['danger'],
                      self.colors['success'], self.colors['warning']]

        wedges, texts, autotexts = ax3.pie(cost_by_warehouse.values(),
                                           labels=cost_by_warehouse.keys(),
                                           autopct='%1.1f%%',
                                           colors=colors_pie,
                                           startangle=90)

        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(9)
            autotext.set_fontweight('bold')

        ax3.set_title('Cost Distribution', fontsize=12, fontweight='bold')

        # 4. Supply vs Demand
        ax4 = fig.add_subplot(gs[2, 0])
        total_supply = sum(self.optimizer.supply.values())
        total_demand = sum(self.optimizer.demand.values())
        total_used = sum(self.optimizer.x[(w, d)].varValue if self.optimizer.x[(w, d)].varValue else 0
                         for w in self.optimizer.warehouses for d in self.optimizer.destinations)

        categories = ['Total\nSupply', 'Total\nDemand', 'Actual\nUsed']
        values = [total_supply, total_demand, total_used]
        colors_bar = [self.colors['primary'], self.colors['danger'], self.colors['success']]

        bars = ax4.bar(categories, values, color=colors_bar, alpha=0.8)
        ax4.set_ylabel('Units', fontsize=10)
        ax4.set_title('Supply vs Demand', fontsize=12, fontweight='bold')
        ax4.grid(axis='y', alpha=0.3)

        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height + 10,
                     f'{int(value)}',
                     ha='center', va='bottom', fontsize=10, fontweight='bold')

        # 5. Top Routes by Cost
        ax5 = fig.add_subplot(gs[2, 1:])
        route_costs = []
        for (w, d), quantity in self.optimizer.solution.items():
            cost = self.optimizer.costs[(w, d)] * quantity
            route_costs.append({
                'Route': f"{w} → {d.replace('_', ' ')}",
                'Cost': cost,
                'Units': quantity
            })

        df_routes = pd.DataFrame(route_costs).sort_values('Cost', ascending=False).head(5)

        bars = ax5.barh(df_routes['Route'], df_routes['Cost'],
                        color=self.colors['secondary'], alpha=0.8)
        ax5.set_xlabel('Cost (Rp thousands)', fontsize=10)
        ax5.set_title('Top 5 Routes by Cost', fontsize=12, fontweight='bold')
        ax5.grid(axis='x', alpha=0.3)

        for i, (bar, cost) in enumerate(zip(bars, df_routes['Cost'])):
            width = bar.get_width()
            ax5.text(width + max(df_routes['Cost'])*0.02, bar.get_y() + bar.get_height()/2,
                     f'Rp {cost:,.0f}k',
                     ha='left', va='center', fontsize=9, fontweight='bold')

        # Add main title
        total_cost = sum(self.optimizer.costs[(w, d)] * self.optimizer.x[(w, d)].varValue
                         for w in self.optimizer.warehouses
                         for d in self.optimizer.destinations
                         if self.optimizer.x[(w, d)].varValue)

        fig.suptitle(f'Transportation Optimization Dashboard - Total Cost: Rp {total_cost:,.0f},000',
                     fontsize=16, fontweight='bold', y=0.98)

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Dashboard saved to {save_path}")

        plt.show()


# Example usage
if __name__ == "__main__":
    from model_formulation import TransportationData
    from python_solver import TransportationOptimizer

    # Solve the problem first
    optimizer = TransportationOptimizer()
    optimizer.build_model()
    optimizer.solve()

    # Create visualizer
    viz = TransportationVisualizer(optimizer)

    # Generate all visualizations
    viz.plot_allocation_heatmap('allocation_heatmap.png')
    viz.plot_utilization('utilization_chart.png')
    viz.plot_cost_breakdown('cost_breakdown.png')
    viz.plot_network_flow('network_flow.html')
    viz.create_dashboard('optimization_dashboard.png')

    print("\n✓ All visualizations created successfully!")