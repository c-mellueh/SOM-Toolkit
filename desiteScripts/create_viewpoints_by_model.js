// ---------------------------------------------------------------
// ----- Gruppierung der Pruefungen nach IfcModellen und Ausgabe als Viewpints -----
// ---------------------------------------------------------------
var timestamp = getDate()
issues = desiteAPI.getModelListByDomain("issues")
model = desiteAPI.createModel(timestamp + " Modelcheck", true, domain = "issues")

console.log("Pruefungen Scannen")

var modelcheck = desiteAPI.getAllElements("qa"); // Alle Modelchecks sammeln
var element_anzahl = modelcheck.length // Anzahl der Elemente auslesen

console.log(element_anzahl + " Pruefergebnisse gefunden")

ifcDict = {}; //{ "ifc_file_name": { "error": ["element1", "element2"] } }

const prozent = 0.1; // Festlegen welche Fortschrittsinkremente gewählt sind 

var vorheriger_wert = 0.0 //fortschrittswert fuer Textausgabe
errorCounter = 0;
for (i = 0; i < element_anzahl; i++) {

    vorheriger_wert = fortschritt(i, element_anzahl, vorheriger_wert)

    var check_id = modelcheck[i]; //ID des Prüflaufs übergeben
    var element_id = desiteAPI.getPropertyValue(check_id, "Result:CheckedElement", "xs:IDREF"); // ID des geprüften Elementes übergeben
    var checkstate = desiteAPI.getPropertyValue(check_id, "CheckState", "xs:string"); // Checkstate des geprüften Elementes übergeben
    var element_name = desiteAPI.getPropertyValue(element_id, "ifcObjectType", "xs:string"); // Name des geprüften Elementes übergeben
    var check_nachricht = desiteAPI.getPropertyValue(check_id, "Result:Message", "xs:string"); // Nachricht des geprüften Elementes übergeben
    var ifc_modell = desiteAPI.getPropertyValue(element_id, "ImportFileName", "xs:string");

    if (check_nachricht == undefined || checkstate == "Passed") {
        continue;
    } // bei undefinierten Objekten (z.B. Containern) und Erfolgreichen Checks wird abgebrochen

    if (!(ifc_modell in ifcDict)) {
        ifcDict[ifc_modell] = {};
    }
    errorDict = ifcDict[ifc_modell];
    var nachricht_list = check_nachricht.split("];"); // Nachrichten werden in Liste aufgeteilt
    var nachricht_length = nachricht_list.length;

    for (k in nachricht_list) {
        var nachricht = nachricht_list[k];
        var nachricht = nachricht.slice(11);
        if (nachricht_length != 1) { nachricht += "]" }

        if (!(nachricht in errorDict)) {
            errorDict[nachricht] = [];
            errorCounter += 1;
        }
        errorDict[nachricht].push(element_id)
    }

}
//console.log("");
//console.log(errorCounter+" Issues erstellen");
//console.log("");
desiteAPI.showAll(true);
var vorheriger_wert = 0.0; //fortschrittswert fuer Textausgabe

issueIndex = 0
for (ifcName in ifcDict) {
    var errorDict = ifcDict[ifcName];
    desiteAPI.clearSelection(true);
    var container = createContainer(model, ifcName);

    for (errorMessage in errorDict) {
        vorheriger_wert = fortschritt(issueIndex, errorCounter, vorheriger_wert)
        issueIndex += 1;
        var error_items = errorDict[errorMessage];
        print("Error:" + error_items)
        //console.log(items)
        desiteAPI.selectElements(error_items.join(";"), true);
        desiteAPI.zoomToSelected();
        createIssue("Issue", errorMessage, container);
    }
}

desiteAPI.showAll(true);
console.log("")
"Ansichtspunkte erstellt"


function createContainer(modelId, ifcName) {
    var containerDict = { "container": { "ID": ifcName, "name": ifcName } };
    var containerId = desiteAPI.createObject(modelId, containerDict);
    return containerId
}

function createIssue(issueName, description, modelId) {
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
function getDate() {
    date = new Date()
    return [
        date.getDate(),
        date.getMonth() + 1,
        date.getFullYear(),
    ].join('.') + " " + date.toLocaleTimeString();
}
function fortschritt(durchlauf, anzahl_gesamt, vorheriger_wert) {

    steigerung = 5
    prozent = durchlauf / anzahl_gesamt * 100;
    if (prozent >= vorheriger_wert + steigerung) {
        console.log("	 Fortschritt: " + Math.round(prozent, 1) + "%")
        return Math.floor(prozent)


    } else {
        return vorheriger_wert
    }

}
function pad(num, size) { // vorlaufende Nullstellen hinzufÃ¼gen
    num = num.toString();
    while (num.length < size) num = "0" + num;
    return num;
}