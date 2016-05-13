$(document).ready(function () {
    var optionsArr = [];
    var optionBody = $('.option-body');

    var func = $('#func');
    var alg = $('#alg');

    var tableOptFunc = $('.tableOptFunction').find('tbody');
    var tableOptAlg = $('.tableOptAlgorithm').find('tbody');

    var mainUrlFunc = 'getfuncopt/';
    var mainUrlAlg = 'getalgopt/';

    var generateOptionForm = function (type, key, container) {
        container.append(
            '<tr>' +
                '<td><label for="' + key + '">' + key + '</label></td>' +
                '<td><input type="' + type + '" name="' + key + '" id="' + key + '" class="form-control"/></td>' +
                '</tr>'
        );
    };

    var getFuncOpt = function (url) {
        $.get(url, function (json) {
            var optionList = json['option_list'];
            optionsArr = [];
            tableOptFunc.empty();

            for (var key in optionList) {
                var label = key + '';
                optionsArr[optionsArr.length] = label;

                if (optionList[label] == 'int') {
                    generateOptionForm('number', label, tableOptFunc);
                }
                if (optionList[label] == 'string' || optionList[key + ''] == 'double') {
                    generateOptionForm('string', label, tableOptFunc);
                }
            }
        });
    }

    var getAlgOpt = function (url) {
        $.get(url, function (json) {
            var optionList = json['option_list'];
            optionsArr = [];
            tableOptAlg.empty();

            for (var key in optionList) {
                var label = key + '';
                optionsArr[optionsArr.length] = label;

                if (optionList[label] == 'int') {
                    generateOptionForm('number', label, tableOptAlg);
                }
                if (optionList[label] == 'string' || optionList[key + ''] == 'double') {
                    generateOptionForm('string', label, tableOptAlg);
                }
            }
        });
    };

    func.change(function () {

        var task = $(this).val();
        var url = 'getalg/' + task;

        $.get(url, function (json) {
            var algList = json['alg_list'];
            var selectAlg = $('#alg');

            selectAlg.empty();
            optionBody.empty();

            for (var i = 0; i < algList.length; i++) {
                selectAlg.append('<option value = "' + algList[i] + '">' + algList[i] +
                    '</option>');
            }

            getFuncOpt(mainUrlFunc + task);
            getAlgOpt(mainUrlAlg + selectAlg.val());
        });

    });

    alg.change(function () {
        var alg = $(this).val();
        var url = 'getalgopt/' + alg;

        getAlgOpt(url);
    });

    $('#form-task-conf').submit(function (event) {
        event.preventDefault();

        var form = $(this);

        var optData = form.serialize();
        var url = form.attr('action');

        $.post(url, optData, function (json) {
            if (json['result'] == 'success') {
                alert("success");
            }
            else {
                alert("error");
            }
        });
    });


    if (func.length) {
        getFuncOpt(mainUrlFunc + func.val());
    }

    if (alg.length) {
        getAlgOpt(mainUrlAlg + alg.val());
    }

});