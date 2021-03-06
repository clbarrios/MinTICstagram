let tabActual = null,tabImg = null ,contentActual = null, contentImg = null;
window.onload = function(){    
    //document.getElementById("myImgs-tab").click();
}


function openTab(id) {
    if(contentActual != null){
        contentActual.style.display = "none"
        contentActual.className=contentActual.className.replace("active","")
    }

    contentActual = document.getElementById(id + "-content");

    if(contentActual.getAttribute("id") == "myImgs-content"){
        obtenerSubTab("privadas")
    }
    
   
    contentActual.style.display = "block"

    if(tabActual != null){
        
        tabActual.className=tabActual.className.replace("active","")
    }
    tabActual= document.getElementById(id + "-tab")
    tabActual.className += " active"

}

function obtenerSubTab(id){
    if(contentImg!= null){
        contentImg.style.display = "none"
        contentImg.className=contentImg.className.replace("active","")
    }

    contentImg = document.getElementById(id + "-content");
    contentImg.style.display = "block"
    if(tabImg!= null){
        tabImg.className=tabImg.className.replace("active","")
    }

    tabImg =  document.getElementById(id + "-tab")
    tabImg.className += " active"

}

/*
 * Función para mostrar imagen al cargarla en modal de Agregar Imagen 
 * 
 */
function displayImg(event) {
    // objeto imagen para consultar dimensiones antes de mostrarla
    var img = new Image();
    // cuando cargue la imagen ajustar tamaño a mostrar según las dimensiones de la imagen
    img.onload = function() {
        var h = img.height;
        var w = img.width;
        console.log("img size: " + this.width + "x" + this.height);
        var dispImg = document.getElementById("imgDisplay");
        dispImg.src = this.src;
        if (w >= h) {
            dispImg.style.width = "100%";
            dispImg.style.height = "";
        } else {
            dispImg.style.height = "100%";
            dispImg.style.width = "";
        }
        document.getElementById("imgPlaceholder").style.display = "none";
        dispImg.style.display = "block";
    }
    // asignar imagen cargada al objeto imagen luego de validar la extensión del archivo
    var url = document.getElementById("imgInputFile").value;
    if (validateImgURL(url)) {
        img.src = URL.createObjectURL(event.target.files[0]);

        // codigo para cambiar la apariencia del label
        var input = document.getElementById("imgInputFile");
        var label = document.getElementById("imgInputLabel"),
            defaultLabel = label.innerHTML;
        var filename = "";
        filename = input.value.split('\\').pop();

        if (filename) {
            label.querySelector("span").innerHTML = filename;
        } else {
            label.innerHTML = defaultLabel;
        }

    } else {
        alert("Tipo de archivo no soportado. \nDebes cargar una imagen")
    }
}

function validateImgURL(url){
    // regex
    console.log(url)
    var extensionesPermitidas = /(\.jpg|\.jpeg|\.png|\.gif)$/i;
    if (extensionesPermitidas.exec(url)) {
        return true;
    } else {
        return false;
    }
}

/*
 * Función para mostrar imagen diensionada de acuerdo a su relación de aspecto
 * al abrir modal para actualizar imagen
 */
function displayImgOnUpdateModal(event, id, ruta) {
    var card = event.target;
    while (card.className !== "card mx-auto") {card = card.parentElement};
    
    var img = new Image();
    
    img.onload = function() {
        var w = img.width;
        var h = img.height;
        var dispImg = document.getElementById("imgUpdateDisplay");
        dispImg.src = this.src;
        if (w >= h) {
            dispImg.style.width = "100%";
            dispImg.style.heigt = "";
        } else {
            dispImg.style.width = "";
            dispImg.style.heigt = "100%";
        }
        dispImg.style.display = "block";
    }

    img.src = card.querySelector("img").src;

    // cargar datos de la imagen en el formulario
    var modal = document.getElementById("actualizarImgModal")

    // nombre de la imagen
    document.forms["actualizar_imagen"]["nombre"].value = card.querySelector(".card-title").innerHTML;

    // etiquetas
    var etiquetas_str = "";
    for (var e of card.querySelectorAll("li")) {
        etiquetas_str = etiquetas_str + " " + e.innerHTML;
        console.log(e.innerHTML);
    }
    
    document.forms["actualizar_imagen"]["etiquetas"].innerHTML = etiquetas_str;

    document.forms["actualizar_imagen"]["id"].value = id;
    document.forms["actualizar_imagen"]["ruta"].value = ruta; 
}

function setRadioBtn(option) {
    document.getElementById("radioBtn" + option).checked = true;
}


//para redirigir con el boton de cerrar sesion

function irIngreso(){
    location.href = "../";
}

// para hacer efecto de like/dislike con botón 
function toggleHeart(event) {
    var btn = event.target;
    while (btn.nodeName != "BUTTON") {btn = btn.parentElement};
    console.log(btn.className)
   
    for (var heart of btn.querySelectorAll("svg")) {
        heart.style.display = heart.style.display == "none" ? "inline" : "none";
    }
}

/*
Función para mostrar modal de imagen en pantalla completa
*/
function showImgModal(event) {
    var sourceImg = event.target;

    var card = event.target;
    while (card.className !== "card mx-auto") {card = card.parentElement};


    var img = new Image();
    img.onload = function() {
        var modal = document.getElementById("showImgModal");
        var modalImg = modal.querySelector("img");
        var imgTitle = card.querySelector(".card-title");
        var modalCaption = modal.querySelector("#showImgModal-caption");

        var h = this.height;
        var w = this.width;

        if (w >= h) {
            modalImg.style.width = "80%";
            modalImg.style.height = "";
        } else {
            modalImg.style.width = "";
            modalImg.style.height = "100%";
        }
        
        modal.style.display = "block";
        modalImg.src = this.src;
        modalCaption.innerHTML = imgTitle.innerHTML;
    }

    img.src = sourceImg.src;
}

function closeImgModal() {
    document.getElementById("showImgModal").style.display = "none";
}
