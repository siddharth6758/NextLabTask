$(document).ready(function() {

    $.ajax({
        url:'/get_user_points/',
        method: "POST",
        success: function(response){
            if(response.status==200){
                $('#user-point-value').text(response.points)
            }
        },
        error: function(response){
            if(response.status==500){
                $('#user-point-value').text(response.points)
            }
        }
    })

    $('#btn_edit').click(function() {
        $('input[type="text"], input[type="email"]').removeAttr('disabled');

        $(this).hide();
        $('#btn_change_password').hide();
        $('#btn_save').show();
        $('#btn_cancel').show();
    });

    $('#btn_change_password').click(function() {
        $('input[type="password"]').parent().removeClass('hidden');
        $('input[type="text"], input[type="email"]').parent().hide();

        $(this).hide()
        $('#btn_edit').hide()
        $('#btn_save').show();
        $('#btn_cancel').show();
    });

    $('#btn_cancel').click(function() {
        location.reload();
    });

    $('.delete-btn').click(function(){
        var id = $(this).closest('.app-item').data('app-id')
        $.ajax({
            url: '/delete_app/',
            method: 'POST',
            data: {
                'id':id
            },
            success: function(response) {
                if(response.status==200){
                    location.reload();
                }
            },
            error: function(response) {
                if(response.status==500){
                    location.reload();
                }
            }
        })
    });

    $('.uninstall-app-button').click(function(){
        var id = $(this).closest('.app-item').data('app-id')
        $.ajax({
            url: '/uninstall_app_user/',
            method: 'POST',
            data: {
                'id':id
            },
            success: function(response) {
                if(response.status==200){
                    location.reload();
                }
            },
            error: function(response) {
                if(response.status==500){
                    location.reload();
                }
            }
        })
    });

    $('#id_category').change(function() {
        var category_id = $(this).val();
        $.ajax({
            url: '/get_subcategories/',
            method: "POST",
            data: {
                'category_id': category_id
            },
            success: function(data) {
                var $sub_category = $('#id_sub_category');
                $sub_category.empty();
                $.each(data, function(index, subcategory) {
                    $sub_category.append($('<option></option>').attr('value', subcategory.id).text(subcategory.sub_category));
                });
            }
        });
    });

});
