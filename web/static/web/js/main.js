var API_URL = "http://localhost:8000/api/"
var RESPONSE_SUCCESS = "0"
var RESPONSE_ERROR = "9"

$( document ).ready(function() {
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
});

