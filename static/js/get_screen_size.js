$( document ).ready(function(){
    var ScreenHeight = window.screen.height;
    var ScreenWidth = window.screen.width;

   if (ScreenWidth < 600){
        window.location.href = '/form_m'
   } else {
       window.location.href = '/form_c'
   }
});
