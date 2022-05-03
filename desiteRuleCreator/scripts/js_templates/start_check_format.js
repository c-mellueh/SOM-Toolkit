function check_format(name, pSet, return_format, format_list) {

    //Kontrolle ob pSet+name dem Format format entsprechen
    //Ausgabetexte


    var text1 = 'Eigenschaft ';
    var text2 = ' nicht vorhanden! ';
    var text3 = ' besitzt nicht den richtigen Wert oder das richtige Format!';
    var text4 = " ( Wert ist :";
    var text5 = "[Fehler ";

    return_value = 0;

    var svalue = pSet + name;


    //Attribut wird aus Objekt gelesen
    var value = desiteAPI.getPropertyValue(id, svalue, return_format);

    //Kontrolle, ob Attribut existiert		
    if (value == undefined) {

        if (!check_datatype(name, pSet, return_format)) {
            desiteResult.addMessage("Eigenschaft " + svalue + " besitzt den falschen Datentyp! [Fehler 5]");
            return_value += 1;
        } else {
            desiteResult.addMessage(text1 + svalue + text2 + text5 + "3]");
            return_value += 1;
        }
    }


    for (i in format_list) {

        format = new RegExp(format_list[i], "i")

        //Kontrolle, ob Format eingehalten ist
        if (!format.test(value)) {
            return_value += 1;
        }
    }

    //Wenn keine Fehler existieren ist die Prüfung erfolgreich abgeschlossen
    if (return_value != format_list.lenght) {
        return 0;
    } else {
        desiteResult.addMessage(text1 + svalue + text3 + text4 + value + " ) " + text5 + "1]");
        return 1
    }
}