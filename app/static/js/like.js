function like(id){
    fetch("/votes/"+id,{
        method:"POST"
    ,})
    .then(response=>response.json())
    .then(document.getElementById(id).innerHTML ="")
    .then(data => document.getElementById(id).innerHTML = data.vote)
    .catch(err => location.replace("/login/"))
}
