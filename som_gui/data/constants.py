# Aggregation Window
SCALING_FACTOR = 0.1
BOX_MARGIN = 60
BOX_BOTTOM_DISTANCE = 40
ARROW_HEIGHT = 20
ARROW_WIDTH = ARROW_HEIGHT / 2
AGGREGATION = 1
INHERITANCE = 2
HEADER_HEIGHT = 35
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
PROJECT_PHASE_COUNT = 9
RANGE_STRINGS = ["Range", "range", "RANGE",GER_RANGE]
VALUE_TYPE_LOOKUP = {GER_VALUE: "Value", GER_FORMAT: "Format", GER_RANGE: "Range", GER_LIST: "List",
                     VALUE: "Value", FORMAT: "Format", RANGE: "Range", LIST: "List", }

GER_TYPES_LOOKUP = {VALUE: GER_VALUE, FORMAT: GER_FORMAT, RANGE: GER_RANGE, LIST: GER_LIST,}

PREDEFINED_PROPERTY_WINDOW_NAME = "Predefined Properties"

DATATYPE_NUMBER = "xs:double"
ICON_PATH = "icons/icon.ico"
INHERITED_TEXT = "Predefined Pset"

NODES = "Nodes"

# Mapping
SHARED_PARAMETERS = "SharedParameters"
FILETYPE = "SOM Project  (*.SOMjson);;all (*.*)"
