
$('#submit').on(function(){
    $.post('/goals', $('#newgoal').serialize(), function(result){
        $('#message').html(result.message)
    }, 'json')
});
