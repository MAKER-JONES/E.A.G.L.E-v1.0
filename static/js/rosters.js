function flightDisplay(flightName){
    console.log(flightName)
    document.getElementById("cadetFrame").src = "/rosterlist/"+flightName
    document.getElementById("flight-info-edit").href = "/edit-flight/"+flightName
}