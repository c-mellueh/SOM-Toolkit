function check_exist(name, Pset, return_format) {

    //Kontrolle, ob ein Attribut existiert, ohne dessen Wert zu überprüfen

    //Ausgabetexte

    var text1 = 'Eigenschaft ';
    var text2 = ' nicht vorhanden! ';
    var text3 = ' besitzt nicht den richtigen Wert!';
    var text4 = " ( Wert ist :";
    var text5 = "[Fehler ";

    var svalue = pSet + name;

    //Attribut wird aus Objekt gelesen
    var value = desiteAPI.getPropertyValue(id, svalue, return_format);

    //Kontrolle, ob Attribut existiert	
    if (value == undefined) {
        if (!check_datatype(name, pSet, return_format)) {
            desiteResult.addMessage("Eigenschaft " + svalue + " besitzt den falschen Datentyp! [Fehler 5]");
            return 1;
        } else {

            desiteResult.addMessage(text1 + svalue + text2 + text5 + "3]");
            return 1;
        }
    }

    //Wenn keine Fehler existieren ist die Prüfung erfolgreich abgeschlossen
    else {
        return 0;
    }
}