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
            console.log(productImgContainer[i].getElementsByTagName('input')[0]);
            console.log(productImgContainer[i].getElementsByTagName('input')[0].defaultValue);
        }
    }

    let selectCategory = d_try_on.querySelectorAll(".selectCategoryContainer");
    let garmentOptions = d_try_on.querySelector(".garmentOptions");
    let list_cate_products = garmentOptions.querySelectorAll('.p-list');
    console.log(list_cate_products);
    for (let i = 0; i < selectCategory.length; i++) {
     selectCategory[i].onclick = () => {
            console.log(selectCategory[i].getAttribute("name"));
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
            d_try_on.querySelector('.modelImg').src = image_options[i].getElementsByTagName('input')[0].defaultValue;
            popup_change_model.style.display = 'none';
            d_try_on.style.display = 'contents';
        }
    }

    function saveData() {
        var myFormData = new FormData();
        var file = document.getElementsByClassName('i-upload-model')[0].files[0];
        myFormData.append('upload_files', file);
        console.log(file, "ancddd")
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
    function selectOption(option) {
      var buttons = document.getElementsByClassName("option");
      for (var i = 0; i < buttons.length; i++) {
        buttons[i].classList.remove("selected");
      }

      var selectedButton = document.querySelector(".option:nth-child(" + option + ")");
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
}