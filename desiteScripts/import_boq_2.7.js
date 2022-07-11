var path = desiteAPI.showOpenFileDialog("CSV Datei Oeffnen","","CSV (*.csv);; All files (*.*)");
var csv_object = desiteAPI.csvOpen(path)
var header = desiteAPI.csvNextLine()
var all_elements = desiteAPI.getAllElements('geometry')


while (desiteAPI.csvHasNextLine()) {
	var line = desiteAPI.csvNextLine()
	
	filtered_list = filter(all_elements,line)
		
	for( i in filtered_list) {

	var object_id = filtered_list[i]

	for(k =2; k< header.length;k++) {
			var attribute = header[k]
			var value = line[k]
			console.log(attribute+"->"+value)
desiteAPI.setPropertyValue(object_id,attribute,"xs:string",value)
			}

}	

}

function filter(all_elements,line) {
filter_list = []

for (k in all_elements) {
	id = all_elements[k]
	attribute = desiteAPI.getPropertyValue(id,line[0],"xs:string")
	if (attribute == line[1]) {
	filter_list.push(id)

}
}
return filter_list
}