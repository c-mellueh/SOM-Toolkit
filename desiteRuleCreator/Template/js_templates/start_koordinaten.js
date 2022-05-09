var id = desiteThis.ID();

geo=[]
geo.push(desiteAPI.getPropertyValue(id,"cpCOGx","xs:double"))
geo.push(desiteAPI.getPropertyValue(id,"cpCOGy","xs:double"))
geo.push(desiteAPI.getPropertyValue(id,"cpCOGz","xs:double"))

val = true

container = desiteAPI.getPropertyValue(id,"cpIsContainer","xs:boolean")

if(!container) {

for (i in geo){
	loc = geo[i]
	bool = loc >-10000.00 && loc < 10000.00
	console.log(bool)	
	val = val	&& bool
}
if (!val) {
desiteResult.addMessage("Koordinaten passen nicht zum Rest des Modelles![Fehler 9]")
desiteResult.setCheckState('Warning');
}
}