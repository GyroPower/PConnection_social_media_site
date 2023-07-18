async function get_current_user(){
    const response = await fetch("/user/",{
        method:"GET",
    })

    const data = await response.json()

    return data.user_id
}



async function post_a_comment(id){

    const form = document.getElementById("form")

    form.addEventListener("submit",async function(f){
        f.preventDefault();

        const payload = new FormData(form);


        const response = await fetch("/operations/comment/"+id,{
            method: "POST",
            body:payload
        });

        const data = await response.json();

            //seeing if the current user is the autor of the comment
        const user =await get_current_user();


        //creating the div for the comment
        const div_comment = document.createElement("div")
        //div for the content of the comment
        const div_comment_cont = document.createElement("div")
        div_comment.classList.add("card-body","text-left")
        div_comment.id = ""+data.id

        //the div where to put the div which contains the comment info, the username and the content
        let content = document.getElementById("content_comment");

        //div which contains the link to the user and the options if the current user is the autor
        const div_comment_user = document.createElement("div")
        div_comment_user.classList.add("row")

        const div_username = document.createElement('div')
        div_username.classList.add("col")
        div_comment_user.appendChild(div_username)
        //creating the a etiquet for redirect to the user info of the autor
        let text=document.createTextNode(data.username);
        let username = document.createElement("a");
        username.appendChild(text);
        username.classList.add("text-light");
        username.href = "/user-info/"+data.user_id;

        div_username.appendChild(username);
        div_comment.appendChild(div_comment_user)



        if (user == data.user_id){
            const div_options = document.createElement("div");
            div_options.classList.add("col","text-right","vav-item","dropdown");
            div_comment_user.appendChild(div_options);

            const fake_button_dropdown = document.createElement("a");
            fake_button_dropdown.classList.add("nav-link","dropdown-toggle");
            fake_button_dropdown.role="button";
            fake_button_dropdown.href="#";
            fake_button_dropdown.id="navbarDropdownC";


            div_options.appendChild(fake_button_dropdown)

            const div_list_options = document.createElement("ul")
            div_list_options.classList.add("dropdown-menu","dropdown-menu-dark","text-center")
            div_list_options.style.width="10:rem";

            div_options.appendChild(div_list_options)

            const edit_list_option = document.createElement("li")
            const button_edit = document.createElement("button")

            let text_on_widget = document.createTextNode("Edit")
            button_edit.appendChild(text_on_widget)
            button_edit.type="button"
            button_edit.onclick = function(){update_comment(data.id)}
            button_edit.classList.add("dropdown-item")
            edit_list_option.appendChild(button_edit)

            const delete_list_option = document.createElement("li")
            const button_delete = document.createElement("button")

            text_on_widget = document.createTextNode("Delete")
            button_delete.appendChild(text_on_widget)
            button_delete.type="button"
            button_delete.onclick=function(){f_delete_comment(data.id)}
            button_delete.classList.add("dropdown-item")
            delete_list_option.appendChild(button_delete)

            div_list_options.appendChild(edit_list_option)
            div_list_options.appendChild(delete_list_option)

        }


        //the textarea which contains the content of the comment
        let para = document.createElement("p");
        text = document.createTextNode(data.data);
        para.appendChild(text);
        para.classList.add("bg-dark","text-light")


        div_comment_cont.appendChild(para);
        div_comment.appendChild(div_comment_cont);

        content.appendChild(div_comment);

        $(".dropdown-toggle").dropdown();

    })

}
