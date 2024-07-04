function get_current_file_id() {
    var selectedElements = document.getElementsByClassName('selected');
    var element = selectedElements[0].parentElement;
    return element.querySelector('a').getAttribute('id');
}



function get_file_path_list(elementId, currentPath) {
    var element = document.getElementById(elementId);
    var currentName = element.innerText;

    if (element.classList.contains('is-dir')) {
        currentPath.push(currentName);
    }

    var parent = element.parentNode.parentNode.parentNode.parentNode;
    if (parent.tagName === 'LI') {
        var anchorElement = parent.querySelector('a');
        var parentId = anchorElement.getAttribute('id');
        get_file_path_list(parentId, currentPath);
    }
    return currentPath;
}

function get_file_path() {
    var path_list = get_file_path_list(get_current_file_id(), []);
    path_list.push("/");
    //path_list = path_list.reverse();
    var path = path_list.reverse().join("/");
    if (path === "/") {

    } else {
        path = path.substring(1);
    }
    //path.append('/');
    return path;
}
function get_full_file_path_list(elementId, currentPath) {
    var element = document.getElementById(elementId);
    var currentName = element.innerText;
    currentPath.push(currentName);
    var parent = element.parentNode.parentNode.parentNode.parentNode;
    if (parent.tagName === 'LI') {
        var anchorElement = parent.querySelector('a');
        var parentId = anchorElement.getAttribute('id');
        get_file_path_list(parentId, currentPath);
    }
    return currentPath;
}

function get_full_file_path() {
    var path_list = get_full_file_path_list(get_current_file_id(), []);
    path_list.push("/");
    //path_list = path_list.reverse();
    var path = path_list.reverse().join("/");
    if (path === "/") {

    } else {
        path = path.substring(1);
    }
    //path.append('/');
    return path;
}
function check_is_dir() {
    var elementId = get_current_file_id();
    var element = document.getElementById(elementId);
    return element.classList.contains('is-dir');
}

const json_name = "../static/test.json"
const search_result = "../static/test2.json"
//var id = 1;
var path = "";
var full_path = "";
function generate_list(data, parent) {
    var ul = $('<ul>').addClass('list-group');
    parent.append(ul);

    $.each(data.children, function (index, item) {
        var li = $('<li>').addClass('list-group-item selectable-block');
        ul.append(li);

        if (item.isdir) {
            var a = $('<a>').attr('data-toggle', 'collapse').attr('href', '#level' + item.id).attr('id', 'element' + item.id).text(item.name);
            a.addClass('is-dir');
            li.append(a);

            var button = $('<button>').addClass('check-box btn-primary').text('select');
            li.append(button);
            button.click(function() {
                $(this).text('selected');
                $(this).addClass('selected');
                $('.check-box').not(this).text('select');
                $('.check-box').not(this).removeClass('selected');
                path = get_file_path(get_current_file_id(), []);
                document.getElementById("path_value").value = path;
                full_path = get_full_file_path(get_current_file_id(), []);
                document.getElementById("full_path_value").value = full_path;
                document.getElementById("download_is_dir").value = check_is_dir();
                document.getElementById("remove_is_dir").value = check_is_dir();
                document.getElementById("remove_id").value = get_current_file_id();
                document.getElementById("dir_path_value").value = path;
                document.getElementById("download_path_value").value = full_path;
                document.getElementById("download_id").value = get_current_file_id();
                //console.log(get_current_file_id());
            });

            var childrenUl = $('<ul>').addClass('collapse').attr('id', 'level' + item.id);
            li.append(childrenUl);

            generate_list(item, childrenUl);
        } else {
            var a = $('<a>').text(item.name).attr('id', 'element' + item.id);
            a.addClass('is-file');
            li.append(a);

            var button = $('<button>').addClass('check-box btn-primary').text('select');
            li.append(button);
            button.click(function() {
                $(this).text('selected');
                $(this).addClass('selected');
                $('.check-box').not(this).text('select');
                $('.check-box').not(this).removeClass('selected');
                path = get_file_path(get_current_file_id(), []);
                document.getElementById("path_value").value = path;
                full_path = get_full_file_path(get_current_file_id(), []);
                document.getElementById("full_path_value").value = full_path;
                document.getElementById("download_is_dir").value = check_is_dir();
                document.getElementById("remove_is_dir").value = check_is_dir();
                document.getElementById("remove_id").value = get_current_file_id();
                document.getElementById("dir_path_value").value = path;
                document.getElementById("download_path_value").value = full_path;
                document.getElementById("download_id").value = get_current_file_id();
            });
        }
    });

}
