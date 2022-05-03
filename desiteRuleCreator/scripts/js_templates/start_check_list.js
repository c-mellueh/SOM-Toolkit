function check_list(name, pSet, return_format, list) {

    //Kontrolle ob pSet+name sich in einer Liste (getrennt durch "," oder "/") wiederfinden (not enumerated list)

    //Ausgabetexte

    var text1 = 'Eigenschaft "';
    var text2 = '" nicht vorhanden! ';
    var text3 = ' entspricht nicht den Vorgaben in MEM!';
    var text4 = " ( Wert ist :";
    var text5 = "[Fehler ";
    var error = 0;
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
            error += 1;
        }
    }
    //Kontrolliert ob das Element in Liste enthalten ist 
    else if (list.indexOf(value) != -1) {
        return 0
    }




    //Kontrolle, durch welchen Seperator die Liste getrennt ist -> Liste dementsprechend aufteilen
    if (value.indexOf(",") != -1) {
        var val_list = value.split(",")
    } else if (value.indexOf("/") != -1) {
        var val_list = value.split("/")
    }


    //Wenn keine Trennzeichen vorhanden sind, besteht die Liste aus einem Element
    else {
        val_list = [value]
    }


    for (i in val_list) {

        val_list[i] = val_list[i].trim(); //evtl. Leerzeichen am Anfang und Ende beseitigen  


        //Kontrolle, ob Das Element aus val_list in list enthalten ist (Case-insensitive)
        if (list.indexOf(val_list[i]) == -1) {
            desiteResult.addMessage(text1 + svalue + '" (' + value + ") " + text3 + text5 + "1]");
            return 1;
            error += 1;
        }
    }
    //Wenn alle Werte in liste enthalten sind, ist die Prüfung erfolgreich abgeschlossen
    if (error == 0) {
        return 0;
    }
}