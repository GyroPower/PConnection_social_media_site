function clearInputFile(id){

    fetch("/operations/"+id,{
        method:"PUT"
    ,})
    .then(response => response.json())
    .then(document.getElementById("preview").innerHTML= "No image");

}
