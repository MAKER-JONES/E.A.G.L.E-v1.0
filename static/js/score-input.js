
function sub(length,ids){
    let inputFormat = ""
    for (i = 0; i< parseInt(length); i++){
        cadet =document.getElementById("0,"+i).innerText
        let id = ids.split(",")[i]
        let uniform = document.getElementById("1,"+i).value.toString()
        let PT = document.getElementById("2,"+i).value.toString()
        let MBC = document.getElementById("3,"+i).value.toString()
        date = document.getElementById("4,"+i).value.toString() //year-month-date
        
        
        if((uniform != "" || PT != "" || MBC != "") && date == ""){
            alert("Error: "+ cadet+ " missing date")
            return 0;
        }
        if(uniform == "") {uniform = "N/A"}
        if(PT == "") {PT = "N/A"}
        if(MBC == "") {MBC = "N/A"}
        if(date == "") {date = "N/A"}
        inputFormat = inputFormat + id + "+" +uniform+ "+" +PT+ "+" +MBC+ "+" +date +","

    }
    inputFormat = inputFormat.slice(0,-1)
    document.getElementById("submit-input").value = inputFormat
    document.getElementById("input-form").submit()

}

// remove last chracter str = str.slice(0, -1); 