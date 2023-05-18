function clearInputFile(id){

    fetch("/votes/"+id,{
        method:"PUT"
    ,})
    .then(response => response.json())
    .then(document.getElementById("preview").innerHTML= "No image");

}
