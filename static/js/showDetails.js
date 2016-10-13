$(function(){
    $('.detalles').each(function(event){ /* selecciona los div con la clase .detalles*/
    
        var largo_max = 140; /* indica cuantos caracteres apareceran antes de que aparezca "Mas detalles" */

        if($(this).html().length > largo_max){
            var contenido_corto   = $(this).html().substr(0,largo_max); /* Divide el contenido en dos partes */
            var contenido_largo    = $(this).html().substr(largo_max);
            
            $(this).html(contenido_corto+'<span class="ocultar"> (...)</span>'+
                         '<a href="#" class="leer_mas"><br/>Mas detalles</a>'+
                         '<span class="mas_texto" style="display:none;">'+contenido_largo+'</span>'+
                         '<a href="#" class="leer_menos" style="display:none;"><br/>Menos detalles</a>'); /* Nueva forma del contenido, para usar la funcionalidad */

                         
            $(this).find('a.leer_mas').click(function(event){
                event.preventDefault();
                $(this).hide(); /* esconde "Mas detalles" */
                $(this).parents('.detalles').find('.ocultar').hide(); /* esconde los puntos suspensivos */
                $(this).parents('.detalles').find('.mas_texto').show(); /* muestra el resto del texto */
                $(this).parents('.detalles').find('.leer_menos').show(); /* muestra "Menos detalles" */
         
            });

            $(this).find('a.leer_menos').click(function(event){
                event.preventDefault(); 
                $(this).hide(); /* esconde "Menos detalles" */
                $(this).parents('.detalles').find('.ocultar').show(); /* muestra los puntos suspensivos */
                $(this).parents('.detalles').find('.mas_texto').hide(); /* esconde el texto largo */
                $(this).parents('.detalles').find('.leer_mas').show(); /* muestra "Mas detalles" */
         
            });
        }


        
    });
})