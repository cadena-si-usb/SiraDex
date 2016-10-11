var programaEliminar = undefined;

$(document).ready(function(){
  var maxLongNombre  = 256;    // Longitud máxima que tendrá el campo nombre.
  var maxLongDescrip = 2048;   // Longitud máxima que tendrá el campo descripción.

  // Obtengo la lista de errores generados por el formulario de agregar.
  var mensajeErrorAgregar = $("#modalAgregar").attr("data-hayErroresAgregar");
  mensajeErrorAgregar = mensajeErrorAgregar.replace(/<Storage |>/gi, "").replace(/'/g, '"')

  // Definición del comportamiento del botón agregar programa cuando se hace click.
  $("#agregarProgBtn").click(function(){
    // Muestra la cantidad de caracteres disponible en el textfield de nombre.
    textoRestante(maxLongNombre,  "#no_table_Nombre");

    // Muestra la cantidad de caracteres disponible en el textarea de descripción.
    textoRestante(maxLongDescrip, "#no_table_Descripcion");
  });


  $('[id="editarProgBtn"]').click(function(){
    // Muestra la cantidad de caracteres disponible en el textfield de nombre.
    textoRestante(maxLongNombre,  "#no_table_Nombre");

    // Muestra la cantidad de caracteres disponible en el textarea de descripción.
    textoRestante(maxLongDescrip, "#no_table_Descripcion");
  });

  // Si hay errores en el formulario agregar...
  if (mensajeErrorAgregar != '{}'){
      $("#agregarProgBtn").click();
      $(".error_wrapper").css('color','red');
  }

  // Pasamos los argumentos para editar el catalogo.
  $('#ModalEditarPrograma').on('show.bs.modal', function(e){
      var id_programa = $(e.relatedTarget).data('id-programa');
      var nombre      = $(e.relatedTarget).data('nombre');
      var descripcion = $(e.relatedTarget).data('descripcion');
      console.log($(e.currentTarget).find('input[name="Descripcion"]'));
      $(e.currentTarget).find('input[name="id_programa"]').val(id_programa);
      $(e.currentTarget).find('input[name="Nombre"]').val(nombre);
      $(e.currentTarget).find("#no_table_Descripcion").text(descripcion);
  });

  $("#no_table_id_programa__row").hide();

  // Pasamos los argumentos para eliminar catalogo.
  $('#modalEliminarPrograma').on('show.bs.modal', function(e){
      var linkEliminar = $(e.relatedTarget).data('link-eliminar-programa');
      $("#BotonEliminar").attr("href", linkEliminar);
  });

  function prueba(id){
    programaEliminar = id;
    console.log(id);
    var toAjax = "'{{=URL('eliminar_programa')}}/" + programaEliminar +"'"
    console.log(toAjax)
    ajax(toAjax,[]);
  }
});
