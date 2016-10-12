$(document).ready(function(){
    // Pasamos los argumentos para eliminar tipo actividad.
  $('#myModalRestaurar').on('show.bs.modal', function(e){
      var linkRestaurar = $(e.relatedTarget).data('link-restaurar');
      $("#BotonRestaurar").attr("href", linkRestaurar);
  });
});
