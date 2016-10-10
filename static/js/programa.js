$(document).ready(function(){
  var maxLongNombre  = 256;    // Longitud máxima que tendrá el campo nombre.
  var maxLongDescrip = 2048;   // Longitud máxima que tendrá el campo descripción.

  // Muestra la cantidad de caracteres disponible en el textfield de nombre.
  textoRestante(maxLongNombre,  "#no_table_Nombre");

  // Muestra la cantidad de caracteres disponible en el textarea de descripción.
  textoRestante(maxLongDescrip, "#no_table_Descripcion");
});
