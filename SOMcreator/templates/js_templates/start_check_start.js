function check_for_single(value, range) {
    var treffer = 0;
    for (k in range) {
        pair = range[k]
        if (pair.indexOf("") > -1 || pair.length < 2) {

            for (t in pair) {
                if (pair[t] == value) {
                    treffer += 1
                }
            }
        }
    }
    return treffer
}

function check_range(attribute_name, property_set_name, return_format, range, existing_data) {
    //Kontrolliert, ob sich 	 pSet+name in einem Bestimmten Wertebereich bewegen

    //range[*][0] -> untere Grenze
    //range[*][1] -> obere Grenze

    //Ausgabetext
    var text1 = 'Eigenschaft "';
    var text2 = '" nicht vorhanden! ';
    var text3 = '" liegt außerhalb des vorgegebenen Wertebereichs in MEM! ';
    var text4 = '" ( Wert ist : ';
    var text5 = "[Fehler ";
    var svalue = property_set_name + attribute_name;


    //Kontrolle, ob Attribut existiert
    if (check_exist(attribute_name, property_set_name, return_format, existing_data) === 1) {
        return 1
    }
    var value = existing_data["Value"];
    var unit = existing_data["Unit"];
    //Wenn das Format xs:string ist, wird das Attribut in eine Float Zahl umgewandelt
    if (return_format === "xs:string") {
        parsed_value = value
        replaced = parsed_value.replace(',', '.')
        parsed_value = parseFloat(replaced)
        if (!isNaN(parsed_value)) {
            value = parsed_value;
        }
    }
    //Anzahl der Wertebereiche

    var treffer = 0;

    if (unit === "m") {
        value = value / 1000
    }
    treffer += check_for_single(value, range)

    for (i = 0; i < range.length; i++) {
        var untere_grenze = parseFloat(range[i][0].replace(",", "."));
        var obere_grenze = parseFloat(range[i][1].replace(",", "."));

        if (value >= untere_grenze && value <= obere_grenze) {
            treffer += 1
        }
    }


    if (treffer < 1) {
        desiteResult.addMessage(text1 + svalue + text3 + text4 + value + ")" + text5 + "2]");
        return 1;
    }
    return 0
}


function check_format(attribute_name, property_set_name, return_format, format_list, existing_data) {

    //Kontrolle ob pSet+name dem Format format entsprechen
    //Ausgabetexte


    var text1 = 'Eigenschaft ';
    var text2 = ' nicht vorhanden! ';
    var text3 = ' besitzt nicht den richtigen Wert oder das richtige Format!';
    var text4 = " ( Wert ist :";
    var text5 = "[Fehler ";
    var svalue = property_set_name + ":" + attribute_name;

    return_value = 0;


    //Kontrolle, ob Attribut existiert
    if (check_exist(attribute_name, property_set_name, return_format, existing_data) === 1) {
        return 1
    }

    var value = existing_data["Value"]

    for (i in format_list) {

        format = new RegExp(format_list[i], "i")

        //Kontrolle, ob Format eingehalten ist
        if (!format.test(value)) {
            return_value += 1;
        }
    }

    //Wenn mindestens eine RegEx richtig war ist die Prüfung erfolgreich abgeschlossen
    if (return_value !== format_list.lenght) {
        return 0;
    } else {
        desiteResult.addMessage(text1 + svalue + text3 + text4 + value + " ) " + text5 + "1]");
        return 1
    }
}

function check_exist(attribute_name, property_set_name, return_format, existing_data) {

    //Kontrolle, ob ein Attribut existiert, ohne dessen Wert zu überprüfen

    //Ausgabetexte

    var text1 = 'Eigenschaft ';
    var text2 = ' nicht vorhanden! ';
    var text3 = "[Fehler ";
    var text4 = " besitzt den falschen Datentyp! ";
    var svalue = property_set_name + ":" + attribute_name;


    //Kontrolle, ob Attribut existiert
    if (existing_data === undefined) {
        desiteResult.addMessage(text1 + svalue + text2 + text3 + "3]");
        return 1;
    }
    //Kontrolle ob Datentyp stimmt
    else if (existing_data["Type"] !== return_format) {
        desiteResult.addMessage(text1 + svalue + text4 + text3 + "5]");
        return 1;
    }
    //Wenn keine Fehler existieren ist die Prüfung erfolgreich abgeschlossen
    else {
        return 0;
    }
}

function check_for_value(attribute_name, property_set_name, return_format, list, existing_data) {

    //Kontrolle ob pSet+name sich in einer Liste (getrennt durch "," oder "/") wiederfinden (not enumerated list)

    //Ausgabetexte

    var text1 = 'Eigenschaft "';
    var text2 = '" nicht vorhanden! ';
    var text3 = ' entspricht nicht den Vorgaben in MEM!';
    var text4 = " ( Wert ist :";
    var text5 = "[Fehler ";
    var error = 0;
    var svalue = property_set_name + ":" + attribute_name;


    //Kontrolle, ob Attribut existiert
    if (check_exist(attribute_name, property_set_name, return_format, existing_data) === 1) {
        return 1
    }

    var value = existing_data["Value"];

    //Kontrolliert ob das Element in Liste enthalten ist
    if (list.indexOf(value) !== -1) {
        return 0
    }
    if (typeof (value) == "string") {
        //Kontrolle, durch welchen Seperator die Liste getrennt ist -> Liste dementsprechend aufteilen
        if (value.indexOf(",") !== -1) {
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
            if (list.indexOf(val_list[i]) === -1) {
                desiteResult.addMessage(text1 + svalue + '" (' + value + ") " + text3 + text5 + "1]");
                error += 1;
            }
        }
        //Wenn alle Werte in liste enthalten sind, ist die Prüfung erfolgreich abgeschlossen
        if (error === 0) {
            return 0;
        } else {
            return 1;
        }
    } else {
        desiteResult.addMessage(text1 + svalue + '" (' + value + ") " + text3 + text5 + "1]");
        return 1;
    }
}

function get_property_set_dict(id) {

    var values = desiteAPI.getPropertyValuesByObject(id)

    var attributes = {}

    for (index in values) {
        var data_set = values[index];
        var name = JSON.stringify(data_set["Name"])
        var test = name.split(":")
        if (test.length < 2) {
            continue
        }
        var pset_name = test[0]
        var attribute_name = test[1].slice(0, -1)

        pset_name = pset_name.substring(1)
        if (!(pset_name in attributes)) {
            attributes[pset_name] = {}
        }

        attributes[pset_name][attribute_name] = data_set
    }
    return attributes
}

function check_property_set(pset_dict, pset_name) {
    if (!(pset_name in pset_dict)) {
        desiteResult.addMessage('PropertySet "' + pset_name + '" existiert nicht [Fehler 4]')
        return false
    }
    return true
}

id = desiteThis.ID()
desiteAPI.setPropertyValue(id, "Check_State", "xs:string", "Ungeprüft")
