var API_URL = "http://localhost:8000/api/"
var BASE_URL = "http://localhost:8000/"
var RESPONSE_SUCCESS = "0"
var RESPONSE_ERROR = "9"

$(document).ready(function() {
    $('#get-started').click(function() {
        window.location.replace(BASE_URL + "welcome/create-repo/")
    });

    $('#select-file-btn').click(function() {
        $("#file-input").trigger("click");
    })

    $('#change-file-btn').click(function() {
        $("#file-input").trigger("click");
    })

    $('#file-input').change(function(){
        var filename = $('input[type=file]').val().split('\\').pop();
        $('#filename-placeholder').text(filename);
        $('#filename-placeholder').show();
        $('#select-file-btn').hide();
        $('#change-file-btn').show();
    });

    $('#next-btn').click(function(event){
        $('#errormsg-file').hide();
        $('#errormsg-name').hide();
        if($('#repo-name').val() != ""){            
            if ($('#file-input').get(0).files.length > 0) {
                uploadRepo(event);
                $('#content').animate({
                    opacity: 0, // animate slideUp
                    marginLeft: '-200px'
                  }, 300, 'swing', function() {
                    $(this).hide();
                });
        
                $('#progress-create').fadeIn(500);
            }
            else{
                $('#errormsg-file').text("Please insert a zip file");
                $('#errormsg-file').show();
            }
        }
        else{
            $('#errormsg-name').text("Repository name cannot be empty");
            $('#errormsg-name').show();
        }        
    });

    $('#back-btn').click(function(event){
        window.location.replace(BASE_URL + "welcome/")
    });
});

function uploadRepo(event){
    event.preventDefault();
    $('#upload-loader').show();
    var formData = new FormData();
 
    formData.append('RepoFile', $('#file-input')[0].files[0]);
    formData.append('RepositoryName', $('#repo-name').val());

    $.ajax({
        url: API_URL + "indexing/UploadRepository/",
        type: "POST",
        data: formData,
        cache: false,
        processData: false,
        contentType: false,
        enctype: 'multipart/form-data',
        success: function(response) {
            // response = JSON.parse(data);
            if(response.ResponseCode == "0"){
                $('#upload-loader').hide();
                $('#upload-check').show();
                repoID = response.ResponseMessage;
                indexRepo(repoID);
            }
            else{
                $('#upload-loader').hide();
            }
            console.log(data);
        },
        
    });
}

function indexRepo(repoID){
    $('#indexing-loader').show();
}