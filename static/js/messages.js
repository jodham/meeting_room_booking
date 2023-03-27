window.addEventListener('load', function(){
    document.querySelectorAll('.alert').forEach(function (alert){
        setTimeout(function (){
        alert.remove();
        }, 3000);
    });
});