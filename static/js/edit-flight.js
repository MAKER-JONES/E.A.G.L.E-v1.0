
let nameID = 1
let ID_list = [0]


function addCadet2(first_name,last_name){
    let nameBox = document.createElement("div")
    let lastNameBox = document.createElement("input")
    let firstNameBox = document.createElement("input")
    let subBox = document.createElement("button")
    subBox.classList.add("subtract-button")
    subBox.id = nameID
    subBox.innerText = "-"
    subBox.setAttribute("onclick","sub(this)")
    nameBox.classList.add("cadet-name")
    nameBox.id = "cadet-" + nameID.toString()
    lastNameBox.classList.add("name-input")
    lastNameBox.setAttribute("onkeypress", "return avoidSpace(event)")
    firstNameBox.setAttribute("onkeypress", "return avoidSpace(event)")
    firstNameBox.classList.add("name-input")

    lastNameBox.placeholder = "Last Name"
    lastNameBox.id = nameID.toString() + "-last"
    firstNameBox.placeholder = "First Name"
    firstNameBox.id = nameID.toString() + "-first"
    firstNameBox.value = first_name
    lastNameBox.value = last_name
    nameBox.append(subBox)
    nameBox.append(firstNameBox)
    nameBox.append(lastNameBox)
    let outerform = document.getElementById("flight-input-cadets")
    outerform.append(nameBox)
    ID_list.push(nameID)
    nameID+=1
    
    
}
function addCadet(){
    let nameBox = document.createElement("div")
    let lastNameBox = document.createElement("input")
    let firstNameBox = document.createElement("input")
    let subBox = document.createElement("button")
    subBox.classList.add("subtract-button")
    subBox.id = nameID
    subBox.innerText = "-"
    subBox.setAttribute("onclick","sub(this)")
    nameBox.classList.add("cadet-name")
    nameBox.id = "cadet-" + nameID.toString()
    lastNameBox.classList.add("name-input")
    lastNameBox.setAttribute("onkeypress", "return avoidSpace(event)")
    firstNameBox.setAttribute("onkeypress", "return avoidSpace(event)")
    firstNameBox.classList.add("name-input")

    lastNameBox.placeholder = "Last Name"
    lastNameBox.id = nameID.toString() + "-last"
    firstNameBox.placeholder = "First Name"
    firstNameBox.id = nameID.toString() + "-first"
    nameBox.append(subBox)
    nameBox.append(firstNameBox)
    nameBox.append(lastNameBox)
    let outerform = document.getElementById("flight-input-cadets")
    outerform.append(nameBox)
    ID_list.push(nameID)
    nameID+=1
    
    
}
function sub(element){
    let cadetInput = document.getElementById("cadet-"+ element.id.toString())
    ID_list.splice(ID_list.indexOf(parseInt(element.id)),ID_list.indexOf(parseInt(element.id)))
    cadetInput.remove()
    console.log(ID_list)

}
let lastNames = ""
let firstNames = ""
let flightName
let submitStatus = false
function submitFlight(){
    flightNameInput = document.getElementById("flight-input-name")
    if (flightNameInput.value  != ''){
        flightName = flightNameInput.value
        for( i in ID_list){
            if( ID_list[i] != 0){
                console.log(i)
                if(document.getElementById(ID_list[i].toString() + "-last").value != "" && document.getElementById(ID_list[i].toString() + "-first").value != "" ){
                    lastNames = lastNames + document.getElementById(ID_list[i].toString() + "-last").value + ","
                    firstNames = firstNames + document.getElementById(ID_list[i].toString() + "-first").value + ","
                    submitStatus=true
                }else{
                    submitStatus = false
                    lastNames = ""
                    firstNames = ""
                    break
                }
                
            }
        }
        if(submitStatus){
            console.log(lastNames)
            console.log(firstNames)
            document.getElementById("form-lastNames").value = lastNames
            document.getElementById("form-firstNames").value = firstNames
            document.getElementById("form-flightName").value = flightName
            document.getElementById("infoForm").submit()
        }
        

    }
    
}
function avoidSpace(event){
    var k = event ? event.which : window.event.keyCode;
    if (k == 32) return false;
}
function fillNames(firstNames,lastNames){
    console.log("running")
    firstNames = firstNames.split(",")
    lastNames = lastNames.split(",")
    for(i in firstNames){
        
        addCadet2(firstNames[i],lastNames[i])
    } 
}

