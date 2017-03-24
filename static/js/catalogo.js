$(document).ready(function(){
  var maxLongNombre  = 128;    // Longitud máxima que tendrá el campo nombre.

  // Obtengo la lista de errores generados por el formulario de agregar.
  var mensajeErrorAgregar = $("#modalAgregar").attr("data-hayErroresAgregar");
  mensajeErrorAgregar = mensajeErrorAgregar.replace(/<Storage |>/gi, "").replace(/'/g, '"')

  // Obtengo la lista de errores generados por el formulario de agregar.
  var mensajeErrorAgregarCampo = $("#modalAgregarCampoCat").attr("data-hayErroresAgregarCampo");
  mensajeErrorAgregarCampo = mensajeErrorAgregarCampo.replace(/<Storage |>/gi, "").replace(/'/g, '"')

  // Obtengo la lista de errores generados por el formulario de editar nombre.
  var mensajeErrorEditarNombre = $("#renombrarNombreBtn").attr("data-hayErroresEditarNombre");
  mensajeErrorEditarNombre = mensajeErrorEditarNombre.replace(/<Storage |>/gi, "").replace(/'/g, '"')

  // Definición del comportamiento del botón agregar catálogo cuando se hace click.
  $("#agregarCatalogoBtn").click(function(){
    // Muestra la cantidad de caracteres disponible en el textfield de nombre.
    textoRestante(maxLongNombre,  "#no_table_nombre");
  });

  // Definición del comportamiento del botón editar catálogo cuando se hace click.
  $('#modalCambiarNombre').on('show.bs.modal', function(e){
    var id_catalogo = $(e.relatedTarget).data('id-catalogo');
    var nombre      = $(e.relatedTarget).data('nombre');
    $(e.currentTarget).find('input[name="Id_catalogo"]').val(id_catalogo);
    localStorage.setItem("nombreCatalogoEditar", id_catalogo);
    $("#no_table_id_catalogo__row").css("display","none");
    $(e.currentTarget).find('input[name="Nombre"]').val(nombre);

    // Muestra la cantidad de caracteres disponible en el textfield de nombre.
    textoRestante(maxLongNombre,  $(e.currentTarget).find("#no_table_nombre"));
  });


  // Si hay errores en el formulario agregar...
  if (mensajeErrorAgregar != '{}'){
      console.log("OK")
      $("#agregarCatalogoBtn").click();        // Abre el modal (da click en el botón agregar).
      $(".error_wrapper").css('color','red');  // Se pone el error en rojo.
  }

  // Si hay errores en el formulario agregar...
  if (mensajeErrorAgregarCampo != '{}'){
      console.log("OK")
      $("#agregarCampoCatalogoBtn").click();        // Abre el modal (da click en el botón agregar).
      $(".error_wrapper").css('color','red');  // Se pone el error en rojo.
  }

  // Si hay errores en el formulario editar nombre...
  if (mensajeErrorEditarNombre != '{}'){
      var catalogoEditar = localStorage.getItem("nombreCatalogoEditar");
      $('#renombrarNombreBtn[data-id-catalogo="' + catalogoEditar + '"]').click();
      $(".error_wrapper").css('color','red');
  }

  // Para limpiar el modal de agregar cuando se cierra.
  $("#modalAgregarCatalogo").on("hidden.bs.modal", function(){
    $("#no_table_nombre").val("");
    $(".error").html("");
  });

  // Para limpiar el modal de editar cuando se cierra.
  $("#modalCambiarNombre").on("hidden.bs.modal", function(){
    $(".error").html("");
  });
});
