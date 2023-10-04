from SOMcreator import value_constants

# Aggregation Window
SCALING_FACTOR = 0.1
BOX_MARGIN = 60
BOX_BOTTOM_DISTANCE = 40
ARROW_HEIGHT = 20
ARROW_WIDTH = ARROW_HEIGHT / 2
HEADER_HEIGHT = 35
SCENE_MARGIN = 200
PREDEFINED_PROPERTY_WINDOW_NAME = "Vordefinierte PropertySets"

NODES = "Nodes"

AGGREGATION_SCENES = "AggregationScenes"

GER_VALUE = "Wert"
GER_FORMAT = "Formatvorgabe"
GER_RANGE = "Wertebereich"
GER_LIST = "Liste"

RANGE_STRINGS = ["Range", "range", "RANGE", GER_RANGE]

GER_TYPES_LOOKUP = {value_constants.VALUE: GER_VALUE,
                    value_constants.FORMAT: GER_FORMAT,
                    value_constants.RANGE: GER_RANGE,
                    value_constants.LIST: GER_LIST, }
EN_TYPE_LOOKUP = {value: key for key, value in GER_TYPES_LOOKUP.items()}


