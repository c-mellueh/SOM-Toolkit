function check_range(name, pSet, return_format, range) {

    //Kontrolliert, ob sich 	 pSet+name in einem Bestimmten Wertebereich bewegen

    //range[*][0] -> untere Grenze
    //range[*][1] -> obere Grenze

    //Ausgabetext	

    var text1 = 'Eigenschaft "';
    var text2 = '" nicht vorhanden! ';
    var text3 = '" liegt außerhalb des vorgegebenen Wertebereichs in MEM! ';
    var text4 = '" ( Wert ist : ';
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
    } else {

        //Wenn das Format xs:string ist, wird das Attribut in eine Float Zahl umgewandelt
        if (return_format == "xs:string") {
            val = parseFloat(value.replace(',', '.'))
        	console.log(val)
					if(isNaN(val)) {
					
					desiteResult.addMessage(svalue+" entspricht nicht den Vorgaben in MEM (Wert ist: '"+value+"') [Fehler 1]");
return 1

					}else {value = val}
					
					}



        //Anzahl der Wertebereiche

        var treffer = 0;

        if (desiteAPI.getPropertyUnit(svalue, return_format) == "m") {
            value = value / 1000
        }

        for (i = 0; i < range.length; i++) {
            if (range[i].length == 1) {
                if (value == range[i][0]) {
                    treffer += 1
                }
            } else {
                var untere_grenze = range[i][0];
                var obere_grenze = range[i][1];

                if (value >= untere_grenze && value <= obere_grenze) {
                    treffer += 1
                }
            }
        }

        if (treffer != 1) {
            desiteResult.addMessage(text1 + svalue + text3 + text5 + "2]");
            return 1;
        }
        //Kontrolle, ob das Attribt im Wertebereich liegt
        else {
            return 0
        }
    }
}