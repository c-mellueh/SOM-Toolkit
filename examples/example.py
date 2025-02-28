from SOMcreator import Project, SOMClass, PropertySet, Attribute
from SOMcreator.constants.value_constants import BOOLEAN, INTEGER, LIST

# Create a new Project
project = Project(name="Example SOM")

# Create a new Identity Attribute
identifier_attribute = Attribute(name="identifier")
identifier_attribute.value = ["w.100.100"]

# Create a Object representing a custom Wall Definition
wall = SOMClass(name="MyWall", ident_attrib=identifier_attribute, project=project)

# Define the PropertySet in which the Identity Attribute will be placed
pset = PropertySet(name="CustomMainPset")
pset.add_attribute(identifier_attribute)
wall.add_property_set(pset)

# Define a 2nd PropertySet
common_pset = PropertySet(name="Pset_WallCommon")
common_pset.add_attribute(Attribute(name="LoadBearing", data_type=BOOLEAN))

# Define a Attribute with multiple allowed Values
fire_rating = Attribute(name="FireRating", data_type=INTEGER, value_type=LIST)
fire_rating.value = [30, 60, 90]
common_pset.add_attribute(fire_rating)

# Add PropertySet to Object
wall.add_property_set(common_pset)

# Export
project.export_bSDD("bsdd_example.json")
