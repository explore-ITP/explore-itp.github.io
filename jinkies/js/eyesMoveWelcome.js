//<!--begin JAVASCRIPT for EYES following MOUSE-->
            $(document).ready(function(){
                $('html').mousemove(function(e){
                    var x = ((e.pageX - this.offsetLeft)/50 + 290)*$(window).width()/1000;
                    var y = ((e.pageY - this.offsetTop)/40 + 30)*$(window).width()/1000 - ((e.pageX - this.offsetLeft)/40)*$(window).width()/3000;
                $('div.eyesMoveFull').css({'top': y,'left': x}); 
                });
            });
