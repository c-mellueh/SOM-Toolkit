function check_datatype(name, pSet, return_format) {

    var svalue = pSet + name;
    //list = desiteAPI.getPropertyTypeListByObject(id, svalue)

		if (return_format == "xs:string") {

		alt_datatype = "xs:double"}

		else if (return_format == "xs:double") {

		alt_datatype = "xs:string"
}
	else {
	desiteResult("Check_Datatyp muss ergaenzt werden")
}


	//obj = list[0]
	

	prop1 = desiteAPI.getPropertyValue(id,svalue,return_format)
	prop2 = desiteAPI.getPropertyValue(id,svalue,alt_datatype)


	if (prop2 != undefined) {return false}
	else {return true}


}