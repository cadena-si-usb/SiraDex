$(document).ready(function(){
  var maxLongNombre  = 256;    // Longitud máxima que tendrá el campo nombre.
  var maxLongDescrip = 2048;   // Longitud máxima que tendrá el campo descripción.

  // Obtengo la lista de errores generados por el formulario de agregar.
  var mensajeErrorAgregar = $("#modalAgregar").attr("data-hayErroresAgregar");
  mensajeErrorAgregar = mensajeErrorAgregar.replace(/<Storage |>/gi, "").replace(/'/g, '"')

  // Obtengo la lista de errores generados por el formulario de editar.
  var mensajeErrorEditar = $("#modalEditar").attr("data-hayErroresEditar");
  mensajeErrorEditar = mensajeErrorEditar.replace(/<Storage |>/gi, "").replace(/'/g, '"')

  // Definición del comportamiento del botón agregar programa cuando se hace click.
  $("#agregarProgBtn").click(function(){
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
      localStorage.setItem("programaEditar", id_programa);
      $(e.currentTarget).find('input[name="id_programa"]').val(id_programa);
      $(e.currentTarget).find('input[name="Nombre"]').val(nombre);
      $(e.currentTarget).find("#no_table_Descripcion").val(descripcion);

      // Muestra la cantidad de caracteres disponible en el textfield de nombre.
      textoRestante(maxLongNombre,  $(e.currentTarget).find("#no_table_Nombre"));

      // Muestra la cantidad de caracteres disponible en el textarea de descripción.
      textoRestante(maxLongDescrip, $(e.currentTarget).find("#no_table_Descripcion"));
  });

  // Si hay errores en el formulario editar...
  if (mensajeErrorEditar != '{}'){
      var programaEditar = localStorage.getItem("programaEditar");
      $('span[data-id-programa="' + programaEditar + '"]').click();
      $(".error_wrapper").css('color','red');
      console.log(programaEditar);
  }

  // Se tuvo que añadir el id al formulario para poder editarlo o eliminarlo en
  // un futuro. Por eso se oculta.
  $("#no_table_id_programa__row").hide();

  // Pasamos los argumentos para eliminar el programa.
  $('#modalEliminarPrograma').on('show.bs.modal', function(e){
      var linkEliminar = $(e.relatedTarget).data('link-eliminar-programa');
      $("#BotonEliminar").attr("href", linkEliminar);
  });

  // -.........................................................................-
  // Para realizar la búsqueda.
  var options = {
    valueNames: ['nombre_programa', 'descripcion_programa', { data: ['nombre', 'descripcion'] }],
    item: '<td class="nombre_programa"></td><td class="descripcion_programa"><center></center></td>'
  };

  var programList = new List('programs', options);

  // -.........................................................................-
});
