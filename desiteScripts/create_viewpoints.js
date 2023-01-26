// ---------------------------------------------------------------
// ----- Gruppierung der PrÃ¼fungen und Ausgabe als Viewpints -----
// ---------------------------------------------------------------

var timestamp = getDate()
issues = desiteAPI.getModelListByDomain("issues")
model = desiteAPI.createModel(timestamp + " Modelcheck", true, domain = "issues")

var modelcheck = desiteAPI.getAllElements("qa"); // Alle Modelchecks sammeln
console.log(modelcheck)

var element_anzahl = modelcheck.length // Anzahl der Elemente auslesen

var Meldungen = []; // Liste mit Meldungen erstellen
var id_list = []; // Liste mit GUIDs erstellen
var checkstate_list = []; // Liste der Fehlertypen erstellen


console.log("Pruefungen Scannen")
console.log("")
console.log(element_anzahl + " Pruefergebnisse gefunden")

var vorheriger_wert = 0.0 //fortschrittswert fuer Textausgabe

for (i in modelcheck) { // Fuer alle Pruefdurchlaeufe


    vorheriger_wert = fortschritt(i, element_anzahl, vorheriger_wert)

    var check_id = modelcheck[i]; //ID des PrÃ¼flaufs Ã¼bergeben
    var element_id = desiteAPI.getPropertyValue(check_id, "Result:CheckedElement", "xs:IDREF"); // ID des geprÃ¼ften Elementes Ã¼bergeben
    var checkstate = desiteAPI.getPropertyValue(check_id, "CheckState", "xs:string"); // Checkstate des geprÃ¼ften Elementes Ã¼bergeben
    var element_name = desiteAPI.getPropertyValue(element_id, "ifcObjectType", "xs:string"); // Name des geprÃ¼ften Elementes Ã¼bergeben
    var check_nachricht = desiteAPI.getPropertyValue(check_id, "Result:Message", "xs:string"); // Nachricht des geprÃ¼ften Elementes Ã¼bergeben
    if (check_nachricht == undefined || checkstate == "Passed") {
        continue;
    } // bei undefinierten Objekten (z.B. Containern) und Erfolgreichen Checks wird abgebrochen

    var nachricht_list = check_nachricht.split("];") // Nachrichten werden in Liste aufgeteilt
    nachricht_length = nachricht_list.length

    for (k = 0; k < nachricht_length - 1; k++) {
        nachricht_list[k] = nachricht_list[k] + "]"
    }


    for (k in nachricht_list) { //Ã¼ber alle Nachrichten iterieren
        var typ = parseInt(nachricht_list[k].slice(-2, -1)); // Fehlertyp auslesen
        if (typ == "NaN") {
            console.log("Fehlermeldung besitzt keine Typ:" + nachricht_liste[k])
        } // Kontrolle ob Fehlertyp eine Zahl ist
        var index = Meldungen.indexOf(nachricht_list[k]); // kontrollieren, ob die Fehlermeldung schonmal gespeichert wurde
        if (index == -1) { // Wenn die Fehlermeldung noch nicht gespeichert wurde:
            Meldungen.push(nachricht_list[k]); // Fehlermeldung speichern
            id_list.push(element_id); // ID des geprÃ¼ften Elementes zur ID-Liste hinzufÃ¼gen
            checkstate_list.push(typ); // PrÃ¼fstatus abspeichern
        } else {
            id_list[index] = id_list[index] + ";" + element_id;
        } // Wenn die Meldung schon vorhanden ist wird die ID-Liste um die ElementID ergÃƒÂ¤nzt 

    }
}

desiteAPI.showAll(true)

var elm = desiteAPI.getAllElements("geometry");
var element = ""
for (i in elm) {
    element = element + ";" + elm[i]
}

console.log("")
console.log(Meldungen.length + " Ansichtspunkte erstellen")


var vorheriger_wert = 0.0 //fortschrittswert fuer Textausgabe

for (i in Meldungen) { // Fuer alle unterschiedlichen Fehlermeldungen

    vorheriger_wert = fortschritt(i, Meldungen.length, vorheriger_wert)


    desiteAPI.clearSelection(true)
    id_liste = id_list[i].split(";") // Die IDs der Elemente aus einer Stringlist in eine Liste umwandeln	
    desiteAPI.selectElements(id_list[i], true); // Die Elemente, welche zur Fehlermeldung gehÃƒÂ¶ren auswÃƒÂ¤hlen
    desiteAPI.zoomToSelected(); // Auf die Elemente, welche zur Fehlermeldung zoomen

    for (k in id_liste) {
        id_liste[k] = "\n" + id_liste[k];
    } // Zeilenumbruch hinzufÃ¼gen 
    var num = pad(+i + 1, 3); // vorlaufende Nullstellen hinzufÃ¼gen

    name = timestamp + " (Issue " + num + ")"

    issueId = createIssue(name, Meldungen[i], model)
    //desiteAPI.setPropertyValue(vp_id, "Description", "xs:string", Meldungen[i])
    //desiteAPI.saveViewpoint(, true, true, Meldungen[i], false, false);

}

desiteAPI.showAll(true);
console.log("")
"Ansichtspunkte erstellt"


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
    options = getOptions(name)

    vp_id = desiteAPI.createViewpointFromCurrentView(issueId, options)
    return issueId

}


function pad(num, size) { // vorlaufende Nullstellen hinzufÃ¼gen
    num = num.toString();
    while (num.length < size) num = "0" + num;
    return num;
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

function getDate() {
    date = new Date()
    return [
        date.getDate(),
        date.getMonth() + 1,
        date.getFullYear(),
    ].join('.') + " " + date.toLocaleTimeString();
}

function getOptions(name) {


    return {
        "name": name,
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