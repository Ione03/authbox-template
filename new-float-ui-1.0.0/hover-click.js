// Create a tooltip element
// 2025 Agustus 30
// Authbox.web.id

// function refresh_mode(element_id, modal_title, modal_code, modal_type, tooltip) {
//     const m_object = document.getElementById("main-1");
//     m_object.innerHTML = '<span data-modal-code="bi-icon-70" data-modal-title="bi-arrow-up-short" data-modal-type="icon" data-tooltip="Link ini hanya tampil di mode edit. Silahkan klik untuk mengedit data!">TEST 123</span>'    
// };
// const modalbtn = "";
// const modal = null;
// let csrftoken = "";

const modalCache = new Map();

// Versi 2
// Preload modal in background
function loadModal(modalFile, modalContainerId) {
    if (modalCache.has(modalFile)) {
        html = modalCache.get(modalFile);
        console.log('Load from cache:', modalFile);
        document.getElementById(modalContainerId).innerHTML = html;
        return;
    };

    // This will run in the background
    setTimeout(() => {
        // Use fetch with low priority
        fetch(modalFile, { priority: 'low' })
            .then(response => {
                if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
                return response.text();
            })
            .then(html => {
                modalCache.set(modalFile, html);
                console.log('Modal preloaded in background:', modalFile);
                document.getElementById(modalContainerId).innerHTML = html;
            })
            .catch(error => {
                console.error('Background preloading failed:', error);
            });
    }, 1000);    
   
    
    // (async () => {
    //     try {
    //         // Use fetch with low priority
    //         fetch(modalFile, { priority: 'low' })
    //             .then(response => {
    //                 if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    //                 return response.text();
    //             })
    //             .then(html => {
    //                 modalCache.set(modalFile, html);
    //                 console.log('Modal preloaded in background:', modalFile);
    //                 document.getElementById(modalContainerId).innerHTML = html;
    //             })
    //             .catch(error => {
    //                 console.error('Background preloading failed:', error);
    //             });
    //     } catch (error) {
    //         console.error("Error in background task:", error);
    //     }
    // })();
    console.log("Show this imidiately");
};

// Function to load modal from external file

// Versi 1 (jalan cuma lama!!)
// async function loadModal(modalFile, modalContainerId) {
//   try {
//     const response = await fetch(modalFile);
//     const html = await response.text();
//     document.getElementById(modalContainerId).innerHTML = html;
//     // modalbtn = document.getElementById('sendRequest');
//     console.log('Modal loaded successfully');
//     //alert('Modal loaded successfully');
//   } catch (error) {
//     console.error('Error loading modal:', error);
//     //alert('Error loading modal ' + error);
//   }
// };
// Load modal when needed
// function loadModalWithJQuery(modalFile, modalId) {
//   $('#modal-container').load(modalFile, function() {
//     $(modalId).modal('show');
//   });
// }
function send_request_ajax() {
    // alert('OKE');
    const csrftoken = getCookie('csrftoken');
    const form = document.querySelector('#infoForm');
    // const data = { username: 'RinaPuspita6', email: 'test@example.com' };
    // tidak ada /id di depannya, maka error (pastikan definisi URL benar)

    // const fileInput = document.getElementById('value_image');
    // const file = fileInput.files[0];

    const formData = new FormData(form);
    let modal_code = '';

    // let formContents = '';
    for (let [key, value] of formData.entries()) {
        // formContents += `${key}: ${value}\n`;
        if (`${key}`=='modalCode') {
            modal_code=`${value}`;
            break;
        }
    };
    // console.log('modal_code', modal_code);
    
    const fileInput = document.getElementById('value_image');
    const hasFile = fileInput.files.length > 0;

    // formData.append('image', file);
    // const jsonData = Object.fromEntries(formData.entries());
    // console.log('formData', jsonData);
    if (hasFile) {
        fetch('/id/api/post-direct-update/', {
                method: 'POST',
                headers: {
                    // 'Content-Type': 'application/json', // Bedanya disini (jika ini diaktifkan maka error saat upload image)
                    // header type otomatis dipiliah saat menggunakan FormData()
                    'X-CSRFToken': csrftoken
                },
                body: formData                 
        })
        .then(response => {
            // console.log('Response status:', response.status); // Log the response status
            
            if (!response.ok) {
                throw new Error(`HTTP error! Status: FAIL`);
            };
            // alert(response.json());
            return response.json();
        })
        .then(data => {
            // alert('Update disini' + data);
            // alert('Data received: ' + JSON.stringify(data, null, 2)); // Log the received data
            // alert('Data received: ' + data); // Log the received data        
        })
        .catch(error => {
            console.log('Error:' + error.message);
        });
    } else {
        // If no file, convert to JSON and send as application/json
        const jsonData = Object.fromEntries(formData.entries());
        // console.log('JSON Data:', jsonData);
        
        fetch('/id/api/post-direct-update/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify(jsonData)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            };
            // tmp = response.json()
            // console.log(tmp);
            return response.json();
        })
        .then(data => {
            const data_json = JSON.stringify(data, null, 2)
            // console.log('update disini:' + data_json);

            const jsonObject = JSON.parse(data_json);
            // console.log('jsonObject:' + jsonObject);

            const valueText = jsonObject.Data.value_text;
            // console.log(valueText); // outputs: desired_value

            const m_elem = document.getElementById(modal_code);
            m_elem.innerHTML = valueText;
            m_elem.setAttribute('data-modal-title',valueText);
            // statusDiv.textContent = 'Form data sent successfully!';
            // statusDiv.className = 'status success';
            // statusDiv.style.display = 'block';
        })
        .catch(error => console.error('Error:', error));

        // .catch(error => {
            // statusDiv.textContent = 'Error: ' + error.message;
            // statusDiv.className = 'status error';
            // statusDiv.style.display = 'block';
        // });

    };

};

function slugifyCaseSensitive(str) {
  return str
    .replace(/[^a-zA-Z0-9\s]/g, '') // Remove special characters
    .trim()                         // Remove leading/trailing spaces
    .replace(/\s+/g, '-')           // Replace spaces with dashes
    .replace(/-+/g, '-');           // Remove duplicate dashes
};

// const slugify = (string) =>
//   string
//     .toLowerCase()
//     .trim()
//     .replace(/[^a-z0-9\s-]/g, '') // Remove unwanted characters
//     .replace(/\s+/g, '-') // Replace spaces with hyphens
//     .replace(/-+/g, '-'); // Remove extra hyphens

function get_request_ajax(code) {
    // get ajax but using POST
    // GET tidak bisa menerima karakter khusus karna data lewat URL atau parameter
    // Jadi tetap menggunakan ajax yg sama seperti send_request_ajax
    const csrftoken = getCookie('csrftoken');
    const elem = document.getElementById(code);    
    const m_type = elem.getAttribute('data-modal-type');
    const m_title = elem.getAttribute('data-modal-title');

    const formData = new FormData();
    formData.append('modalCode', code);
    formData.append('modalType', m_type);
    formData.append('modalTitle', m_title); // m_title tidak berfungsi, untuk ul dan image
        
    // const queryString = new URLSearchParams(formData).toString();
    if (m_type=='image')
        console.log('Tipe Image!');
    else {
        console.log('Tipe Selain Image!');
        const jsonData = Object.fromEntries(formData.entries());
        console.log('jsondata', jsonData);

        fetch('/id/api/get-direct-update/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json', // Bedanya disini (jika ini diaktifkan maka error saat upload image)
                    // header type otomatis dipiliah saat menggunakan FormData()
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify(jsonData)
        })
        .then(response => {
            // console.log('Response status:', response.status); // Log the response status
            
            if (!response.ok) {
                throw new Error(`HTTP error! Status: FAIL`);
            };
            // alert(response.json());
            return response.json();
        })
        .then(data => {
            const data_json = JSON.stringify(data, null, 2)
            // alert('Update disini:' + JSON.stringify(data, null, 2));
            // alert('Data received: ' + JSON.stringify(data, null, 2)); // Log the received data
            // alert('Data received: ' + data); // Log the received data        
            const jsonObject = JSON.parse(data_json);
            // console.log('jsonObject:' + jsonObject);

            const valueText = jsonObject.Data.value_text;
            // console.log(valueText); // outputs: desired_value

            // const m_elem = document.getElementById(code);
            // m_elem.innerHTML = valueText;
            // m_elem.setAttribute('data-modal-title',valueText);


            elem.innerHTML = valueText;
            elem.setAttribute('data-modal-title',valueText);
            
        })
        .catch(error => {
            console.log('Error:' + error.message);
        });    
    }
};

// function ini tidak digunakan!
function get_ajax_data(code) {
    // digunakan untuk refresh awal data di frontend sesuai dengan data id (di manifest.json)

    const elem = document.getElementById(code);
    // const m_code = code;
    const m_type = elem.getAttribute('data-modal-type');
    const m_title = elem.getAttribute('data-modal-title');
    // const queryString = new URLSearchParams(m_code + '/' + m_type + '/' + m_title + '/').toString();
    // console.log('queryString' + queryString);

    // console.log(elem);
    // console.log('title=' + elem.getAttribute('data-modal-title'));
    // console.log('type=' + elem.getAttribute('data-modal-type'));

    // Create a FormData object
    // cara ini OKE (tapi ada kemungkinan di hack)
    // const formData = new FormData();
    // formData.append('code', m_code);
    // formData.append('type', m_type);
    // formData.append('title', m_title);
    // // fetch('/id/api/get-direct-update/?' + queryString, {

    // const formData = new FormData();
    // formData.append('username', 'john');
    // formData.append('avatar', fileInput.files[0]);


    
    // const queryString = new URLSearchParams(formData).toString();
    // if m_type=='image':
    //     print('Tipe Image')
    // else:
    const jsonData = Object.fromEntries(formData.entries());
    fetch('/id/api/post-direct-update/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json', // Bedanya disini (jika ini diaktifkan maka error saat upload image)
                // header type otomatis dipiliah saat menggunakan FormData()
                'X-CSRFToken': csrftoken
            },
            // body: formData                 
    })
    .then(response => {
        // console.log('Response status:', response.status); // Log the response status
        
        if (!response.ok) {
            throw new Error(`HTTP error! Status: FAIL`);
        };
        // alert(response.json());
        return response.json();
    })
    .then(data => {
        // alert('Update disini:' + JSON.stringify(data, null, 2));
        // alert('Data received: ' + JSON.stringify(data, null, 2)); // Log the received data
        // alert('Data received: ' + data); // Log the received data        
    })
    .catch(error => {
        console.log('Error:' + error.message);
    });
};

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie) {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            if (cookie.trim().startsWith(name + '=')) {
                cookieValue = cookie.trim().substring(name.length + 1);
            }
        }
    }
    return cookieValue;
};

    
document.addEventListener("DOMContentLoaded", () => {
    // Hover
    const tooltip = document.getElementById('custom-tooltip');
    const hoverables = document.querySelectorAll('.hoverable');  
    
    // const csrftoken = getCookie('csrftoken');
    
    // console.log('csrftoke ' + csrftoken);
    console.log('Before query run');
    const get_all_id = document.querySelectorAll('.hoverable-mark');  
    // console.log('get all id', get_all_id);

    setTimeout(() => {
        get_all_id.forEach(element => {
            console.log('Element ' + element['id']);    // dengan cara ini, maka tidak perlu manifest.json
            // get_ajax_data(element['id']); // tidak digunakan function ini
            get_request_ajax(element['id']);
        });
    }, 1000); 

    console.log('this is emediate run');

    // get_request_ajax('6-hero-2');
    // Modal
    // const modal = new bootstrap.Modal(document.getElementById('myModal'));
    // console.log('modal',modal);
    // const modal = document.getElementById('myModal');
    // const modalTitle = document.getElementById('modalTitle');
    // const modalCode = document.getElementById('modalCode');
    // const modalType = document.getElementById('modalType');
    // const closeBtn = document.querySelector('.close');
    // const infoForm = document.getElementById('infoForm');

    // $('#infoModal').on('shown.bs.modal', function () {
    //     $(this).find('input:visible:first').focus();
    // });
    
    // console.log('modal button = ' +  modalbtn);
    // modalbtn.addEventListener('click', e => {
    //     e.preventDefault();
    //     alert('ajax send!');
    // });                

    // Track mouse movement for tooltip
    document.addEventListener('mousemove', (e) => {
        // console.log('Mouse moved:', e.pageX, e.pageY);
        if (tooltip.classList.contains('visible')) {
            tooltip.style.left = (e.pageX + 15) + 'px';
            tooltip.style.top = (e.pageY + 15) + 'px';
        }
    });

    // Tooltip functionality
    hoverables.forEach(element => {
        // Mouse enter - show tooltip
        element.addEventListener('mouseenter', (e) => {
            // console.log('Mouse entered:', e.target);
            const text = element.getAttribute('data-tooltip');
            tooltip.textContent = text;
            tooltip.classList.add('visible');
            tooltip.style.left = (e.pageX + 15) + 'px';
            tooltip.style.top = (e.pageY + 15) + 'px';
        });

        // Mouse leave - hide tooltip
        element.addEventListener('mouseleave', () => {
            tooltip.classList.remove('visible');
        });

        // Click - open modal
        element.addEventListener('click', (e) => {
            e.stopPropagation();
            // disini OK tapi saat klik pertama tidak muncul
            // loadModal('/media/smooth-modal.html', 'modal-container');
            // data-modal-code="6-hero-2" 
            // data-modal-title="Working for your success" 
            // data-modal-type="text" 

            // console.log('Element clicked:', e.target);
            // If you want to use the modal, uncomment the following lines
            // const modal = new bootstrap.Modal(document.getElementById('myModal'));
            // const title = element.getAttribute('data-modal-title') || 'Information Form';
            // const code = element.getAttribute('data-modal-code') || 'main-0';
            // const type = element.getAttribute('data-modal-type') || 'text';
            // modalTitle.textContent = title;
            // // modalCode.textContent = code;
            // modalType.value = type;
            // modalCode.value = code;
            // openModal();
            // alert('show me first');
            // console.log('modal', myModal);
            // const modal = new bootstrap.Modal(document.getElementById('myModal'));
            var myModal = new bootstrap.Modal(document.getElementById('myModal'));  
            // alert(element.getAttribute('data-modal-title'));
            const title = element.getAttribute('data-modal-title') || 'Information Form';
            const code = element.getAttribute('data-modal-code') || 'main-0';
            const type = element.getAttribute('data-modal-type') || 'text';
            // console.log('Attribute value' + ' ' + title + ' ' + code + ' ' + type);
            const modalTitle = document.getElementById('modalTitle');
            modalTitle.value = title;
            const modalCode = document.getElementById('modalCode');
            modalCode.value = code;
            const modalType = document.getElementById('modalType');
            modalType.value = type;      
            
            // copy ke input user
            // aktifkan 1 komponen saja
            if ((type=='text') || (type=='icon')) {
                // tag div ini (modal-text) dkk
                document.getElementById('modal-text').classList.remove('d-none');
                document.getElementById('modal-textarea').classList.add('d-none');
                document.getElementById('modal-image').classList.add('d-none');
                document.getElementById('value_text').value = title;
            }
            else if ((type=='unordered-list') || (type=='nav-bar'))  {
                document.getElementById('modal-text').classList.add('d-none');
                document.getElementById('modal-textarea').classList.remove('d-none');
                document.getElementById('modal-image').classList.add('d-none');
                document.getElementById('value_textarea').value = title;
            }
            else if (type=='image')  {
                document.getElementById('modal-text').classList.add('d-none');
                document.getElementById('modal-textarea').classList.add('d-none');
                document.getElementById('modal-image').classList.remove('d-none');
                // document.getElementById('value_text').value = title; (image pending)
            };
            

            myModal.show();
            // loadModalWithJQuery('smooth-modal.html', 'modal-container');
        });
    });

    // document.getElementById('myModal').addEventListener('hidden.bs.modal', function () {
    //     myModal.dispose();
    // });

    // Modal functions
    // function openModal() {
    //     modal.classList.add('show');
    //     document.body.style.overflow = 'hidden';
    //     tooltip.classList.remove('visible');
    // }

    // function closeModal() {
    //     modal.classList.remove('show');
    //     document.body.style.overflow = '';
    // }

    // Close modal events
    // closeBtn.addEventListener('click', closeModal);

    // window.addEventListener('click', (e) => {
    //     if (e.target === modal) {
    //         closeModal();
    //     }
    //     tooltip.classList.remove('visible');
    // });

    // document.addEventListener('keydown', (e) => {
    //     if (e.key === 'Escape') {
    //         closeModal();
    //     }
    // });

    // Form submission
    // infoForm.addEventListener('submit', (e) => {
    //     e.preventDefault();
        
    //     const formData = {
    //         name: document.getElementById('name').value,
    //         email: document.getElementById('email').value,
    //         message: document.getElementById('message').value,
    //         topic: modalTitle.textContent
    //     };
        
    //     console.log('Form submitted:', formData);
    //     alert(`Thank you, ${formData.name}! Your information about "${formData.topic}" has been submitted.`);
        
    //     // Reset form and close modal
    //     infoForm.reset();
    //     closeModal();
    // });

    // Hide tooltip on click anywhere
    // document.addEventListener('click', () => {
    //     tooltip.classList.remove('visible');
    // });
    loadModal('/media/smooth-modal.html', 'modal-container');
});
