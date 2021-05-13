var API_URL = "http://127.0.0.1:8000/api/";
var BASE_URL = "http://127.0.0.1:8000/";
var RESPONSE_SUCCESS = "0";
var RESPONSE_ERROR = "9";
var NO_REPOSITORY_FOUND = "5";

$(document).ready(function () {
    $('#code-markup').hide();
    var repository = JSON.parse(document.getElementById('repository').textContent);
    var x = "";

    //get autocompleter
    autocomplete(document.getElementById("search-bar"), repository);

    // var repoSelect = $('repo-select').val();
    // sxQuery("#search").unibox({
    //     // these are the required:
    //     suggestUrl: '/api/searchSuggest?&q=', // the URL where to get the search suggests
    //     animationSpeed: 200,
    //     instantVisualFeedback: 'all',
    //     showOnMobile: true,
    //     });

    $('#tab-browse').click(function () {
        if (!$('#tab-browse').hasClass("active")) {
            $('#tab-browse').addClass("active");
        }
        if ($('#tab-search').hasClass("active")) {
            $('#tab-search').removeClass("active");
        }
    });

    $('#tab-search').click(function () {
        if (!$('#tab-search').hasClass("active")) {
            $('#tab-search').addClass("active");
        }
        if ($('#tab-browse').hasClass("active")) {
            $('#tab-browse').removeClass("active");
        }
    });

    $('#folder-tree').jstree({
        'core': {
            'data': {
                'url': API_URL + 'files/GetFilesInRepository/?RepositoryID=' + repository.RepositoryID
            },
        }
    });

    $('#folder-tree').on(
        "select_node.jstree", function (event, data) {
            if (!data.node.children.length > 0) {
                $('#code-title').show();
                document.getElementById("overlay").style.display = "block";
            }
            else {
                $('#code-title').hide();
            }
            $.ajax({
                url: API_URL + "files/Get/?FileID=" + data.node.id,
                method: 'GET',
                success: function (result) {
                    displayCode(result, data.node);
                },
                error: function() {
                    displayCode("Problem getting file data", data.node);
                }
            });
        }
    );

    // $('#help-btn').click(function(event){
    //     // event.preventDefault();
    //     $('#modal-help').modal({
    //         fadeDuration:100,
    //         show
    //     });
    // });
});

function generateFileType(format) {
    switch (format) {
        case "py": return "-python";
        case "html": return "-markup";
        case "css": return "-css";
        case "xml": return "-markup";
        case "js": return "-javascript";
        default: return "-vim";
    }
}

function displayCode(data, node) {
    var codeTitle = node.text;
    var codeTitles = codeTitle.split(".");
    var fileFormat = codeTitles[codeTitles.length - 1];
    var filetype = generateFileType(fileFormat);
    var generatedClass = "language" + filetype;
    document.getElementById("overlay").style.display = "none";
    $('#code').removeClass();
    $('#code').addClass(generatedClass);
    $('#code-title').text(codeTitle);
    if ($('#code').children().length > 0) {
        if (generatedClass.indexOf("html") > 0) {
            $('#code-pre').hide();
            $('#code').hide();
            $('#code-markup').append('<script type="text/plain" class="language-markup">' + data + '</script>');
            $('#code-markup').show();
        }
        else {
            if ($('#code-pre').is(":hidden") || $('#code').is(":hidden")) {
                $('#code-pre').show();
                $('#code').show();
                $('#code-markup').hide();
                $('#code-markup').empty();
            }
        }
        $('#code').empty();
        $('#code').append(data);

        $('#code-pre').attr("data-line", "");

        Prism.highlightAll();
    }
    else {

        $('#code-pre').attr("data-line", "");

        $('#code').append(data);
        Prism.highlightAll();
    }
}

function displayCodeFromSearch(data, searchResult) {
    var codeTitle;
    var codeTitles;
    var fileFormat;
    var filetype;
    if (Boolean(searchResult.Filename)) {
        codeTitle = searchResult.Filename;
        codeTitles = codeTitle.split(".");
        fileFormat = codeTitles[codeTitles.length - 1];
        filetype = generateFileType(fileFormat);
    }
    else {
        codeTitle = "";
        filetype = "-vim";
    }
    var generatedClass = "language" + filetype;
    document.getElementById("overlay").style.display = "none";
    $('#code').removeClass();
    $('#code').addClass(generatedClass);
    $('#code-title').text(codeTitle);
    document.getElementById("overlay").style.display = "none";
    if ($('#code').children().length > 0) {
        if (generatedClass.indexOf("html") > 0) {
            $('#code-pre').hide();
            $('#code').hide();
            $('#code-markup').append('<script type="text/plain" class="language-markup">' + data + '</script>');
            $('#code-markup').show();
        }
        else {
            if ($('#code-pre').is(":hidden") || $('#code').is(":hidden")) {
                $('#code-pre').show();
                $('#code').show();
                $('#code-markup').hide();
                $('#code-markup').empty();
            }
        }
        $('#code').empty();
        if(!Boolean(searchResult.LineNo) && Boolean(searchResult.Query)){
            const searchText = searchResult.Query;
            const regex = new RegExp(searchText, 'gi');
            let text = data;
            text = text.replace(/(<mark class="highlight">|<\/mark>)/gim, '');

            const newText = text.replace(regex, '<mark class="highlight">$&</mark>');
            data = newText;
        }
        $('#code').append(data);
        if (Boolean(searchResult.LineNo)) {
            var line = parseInt(searchResult.LineNo);
            $('#code-pre').attr("data-line", line);
        }
        else {
            $('#code-pre').attr("data-line", "");
        }
        Prism.highlightAll();
    }
    else {
        if(!Boolean(searchResult.LineNo) && Boolean(searchResult.Query)){
            const searchText = searchResult.Query;
            const regex = new RegExp(searchText, 'gi');
            let text = data;
            text = text.replace(/(<mark class="highlight">|<\/mark>)/gim, '');

            const newText = text.replace(regex, '<mark class="highlight">$&</mark>');
            data = newText;
        }
        $('#code').append(data);
        if (Boolean(searchResult.LineNo)) {
            var line = parseInt(searchResult.LineNo);
            $('#code-pre').attr("data-line", line);
        }
        else {
            $('#code-pre').attr("data-line", "");
        }
        Prism.highlightAll();
    }
}

function autocomplete(inp, repository) {
    /*the autocomplete function takes two arguments,
    the text field element and an array of possible autocompleted values:*/
    var currentFocus;
    /*execute a function when someone writes in the text field:*/
    inp.addEventListener("input", function (e) {
        var a, b, i, val = this.value;
        /*close any already open lists of autocompleted values*/
        closeAllLists();
        if (!val) { return false; }
        currentFocus = -1;

        $.ajax({
            url: API_URL + "search/SearchSuggest/",
            data: {
                q: val,
                Repository: repository.RepositoryID
            },
            method: "GET",
            success: function (data) {
                /*create a DIV element that will contain the items (values):*/
                a = document.createElement("DIV");
                a.setAttribute("id", inp.id + "autocomplete-list");
                a.setAttribute("class", "autocomplete-items");
                /*append the DIV element as a child of the autocomplete container:*/
                inp.parentNode.appendChild(a);
                /*for each item in the array...*/
                for (i = 0; i < data.length; i++) {
                    /*check if the item starts with the same letters as the text field value:*/
                    if (data[i].string.substr(0, val.length).toUpperCase() == val.toUpperCase()) {
                        /*create a DIV element for each matching element:*/
                        b = document.createElement("DIV");
                        /*make the matching letters bold:*/
                        b.innerHTML = "<strong>" + data[i].string.substr(0, val.length) + "</strong>";
                        b.innerHTML += data[i].string.substr(val.length);
                        /*insert a input field that will hold the current array item's value:*/
                        b.innerHTML += "<input class='ac' type='hidden' value='" + data[i].string + "'>";
                        /*execute a function when someone clicks on the item value (DIV element):*/
                        b.addEventListener("click", function (e) {
                            /*insert the value for the autocomplete text field:*/
                            inp.value = this.getElementsByClassName("ac")[0].value;
                            /*close the list of autocompleted values,
                            (or any other open lists of autocompleted values:*/
                            closeAllLists();
                            $('#tab-browse').removeClass("active");
                            $('#tab-browse > a').removeClass("active");
                            $('#tab-browse-content').removeClass("active");
                            $('#tab-search').addClass("active");
                            $('#tab-search > a').addClass("active");
                            $('#tab-search-content').addClass("active");
                            $('#tab-search-content').addClass("show");
                            search(inp.value, repository);
                        });
                        a.appendChild(b);
                    }
                }
            }
        });
    });
    /*execute a function presses a key on the keyboard:*/
    inp.addEventListener("keydown", function (e) {
        var x = document.getElementById(inp.id + "autocomplete-list");
        if (x) x = x.getElementsByTagName("div");
        if (e.keyCode == 40) {
            /*If the arrow DOWN key is pressed,
            increase the currentFocus variable:*/
            currentFocus++;
            /*and and make the current item more visible:*/
            addActive(x);
        } else if (e.keyCode == 38) { //up
            /*If the arrow UP key is pressed,
            decrease the currentFocus variable:*/
            currentFocus--;
            /*and and make the current item more visible:*/
            addActive(x);
        } else if (e.keyCode == 13) {
            /*If the ENTER key is pressed, prevent the form from being submitted,*/
            e.preventDefault();
            if (currentFocus > -1) {
                /*and simulate a click on the "active" item:*/
                if (x) x[currentFocus].click();
            }
            val = this.value;
            search(val, repository);
            $('#tab-browse').removeClass("active");
            $('#tab-browse > a').removeClass("active");
            $('#tab-browse-content').removeClass("active");
            if (!$('#tab-search').hasClass("active")) {
                $('#tab-search').addClass("active");
                $('#tab-search > a').addClass("active");
                $('#tab-search-content').addClass("active");
                $('#tab-search-content').addClass("show");
            }
        }
    });
    function addActive(x) {
        /*a function to classify an item as "active":*/
        if (!x) return false;
        /*start by removing the "active" class on all items:*/
        removeActive(x);
        if (currentFocus >= x.length) currentFocus = 0;
        if (currentFocus < 0) currentFocus = (x.length - 1);
        /*add class "autocomplete-active":*/
        x[currentFocus].classList.add("autocomplete-active");
    }
    function removeActive(x) {
        /*a function to remove the "active" class from all autocomplete items:*/
        for (var i = 0; i < x.length; i++) {
            x[i].classList.remove("autocomplete-active");
        }
    }
    function closeAllLists(elmnt) {
        /*close all autocomplete lists in the document,
        except the one passed as an argument:*/
        var x = document.getElementsByClassName("autocomplete-items");
        for (var i = 0; i < x.length; i++) {
            if (elmnt != x[i] && elmnt != inp) {
                x[i].parentNode.removeChild(x[i]);
            }
        }
    }
    /*execute a function when someone clicks in the document:*/
    document.addEventListener("click", function (e) {
        closeAllLists(e.target);
    });
}

function search(query, repository) {
    container = $('#tab-search-content');
    $.ajax({
        url: API_URL + "search/Search/",
        data: {
            q: query,
            Repository: repository.RepositoryID
        },
        method: "GET",
        success: function (result) {
            container.empty();
            console.log(result);
            result.forEach(item => {
                if (item.HasRelation) {
                    container.append(generateResultWithRelation(item));
                }
                else {
                    container.append(
                        $(generateResultNoRelation(item))
                            .bind("click", function () {
                                // console.log(item.Result);
                                document.getElementById("overlay").style.display = "block";
                                if (Boolean(item.FileID)) {
                                    $.ajax({
                                        url: API_URL + "files/Get/?FileID=" + item.FileID,
                                        method: 'GET',
                                        success: function (fileResult) {
                                            displayCodeFromSearch(fileResult, item);
                                        },
                                        error: function() {
                                            item.LineNo = "";
                                            displayCodeFromSearch("Problem getting file data", item);
                                        }
                                    });
                                }
                            })
                    );
                }
            });
            // for (item in result) {
            //     if(item.HasRelation){

            //     }
            //     else{
            //         container.append(
            //             $(generateResultNoRelation(item))
            //             .bind("click",function(){
            //                 console.log(item.Result);
            //             })
            //         );
            //     }
            // }
        }
    });
}

function generateResultWithRelation(result) {
    var arrRelationsParent = [];
    var arrRelationsChild = [];
    var arrRelationsClass = [];
    var pParent = $('<p class="text-muted mb-0">Parent:</p>');
    var pChild = $('<p class="text-muted mb-0">Child:</p>');
    var pClass = $('<p class="text-muted mb-0">In class:</p>');
    result.Relations.forEach(obj => {
        var relation = $('<a href="#"><div class="card card-detail mb-2"><div class="card-body"><h6 class="text-muted card-subtitle mb-1">' + obj.Result + '</h6></div></div></div></a>').bind("click", function (e) {
            e.preventDefault();
            // console.log(obj.Result);
            document.getElementById("overlay").style.display = "block";
            if (Boolean(obj.FileID)) {
                $.ajax({
                    url: API_URL + "files/Get/?FileID=" + obj.FileID,
                    method: 'GET',
                    success: function (fileResult) {
                        displayCodeFromSearch(fileResult, obj);
                    },
                    error: function() {
                        obj.LineNo = "";
                        displayCodeFromSearch("Problem getting file data", obj);
                    }
                });
            }
            else {
                displayCodeFromSearch("External library", obj);
            }
        });
        if (obj.RelationName.indexOf("parent") !== -1) {
            var level = obj.RelationName.split("-");
            if(level.length > 1){
                relation.find('.card-body').append('<p class="mb-0">Parent level '+level[1]+'</p');
                arrRelationsParent.push(relation);
            }
            else{
                arrRelationsParent.push(relation);    
            }
        }
        else if (obj.RelationName.indexOf("child") !== -1) {
            var level = obj.RelationName.split("-");
            if(level.length > 1){
                relation.find('.card-body').append('<p class="mb-0">Child level '+level[1]+'</p');
                arrRelationsChild.push(relation);
            }
            else{
                arrRelationsChild.push(relation);
            }
        }
        else if (obj.RelationName == "class") {
            arrRelationsClass.push(relation);
        }
    });
    var node = $('<div class="card card-main mb-3" style="border-radius: 10px;border:0px;"><div id="card-body-main" class="card-body"></div>');
    var cardTitle = $('<a href="#"><div><h4 class="card-title">' + result.Result + '</h4><h6 class="text-muted card-subtitle mb-2">' + result.Filename + '</h6></div></a>')
        .bind("click", function () {
            document.getElementById("overlay").style.display = "block";
            if (Boolean(result.FileID)) {
                $.ajax({
                    url: API_URL + "files/Get/?FileID=" + result.FileID,
                    method: 'GET',
                    success: function (fileResult) {
                        displayCodeFromSearch(fileResult, result);
                    },
                    error: function() {
                        result.LineNo = "";
                        displayCodeFromSearch("Problem getting file data", result);
                    }
                });
            }
        });
    node.find('#card-body-main').append(cardTitle);
    if (arrRelationsParent.length > 0) {
        node.find('#card-body-main').append(pParent);
        arrRelationsParent.forEach(item => {
            node.find('#card-body-main').append(item);
        });
    }
    if (arrRelationsChild.length > 0) {
        node.find('#card-body-main').append(pChild);
        arrRelationsChild.forEach(item => {
            node.find('#card-body-main').append(item);
        });
    }
    if (arrRelationsClass.length > 0) {
        node.find('#card-body-main').append(pClass);
        arrRelationsClass.forEach(item => {
            node.find('#card-body-main').append(item);
        });
    }
    return node;
}

function generateResultNoRelation(result) {
    return '<a href="#"><div class="card card-main mb-3" style="border-radius: 10px;border:0px;"><div class="card-body"><h4 class="card-title">' + result.Result + '</h4><h6 class="text-muted card-subtitle mb-2">' + result.Filename + '</h6></div></a>';
}

