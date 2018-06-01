
jQuery(document).ready(function(){
	// All jquery is a 2 step process:
	// 1) select an element
	// 2) act on it
	// syntax- period corresponds to class.

	jQuery(".ui-delete").click(function(){     
        var id=($(this).parents(".ui-element")).attr("id")
        console.log(id);
        jQuery.ajax({
            data: {
                id : id
            },
            type: 'DELETE',
            url: '/student/'+id


            //url: '/student/33'//+'$(\'#idDisplay\').val()'
        })

        .done(function(data) {
        console.log(data);


        //     if(data['error']!=null) {
        //         //$('#ui-info-message').show();
        //         console.log("error")
        //         //$('#ui-error-message').show();
        //     }
        //     else {
        //         //$('#ui-info-message').show(); //set attr to error. check args?
        //         console.log("no error")
        //         jQuery(this).parents(".ui-element").fadeOut();
			     // // "this" refers to the current element, since there could be multiple events with class "ui-delete"
			     // // making the parent element disappear also makes current element disappear
                
        //     }
        });
        jQuery(this).parents(".ui-element").fadeOut();

        event.preventDefault();
	});
});

