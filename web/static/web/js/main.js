var API_URL = "http://localhost:8000/api/"

$( document ).ready(function() {
    $('#btn-search').click(function(){
        var searchQuery = $('#search').val();
        var repoSelect = $('repo-select').val();
        $.ajax({

        })
    });

    var repoSelect = $('repo-select').val();
    sxQuery("#search").unibox({
        // these are the required:
        suggestUrl: '/api/searchSuggest?&q=', // the URL where to get the search suggests
        animationSpeed: 200,
        instantVisualFeedback: 'all',
        showOnMobile: true,
        });
});

