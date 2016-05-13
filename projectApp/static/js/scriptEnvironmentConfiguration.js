// $(document).ready(function () {
//     var optionsArr = [];
//     var env = $('#environment');
//     var tableOptEnv = $('.tableOptEnvironment').find('tbody');
//
//     var mainUrlEnv = 'envopt/';
//
//     var generateOptionFormEnv = function (type, key, container) {
//         container.append(
//             '<tr>' +
//                 '<td><label for="' + key + '">' + key + '</label></td>' +
//                 '<td><input type="' + type + '" name="' + key + '" id="' + key + '" class="form-control"/></td>' +
//                 '</tr>'
//         );
//     };
//
//     var getOptEnv = function (url) {
//         $.get(url, function (json) {
//             var optionList = json['option_list'];
//             optionsArr = [];
//             tableOptEnv.empty();
//
//             for (var key in optionList) {
//                 var label = key + '';
//                 optionsArr[optionsArr.length] = label;
//
//                 if (optionList[label] == 'int') {
//                     generateOptionFormEnv('number', label, tableOptEnv);
//                 }
//                 if (optionList[label] == 'string' || optionList[key + ''] == 'double') {
//                     generateOptionFormEnv('string', label, tableOptEnv);
//                 }
//             }
//         });
//     }
//
//     env.change(function () {
//         getOptEnv(mainUrlEnv + $(this).val());
//     });
//
//     if (env.length) {
//         getOptEnv(mainUrlEnv + env.val());
//     }
//
// });