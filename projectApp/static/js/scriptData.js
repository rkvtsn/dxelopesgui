/*
 *
 *   Скрипты во вкладке Data
 *
 * */

$(document).ready(function () {

    if ($('#sql').length) {
//        var myCodeMirror = CodeMirror.fromTextArea(document.getElementById('sql'), {
//            lineNumbers: true,
//            mode: 'text/x-mysql',
//            theme: 'mdn-like',
//            readOnly: false
//        });
    }

    //  Переключение типа загружаемых данных -------------------------------------------

    $('.radioData').change(function () {
        $(this).closest('.group-inputs').find('.form-group').find('input, textarea').removeAttr('readonly');

        var prev = $(this).closest('.group-inputs').prevAll('.group-inputs');
        var next = $(this).closest('.group-inputs').nextAll('.group-inputs');

        prev.find('.form-group').find('input, textarea').attr('readonly', 'readonly');
        next.find('.form-group').find('input, textarea').attr('readonly', 'readonly');

//        myCodeMirror.setOption('readOnly', false);
    });


    //  Заглузка данных ---------------------------------------------------------------

    $('#form_data').submit(function (event) {
        event.preventDefault();

        var form = $(this);

        var data = form.serialize();
        var urlForm = form.attr('action');

        $.post(urlForm, data, function (json) {
            if (json['result'] == 'error') {

                var errorContent = '<div class="alert alert-danger" role="alert">' +
                    '<button type="button" class="close" data-dismiss="alert" aria-label="Close">' +
                    '<span aria-hidden="true">&times;</span>' +
                    '</button>' +
                    '<strong>Wrong dataset name!</strong> ' + json['message'] +
                    '</div>';

                form.find('.error-message').html(errorContent);
            }
            else {
                window.location.replace(json['data_name']);
            }
        });
    });

});