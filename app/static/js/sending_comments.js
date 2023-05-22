
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

        const div_comment = document.createElement("div")

        div_comment.classList.add("card-body","text-left")
        div_comment.id = ""+data.id

        let content = document.getElementById("content_comment");

        let text=document.createTextNode(data.username);
        let username = document.createElement("a");
        username.appendChild(text);
        username.classList.add("text-light");
        username.href = "/user-info/"+data.user_id;
        div_comment.appendChild(username);
        let para = document.createElement("p");
        para.classList.add("text-light");
        text = document.createTextNode(data.data);
        para.appendChild(text);
        div_comment.appendChild(para);

        content.appendChild(div_comment)



    })
}
