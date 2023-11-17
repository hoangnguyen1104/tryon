const d_upscale_image = document.querySelector(".upscale_image");
if (d_upscale_image !== null) {
    // upload image from local
    const dropArea = document.querySelector(".drag-area");
    const dragText = document.querySelector(".header");

    let button = dropArea.querySelector(".button");
    let input = dropArea.querySelector("input");

    let file;

    button.onclick = () => {
      input.click();
    };

    // when browse
    input.addEventListener("change", function () {
      file = this.files[0];
      dropArea.classList.add("active");
      displayFile();
    });

    // when file is inside drag area
    dropArea.addEventListener("dragover", (event) => {
      event.preventDefault();
      dropArea.classList.add("active");
      dragText.textContent = "Release to Upload";
      // console.log('File is inside the drag area');
    });

    // when file leave the drag area
    dropArea.addEventListener("dragleave", () => {
      dropArea.classList.remove("active");
      // console.log('File left the drag area');
      dragText.textContent = "Drag & Drop";
    });

    // when file is dropped
    dropArea.addEventListener("drop", (event) => {
      event.preventDefault();
      // console.log('File is dropped in drag area');

      file = event.dataTransfer.files[0]; // grab single file even of user selects multiple files
      // console.log(file);
      displayFile();
    });

    function displayFile() {
      let fileType = file.type;

      let validExtensions = ["image/jpeg", "image/jpg", "image/png"];

      if (validExtensions.includes(fileType)) {
        let fileReader = new FileReader();

        fileReader.onload = () => {
          let fileURL = fileReader.result;
          let image_upscale = dropArea.querySelector('.image_upscale');
          let select_image_up = dropArea.querySelector('.select_image_up');

          select_image_up.style.display = "none";
          image_upscale.style.display = "block";
          image_upscale.onload = function() {
              let upscale_image = document.querySelector(".upscale_image");
              let image_size = upscale_image.querySelector(".image_size");
              image_size.innerHTML = this.width + 'x' + this.height;
            }
          image_upscale.src = fileURL;
        };
        fileReader.readAsDataURL(file);
      } else {
        alert("This is not an Image File");
        dropArea.classList.remove("active");
      }
    }

    // action tai lai
    const upscale_image = document.querySelector(".upscale_image");
    let button_tai_lai = upscale_image.querySelector(".clear-image");
    button_tai_lai.onclick = () => {
        dropArea.classList.remove("active");
        let image_upscale = dropArea.querySelector('.image_upscale');
        let select_image_up = dropArea.querySelector('.select_image_up');
        image_upscale.style.display = "none";
        select_image_up.style.display = "contents";
    };

    // action process upscale
    let button_process_up = upscale_image.querySelector(".process_upscale_val");
    button_process_up.onclick = async () => {
        const toBase64 = file => new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.readAsDataURL(file);
            reader.onload = () => resolve(reader.result);
            reader.onerror = reject;
        });

          let image_upscale = input.files[0];
          let upscale_val = document.getElementById("upscale_val");
          try {
              const result = await toBase64(file);
              var xhr = new XMLHttpRequest();
              var url = 'https://api.example.com/data?image=' + result + '&scale=' + upscale_val.value;
              xhr.open('GET', url, true);

              xhr.onreadystatechange = function() {
                if (xhr.readyState === 4 && xhr.status === 200) {
                  var response = xhr.responseText;
                  // Process the response data as needed
                  console.log(response);
                }
              };

              xhr.send();
           } catch(error) {
              console.error(error);
           }
    };
}