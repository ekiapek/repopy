var API_URL = "http://127.0.0.1:8000/api/";
var BASE_URL = "http://127.0.0.1:8000/";
var RESPONSE_SUCCESS = "0";
var RESPONSE_ERROR = "9";
var NO_REPOSITORY_FOUND = "5";

$( document ).ready(function() {
    var repository = JSON.parse(document.getElementById('repository').textContent);
    var x = "";
    $('#btn-search').click(function(){
        var searchQuery = $('#search').val();
        var repoSelect = $('repo-select').val();
        $.ajax({

        })
    });

    // var repoSelect = $('repo-select').val();
    // sxQuery("#search").unibox({
    //     // these are the required:
    //     suggestUrl: '/api/searchSuggest?&q=', // the URL where to get the search suggests
    //     animationSpeed: 200,
    //     instantVisualFeedback: 'all',
    //     showOnMobile: true,
    //     });
    
    $('#tab-browse').click(function(){
        if(!$('#tab-browse').hasClass("active")){
            $('#tab-browse').addClass("active");
        }
        if($('#tab-search').hasClass("active")){
            $('#tab-search').removeClass("active");
        }
    });

    $('#tab-search').click(function(){
        if(!$('#tab-search').hasClass("active")){
            $('#tab-search').addClass("active");
        }
        if($('#tab-browse').hasClass("active")){
            $('#tab-browse').removeClass("active");
        }
    });

    $('#folder-tree').jstree({
        'core':{
            'data':{
                'url' : API_URL + 'files/GetFilesInRepository/?RepositoryID=' + repository.RepositoryID
            },
        }
    });

    $('#folder-tree').on(
        "select_node.jstree", function(event, data){
            $.ajax({
                url : API_URL + "files/Get?FileID=" + data.node.id,
                method: 'GET',
                success: function(data){
                    if($('#code').children().length > 0){
                        $('#code').empty();
                        $('#code').append(data);
                        Prism.highlightAll();
                    }
                    else{
                        $('#code').append(data);
                        Prism.highlightAll();
                    }
                }
            });
        }
    );
});

