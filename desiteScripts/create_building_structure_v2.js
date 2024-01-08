//Die Erstellung der Bauwerksstruktur ist Aufgabe des AN
//Dieses Script ist nur eine HILFESTELLUNG
//DER AG ÜBERNIMMT KEINE VERANTWORTUNG FÜR DIE ERSTELLTE STRUKTUR
//Die Bauwerksstruktur muss im Nachhinein haendisch auf Fehler Geprueft werden!

//+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//++++++++++++++++++++++++++++++++++++++ Anpassen +++++++++++++++++++++++++++++++++++++++++
//+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

// Attribut, dass zu Klassifizierung genutzt wird
var KLASSIFIKATION = "Allgemeine Eigenschaften:bauteilKlassifikation";

//Attribut, dass zu Gruppierung genutzt wird
var GRUPPIERUNGSATTRIB = "Gruppierung:idGruppe"

//Name der Bauwerksstruktur
var BSNAME = "Bauwerksstruktur"

//Ablageorrt der Abkuerzungsdatei
var SOM_JSON_DATEI = "" //<-- Hier Pfad zu SOMjson einfügen Bsp: "C:/Users/ChristophMellueh/Desktop/test.SOMjson"
//Trennzeichen bei mehrfacher Gruppenzugehörigkeit
var GRUPPENTRENNER = ";"

//Kontrolliert, ob Gruppenbezeichnung den Vorgaben entsprechen
var GRUPPENKONTROLLE = true //  true/false

//+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//+++++++++++++++++++ ALLES WAS FOLGT DARF NICHT ANGEPASST WERDEN! ++++++++++++++++++++++++
//+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

const STRNG = "xs:string";
const t1 = '<section name="';
const t2 = '" type="typeBsGroup"/>';
var timestamp = getDate()
var modelId = desiteAPI.createModel(timestamp + " GroupIssues", true, domain = "issues")

main()

function main() {
    var abkuerzungs_dict = getAbkuerzung(SOM_JSON_DATEI)
    var bauwerksstruktur = getBS(abkuerzungs_dict); // gewollte Bauwerksstruktur als JSON einlesen
    var model = getModel(BSNAME); // BS Model mit BSNAME finden
    buildLayer(model, bauwerksstruktur, abkuerzungs_dict); //BS erstellen und verlinken
    search_for_empty_groups(modelId) // Leere Gruppen löschen
}

function buildLayer(parent_id, bsLayerDict, abkuerzungs_dict) { // Ebene erstellen

    for (var layerKuerzel in bsLayerDict) {
        var desiteBSID = createIfNotExist(parent_id, layerKuerzel, undefined, abkuerzungs_dict);

        for (var layerChild in bsLayerDict[layerKuerzel].children) {
            buildInstances(desiteBSID, bsLayerDict, layerChild, layerKuerzel, abkuerzungs_dict);


        }
        for (var i in bsLayerDict[layerKuerzel].instances) {
            var guid = bsLayerDict[layerKuerzel].instances[i]
            desiteAPI.setLinkedObjects(desiteBSID, guid)


        }
    }
}

function buildInstances(parent_id, bs_dictIn, levelName, instanceKuerzel, abkuerzungs_dict) { //individuen verknüpfen
    var desiteBSID = createIfNotExist(parent_id, instanceKuerzel, "_" + levelName, abkuerzungs_dict);
    buildLayer(desiteBSID, bs_dictIn[instanceKuerzel].children[levelName], abkuerzungs_dict);
}

function createIfNotExist(par_id, kuerzel, suffix, abkuerzungs_dict) { // wenn layer noch nicht existiert, wird es erstellt

    if (suffix == undefined) {
        suffix = ""
    }
    var vgKlass = getBauteilKlassifikation(kuerzel, abkuerzungs_dict);
    var vgName = getName(kuerzel, abkuerzungs_dict) + suffix;
    var does_not_exist = true;
    var child_elements = desiteAPI.getContainedElements(par_id, 1);
    for (var i in child_elements) {
        var child_id = child_elements[i];
        var bauteilKlassifikation = desiteAPI.getPropertyValue(child_id, KLASSIFIKATION, STRNG);
        var bsName = desiteAPI.getPropertyValue(child_id, "cpName", STRNG);

        if (bsName == vgName && bauteilKlassifikation == vgKlass) {
            does_not_exist = false;
            var id = child_id;
        }
    }
    if (does_not_exist) {
        var id = desiteAPI.createObjectFromXml(par_id, t1 + vgName + t2);
        desiteAPI.setPropertyValue(id, KLASSIFIKATION, STRNG, vgKlass);

    }
    return id;
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
    id = desiteAPI.createModel(bsName, createRootC = false, domain = "building") + "-oh"
    return id
}


function getBauteilKlassifikation(abkuerzung, abkuerzungs_dict) { //bauteilKlassifikation anhand von Abkuerzung erhalten
    abkuerzung = abkuerzung.toUpperCase()
    if (abkuerzung in abkuerzungs_dict) {

        return abkuerzungs_dict[abkuerzung][0]

    } else {
        console.log("Abkuerzung nicht bekannt: " + abkuerzung)
        return "undef"
    }

}

function getName(abkuerzung, abkuerzungs_dict) { //BauteilName als Abkuerzungsverzeichnis lesen
    abkuerzung = abkuerzung.toUpperCase()

    if (abkuerzung in abkuerzungs_dict) {

        return abkuerzungs_dict[abkuerzung][1]

    } else {
        console.log("Abkuerzung nicht bekannt: " + abkuerzung)
        return "undef"
    }

}

function getBS(abkuerzungs_dict) { // gewollte Bauwerksstruktur als JSON erstellen
    var all_elements = desiteAPI.getAllElements("geometry");
    var element_liste = [];
    var bauwerksstruktur = {};
    var elementeOhneGruppenAttribut = [];
    for (var i in all_elements) { //Erstellt Liste aus allen Elementen und deren Gruppenzugehörigkeiten
        var id = all_elements[i];
        if (desiteAPI.isContainer(id)) {
            continue
        }
        var gruppe = desiteAPI.getPropertyValue(id, GRUPPIERUNGSATTRIB, STRNG)
        var bauteilKlassifikation = desiteAPI.getPropertyValue(id, KLASSIFIKATION, STRNG)
        if (gruppe != undefined) {
            groups = gruppe.split(GRUPPENTRENNER) //Bei mehrfachgruppierung
            for (g in groups) {
                element_liste.push([id, groups[g], bauteilKlassifikation])
            }
        } else {
            elementeOhneGruppenAttribut.push(id);
        }


    }

    var groupErrorList = []
    for (var i in element_liste) { // Erstellt BS als JSON
        id = element_liste[i][0];
        identitaet = element_liste[i][1];   //Wert von idGruppe nach split(";")
        bauteilKlassifikation = element_liste[i][2]
        if (checkForGroupError(identitaet, abkuerzungs_dict)) {
            groupErrorList.push(id)
        }
        eigene_abkuerzung = getReverseAbkuerzung(bauteilKlassifikation, abkuerzungs_dict)

        split_ident = identitaet.split("_")
        fokus_struktur = bauwerksstruktur
        for (var k in split_ident) {
            klass_ident = split_ident[k]
            if (k % 2 == 0) {
                if (klass_ident in fokus_struktur) {
                    fokus_struktur = fokus_struktur[klass_ident];
                } else {
                    fokus_struktur[klass_ident] = {"children": {}, "instances": []}
                    fokus_struktur = fokus_struktur[klass_ident]

                }

            } else {
                if (klass_ident in fokus_struktur.children) {
                    fokus_struktur = fokus_struktur.children[klass_ident]
                } else {
                    fokus_struktur.children[klass_ident] = {}
                    fokus_struktur = fokus_struktur.children[klass_ident]
                }
            }
            if (k == split_ident.length - 1) {
                if (!(eigene_abkuerzung in fokus_struktur)) {
                    fokus_struktur[eigene_abkuerzung] = {"children": {}, "instances": []}
                }
                fokus_struktur[eigene_abkuerzung].instances.push(id)


            }
        }
    }

    if (groupErrorList.length > 0) {
        text = "Fehler in Aufbau von idGruppe"
        console.log("Einige Elemente haben einem Fehler im Attribut '" + GRUPPIERUNGSATTRIB + "' -> Viewpoint wurde erstellt")
        createIssue("Fehler Aufbau", text, modelId, groupErrorList)
    }
    if (elementeOhneGruppenAttribut.length > 0) {
        console.log("Einige Elemente haben nicht das Attribut '" + GRUPPIERUNGSATTRIB + "' -> Viewpoint wurde erstellt")
        text = "Attribut " + GRUPPIERUNGSATTRIB + "Fehlt"
        createIssue("Fehler Attribut", text, modelId, elementeOhneGruppenAttribut)
    }

    return bauwerksstruktur
}


function getIdentAttrib(objectDict, attributeId) {
    var pset_dict = objectDict["PropertySets"];
    for (var pset_id in pset_dict) {
        var attributes_dict = pset_dict[pset_id]["Attributes"]
        for (var a_id in attributes_dict) {
            if (a_id !== attributeId) {
                continue
            }
            var value_list = attributes_dict[a_id]["Value"]
            if (value_list.length > 0) {
                return value_list[0]
            } else {
                return undefined
            }
        }
    }
}

function getAbkuerzung(path) { // abkuerzungsverzeichnis einlesen
    var text = desiteAPI.readTextFileAsString(path)
    var somjson = JSON.parse(text);
    var return_dict = {}
    for (var obj_id in somjson["Objects"]) {
        var obj_dict = somjson["Objects"][obj_id];
        var abbrev = obj_dict["abbreviation"]
        var name = obj_dict["name"]
        var ident = getIdentAttrib(obj_dict, obj_dict["ident_attribute"])
        return_dict[abbrev] = [ident, name]
    }
    return return_dict
}

function getReverseAbkuerzung(bk, abkuerzungs_dict) { // abkuerzungsverzeichnis umwandlen -> bauteilKlassifikation als Key
    var reverse_abkz = {};
    abkz = abkuerzungs_dict
    for (i in abkz) {
        bauteilKlass = abkz[i][0];
        reverse_abkz[bauteilKlass] = i;
    }
    ret = reverse_abkz[bk]
    if (ret == undefined) {
        console.log("BauteilKLasse '" + bk + "' kommt nicht im Abkürzungsverzeichnis vor")
        ret = "undef"
    }
    return ret
}

function checkForGroupError(identitaet, abkuerzungs_dict) { // Fehlermeldung wenn gruppenid komisch ist
    check_bool = false

    sp = identitaet.split("_")
    last_entry = sp[sp.length - 1]
    if (last_entry in abkuerzungs_dict) {
        check_bool = true
    }
    if (sp.length % 2 != 0) {
        check_bool = true
    }
    return check_bool
}

function createIssue(issueName, description, modelId, idList) {
    function getOptions(IssueName) {


        return {
            "name": IssueName,
            "saveVisible": true,
            "linkVisible": false,
            "saveSelected": true,
            "linkSelected": true,
            "saveLocked": false,
            "saveClipping": false,
            "saveRedlining": false,
            "saveMeasuring": false
        }

    }

    desiteAPI.selectElements(idList.join(";"), true);
    desiteAPI.zoomToSelected();
    map = {
        "issue": {
            "name": description, "description": description, "status": "Open", "priority": "Normal",
        }
    }

    issueId = desiteAPI.createObject(modelId, map)
    options = getOptions(issueName)

    vp_id = desiteAPI.createViewpointFromCurrentView(issueId, options)
    return issueId

}

function getDate() {
    date = new Date()
    return [date.getDate(), date.getMonth() + 1, date.getFullYear(),].join('.') + " " + date.toLocaleTimeString();
}

function search_for_empty_groups(element_id) {
    var children = check_and_delete_empty_groups(element_id)
    for (child_index in children) {
        var child_id = children[child_index];
        var child_type = desiteAPI.getPropertyValue(child_id, "Type", "xs:string");
        if (child_type === "typeBsGroup") {
            search_for_empty_groups(child_id);
        }
    }
}

function check_and_delete_empty_groups(element_id) {
    var children = desiteAPI.getContainedElements(element_id, 1);
    var linked_objects = desiteAPI.getLinkedObjects(element_id);
    if (children.length === 0 && linked_objects.length === 0) {
        var name = desiteAPI.getPropertyValue(element_id, "cpName", "xs:string");
        console.log("Delete " + element_id + "   " + name +" because it's empty");
        var parent_id = desiteAPI.getParent(element_id);
        desiteAPI.deleteObjects([element_id]);
        check_and_delete_empty_groups(parent_id);
    }
    return children
}
