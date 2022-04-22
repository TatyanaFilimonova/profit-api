let currentDirectionIndex;

function onLoadDirection() {
  currentDirection = document.getElementById('direction');
  currentDirectionIndex = currentDirection.selectedIndex;
  console.log(currentDirection.options[currentDirectionIndex]);
};


function submitForm(formName){
    if (validFormData(formName)){
        document.getElementById(formName).submit()
    }
}

function validFormData(formName) {
    const form = document.forms[formName];
    const formData = new FormData(form);
    const keys = formData.keys();
    for (const key of keys) {
        if (!form[key].validity.valid) {
                form[key].focus();
                return false;
        }
    }
    return true;
}

function setList(selectObject){
    console.log("onChange catcher")
    const selectedValue = selectObject.options[selectObject.selectedIndex].value;
    if (selectedValue =="add"){
        document.getElementById('newDirectionModal').style.display = "flex";
    }
    if (selectedValue =="remove"){
        console.log('trying to remove row from directions list')
        document.getElementById('removeDirectionModal').style.display = "flex";
    }
}

function closeDirectionModal(modalId){
    console.log(currentDirectionIndex);
    currentDirection = document.getElementById(modalId);
    document.getElementById('direction').options[currentDirectionIndex].selected = true;
    currentDirection.style.display = 'none';
}


async function  addDirection(event, FormName) {
    if (!validFormData(FormName)){
        return false;
    }
    const form = document.forms[FormName];
    const formData = new FormData(form);
    let object = {};
    formData.forEach(function(value, key){
        object[key] = value;
    });
    console.log(object);
    const request_params = {
        method: "POST",
        cache: 'no-cache',
        mode: 'cors',
        headers: {
            'Content-Type': "application/json",
            // 'Access-Control-Allow-Origin': '*'
            'X-CSRFToken' : getCSRFTokenValue()
        },
        body: JSON.stringify(object)
    };
    try {
        const response = await fetch(window.location.href+"/adddirection/", request_params);
        const result = await response.json();
        const resp_status = response.status;
        if (resp_status == 400) {
            window.alert(result['result']);
        }
        closeDirectionModal('newDirectionModal');
        location.reload();
        return [resp_status];
    } catch (e) {
        window.alert(e);
        return [400, ""]
    }
}

async function  delDirection(event, FormName) {
    if (!validFormData(FormName)){
        return false;
    }
    const form = document.forms[FormName];
    const formData = new FormData(form);
    let object = {};
    formData.forEach(function(value, key){
        object[key] = value;
    });
    console.log(object);
    const request_params = {
        method: "POST",
        cache: 'no-cache',
        mode: 'cors',
        headers: {
            'Content-Type': "application/json",
            // 'Access-Control-Allow-Origin': '*'
            'X-CSRFToken' : getCSRFTokenValue()
        },
        body: JSON.stringify(object)
    };
    try {
        const response = await fetch(window.location.href+"/deldirection/", request_params);
        const result = await response.json();
        const resp_status = response.status;
        if (resp_status == 400) {
            window.alert(result['result']);
        }
        closeDirectionModal('removeDirectionModal');
        location.reload();
        return [resp_status];
    } catch (e) {
        window.alert(e);
        return [400, ""]
    }
}


function getCSRFTokenValue(){

  if (!document.cookie) {
    return null;
  }

  const xsrfCookies = document.cookie.split(';')
    .map(c => c.trim())
    .filter(c => c.startsWith('csrftoken' + '='));
  if (xsrfCookies.length === 0) {
    return null;
  }
  return decodeURIComponent(xsrfCookies[0].split('=')[1]);
}