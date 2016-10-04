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
});
