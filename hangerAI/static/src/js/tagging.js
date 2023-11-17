odoo.define('website.tagging', function (require) {
    'use strict';
    var ajax = require('web.ajax');
    const d_image_tagging = document.querySelector(".image_tagging");
    if (d_image_tagging !== null) {
        let tai_anh = d_image_tagging.querySelector(".btn-upload");
        let input = d_image_tagging.querySelector(".i_upload");
        tai_anh.onclick = () => {
          input.click();
        };
        // when browse
        input.addEventListener("change", function () {
          var file = this.files[0];
          if (file != null) displayFile(file);
        });

        function displayFile(file) {
          let fileType = file.type;

          let validExtensions = ["image/jpeg", "image/jpg", "image/png"];

          if (validExtensions.includes(fileType)) {
            let fileReader = new FileReader();

            fileReader.onload = () => {
              let fileURL = fileReader.result;
              let image = d_image_tagging.querySelector('.e_image_tagging');
              image.src = fileURL;
              image.style.display = "block";
              let image_container = d_image_tagging.querySelector('.image-container');
              image_container.style.height = "unset";
            };
            fileReader.readAsDataURL(file);

            // call model tagging
            const handleSubmit = async (upload_file) => {
                const url = 'https://f674-42-114-127-65.ngrok-free.app/upload_image/';
                var formData = new FormData();
                formData.append("input_image", upload_file);
                const config = {
                  headers: {
                    "Content-Type": "multipart/form-data"
                  },
                };

                $.ajax({
                    url: 'https://d7b7-2a09-bac5-d45b-16dc-00-247-a6.ngrok-free.app/upload_image/',
                    type: "POST",
                    data: formData,
                    processData: false,
                    contentType: false,
                    success: function(response){
                        // Handle success response
                        var details = ``;
                        for (const image in response){
                            var names = []
                            let idx = 0;
                            for (const item in response[image]){
                                var data = response[image][item];
                                var table = `<table id="product-${idx}" style="display:none;">`
                                idx += 1;
                                table += `
                                    <tr>
                                      <td class="td-name">supercategory</td>
                                      <td class="td-content">${data.supercategory}</td>
                                    </tr>
                                `
                                var attribute_info = data.attribute_info;
                                for (var attr in attribute_info){
                                    table += `
                                        <tr>
                                          <td class="td-name">${attr}</td>
                                          <td class="td-content">${attribute_info[attr]}</td>
                                        </tr>
                                    `
                                }
                                table += `</table>`;
                                details += table;
                                names.push(data.name);
                            }
                        }
                        let details_info = d_image_tagging.querySelector('.details_info');
                        details_info.innerHTML = details;
                        let d_list_p = d_image_tagging.querySelector('.list-product');
                        let tmp = `<ul class="horizontal-menu">`;
                        for (var i in names){
                            tmp += `<li class="li_label" id="product-${i}">
                                        <a href="#" class="p_label_btn" id="${names[i]}">${names[i]}</a>
                                    </li>`
                        }
                        tmp += `</ul>`;
                        d_list_p.innerHTML = tmp

                        // add event
                        let li_labels = d_image_tagging.querySelectorAll("li");
                        for (let i=0; i<li_labels.length; i++){
                            let click_id = li_labels[i].getAttribute("id");
                            li_labels[i].onclick = () => {
                                let table_details = d_image_tagging.querySelectorAll("table");
                                for (let j=0; j<table_details.length; j++){
                                    if (table_details[j].getAttribute("id") == click_id){
                                        table_details[j].style.display = 'contents';
                                    }
                                    else{
                                        table_details[j].style.display = 'none';
                                    }
                                }
                            }
                        }
                    },
                    error: function(xhr, textStatus, error){
                        // Handle error response
                    }
                });

//                const response = await ajax.post(url, formData, config);
//                var result = response.data;
//                console.log(result);
            }
            handleSubmit(file);
          } else {
            alert("This is not an Image File");
          }
        }
    }
});