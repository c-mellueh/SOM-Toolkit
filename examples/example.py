from SOMcreator import SOMProject, SOMClass, SOMPropertySet, SOMProperty
from SOMcreator.constants.value_constants import BOOLEAN, INTEGER, LIST

# Create a new Project
project = SOMProject(name="Example SOM")

# Create a new Identity Property
identifier_property = SOMProperty(name="identifier")
identifier_property.allowed_values = ["w.100.100"]

# Create a Object representing a custom Wall Definition
wall = SOMClass(
    name="MyWall", identifier_property=identifier_property, project=project
)

# Define the PropertySet in which the Identity Property will be placed
pset = SOMPropertySet(name="CustomMainPset")
pset.add_property(identifier_property)
wall.add_property_set(pset)

# Define a 2nd PropertySet
common_pset = SOMPropertySet(name="Pset_WallCommon")
common_pset.add_property(SOMProperty(name="LoadBearing", data_type=BOOLEAN))

# Define a Property with multiple allowed Values
fire_rating = SOMProperty(name="FireRating", data_type=INTEGER, value_type=LIST)
fire_rating.allowed_values = [30, 60, 90]
common_pset.add_property(fire_rating)

# Add PropertySet to Object
wall.add_property_set(common_pset)

# Export
project.export_bSDD("bsdd_example.json")
