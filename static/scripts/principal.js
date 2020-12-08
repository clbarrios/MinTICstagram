
function openTab(id) {
    var i, tabcontents, tabs, activeTab, tabscon, tabss;
    tabcontents = document.getElementsByClassName("tab-content");

    for (i = 0; i < tabcontents.length; i++) {
        tabcontents[i].style.display = "none";
    }

    tabs = document.getElementsByClassName("tab")
    for (i = 0; i < tabs.length; i++) {
        tabs[i].className = tabs[i].className.replace(" active", "");
    }

    tabscon = document.getElementsByClassName("tabb-contentt");
    for (i = 0; i < tabscon.length; i++) {
        tabscon[i].style.display = "none";
    }

    tabss = document.getElementsByClassName("tabb")
    for (i = 0; i < tabss.length; i++) {
        tabss[i].className = tabss[i].className.replace(" active", "");
    }


    console.log(id+"-content");
  
        activeTab = document.getElementById(id + "-content");
        activeTab.style.display = "block";

        console.log(id+"-tab");
        activeTab = document.getElementById(id + "-tab");
        activeTab.className += " active";

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
        //dispImg.style.margin = "auto";
    }
    // asignar imagen cargada al objeto imagen luego de validar la extensión del archivo
    var url = URL.createObjectURL(event.target.files[0])
    if (validateImgURL(url)) {
        img.src = URL.createObjectURL(event.target.files[0])
    } else {
        alert("Tipo de archivo no soportado. \nDebes cargar una imagen")
        document.getElementById("imgInputFile").value = "";
    }
    
}

function validateImgURL(url){
    // regex
    var extensionesPermitidas = /(\.jpg|\.jpeg|\.png|\.gif)$/i;
    if (extensionesPermitidas.exec(url)) {
        return true;
    } else {
        return false;
    }
}
