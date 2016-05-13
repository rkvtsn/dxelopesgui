$(document).ready(function () {

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

    //  Добавление/Удаление select для выбора набора данных

    var arrSelects = ['dataSet0'];

    function addNewSelect() {
        var num = arrSelects.length;
        var id = 'dataSet' + num;
        arrSelects[num] = id;

        var group = $('.groupDataSets').find('.form-group').first();

        var newGroup = group.clone().appendTo('.groupDataSets');

        newGroup.find('.l-select-container').find('select').wrap('<div class="input-group"></div>');

        newGroup.find('.input-group').append(
            '<span class="input-group-btn">' +
                '<button class="btn btn-danger removeSelect" type="button">' +
                '<span class="glyphicon glyphicon-remove"></span>' +
                '</button>' +
                '</span>');

        newGroup.find('label').attr('for', id);
        newGroup.find('select').attr('id', id).attr('name', id);
    }

    $('#addNewPhysicalDataSet').click(function (event) {
        event.preventDefault();
        addNewSelect();
    });

    $(document).on('click', '.removeSelect', function (event) {
        event.preventDefault();

        var row = $(this).closest('.form-group');

        var selectId = row.find('select').attr('id');

        var index = arrSelects.indexOf(selectId);

        if (index >= 0) {
            arrSelects.splice(index, 1);

            var arr = arrSelects;

            row.remove();
        }
    });


    //  Создание новой задачи
    function sendFormTasks(data) {
        $.post($('#formTasks').attr('action'), data, function (json) {
            var result = json['result'];

            if (result == "error") {
                alert(json['error']);
            }
            else {
                window.location.replace(json['task_name']);
            }

        }, "json");
    }

    $('#formTasks').submit(function (event) {
        event.preventDefault();

        var flag = true;

        var errorContainer = $('.error-messages');
        errorContainer.empty();

        if ($('#name').val() == "") {
            flag = false;

            errorMessage(errorContainer, 'Enter task name.');
        }

        for (var i = 0; i < arrSelects.length; i++) {
            var select = $('select#' + arrSelects[i]);

            if (select.val() == '') {
                flag = false;

                errorMessage(errorContainer, 'Select data set.');

                break;
            }
        }

        if (flag) {
            var data = $(this).serialize() + '&arr_selects=' + arrSelects;
            sendFormTasks(data);
        }
    });

    // Удаление задачи


    //  Выбор и настройка преобразования

    var typeAssignment = $('#typeAssignment');

    $.get(typeAssignment.attr('data-url'), function (data) {
        $('#panelTasksSettings').html(data)
    });

    function uploadAssignmentSettings(type) {
        $.get(typeAssignment.attr('data-url'), {'type': type}, function (data) {
            $('#panelTasksSettings').html(data)
        })
    }

    typeAssignment.change(function () {
        var type = $(this).val();

        uploadAssignmentSettings(type);
    });

});