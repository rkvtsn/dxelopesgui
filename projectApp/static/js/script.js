
var srv = {

};

$(document).ready(function () {

    var serverMessages = $("#server-messages");

    srv.showServerMessages = function(msgArray){
        serverMessages.find('li').remove();
        serverMessages.hide();

        if (msgArray == null || msgArray.length == 0) return;

        $.each(msgArray, function(index,msg) {
            serverMessages.append('<li>'+msg+'</li>')
        });
        serverMessages.show();
    };

    // Error messages ---------------------------------------------------------------
    function errorMessage(container, message) {
        var error = '<div class="alert alert-danger" role="alert">' +
            '<button type="button" class="close" data-dismiss="alert" aria-label="Close">' +
            '<span aria-hidden="true">&times;</span>' +
            '</button>' +
            '<strong>Error!</strong> ' + message +
            '</div>';

        container.append(error);
    }

    // End Error messages ---------------------------------------------------------------


    //  Tooltips ----------------------------------------------------------

    $('[data-toggle="tooltip"]').tooltip();

    //  End Tooltips ----------------------------------------------------------


    // Log In ---------------------------------------------------------------------

    var modalLogIn = $('#modalLogIn');
    var formLogIn = $('#formLogIn');
    var urlLogIn = formLogIn.attr('action');

    formLogIn.submit(function (event) {
        event.preventDefault();

        var form = $(this);

        var name = $('#name');
        var password = $('#password');

        if (name.val() == "" || password.val() == "") {
            name.closest('.form-group').addClass('has-error');
            password.closest('.form-group').addClass('has-error');
            modalLogIn.addClass('animated shake');
        }
        else {
            name.closest('.form-group').removeClass('has-error');
            password.closest('.form-group').removeClass('has-error');

            var data = form.serialize();

            $.post(urlLogIn, data, function (json) {

                if (json['result'] == 'error') {
                    name.closest('.form-group').addClass('has-error');
                    password.closest('.form-group').addClass('has-error');
                    modalLogIn.addClass('animated shake');
                }
                else {
                    modalLogIn.modal('hide');
                    window.location.reload();
                }
            });
        }
    });

    modalLogIn.on('hidden.bs.modal', function (e) {
        $(this).removeClass('animated shake');
        $(this).find('.form-group').removeClass('has-error');
        $('#name').val("");
        $('#password').val("");
    });

    $('.link-logout').click(function (event) {
        event.preventDefault();

        var url = $(this).attr('href');

        $.get(url, function (json) {
            window.location.replace("/");
        });
    });

    // End Log In ---------------------------------------------------------------------

    // Registration ---------------------------------------------------------------------

    var modalReg = $('#modalReg');

    $('#formReg').submit(function (event) {
        event.preventDefault();

        var form = $(this);

        var url = form.attr('action');

        var name = $('#reg-name');
        var password = $('#reg-password');

        if (name.val() == "" || password.val() == "") {
            name.closest('.form-group').addClass('has-error');
            password.closest('.form-group').addClass('has-error');
            modalLogIn.addClass('animated shake');
        }
        else {
            name.closest('.form-group').removeClass('has-error');
            password.closest('.form-group').removeClass('has-error');

            var data = form.serialize();

            $.post(url, data, function (json) {

                if (json['result'] == 'error') {
                    name.closest('.form-group').addClass('has-error');
                    password.closest('.form-group').addClass('has-error');
                    modalReg.addClass('animated shake');
                }
                else {
                    modalReg.modal('hide');
                    window.location.reload();
                }
            });
        }
    });

    modalReg.on('hidden.bs.modal', function (e) {
        $(this).removeClass('animated shake');
        $(this).find('.form-group').removeClass('has-error');
        $('#reg-name').val("");
        $('#reg-password').val("");
    });

    // New Project ---------------------------------------------------------------------

    var formNewProject = $('#formNewProject');
    var modalNewProject = $('#modalCreateProject');

    formNewProject.submit(function (event) {
        event.preventDefault();
        var form = $(this);
        var projectName = $('#projname');

        var str = projectName.val().toString();

        if (projectName.val().length === 0 || str.indexOf(',') != -1) {
            projectName.closest('.form-group').addClass('has-error');
            errorMessage(form.find('.error-messages'), 'Please, enter correct project name.');
        }
        else {
            projectName.closest('.form-group').removeClass('has-error');
            form.find('.error-messages').empty();
            var data = form.serialize();
            $.post(form.attr('action'), data, function (json) {
                if (json['result'] == 'error') {
                    errorMessage(form.find('.error-messages'), '');
                }
                else {
                    modalNewProject.modal('hide');
                    window.location.reload();
                }
            })
        }
    });

    // End New Project ---------------------------------------------------------------------


    // Delete Project ----------------------------------------------------------------------

    $('.btn-delete-project').click(function (event) {
        event.preventDefault();
        var row = $(this).closest('.row-proj');
        var link = $(this).attr('href');

        $.get(link, function (json) {
            if (json['result'] == 'success') {
                row.remove();
            }
        })
    });



    //  Delete saved data, configurations and so on ----------------------------------------

    $('.remove').click(function (event) {
        event.preventDefault();

        var elem = $(this).closest('.elem');
        var link = elem.find('.remove').attr('href');

        $.get(link, function (json) {

            if (json['result'] == 'success') {
                elem.remove();
            }
            else {
                alert(json['error']);
            }

        }, "json")
    });

});