//<!--begin JAVASCRIPT for EYES following MOUSE-->
            $(document).ready(function(){
                $('html').mousemove(function(e){
                    var x = ((e.pageX - this.offsetLeft)/120+95)*$(window).width()/1000	;
                    var y = ((e.pageY - this.offsetTop)/130-5)*$(window).width()/1000 - ((e.pageX - this.offsetLeft)/150)*$(window).width()/3000;
                $('div.eyesMove').css({'top': y,'left': x}); 
                });
            });
