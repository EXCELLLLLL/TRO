"""
Master Setup Script
PT. MediCare Indonesia - Transportation Optimization Project

This script sets up the entire project:
1. Creates all necessary directories
2. Generates all data files
3. Creates __init__.py files
4. Validates setup
5. Generates sample outputs

Run this FIRST after cloning/copying the project files.

Usage:
    python setup_project.py
"""

import os
import sys
import shutil
from pathlib import Path


class ProjectSetup:
    """Complete project setup and initialization"""

    def __init__(self):
        """Initialize setup"""
        self.project_root = Path(__file__).parent.parent
        self.required_dirs = [
            'data',
            'src',
            'notebooks',
            'results/UTS',
            'results/UAS/visualizations',
            'docs',
            'presentation'
        ]

        self.setup_log = []

    def log(self, message, level='INFO'):
        """Log setup progress"""
        prefix = {
            'INFO': '✓',
            'WARN': '⚠',
            'ERROR': '✗',
            'STEP': '→'
        }.get(level, '•')

        log_message = f"{prefix} {message}"
        print(log_message)
        self.setup_log.append(log_message)

    def create_directories(self):
        """Create all required directories"""
        self.log("Creating project directories...", 'STEP')

        for dir_path in self.required_dirs:
            full_path = self.project_root / dir_path
            if not full_path.exists():
                full_path.mkdir(parents=True, exist_ok=True)
                self.log(f"Created: {dir_path}")
            else:
                self.log(f"Already exists: {dir_path}", 'WARN')

        print()

    def create_init_files(self):
        """Create __init__.py files for Python packages"""
        self.log("Creating __init__.py files...", 'STEP')

        # Create __init__.py in src/
        init_file = self.project_root / 'src' / '__init__.py'
        if not init_file.exists():
            init_file.write_text('"""PT. MediCare Indonesia - Transportation Optimization"""\n')
            self.log("Created: src/__init__.py")
        else:
            self.log("Already exists: src/__init__.py", 'WARN')

        print()

    def generate_data_files(self):
        """Generate all data files"""
        self.log("Generating data files...", 'STEP')

        try:
            # Import and run data generator
            sys.path.insert(0, str(self.project_root / 'src'))
            from generate_data_files import DataGenerator

            generator = DataGenerator()
            generator.generate_all_files()

            self.log("All data files generated successfully")
        except Exception as e:
            self.log(f"Error generating data files: {str(e)}", 'ERROR')
            self.log("Please run generate_data_files.py manually", 'WARN')

        print()

    def create_gitignore(self):
        """Create .gitignore if not exists"""
        self.log("Checking .gitignore...", 'STEP')

        gitignore_path = self.project_root / '.gitignore'

        if not gitignore_path.exists():
            gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
.venv

# Jupyter
.ipynb_checkpoints

# IDEs
.vscode/
.idea/
*.swp
.DS_Store

# Excel
~$*.xlsx
~$*.xls

# Results (optional)
# results/
# *.png

# OS
Thumbs.db
"""
            gitignore_path.write_text(gitignore_content)
            self.log("Created: .gitignore")
        else:
            self.log("Already exists: .gitignore", 'WARN')

        print()

    def create_requirements_txt(self):
        """Create requirements.txt if not exists"""
        self.log("Checking requirements.txt...", 'STEP')

        req_path = self.project_root / 'requirements.txt'

        if not req_path.exists():
            requirements = """# Transportation Optimization Project Dependencies
# Python 3.8+

# Core Optimization
pulp>=2.7.0
scipy>=1.10.0

# Data Processing
pandas>=1.5.0
numpy>=1.23.0
openpyxl>=3.1.0

# Visualization
matplotlib>=3.6.0
seaborn>=0.12.0
plotly>=5.14.0

# Jupyter
jupyter>=1.0.0
notebook>=6.5.0
ipykernel>=6.20.0

# Additional
xlsxwriter>=3.0.0
tabulate>=0.9.0
"""
            req_path.write_text(requirements)
            self.log("Created: requirements.txt")
        else:
            self.log("Already exists: requirements.txt", 'WARN')

        print()

    def validate_setup(self):
        """Validate that setup is complete"""
        self.log("Validating setup...", 'STEP')

        all_valid = True

        # Check directories
        for dir_path in self.required_dirs:
            full_path = self.project_root / dir_path
            if not full_path.exists():
                self.log(f"Missing directory: {dir_path}", 'ERROR')
                all_valid = False

        # Check data files
        data_files = [
            'data/warehouse_capacity.csv',
            'data/destination_demand.csv',
            'data/transportation_cost.csv',
            'data/input_data.xlsx'
        ]

        for file_path in data_files:
            full_path = self.project_root / file_path
            if not full_path.exists():
                self.log(f"Missing data file: {file_path}", 'WARN')

        # Check source files
        src_files = [
            'src/__init__.py',
            'src/model_formulation.py',
            'src/python_solver.py',
            'src/visualization.py',
            'src/sensitivity_analysis.py',
            'src/excel_solver.py',
            'src/generate_data_files.py'
        ]

        for file_path in src_files:
            full_path = self.project_root / file_path
            if not full_path.exists():
                self.log(f"Missing source file: {file_path}", 'WARN')

        print()

        if all_valid:
            self.log("Setup validation passed!", 'INFO')
        else:
            self.log("Some issues found - please check above", 'WARN')

        return all_valid

    def create_readme(self):
        """Create a quick start README if not exists"""
        self.log("Checking README...", 'STEP')

        readme_path = self.project_root / 'QUICKSTART.md'

        if not readme_path.exists():
            quickstart = """# Quick Start Guide
## Transportation Optimization Project

### 1. Setup Environment

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\\Scripts\\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Verify Data Files

Check that these files exist in `data/`:
- warehouse_capacity.csv
- destination_demand.csv
- transportation_cost.csv
- input_data.xlsx

### 3. Run Notebooks

```bash
cd notebooks
jupyter notebook
```

Run in order:
1. `01_data_exploration.ipynb`
2. `02_manual_solution.ipynb`
3. `04_python_optimization.ipynb`
4. `05_sensitivity_analysis.ipynb`

### 4. Excel Solver (Manual)

```bash
cd src
python excel_solver.py
```

Then open the generated template in Excel and run Solver.

### 5. Generate Reports

After running all notebooks, compile your final report using the template in `docs/final_report_template.md`.

---

For detailed instructions, see `README.md`.
"""
            readme_path.write_text(quickstart)
            self.log("Created: QUICKSTART.md")

        print()

    def display_summary(self):
        """Display setup summary"""
        print()
        print("="*70)
        print("SETUP SUMMARY")
        print("="*70)
        print()

        print("Project Structure Created:")
        for dir_path in self.required_dirs:
            full_path = self.project_root / dir_path
            status = "✓" if full_path.exists() else "✗"
            print(f"  {status} {dir_path}/")

        print()
        print("Data Files:")
        data_files = [
            'warehouse_capacity.csv',
            'destination_demand.csv',
            'transportation_cost.csv',
            'input_data.xlsx'
        ]

        for filename in data_files:
            full_path = self.project_root / 'data' / filename
            status = "✓" if full_path.exists() else "✗"
            print(f"  {status} data/{filename}")

        print()
        print("="*70)
        print("NEXT STEPS")
        print("="*70)
        print()
        print("1. Install dependencies:")
        print("   pip install -r requirements.txt")
        print()
        print("2. Run notebooks in order:")
        print("   cd notebooks")
        print("   jupyter notebook")
        print()
        print("3. Start with: 01_data_exploration.ipynb")
        print()
        print("4. For detailed guide, see: QUICKSTART.md")
        print()
        print("="*70)

    def run_setup(self):
        """Run complete setup"""
        print("="*70)
        print("PROJECT SETUP - PT. MEDICARE INDONESIA")
        print("Transportation Optimization Project")
        print("="*70)
        print()

        # Run setup steps
        self.create_directories()
        self.create_init_files()
        self.create_gitignore()
        self.create_requirements_txt()
        self.generate_data_files()
        self.create_readme()
        self.validate_setup()

        # Display summary
        self.display_summary()

        print()
        print("✓ Setup complete!")
        print()

        # Save setup log
        log_file = self.project_root / 'setup.log'
        log_file.write_text('\n'.join(self.setup_log))
        print(f"Setup log saved to: setup.log")


def main():
    """Main execution"""
    try:
        setup = ProjectSetup()
        setup.run_setup()
        return 0
    except Exception as e:
        print(f"\n✗ Setup failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())