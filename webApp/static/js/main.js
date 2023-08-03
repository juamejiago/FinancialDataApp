function get_cookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(";").shift();
}

function drop_down_user_options(){
  const dropdownMenu = document.getElementById("dropdown_user_options");
  if (dropdownMenu.style.display == "none" || dropdownMenu.style.display == ""){
    dropdownMenu.style.display = "block";
  }else{
    dropdownMenu.style.display = "none";
  }
}

function add_new_category() {
  const options = document.querySelectorAll("input[type='checkbox']");
  let at_least_one_selected = false;
  var selected_tags = new Array();
  const input_field_category = document.getElementById("new_category_field");
  const name_category = input_field_category.value;
  selected_tags.push(name_category)
  options.forEach(function (option) {
    if (option.checked) {
      at_least_one_selected = true;
      // Agrupar las tags seleccionadas
      selected_tags.push(option.value);
    }
  });

  if (!at_least_one_selected) {
    alert("At least one tag must be selected. Try again");
  } else {
    // Crear un objeto XMLHttpRequest
    var xhr = new XMLHttpRequest();

    // Definir la URL y el método de la solicitud
    var url = "/home/";
    var method = "POST";

    // Convertir los datos a formato de cadena
    var jsonData = JSON.stringify(selected_tags);

    // Configurar la solicitud AJAX
    xhr.open(method, url, true);
    xhr.setRequestHeader("X-CSRFToken", get_cookie("csrftoken"));
    xhr.onreadystatechange = function() {
      if (xhr.readyState === XMLHttpRequest.DONE) {
          if (xhr.status === 200) { 
            reload_main_page()
          } else {
              console.error("Error:", xhr.status);
          }
      }
    };

    // Enviar la solicitud con los datos
    xhr.send(jsonData);

  }
  
}

function deploy_entry_field_category() {
  const container = document.getElementById("add_new_categories_container");
  const button_add_new = document.getElementById("dropdown_button_add_new");
  const input_field = document.getElementById("new_category_field");
  const new_button_submit = document.getElementById("button_submit_category");

  if (!container.contains(input_field) || !container.contains(new_button_submit)) {
    const input_field = document.createElement("input");
    input_field.type = "text";
    input_field.id = "new_category_field";
    const new_button_submit = document.createElement("button");
    new_button_submit.id = "button_submit_category";
    new_button_submit.textContent = "Submit";
    new_button_submit.addEventListener("click", add_new_category)
    container.style.display = "grid";
    container.style.gridTemplateColumns = "3fr 1fr";
    button_add_new.style.display = "none";
    input_field.style.display = "block";
    new_button_submit.style.display = "block";
    container.appendChild(input_field);
    container.appendChild(new_button_submit);
  } else {
    container.style.display = "grid";
    container.style.gridTemplateColumns = "3fr 1fr";
    button_add_new.style.display = "none";
    input_field.style.display = "block";
    new_button_submit.style.display = "block";
  }
}

function drop_down_content_categories() {
  const container = document.getElementById("add_new_categories_container");
  var dropdownContent = document.getElementById("dropdown_content");
  const button_add_new = document.getElementById("dropdown_button_add_new");
  const input_field = document.getElementById("new_category_field");
  const button_submit = document.getElementById("button_submit_category");
  if (input_field != null || button_submit != null) {
    if (
      input_field.style.display == "block" &&
      button_submit.style.display == "block"
    ) {
      button_add_new.style.display = "block";
      input_field.style.display = "none";
      button_submit.style.display = "none";
      container.style.display = "";
      container.style.gridTemplateColumns = "";
    }
  }

  dropdownContent.classList.toggle("show_buttons");
  button_add_new.classList.toggle("dropdown_button_content_add_new");
}

function select_all_checkboxes_tags() {
  const options = document.querySelectorAll("input[type='checkbox']");
  options.forEach(function (option) {
    if (option.checked) {
      option.checked = false;
    } else {
      option.checked = true;
    }
  });
}

function delete_tag() {
  const confirmation = confirm("Are you sure you want to delete this/these tag/tags?");
  if(confirmation) {

    const options = document.querySelectorAll("input[type='checkbox']");
    let at_least_one_selected = false;
    var selected_tags = new Array();
    options.forEach(function (option) {
      if (option.checked) {
        at_least_one_selected = true;
        // Agrupar las tags seleccionadas
        selected_tags.push(option.value);
      }
    });

    if (!at_least_one_selected) {
      alert("At least one tag must be selected. Try again");
    } else {
      // Crear un objeto XMLHttpRequest
      var xhr = new XMLHttpRequest();

      // Definir la URL y el método de la solicitud
      var url = "/delete_tag/";
      var method = "POST";

      // Convertir los datos a formato de cadena
      var jsonData = JSON.stringify(selected_tags);

      // Configurar la solicitud AJAX
      xhr.open(method, url, true);
      xhr.setRequestHeader("X-CSRFToken", get_cookie("csrftoken"));

      // Enviar la solicitud con los datos
      xhr.send(jsonData);
      setTimeout(function () {
        location.reload();
      }, 100);
    }
  }
}

function delete_category(selected_category) {
  const confirmation = confirm("Are you sure you want to delete this/these category/categories?");
  if(confirmation) {

    // Crear un objeto XMLHttpRequest
    var xhr = new XMLHttpRequest();

    // Definir la URL y el método de la solicitud
    var url = "/delete_category/";
    var method = "POST";

    // Convertir los datos a formato de cadena
    var jsonData = JSON.stringify(selected_category);

    // Configurar la solicitud AJAX
    xhr.open(method, url, true);
    xhr.setRequestHeader("X-CSRFToken", get_cookie("csrftoken"));

    // Enviar la solicitud con los datos
    xhr.send(jsonData);
    setTimeout(function () {
        location.reload();
    }, 100);
  }
}

function delete_tag_from_category() {
  const options = document.querySelectorAll("input[type='checkbox']");
  let at_least_one_selected = false;
  var selected_tags = new Array();
  options.forEach(function (option) {
    if (option.checked) {
      at_least_one_selected = true;
      // Agrupar las tags seleccionadas
      selected_tags.push(option.value);
    }
  });

  if (!at_least_one_selected) {
    alert("At least one tag must be selected. Try again");
  } else {
    // Crear un objeto XMLHttpRequest
    var xhr = new XMLHttpRequest();

    // Definir la URL y el método de la solicitud
    var url = "/delete_tag_from_category/";
    var method = "POST";

    // Convertir los datos a formato de cadena
    var jsonData = JSON.stringify(selected_tags);

    // Configurar la solicitud AJAX
    xhr.open(method, url, true);
    xhr.setRequestHeader("X-CSRFToken", get_cookie("csrftoken"));

    // Enviar la solicitud con los datos
    xhr.send(jsonData);
    setTimeout(function () {
      location.reload();
    }, 100);
  }
}

function visualize_category() {
  document.addEventListener("click", function(event)
  {
    let button = event.target;
    // Obtener el ID del botón
    let selected_category = button.id; 
    // Crear un objeto XMLHttpRequest
    var xhr = new XMLHttpRequest();

    // Definir la URL y el método de la solicitud
    var url = "/visualize_category/";
    var method = "POST";

    // Convertir los datos a formato de cadena
    var jsonData = JSON.stringify(selected_category);

    // Configurar la solicitud AJAX
    xhr.open(method, url, true);
    xhr.setRequestHeader("X-CSRFToken", get_cookie("csrftoken"));

    // Enviar la solicitud con los datos
    xhr.send(jsonData);
    setTimeout(function () {
      location.reload();
    }, 100);
  });
}

function tag_ordering(selected_filter) {
  // Crear un objeto XMLHttpRequest
  var xhr = new XMLHttpRequest();

  // Definir la URL y el método de la solicitud
  var url = "/tag_ordering/";
  var method = "POST";

  // Convertir los datos a formato de cadena
  var jsonData = JSON.stringify(selected_filter);

  // Configurar la solicitud AJAX
  xhr.open(method, url, true);
  xhr.setRequestHeader("X-CSRFToken", get_cookie("csrftoken"));

  // Enviar la solicitud con los datos
  xhr.send(jsonData);
  setTimeout(function () {
    location.reload();
  }, 100);
}

function update_tag() {
  // Crear un objeto XMLHttpRequest
  var xhr = new XMLHttpRequest();

  // Definir la URL y el método de la solicitud
  var url = "/update_tag/";
  var method = "POST";
  // Configurar la solicitud AJAX
  xhr.open(method, url, true);
  xhr.setRequestHeader("X-CSRFToken", get_cookie("csrftoken"));
  xhr.onreadystatechange = function () {
    if (xhr.readyState === 4 && xhr.status === 200) {
      setTimeout(function () {
        location.reload();
      }, 100);
    }
  };
  // Enviar la solicitud
  xhr.send();
  alert("The button to update tags has been pressed.");
}

function create_tag_url(){
  if(window.location.href == "www.https://juamejiago.pythonanywhere.com/create_tag/"){
    reload_main_page()
  }else{
    window.location.replace("www.https://juamejiago.pythonanywhere.com/create_tag/");
  }
}

function add_tag_to_category_url() {
  if(window.location.href == "www.https://juamejiago.pythonanywhere.com/add_tag_to_category/"){
    reload_main_page()
  }else{
    window.location.replace("www.https://juamejiago.pythonanywhere.com/add_tag_to_category/");
  }
}

function add_tag_to_category() {
  const options_tags = document.getElementsByName("tags_checkboxes_values");
  let at_least_one_selected_tags = false;
  var selected_tags = new Array();
  options_tags.forEach(function (option_tag) {
    if (option_tag.checked) {
      at_least_one_selected_tags = true;
      // Agrupar las tags seleccionadas
      selected_tags.push(option_tag.value);
    }
  });

  const options_categories = document.getElementsByName("categories_checkboxes_values");
  let at_least_one_selected_categories = false;
  var selected_categories = new Array();
  options_categories.forEach(function (option_category) {
    if (option_category.checked) {
      at_least_one_selected_categories = true;
      // Agrupar las tags seleccionadas
      selected_categories.push(option_category.value);
    }
  });

  if (!at_least_one_selected_tags) {
    alert("At least one tag must be selected. Try again");
  } else if (!at_least_one_selected_categories) {
    alert("At least one category must be selected. Try again");
  } 
  else {
    // Crear un objeto XMLHttpRequest
    var xhr = new XMLHttpRequest();

    // Definir la URL y el método de la solicitud
    var url = "/add_tag_to_category/";
    var method = "POST";

    const data_to_send = {
      selected_categories: selected_categories,
      selected_tags: selected_tags
  };

    // Convertir los datos a formato de cadena
    var jsonData = JSON.stringify(data_to_send);

    // Configurar la solicitud AJAX
    xhr.open(method, url, true);
    xhr.setRequestHeader("X-CSRFToken", get_cookie("csrftoken"));
    xhr.onreadystatechange = function() {
      if (xhr.readyState === XMLHttpRequest.DONE) {
          if (xhr.status === 200) {
            reload_main_page()
          } else {
            console.error("Error:", xhr.status);
          }
      }
    };

    // Enviar la solicitud con los datos
    xhr.send(jsonData);
  }
}

function transfer_tag_between_categories_url() {
  if(window.location.href == "www.https://juamejiago.pythonanywhere.com/transfer_tag_between_categories/"){
    reload_main_page()
  }else{
    window.location.replace("www.https://juamejiago.pythonanywhere.com/transfer_tag_between_categories/");
  }
}

function transfer_tag_between_categories() {
  const options_tags = document.getElementsByName("tags_checkboxes_values");
  let at_least_one_selected_tags = false;
  var selected_tags = new Array();
  options_tags.forEach(function (option_tag) {
    if (option_tag.checked) {
      at_least_one_selected_tags = true;
      // Agrupar las tags seleccionadas
      selected_tags.push(option_tag.value);
    }
  });

  const options_categories = document.getElementsByName("categories_checkboxes_values");
  let at_least_one_selected_categories = false;
  var selected_categories = new Array();
  options_categories.forEach(function (option_category) {
    if (option_category.checked) {
      at_least_one_selected_categories = true;
      // Agrupar las tags seleccionadas
      selected_categories.push(option_category.value);
    }
  });

  if (!at_least_one_selected_tags) {
    alert("At least one tag must be selected. Try again");
  } else if (!at_least_one_selected_categories) {
    alert("At least one category must be selected. Try again");
  } 
  else {
    // Crear un objeto XMLHttpRequest
    var xhr = new XMLHttpRequest();

    // Definir la URL y el método de la solicitud
    var url = "/transfer_tag_between_categories/";
    var method = "POST";

    const data_to_send = {
      selected_categories: selected_categories,
      selected_tags: selected_tags
  };

    // Convertir los datos a formato de cadena
    var jsonData = JSON.stringify(data_to_send);

    // Configurar la solicitud AJAX
    xhr.open(method, url, true);
    xhr.setRequestHeader("X-CSRFToken", get_cookie("csrftoken"));

    xhr.onreadystatechange = function() {
      if (xhr.readyState === XMLHttpRequest.DONE) {
          if (xhr.status === 200) { 
            reload_main_page()
          } else {
            console.error("Error:", xhr.status);
          }
      }
    };

    // Enviar la solicitud con los datos
    xhr.send(jsonData);

  }
}

function reload_main_page() {
  const url = "www.https://juamejiago.pythonanywhere.com/home";
  window.location.replace("www.https://juamejiago.pythonanywhere.com/home");
}