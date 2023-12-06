const d_try_on = document.querySelector(".try_on_frame");
if (d_try_on !== null) {
    let changeModelButton = d_try_on.querySelector(".changeModelButton");
    changeModelButton.onclick = () => {
        let popup_change_model = document.querySelector(".popup_change_model");
        popup_change_model.style.display = 'contents';
        d_try_on.style.display = 'none';
    };

    let productImgContainer = d_try_on.querySelectorAll(".productImgContainer");
    for (let i = 0; i < productImgContainer.length; i++) {
        productImgContainer[i].onclick = () => {
            let e = productImgContainer[i].getElementsByTagName('input')[0];
            console.log(e);
            var myFormData = new FormData();
            myFormData.append('cloth_id', e.getAttribute("name"));
            myFormData.append('type_gallery', e.getAttribute("value"));
            myFormData.append('model_id', d_try_on.querySelector('.save-model-id').value);
            $.ajax({
              url: '/mkdir_cloth',
              type: 'POST',
              processData: false,
              contentType: false,
              dataType : 'json',
              data: myFormData,
              success: function(response) {
                var imageSrc = "data:" + response.content_type + ";base64," + response.image;
                var modelImg = d_try_on.querySelector('.modelImg');
                var image_to_download = d_try_on.querySelector('.image_to_download');
                var image_to_upscale = d_try_on.querySelector('.image_to_upscale');
                modelImg.src = imageSrc;
                image_to_download.value = imageSrc;
                image_to_upscale.value = imageSrc;
                console.log(image_to_download);
                console.log(image_to_upscale);
               },
               error: function (xhr, status, error) {
                console.log('xhr:', xhr);
                console.log('status:', status);
                console.log('error:', error);
               }
            });
        }
    }

    let selectCategory = d_try_on.querySelectorAll(".selectCategoryContainer");
    let garmentOptions = d_try_on.querySelector(".garmentOptions");
    let type_gallery = document.querySelector(".type-gallery");
    let list_cate_products = garmentOptions.querySelectorAll('.p-list');
    console.log(list_cate_products);
    for (let i = 0; i < selectCategory.length; i++) {
     selectCategory[i].onclick = () => {
            console.log(selectCategory[i].getAttribute("name"));
            type_gallery.value = selectCategory[i].getAttribute("name");
            let name = selectCategory[i].getAttribute("name");
            for (let j=0; j<list_cate_products.length; j++){
                list_cate_products[j].style.display = 'none';
                console.log(list_cate_products[j]);
                if (list_cate_products[j].getAttribute("id") == name){
                    list_cate_products[j].style.display = 'contents';
                    console.log(list_cate_products[j]);
                }
            }
        }
    }
}

const popup_change_model = document.querySelector(".popup_change_model");
if (popup_change_model !== null){
    let image_options = popup_change_model.querySelectorAll(".modelsImg");
    for (let i = 0; i < image_options.length; i++) {
      image_options[i].onclick = () => {
            var myFormData = new FormData();
            //var file = document.getElementsByClassName('i-upload-model')[0].files[0];
            myFormData.append('model_id', image_options[i].getAttribute("name"));
            $.ajax({
              url: '/mkdir_model',
              type: 'POST',
              processData: false,
              contentType: false,
              dataType : 'json',
              data: myFormData,
              success: function() {
                alert('Upload thành công!');
               },
               error: function () {
               }
            });
            d_try_on.querySelector('.save-model-id').value = image_options[i].getAttribute("name");
            d_try_on.querySelector('.modelImg').src = image_options[i].getElementsByTagName('input')[0].defaultValue;
            d_try_on.querySelector('.image_to_upscale').value = image_options[i].getElementsByTagName('input')[0].defaultValue;
            d_try_on.querySelector('.image_to_download').value = image_options[i].getElementsByTagName('input')[0].defaultValue;
            popup_change_model.style.display = 'none';
            d_try_on.style.display = 'contents';
        }
    }

    function saveData() {
        var myFormData = new FormData();
        var file = document.getElementsByClassName('i-upload-model')[0].files[0];
        myFormData.append('upload_files', file);
        $.ajax({
          url: '/upload_model',
          type: 'POST',
          processData: false,
          contentType: false,
          dataType : 'json',
          data: myFormData,
          success: function() {
            alert('Upload thành công!');
            location.reload();
           },
           error: function () {
            location.reload();
           }
        });
    }
    function selectOptionCloth(option) {
      var container = document.querySelector(".toggleGarmentContainer");
      var buttons = container.querySelectorAll(".option");
      console.log(buttons);
      for (var i = 0; i < buttons.length; i++) {
        buttons[i].classList.remove("selected");
      }

      var selectedButton = container.querySelector(".option:nth-child(" + option + ")");
      selectedButton.classList.add("selected");
      let type_gallery = document.querySelector(".type-gallery").value;
      let your_cloth = document.querySelector(".tops_your_gallery");
      let system_cloth = document.querySelector(".tops_system_gallery");
      if (type_gallery == "bottoms"){
        your_cloth = document.querySelector(".bottoms_your_gallery");
        system_cloth = document.querySelector(".bottoms_system_gallery");
      }
      if (option==1){
        your_cloth.style.display = 'block';
        system_cloth.style.display = 'none';
      }
      if (option==2){
        your_cloth.style.display = 'none';
        system_cloth.style.display = 'block';
      }
    }

    function selectOptionModel(option) {
      var container = document.querySelector(".modelsFrame");
      var buttons = container.querySelectorAll(".option");
      for (var i = 0; i < buttons.length; i++) {
        buttons[i].classList.remove("selected");
      }

      var selectedButton = container.querySelector(".option:nth-child(" + option + ")");
      selectedButton.classList.add("selected");
      let your_model = document.querySelector(".your_model");
      let system_model = document.querySelector(".system_model");
      if (option==1){
        your_model.style.display = 'flex';
        system_model.style.display = 'none';
      }
      if (option==2){
        your_model.style.display = 'none';
        system_model.style.display = 'flex';
      }
    }


    function showModal() {
      var modal = document.getElementById('imageSizeModal');
      modal.style.display = 'block';
    }

    // Function to handle the confirm button click event
    function handleConfirmButtonClick() {
      // Get the selected image size
      var imageSizeSelect = document.getElementById('imageSizeSelect');
      var imageSize = imageSizeSelect.value;
      console.log(imageSize, "imageSize");

      // Hide the modal
      var modal = document.getElementById('imageSizeModal');
      modal.style.display = 'none';

      var myFormData = new FormData();
        var modelImg = d_try_on.querySelector('.modelImg');
        var file = modelImg.src
        myFormData.append('upload_files', file);
        myFormData.append('imageSize', imageSize);
        $.ajax({
          url: '/download_result',
          type: 'POST',
          processData: false,
          contentType: false,
          dataType : 'json',
          data: myFormData,
          success: function() {
           },
           error: function () {
           }
        });
    }

    // Function to handle the cancel button click event
    function handleCancelButtonClick() {
      var modal = document.getElementById('imageSizeModal');
      modal.style.display = 'none';
    }

    // Function to handle the cancel button click event
    function handleConfirmUpscale() {
      var modelImg = d_try_on.querySelector('.modelImg');
      var file = modelImg.src;
      var myFormData = new FormData();
      myFormData.append('file', file);
      $.ajax({
          url: '/upscale',
          type: 'POST',
          processData: false,
          contentType: false,
          dataType : 'json',
          data: myFormData,
          success: function(response) {
            $('#targetElement').html(response);
           },
           error: function (response) {
               $('#targetElement').html(response);
           }
        });
    }


    // Add click event listener to the download button
    var downloadButton = document.getElementById('downloadButton');
    downloadButton.addEventListener('click', showModal);

    // Add click event listener to the confirm button in the modal
    var confirmButton = document.getElementById('confirmButton');
    //confirmButton.addEventListener('click', handleConfirmButtonClick);

    // Add click event listener to the confirm button in the modal
    var cancelButton = document.getElementById('cancelButton');
    cancelButton.addEventListener('click', handleCancelButtonClick);

    // Add click event listener to the confirm button in the modal
    var confirmUpscale = document.getElementById('confirmUpscale');
    confirmUpscale.addEventListener('click', handleConfirmUpscale);
}