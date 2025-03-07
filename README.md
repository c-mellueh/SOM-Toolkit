# SOM-Toolkit

The **SOM-Toolkit** is an open-source project designed for the creation, management, and modification of Semantic Object Models (SOMs) in the context of Building Information Modeling (BIM). It provides both a powerful **Python library (SOMcreator)** for developers and a user-friendly **GUI (som_gui)** built with PySide6, catering to a wide range of users and use cases.

---

## Overview

Semantic Object Models (SOMs) are crucial for defining the semantics of objects in BIM workflows. The SOM-Toolkit streamlines the process of defining objects, property sets, and properties, making it easier to adhere to standards like buildingSMART Data Dictionary (bSDD) and Information Delivery Specification (IDS).

---

## Components

### 1. **SOMcreator**
The `SOMcreator` library is the backbone of the SOM-Toolkit, offering an object-oriented data structure for managing the core components of Semantic Object Models.

**Key Features:**
- **Projects and Objects**: Define projects containing objects with detailed metadata.
- **Property Sets and properties**: Link objects to property sets and their properties to enhance semantic modeling.
- **Export Formats**:
  - **bSDD**: Export models to the buildingSMART Data Dictionary format for interoperability.
  - **IDS**: Export to the Information Delivery Specification format for compliance with BIM execution plans.
- **Programmatic Flexibility**: Designed for developers to integrate directly into Python projects.

**Core Classes and Functions:**
- `SOMProject`: Represents a project containing multiple objects and their relationships.
- `SOMClass`: Defines an individual classes within the project.
- `SOMPropertySet` and `SOMProperty`: Define and attach detailed semantic data to classes.

---

### 2. **som_gui**
The `som_gui` is a graphical user interface for non-programmers or users seeking an interactive way to work with Semantic Object Models.

**Key Features:**
- **Interactive Editing**: Create, view, and modify objects, property sets, and properties.
- **Project Management**: Easily manage multiple projects and export data in the desired format.
- **Responsive Interface**: Built with PySide6, offering a modern and intuitive design.

---

## Installation

### Prerequisites
- **Python 3.8 or higher**: Ensure Python is installed on your system. You can download it from [python.org](https://www.python.org/).
- **Pip**: Ensure pip is available for managing dependencies.

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/SOM-Toolkit.git
   cd SOM-Toolkit
   
2. Install dependencies
   ```bash
   pip install -r requirements.txt

3. Test the installation:
* for SOMcreator: Run the example script in examples/.
* For som_gui: Start the GUI with:
   ```bash
   python -m som_gui

# Usage

## Using SOMcreator
Import the library in your Python project to define and manage Semantic Object Models programmatically.
Example Code:
   ```python
from SOMcreator import SOMProject, SOMClass, SOMProperty, SOMPropertySet
from SOMcreator.constants.value_constants import BOOLEAN, INTEGER, LIST

# Create a new Project
project = SOMProject(name="Example SOM")

# Create a new Identity Attribute
ident_property = SOMProperty(name="identifier")
ident_property.allowed_values = ["w.100.100"]

# Create a Object representing a custom Wall Definition
wall = SOMClass(name="MyWall", identifier_property=ident_property, project=project)

# Define the PropertySet in which the Identity Attribute will be placed
pset = SOMPropertySet(name="CustomMainPset")
pset.add_property(ident_property)
wall.add_property_set(pset)

# Define a 2nd PropertySet
common_pset = SOMPropertySet(name="Pset_WallCommon")
common_pset.add_property(SOMProperty(name="LoadBearing", data_type=BOOLEAN))

# Define a Attribute with multiple allowed Values
fire_rating = SOMProperty(name="FireRating", data_type=INTEGER, value_type=LIST)
fire_rating.allowed_values = [30, 60, 90]
common_pset.add_property(fire_rating)

# Add PropertySet to Object
wall.add_property_set(common_pset)

# Export
project.export_bSDD("examples/bsdd_example.json")
```
## Using som_gui
The `som_gui` provides a visual way to interact with Semantic Object Models.

**Running the GUI**:
   ```bash
   python -m som_gui
```
Features:
* **Create a Project**: Start a new project and define objects, properties, and properties interactively.
* **Modify Existing Data**: Import existing models, modify data, and re-export.
* **Export Options**: Save your project in bSDD or IDS formats for interoperability with other BIM tools.
* **IFC-Modelcheck**: Check IFC-Files against specified SOM

# Contribution Guide
We welcome contributions to the SOM-Toolkit! Here’s how you can get involved:

1. Fork the repository:
   * Visit the SOM-Toolkit GitHub page.
   * Click on the "Fork" button to create your own copy.
2. Create a feature branch:
   * Clone your fork locally and create a new branch for your feature:
```bash
git checkout -b feature/your-feature-name
```
3. Make changes and test:
   * Develop your feature and test it thoroughly.
4. Submit a pull request:
   * Push your changes to your fork and open a pull request in the main repository.
