id = desiteThis.ID()
pset = "Bestandsdaten:"


status = desiteAPI.getPropertyValue(id, "Check_State", "xs:string")
objekttyp = desiteAPI.getPropertyValue(id,pset+"Objekttyp","xs:string")
console.log(status)

if (status == "Ungeprüft") {
    desiteResult.setCheckState('failed');

    check_status = "Failed"
	desiteAPI.setPropertyValue(id, "Check_State", "xs:string", check_status);

} 

if (objekttyp == undefined) {
    desiteResult.addMessage(pset+"Objekttyp existiert nicht -> Prüfung kann nicht durchgeführt Werden [Fehler 8]");
	desiteAPI.setPropertyValue(id, "Check_State", "xs:string", "Failed");
desiteResult.setCheckState("Failed")

} else {
    desiteResult.addMessage(pset+"Objekttyp (" + objekttyp + ") konnte nicht in MEM gefunden werden [Fehler 7]")
}

    desiteAPI.setPropertyValue(id, "zu_pruefende_eigenschaften","xs:int",1);
    desiteAPI.setPropertyValue(id, "fehlerhafte_eigenschaften","xs:int",1);