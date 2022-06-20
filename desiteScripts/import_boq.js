var path = desiteAPI.showOpenFileDialog("CSV Datei Oeffnen", "", "CSV (*.csv);; All files (*.*)");
var csv_object = desiteAPI.csvOpen(path)
var header = desiteAPI.csvNextLine()
var all_elements = desiteAPI.getAllElements('geometry')


while (desiteAPI.csvHasNextLine()) {
    var line = desiteAPI.csvNextLine()
    var filtered_list = desiteAPI.filterByProperty(all_elements, line[0], "xs:string", line[1])

    for (i in filtered_list) {

        var object_id = filtered_list[i]

        for (k = 2; k < header.length; k++) {
            var attribute = header[k]
            var value = line[k]
            console.log(attribute + "->" + value)
            desiteAPI.setPropertyValue(object_id, attribute, "xs:string", value)
        }

    }

}