'use strict';
var BS_NAME = "BS Model [BS Model [Gruppierung]]";
var SOM_NAME = "SOM MaKa.SOMjson"
var PSET = "Allgemeine Eigenschaften"
var ATTRIB = "bauteilKlassifikation"

"+++++++++++++++++++++++++++++++++++++++++++++++++++++++"
const STRNG = "xs:string";
var model = getModel(BS_NAME); // BS Model mit BSNAME finden;
var path = desiteAPI.getProjectDirectory() + "/DB_scripts/" + SOM_NAME
var som_string = desiteAPI.readTextFileAsString(path)
var som = JSON.parse(som_string)
var attribute_dict = get_attributes(som, PSET, ATTRIB)
var children = desiteAPI.getContainedElements(model, 1)
for (child_index in children) {
    var child_id = children[child_index];
    var child_type = desiteAPI.getPropertyValue(child_id, "Type", "xs:string");

    if (child_type !== "typeBsGroup") { continue }
    check_layer(child_id)


}


function check_layer(layer_id) {
    n = desiteAPI.getPropertyValue(layer_id, "cpName", "xs:string")
    var layer_children = desiteAPI.getContainedElements(layer_id, 1)
    for (child_index in layer_children) {
        var child_id = layer_children[child_index];
        check_element(child_id);
    }

}

function check_element(element_id) {
    var bk = desiteAPI.getPropertyValue(element_id, PSET + ":" + ATTRIB, "xs:string")
    if (bk == undefined) { console.log("bauteilklassifikation existiert nicht") }
    else if (!(bk in attribute_dict)) {
        console.log("Bauteilklassifikation " + bk + " nicht im SOM")
    }
    else {
        var attribute_data = get_existing_attributes(element_id);
        for (var attribute_name in attribute_dict[bk]) {
            if (!(attribute_name in attribute_data)) {
                var value_type = attribute_dict[bk][attribute_name];
                if (value_type == "xs:string") {
                    desiteAPI.setPropertyValue(element_id, attribute_name, value_type, "fuellen!")
                }
                else if (value_type == "xs:integer" || value_type == "xs:int") {
                    desiteAPI.setPropertyValue(element_id, attribute_name, value_type, -1)
                }
                else if (value_type == "xs:double") {
                    desiteAPI.setPropertyValue(element_id, attribute_name, value_type, -1.0)
                }
                else if (value_type == "xs:boolean") {
                    console.log("BooleanAttribut " + attribute_name + " muss gefÃ¼llt werden")
                }
            }
        }
    }
    var children = desiteAPI.getContainedElements(element_id, 1)
    for (sub_index in children) {
        check_layer(children[sub_index]);
    }


}


function getModel(bsName) { //BS MODEL finden oder erstellen
    root_list = desiteAPI.getRootNodeListByDomain("building")
    for (i in root_list) {
        id = root_list[i]
        rootName = desiteAPI.getPropertyValue(id, "cpName", STRNG)
        if (rootName == bsName) {
            return id
        }

    }
    throw new Error("Modell konnte nicht gefunden werden")

}

function get_attributes(som, PSET, ATTRIB) {
    var attribute_dict = {}
    var objects = som["Objects"]
    for (var object_uuid in objects) {
        var bauteilklass = undefined
        var data_type_dict = {}

        var object = objects[object_uuid];
        for (var pset_uuid in object["PropertySets"]) {
            var property_set = object["PropertySets"][pset_uuid];
            if (property_set["name"] == PSET) {

                for (var attribute_uuid in property_set["Attributes"]) {
                    var attribute = property_set["Attributes"][attribute_uuid];
                    if (attribute["name"] == ATTRIB) { bauteilklass = attribute["Value"][0]; }

                }
            }
            for (var attribute_uuid in property_set["Attributes"]) {
                var attribute = property_set["Attributes"][attribute_uuid];
                var combi_name = property_set["name"] + ":" + attribute["name"]
                data_type_dict[combi_name] = attribute["data_type"]
            }
        }
        if (bauteilklass == undefined) {
            console.log("Bauteilklassifikation nicht gefunden")
        }
        else {
            attribute_dict[bauteilklass] = data_type_dict
        }
    }
    return attribute_dict;
}

function get_existing_attributes(element_id) {
    var attribute_data = desiteAPI.getPropertyValuesByObject(element_id)
    var attributes = {}
    for (var index in attribute_data) {
        var data = attribute_data[index]
        var n = data["Name"]
        var inherited = data["isInherited"]
        if (!inherited) { attributes[n] = data }

    }
    return attributes
}