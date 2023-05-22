
async function post_a_comment(id){

    const form = document.getElementById("form")

    form.addEventListener("submit",async function(f){
        f.preventDefault();

        const payload = new FormData(form);


        const response = await fetch("/operations/comment/"+id,{
            method: "POST",
            body:payload
        });

        const data= await response.json();


        console.log(data.username)

        let textarea = document.getElementById("comment")
        textarea.value="";
        let content = document.getElementById("content_comment");
        let text=document.createTextNode(data.username);
        let username = document.createElement("a");
        username.appendChild(text);
        username.classList.add("text-light");
        username.href = "/user_info/"+data.user_id;
        content.appendChild(username);
        let para = document.createElement("p");
        para.classList.add("text-light");
        text = document.createTextNode(data.data);
        para.appendChild(text);
        content.appendChild(para);



    })
}
