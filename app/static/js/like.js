function like(id){
    fetch("/votes"+id,{
        method:"POST"
    ,})
    .then(response=>response.json())
    .then(document.getElementById("vote").innerHTML ="")
    .then(data => document.getElementById("vote").innerHTML = data.vote)
}
