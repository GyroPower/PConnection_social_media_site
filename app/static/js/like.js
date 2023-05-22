function like(id){
    fetch("/operations/"+id,{
        method:"POST"
    ,})
    .then(response=>response.json())
    .then(document.getElementById("like").innerHTML ="")
    .then(data => document.getElementById("like").innerHTML = data.vote)
    .catch(err => location.replace("/login/"))
}
