async function update_comment(id)
{
    const form = document.getElementById("edit");

    form.addEventListener("submit",async function(f){

        f.preventDefault();

        const payload = new FormData(form);

        const response = await fetch("/operations/comments/"+id,{
            method:"PUT",
            body: payload,
        });

        const data = await response.json();
        console.log(data.data)

        if (data.data == "updated"){
            const para = document.createElement("p")
            const text = document.createTextNode(data.content)
            console.log(data.content)
            para.appendChild(text)
            para.classList.add("text-light")

            const div_comment_cont = document.getElementById("div_comment_cont"+id)
            form.remove()

            div_comment_cont.appendChild(para)




        }
    })


}

function edit_comment(id){

    let para = document.getElementById("content"+id);


    const textarea = document.createElement("textarea")

    textarea.style.resize ="none"
    textarea.style.border = "none"
    textarea.classList.add("bg-dark","text-light")
    textarea.id = "content"+id
    textarea.name = "content"

    let text = document.createTextNode(para.textContent)
    textarea.appendChild(text)


    console.log(para.textContent)

    para.remove()
    const div_comment_cont = document.getElementById("div_comment_cont"+id)
    let form = document.createElement("form")
    form.id = "edit"
    form.method="POST"

    const div_textarea = document.createElement("div")
    div_textarea.appendChild(textarea)

    form.appendChild(div_textarea)
    div_comment_cont.appendChild(form)

    const div_button = document.createElement("div")
    let submit_button = document.createElement("button")
    text = document.createTextNode("Edit")
    submit_button.appendChild(text)
    submit_button.classList.add("btn","btn-light")
    submit_button.type="submit"
    div_button.appendChild(submit_button)
    form.appendChild(div_button)
    textarea.focus();
    submit_button.onclick = function(){update_comment(id)}






}
