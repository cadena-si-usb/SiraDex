$(document).ready(function(){
 //-.........................................................................-
  // Para realizar la búsqueda.
  var options = {
    valueNames: ['accion', 'fecha', 'usuario', 'ip', 'descripcion']
    // item: '<td class="nombre_tipo"></td><td class="descripcion_tipo"><center></center></td>'
  };

  var tipo_actividadList = new List('log', options);

});
