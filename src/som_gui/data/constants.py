# Aggregation Window
SCALING_FACTOR = 0.1
BOX_WIDTH = 300
BOX_HEIGHT = 200
BOX_MARGIN = 60
BOX_BOTTOM_DISTANCE = 40
ARROW_HEIGHT = 20
ARROW_WIDTH = ARROW_HEIGHT / 2
AGGREGATION = 1
INHERITANCE = 2
HEADER_HEIGHT = 25
SCENE_MARGIN = 200

AGGREGATION_SCENES = "AggregationScenes"

VALUE = "Value"
FORMAT = "Format"
RANGE = "Range"
LIST = "List"

GER_VALUE = "Wert"
GER_FORMAT = "Formatvorgabe"
GER_RANGE = "Wertebereich"
GER_LIST = "Liste"

XS_STRING = "xs:string"
XS_DOUBLE = "xs:double"
XS_BOOLEAN = "xs:boolean"
XS_INT = "xs:int"
XS_LONG = "xs:long"

DATA_TYPES = [XS_STRING,XS_LONG,XS_INT,XS_DOUBLE,XS_BOOLEAN]

RANGE_STRINGS = ["Range", "range", "RANGE",GER_RANGE]
VALUE_TYPE_LOOKUP = {GER_VALUE: "Value", GER_FORMAT: "Format", GER_RANGE: "Range", GER_LIST: "List",
                     VALUE: "Value", FORMAT: "Format", RANGE: "Range", LIST: "List", }

GER_TYPES_LOOKUP = {VALUE: GER_VALUE, FORMAT: GER_FORMAT, RANGE: GER_RANGE, LIST: GER_LIST,}

PREDEFINED_PROPERTY_WINDOW_NAME = "Predefined Properties"

DATATYPE_NUMBER = "xs:double"
ICON_PATH = "icons/icon.ico"
LINK_ICON_PATH = "icons/link.png"

DATA_POS = 1
FILEPATH_JS = "js_templates"

IGNORE_PSET = "IFC"
INHERITED_TEXT = "Predefined Pset"

# xml export
PREDEFINED_PSETS = "PredefinedPropertySets"
PREDEFINED_PSET = "PredefinedPropertySet"
PROPERTY_SET = "PropertySet"
PROPERTY_SETS = "PropertySets"

ATTRIBUTE = "Attribute"
ATTRIBUTES = "Attributes"
OBJECT = "Object"
OBJECTS = "Objects"
AGGREGATE = "Aggregate"
NAME = "name"
IDENTIFIER = "identifer"
PARENT = "parent"
NONE = "None"
DATA_TYPE = "data_type"
VALUE_TYPE = "value_type"
IS_IDENTIFIER = "is_identifier"
CHILD_INHERITS_VALUE = "child_inherits_value"
IS_CONCEPT = "is_concept"
SCRIPT = "Script"
SCRIPTS = "Scripts"
PROJECT = "Project"
VERSION = "version"
AGGREGATES_TO = "aggregates_to"
AUTHOR = "author"
X_POS = "x_pos"
Y_POS = "y_pos"
IS_ROOT = "root"
CONNECTION = "connection"
NODE = "Node"
NODES = "Nodes"
IFC_MAPPINGS = "IfcMappings"
IFC_MAPPING = "IfcMapping"

# Mapping
SHARED_PARAMETERS = "SharedParameters"
REVIT_MAPPING = "revit_mapping"
FILETYPE = "SOM Project  (*.SOMjson);;all (*.*)"
