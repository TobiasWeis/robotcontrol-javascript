var Joystick = function(divname,num, socket, name){
        this.divname = "#"+divname; // so we can use jquery
        this.num = num;
        this.socket = socket;
        this.name = name;
        this.radius = 50;
        this.sx = -1;
        this.sy = -1;
        this.offset = $(this.divname).offset();

       /* create base div */
        $('<div class="joystick_base" id="'+divname+'_base_'+num+'">').appendTo('body');
        $(this.divname+"_base_"+num).css("width",(this.radius*2)+"px");
        $(this.divname+"_base_"+num).css("height",(this.radius*2)+"px");

        $('<div class="joystick_nip" id="'+divname+'_overlay_'+num+'">').appendTo('body');
        console.log("CTOR called for " + divname);


        /* create listener */
        $(this.divname).bind('touchstart touchmove click', {parentObj:this}, function(evt){
            var parentobj = evt.data.parentObj;
            var touch = evt.originalEvent.targetTouches[0];
            var offset = $(parentobj.divname).offset();
            var x = touch.clientX - offset.left;
            var y = touch.clientY - offset.top;

            if (!(
                touch.clientX <= $(this).offset().left || touch.clientX >= $(this).offset().left + $(this).outerWidth() ||
                touch.clientY <= $(this).offset().top  || touch.clientY >= $(this).offset().top + $(this).outerHeight())){
                if(parentobj.sx == -1){
                    parentobj.start(x,y);
                }else{
                    parentobj.handle(x,y);
                }

                /* send data via websocket */
                var data = {}
                data[parentobj.name] = [(x-parentobj.sx)/parentobj.radius, (y-parentobj.sy)/parentobj.radius];
                parentobj.socket.emit('control', {data:data});
            }
            evt.preventDefault();
        });

        $(this.divname).bind('touchend', {parentObj:this}, function(evt){
            var parentobj = evt.data.parentObj;
            parentobj.sx = -1;
            parentobj.sy = -1;
            $('#output'+parentobj.num).html("joystick end");
            $(parentobj.divname+"_overlay_"+parentobj.num).css("display","none");
            $(parentobj.divname+"_base_"+parentobj.num).css("display","none");

            /* send data via websocket */
            var data = {}
            data[parentobj.name] = [0.0,0.0];
            parentobj.socket.emit('control', {data:data});

            evt.preventDefault();
        });
    }

Joystick.prototype.start = function(sx,sy){
        this.sx = sx;
        this.sy = sy;

        $(this.divname+'_overlay_'+this.num).css("display","block");
        $(this.divname+'_overlay_'+this.num).css("top", (this.sy-25+this.offset.left)+"px");
        $(this.divname+'_overlay_'+this.num).css("left" ,(this.sx-25+this.offset.top)+"px");

        $(this.divname+'_base_'+this.num).css("display","block");
        $(this.divname+'_base_'+this.num).css("top", (this.sy-this.radius+this.offset.top)+"px");
        $(this.divname+'_base_'+this.num).css("left" ,(this.sx-this.radius+this.offset.left)+"px");
    }

Joystick.prototype.handle = function(x,y){
        // calculate relative coordinates to starting point
        if(Math.sqrt(Math.pow(x-this.sx,2)+Math.pow(y-this.sy, 2)) < this.radius){
            $('#output'+this.num).html("joystick move:"+ ((x-this.sx)/this.radius).toFixed(1) + ":" + ((y-this.sy)/this.radius).toFixed(1));

            $(this.divname+'_overlay_'+this.num).css("top", (y-25+this.offset.top)+"px");
            $(this.divname+'_overlay_'+this.num).css("left" ,(x-25+this.offset.left)+"px");
        }
    }

