async function get_comments_for_post(id){
    const response = await fetch("/operations/comments/"+id,{
        method:"GET",
    });

    const data = await response.json();


    for (const comment in data.comments){

        const div_comment = document.createElement("div")

        div_comment.classList.add("card-body","text-left")
        div_comment.id = ""+data.comments[comment].id

        let content = document.getElementById("content_comment");

        let text=document.createTextNode(data.comments[comment].username);
        let username = document.createElement("a");
        username.appendChild(text);
        username.classList.add("text-light");
        username.href = "/user-info/"+data.comments[comment].user_id;
        div_comment.appendChild(username);
        let para = document.createElement("p");
        para.classList.add("text-light");
        text = document.createTextNode(data.comments[comment].content);
        para.appendChild(text);
        div_comment.appendChild(para);

        content.appendChild(div_comment)


    }
}
