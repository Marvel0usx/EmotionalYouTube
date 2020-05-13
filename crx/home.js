$(function(){
    $('#url').keyup(function(){
        $('#greet').text('Analyzing: ' + $('#url').val())
    })
})