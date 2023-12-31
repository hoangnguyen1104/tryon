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
        if (file != null){
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
                  console.log(image_size);
                }
              image_upscale.src = fileURL;
            };
            fileReader.readAsDataURL(file);
          } else {
            alert("This is not an Image File");
            dropArea.classList.remove("active");
          }
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
        document.querySelector(".input_image_size").innerHTML = '';
        document.querySelector(".image_size").innerHTML = '';
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
          console.log("image_upscale", image_upscale);
          console.log(document.querySelector(".image_upscale").src);
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


const t_upscale = document.querySelector(".upload-result");
if (t_upscale !== null) {
    // upload image from local
    const dropArea = document.querySelector(".drag-area");
    const dragText = document.querySelector(".header");

    let button = dropArea.querySelector(".button");
    let input = dropArea.querySelector(".i-upload");

    let file;

    button.onclick = () => {
      input.click();
    };

    // when browse
    if (input != null)
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
        if (file != null){
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
              image_upscale.src = fileURL;
              var image = new Image();
              image.onload = function() {
                    var width = this.width;
                    var height = this.height;
                    document.querySelector(".image_size").innerHTML = width + 'x' + height;
                };
              image.src = fileURL;
              document.querySelector(".origin_image_upscale").src = fileURL;
              document.querySelector(".is-upload-image").value = 'true';
            };
            fileReader.readAsDataURL(file);
          } else {
            alert("This is not an Image File");
            dropArea.classList.remove("active");
          }
        }

    }

    // action tai lai
    const upscale_image = document.querySelector(".t_upscale");
    let button_tai_lai = upscale_image.querySelector(".clear-image");
    button_tai_lai.onclick = () => {
        dropArea.classList.remove("active");
        let image_upscale = dropArea.querySelector('.image_upscale');
        let select_image_up = dropArea.querySelector('.select_image_up');
        image_upscale.style.display = "none";
        select_image_up.style.display = "contents";
        document.querySelector(".input_image_size").innerHTML = '';
        document.querySelector(".image_size").innerHTML = '';
    };

    // action btn_toggle_origin
    let btn_toggle_origin = upscale_image.querySelector(".btn_toggle_origin");
    btn_toggle_origin.onclick = () => {
        document.querySelector(".image_upscale").src = document.querySelector(".origin_image_upscale").src;
    };

    // action process upscale
    let button_process_up = upscale_image.querySelector(".process_upscale_val");
    button_process_up.onclick = () => {
          let upscale_val = document.getElementById("upscale_val");
          var myFormData = new FormData();
          if (document.querySelector(".is-upload-image").value == 'true'){
            myFormData.append('is-upload-image', 'true');
          }
          document.querySelector(".is-upload-image").value = false;
          const result2 = document.querySelector(".origin_image_upscale").src;
          myFormData.append('image', result2);

          myFormData.append('scale', upscale_val.value);
          myFormData.append('res_id', 'null');

          $.ajax({
              url: '/to_upscale',
              type: 'POST',
              processData: false,
              contentType: false,
              dataType : 'json',
              data: myFormData,
              success: function(response) {
                console.log('xhr:', response.image);
                var imageSrc = "data:" + response.content_type + ";base64," + response.image;
                var image_upscale = document.querySelector('.image_upscale');
                var image = new Image();
                  image.onload = function() {
                    var width = this.width;
                    var height = this.height;
                    document.querySelector(".input_image_size").innerHTML = width + 'x' + height;
                };
                image.src = imageSrc;
                image_upscale.src = imageSrc;
               },
               error: function (xhr, status, error) {
                console.log('xhr:', xhr);
                console.log('status:', status);
                console.log('error:', error);
               }
            });
    };

    let available_items = upscale_image.querySelectorAll(".available-item");
    for (let i = 0; i < available_items.length; i++) {
        available_items[i].onclick = () => {
            let e = available_items[i].getElementsByTagName('img')[0];
            console.log(e.src);
            document.querySelector(".select_image_up").style.display = 'none';
            document.querySelector(".origin_image_upscale").src = e.src;
            document.querySelector(".image_upscale").src = e.src;
            document.querySelector(".image_upscale").style.display = 'block';
            document.querySelector(".is-upload-image").value = false;

        }
    }
}