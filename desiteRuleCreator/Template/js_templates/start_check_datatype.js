function check_datatype(name, pSet, return_format) {

    var svalue = pSet + name;
    list = desiteAPI.getPropertyTypeListByObject(id, svalue)

	obj = list[0]
	
	if (obj == undefined) {return true}
	
	else {
	
		if (obj.DataType == return_format) {
			return true
		} else {
			return false
		}
		
	}
}