$(document).ready(function(){
    // Pasamos los argumentos para eliminar catalogo.
  $('#myModalDelete').on('show.bs.modal', function(e){
      var linkEliminar = $(e.relatedTarget).data('link-eliminar-tipo');
      $("#BotonEliminar").attr("href", linkEliminar);
  });
});

$(document).ready(function(){

  var maxLongNombre  = 128;    // Longitud máxima que tendrá el campo nombre.
  var maxLongDescrip = 2048;   // Longitud máxima que tendrá el campo descripción.
  var hayPrograma = $(".formularioTipo").attr("data-hayPrograma");

  // Muestra la cantidad de caracteres disponible en el textfield de nombre.
  textoRestante(maxLongNombre,  "#no_table_Nombre");

  // Muestra la cantidad de caracteres disponible en el textarea de descripción.
  textoRestante(maxLongDescrip, "#no_table_Descripcion");

  // Si no existe un programa, entonces no debería mostrarse el formulario.
  if (!hayPrograma)
  {
    $(".formularioTipo").hide();
  }

  // -.........................................................................-
  // Para realizar la búsqueda.
  var options = {
    valueNames: ['nombre_tipo', 'descripcion_tipo', { data: ['nombre', 'descripcion'] }],
    item: '<td class="nombre_tipo"></td><td class="descripcion_tipo"><center></center></td>'
  };

  var tipo_actividadList = new List('tipo_actividad', options);

  // -.........................................................................-
});
