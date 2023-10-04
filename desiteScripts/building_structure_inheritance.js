//Die Befüllung der Bauwerksstruktur ist Aufgabe des AN
//Dieses Script ist nur eine HILFESTELLUNG
//DER AG ÜBERNIMMT KEINE VERANTWORTUNG FÜR DIE Attribuierte STRUKTUR
//Die Bauwerksstruktur muss im Nachhinein haendisch auf Fehler Geprueft werden!
//Dieses Script schreibt alle Attribute, welche von Desite als "vererbt" (rot) dargestellt sind und überträgt sie als reale Attribute in die BS
//Dieses Script existiert nur weil es ein Bug bei Desite gibt und vererbte Attribute nicht übernommen werden!

//ACHTUNG: Wenn das Script einmal ausgeführt ist, kann man es nicht rückgängig machen!
//+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//++++++++++++++++++++++++++++++++++++++ Anpassen +++++++++++++++++++++++++++++++++++++++++
//+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

var BSNAME = "Test" //Name der Bauwerksstruktur (cpName)
var SOM_JSON_DATEI = "" //<-- Hier Pfad zu SOMjson einfügen Bsp: "C:/Users/ChristophMellueh/Desktop/test.SOMjson"
var PSET = "Allgemeine Eigenschaften"   //Identifikations Pset
var ATTRIB = "bauteilKlassifikation"    //Identifikations Attribut

//+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//+++++++++++++++++++ ALLES WAS FOLGT DARF NICHT ANGEPASST WERDEN! ++++++++++++++++++++++++
//+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

const STRNG = "xs:string";

var model = getModel(BSNAME)
var som = parseSOM(SOM_JSON_DATEI)

var main_attrib_name = PSET + ":" + ATTRIB

fill_bs(model, {})

function fill_bs(container, sad) {
    var children = desiteAPI.getContainedElements(container, 1)
    for (var child_index in children) {
        sub_attribute_dict = JSON.parse(JSON.stringify(sad))
        var child_id = children[child_index]
        console.log("Teste " + desiteAPI.getPropertyValue(child_id, "cpName", STRNG))

        var bk = desiteAPI.getPropertyValue(child_id, main_attrib_name, STRNG)
        if (bk == undefined) {
            console.log(ATTRIB + " vom Objekt " + child_id + " konnte nicht gefunden werden")
            continue
        }

        var required_attributes = som[bk]
        if (required_attributes == undefined) {
            console.log("Bauteilklasse " + bk + " ist nicht im SOM vorhanden")
            continue
        }

        for (var attribute_name in required_attributes) {
            if (attribute_name == main_attrib_name) {
                continue
            }
            var attribute_data_type = required_attributes[attribute_name]
            var vorgabe_value = sub_attribute_dict[attribute_name]
            var attribute_value = desiteAPI.getPropertyValue(child_id, attribute_name, attribute_data_type, false)

            if (attribute_value != undefined) {
                //console.log("Attribut "+attribute_name+" mit Wert "+attribute_value + " gefunden")
                sub_attribute_dict[attribute_name] = attribute_value
            }
            else if (vorgabe_value != undefined) {
                console.log("Attribut " + attribute_name + " mit Wert " + vorgabe_value + " wird geschrieben")
                desiteAPI.setPropertyValue(child_id, attribute_name, attribute_data_type, vorgabe_value)
            }
        }
        console.log("")
        fill_bs(child_id, sub_attribute_dict)

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

function parseSOM(path) {
    var som_string = desiteAPI.readTextFileAsString(path)
    var som = JSON.parse(som_string)
    var objects = som["Objects"]
    var data_dict = {}
    for (var obj_id in objects) {
        var obj_info_dict = {}
        var object = objects[obj_id]
        var ident_id = object["ident_attribute"]
        var property_set_dict = object["PropertySets"]

        for (var pset_id in property_set_dict) {
            var pset = property_set_dict[pset_id]
            var pset_name = pset["name"]
            var attribute_dict = pset["Attributes"]

            for (var attribute_id in attribute_dict) {
                var attribute = attribute_dict[attribute_id]
                attribute_name = attribute["name"]
                if (attribute_id == ident_id) {
                    var ident_value = attribute["Value"][0]
                }
                obj_info_dict[pset_name + ":" + attribute_name] = attribute["data_type"]
            }

        }
        data_dict[ident_value] = obj_info_dict
    }
    return data_dict
}

function remodel_attribute_dict(obj_array) {
    var new_array = {}
    for (var index in obj_array) {
        var old_item = obj_array[index]
        item_name = old_item["Name"]
        new_array[item_name] = old_item

    }
    return new_array
}