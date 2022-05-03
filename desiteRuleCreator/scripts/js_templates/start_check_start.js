id = desiteThis.ID()
desiteAPI.setPropertyValue( id , "Check_State" , "xs:string", "Ungeprüft")


prop = desiteAPI.getPropertyValue(id,"ifcTypeObjectName","xs:string")

if (prop == "BIMR_Koordinationskoerper") {

desiteAPI.setPropertyValue( id , "Check_State" , "xs:string", "Passed")

}