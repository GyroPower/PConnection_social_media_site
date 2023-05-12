
function updateImageDisplay() {
    while(preview.firstChild) {
      preview.removeChild(preview.firstChild);
    }

    const curFiles = input.files;
    if (curFiles.length === 0) {
      const para = document.createElement('p');
      para.textContent = 'No files currently selected for upload';
      preview.appendChild(para);
    } else {


      for (const file of curFiles) {
        const listItem = document.createElement('li');
        const para = document.createElement('p');


          const image = document.createElement('img');
          image.src = URL.createObjectURL(file);
          image.classList.add("card-img")
          preview.appendChild(image);



      }
    }
  }




const input = document.getElementById('file');
const preview = document.querySelector('.preview');



input.addEventListener('change', updateImageDisplay);
