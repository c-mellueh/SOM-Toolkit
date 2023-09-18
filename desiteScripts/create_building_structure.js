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
var ABKUERZUNGSDATEI = desiteAPI.getProjectDirectory() + "/DB_scripts/abkuerzungen.json"

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
    bauwerksstruktur = getBS(); // gewollte Bauwerksstruktur als JSON einlesen
    var model = getModel(BSNAME); // BS Model mit BSNAME finden
    buildLayer(model, bauwerksstruktur); //BS erstellen und verlinken

}

function buildLayer(parent_id, bsLayerDict) { // Ebene erstellen

    for (var layerKuerzel in bsLayerDict) {
        var desiteBSID = createIfNotExist(parent_id, layerKuerzel);
        for (var layerChild in bsLayerDict[layerKuerzel].children) {
            buildInstances(desiteBSID, bsLayerDict, layerChild, layerKuerzel);


        }
        for (var i in bsLayerDict[layerKuerzel].instances) {
            var guid = bsLayerDict[layerKuerzel].instances[i]
            desiteAPI.setLinkedObjects(desiteBSID, guid)


        }
    }
}

function buildInstances(parent_id, bs_dictIn, levelName, instanceKuerzel) { //individuen verknüpfen
    var desiteBSID = createIfNotExist(parent_id, instanceKuerzel, "_" + levelName);
    buildLayer(desiteBSID, bs_dictIn[instanceKuerzel].children[levelName]);
}

function createIfNotExist(par_id, kuerzel, suffix) { // wenn layer noch nicht existiert, wird es erstellt
    if (suffix == undefined) { suffix = "" }
    var vgKlass = getBauteilKlassifikation(kuerzel);
    var vgName = getName(kuerzel) + suffix;
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


function getBauteilKlassifikation(abkuerzung) { //bauteilKlassifikation anhand von Abkuerzung erhalten
    abkuerzung = abkuerzung.toUpperCase()
    if (abkuerzung in getAbkuerzung()) {

        return getAbkuerzung()[abkuerzung][0]

    }
    else {
        console.log("Abkuerzung nicht bekannt: " + abkuerzung)
        return "undef"
    }

}

function getName(abkuerzung) { //BauteilName als Abkuerzungsverzeichnis lesen
    abkuerzung = abkuerzung.toUpperCase()

    if (abkuerzung in getAbkuerzung()) {

        return getAbkuerzung()[abkuerzung][1]

    }
    else {
        console.log("Abkuerzung nicht bekannt: " + abkuerzung)
        return "undef"
    }

}

function getBS() { // gewollte Bauwerksstruktur als JSON erstellen
    var all_elements = desiteAPI.getAllElements("geometry");
    var element_liste = [];
    var bauwerksstruktur = {};
    var elementeOhneGruppenAttribut = [];
    for (var i in all_elements) { //Erstellt Liste aus allen Elementen und deren Gruppenzugehörigkeiten
        var id = all_elements[i];
        if (desiteAPI.isContainer(id)){continue}
        var gruppe = desiteAPI.getPropertyValue(id, GRUPPIERUNGSATTRIB, STRNG)
        var bauteilKlassifikation = desiteAPI.getPropertyValue(id, KLASSIFIKATION, STRNG)
        if (gruppe != undefined) {
            groups = gruppe.split(GRUPPENTRENNER) //Bei mehrfachgruppierung
            for (g in groups) {
                element_liste.push([id, groups[g], bauteilKlassifikation])
            }
        }
        else {
            elementeOhneGruppenAttribut.push(id);
        }


    }

    var groupErrorList = []
    for (var i in element_liste) { // Erstellt BS als JSON
        id = element_liste[i][0];
        identitaet = element_liste[i][1];   //Wert von idGruppe nach split(";")
        bauteilKlassifikation = element_liste[i][2]
        if (checkForGroupError(identitaet)) {
            groupErrorList.push(id)
        }
        eigene_abkuerzung = getReverseAbkuerzung(bauteilKlassifikation)

        split_ident = identitaet.split("_")
        fokus_struktur = bauwerksstruktur
        for (var k in split_ident) {
            klass_ident = split_ident[k]
            if (k % 2 == 0) {
                if (klass_ident in fokus_struktur) {
                    fokus_struktur = fokus_struktur[klass_ident];
                }
                else {
                    fokus_struktur[klass_ident] = { "children": {}, "instances": [] }
                    fokus_struktur = fokus_struktur[klass_ident]

                }

            }
            else {
                if (klass_ident in fokus_struktur.children) {
                    fokus_struktur = fokus_struktur.children[klass_ident]
                }
                else {
                    fokus_struktur.children[klass_ident] = {}
                    fokus_struktur = fokus_struktur.children[klass_ident]
                }
            }
            if (k == split_ident.length - 1) {
                if (!(eigene_abkuerzung in fokus_struktur)) {
                    fokus_struktur[eigene_abkuerzung] = { "children": {}, "instances": [] }
                }
                fokus_struktur[eigene_abkuerzung].instances.push(id)

                continue
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

function getAbkuerzung() { // abkuerzungsverzeichnis einlesen
    txt = desiteAPI.readTextFileAsString(ABKUERZUNGSDATEI)
    return JSON.parse(txt)
}

function getReverseAbkuerzung(bk) { // abkuerzungsverzeichnis umwandlen -> bauteilKlassifikation als Key
    var reverse_abkz = {};
    abkz = getAbkuerzung()
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
function checkForGroupError(identitaet) { // Fehlermeldung wenn gruppenid komisch ist
    check_bool = false

    sp = identitaet.split("_")
    last_entry = sp[sp.length - 1]
    if (last_entry in getAbkuerzung()) {
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
            "name": description,
            "description": description,
            "status": "Open",
            "priority": "Normal",
        }
    }

    issueId = desiteAPI.createObject(modelId, map)
    options = getOptions(issueName)

    vp_id = desiteAPI.createViewpointFromCurrentView(issueId, options)
    return issueId

}

function getDate() {
    date = new Date()
    return [
        date.getDate(),
        date.getMonth() + 1,
        date.getFullYear(),
    ].join('.') + " " + date.toLocaleTimeString();
}