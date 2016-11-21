$(document).ready(function(){

  var maxLongNombre  = 128;    // Longitud máxima que tendrá el campo nombre.
  var maxLongDescrip = 2048;   // Longitud máxima que tendrá el campo descripción.
  var maxLongCodigo = 10;
  var hayPrograma = $(".formularioTipo").attr("data-hayPrograma");

  // Muestra la cantidad de caracteres disponible en el textfield de nombre.
  textoRestante(maxLongNombre,  "#no_table_Nombre");

  // Muestra la cantidad de caracteres disponible en el textarea de descripción.
  textoRestante(maxLongDescrip, "#no_table_Descripcion");

  // Muestra la cantidad de caracteres disponible en el textfield de código.
  textoRestante(maxLongCodigo, "#no_table_Codigo");

  // Obtengo la lista de errores generados por el formulario de agregar.
  var mensajeErrorAgregar = $("#modalAgregar").attr("data-hayErroresAgregar");
  mensajeErrorAgregar = mensajeErrorAgregar.replace(/<Storage |>/gi, "").replace(/'/g, '"')

  // Obtengo la lista de errores generados por el formulario de editar.
  var mensajeErrorEditar = $("#modalEditar").attr("data-hayErroresEditar");
  mensajeErrorEditar = mensajeErrorEditar.replace(/<Storage |>/gi, "").replace(/'/g, '"')

  // Si no existe un programa, entonces no debería mostrarse el formulario.
  if (!hayPrograma)
  {
    $(".formularioTipo").hide();
  }

   // Pasamos los argumentos para eliminar catalogo.
  $('#myModalDelete').on('show.bs.modal', function(e){
      var linkEliminar = $(e.relatedTarget).data('link-eliminar-tipo');
      $("#BotonEliminar").attr("href", linkEliminar);
  });


  // Eliminar definitivamente
  $('#myModalDelete').on('show.bs.modal', function (event) {
    if (event.relatedTarget != null){
      $("#botonDelete").attr("data-id-tipo", event.relatedTarget.getAttribute("data-id-tipo"));
    }
  });

  $("#botonDelete").click(function (event){
    var id_tipo = $("#botonDelete").attr("data-id-tipo");
    ajax("{{=URL('enviar_tipo_papelera')}}/"+id_tipo,[]);
    location.reload();
  });

  $('#myModalEditar').on('show.bs.modal', function(e){
    var id_tipo = $(e.relatedTarget).data('idtipo');
    var nombre      = $(e.relatedTarget).data('nombre');
    var codigo      = $(e.relatedTarget).data('codigo');
    var descripcion = $(e.relatedTarget).data('descripcion');
    var id_programa = $(e.relatedTarget).data('idprograma');
    var tipoPR =  $(e.relatedTarget).data('tipopr');
    $(e.currentTarget).find('input[name="Id_tipo"]').val(id_tipo);
    localStorage.setItem("tipoActividadEditar", id_tipo);
    $("#no_table_Id_tipo__row").css("display","none");
    $(e.currentTarget).find('input[name="Nombre"]').val(nombre);
    $(e.currentTarget).find('input[name="Codigo"]').val(codigo);
    $(e.currentTarget).find('textarea[name="Descripcion"]').val(descripcion);
    $(e.currentTarget).find('#no_table_Programa').val(id_programa);
    $(e.currentTarget).find('#no_table_Tipo').val(tipoPR);
    // Muestra la cantidad de caracteres disponible en el textfield de nombre.
    textoRestante(maxLongNombre,  $(e.currentTarget).find("#no_table_Nombre"));

    // Muestra la cantidad de caracteres disponible en el textarea de descripción.
    textoRestante(maxLongDescrip, $(e.currentTarget).find("#no_table_Descripcion"));
  }); 

  // Si hay errores en el formulario agregar...
  if (mensajeErrorAgregar != '{}'){
      $("#agregarTipoActividadBtn").click();        // Abre el modal (da click en el botón agregar).
      $(".error_wrapper").css('color','red');  // Se pone el error en rojo.
  }

  // Si hay errores en el formulario editar...
  if (mensajeErrorEditar != '{}'){
      var tipoActividadEditar = localStorage.getItem("tipoActividadEditar");
      $('span[data-idtipo="' + tipoActividadEditar + '"]').click();
      $(".error_wrapper").css('color','red');
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
