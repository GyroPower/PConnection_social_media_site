function delete_post(id){
    fetch("/operations/"+id,{
        method:"DELETE"
    ,})
    .then(response => response.json())
    .then(data=> document.getElementById("result").innerHTML = data.detail)
    .then(remove => document.getElementById(id).remove())
}
