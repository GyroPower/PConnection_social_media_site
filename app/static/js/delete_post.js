function delete_post(id){
    fetch("/votes/"+id,{
        method:"DELETE"
    ,})
    .then(response => response.json())
    .then(data=> document.getElementById("result").innerHTML = data.detail);
}
