


function check_WS(){
	console.log("check_WS"); 
      if(  _Connection.readyState == 3 ) {document.getElementById('_link').style.backgroundColor ="#FFA500"; ini_ws();}
else  if(  _Connection.readyState == 0 ) {document.getElementById('_link').style.backgroundColor ="#DC143C";  } 
else  if(  _Connection.readyState == 2 ) {document.getElementById('_link').style.backgroundColor ="#FF0000";  }
  }
function ini_ws()
{
console.log(link); 
_Connection = new WebSocket( link); 
_Connection.onerror = function (error){document.getElementById('_link').value="Link Broken";  document.getElementById('_link').style.backgroundColor ="#FFA500"; }
_Connection.close = function (error)  {document.getElementById('_link').value="Disconnected"; document.getElementById('_link').style.backgroundColor ="#FFE4E1";} //gray
_Connection.onopen = function (evt)   {document.getElementById('_link').value="Connected";    document.getElementById('_link').style.backgroundColor ="#7FFF00";_Connection.send('Hello web server on Firefly' ); }
_Connection.onmessage = function(INCOME){parsing(INCOME.data); }	 
	
setInterval(check_WS, 500);	
}
 
 function parsing(_income)
 {
	document.getElementById("recieve_dats").value+= _income+'\n';
	 
 }

function cameraLeft(id){
	var s=document.getElementById(id).value;/*
   if(s=='Open Camera') 
   {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", "/image", true ); // false for synchronous request
    xmlHttp.responseType = 'blob';
	xhr.onload = function(e) 
	{
	  if (this.status == 200) {
								var blob = this.response;
								var img = document.getElementById('cameraLeft')
								img.onload = function(e) { window.URL.revokeObjectURL(img.src);};
								img.src = window.URL.createObjectURL(blob);
								document.body.appendChild(img);
							  }
     };
	xmlHttp.send(  );
	document.getElementById(id).value='Close Camera';
   } */
    if(s=='Open Camera') {document.getElementById('cameraLeft').src="http://"+location.host+"/image?com=start";
                          document.getElementById(id).value='Close Camera';}
	else                 {document.getElementById('cameraLeft').src="http://"+location.host+"/image?com=stop"; 
						  document.getElementById(id).value='Open Camera';}
          document.getElementById('imagecam').src="http://"+location.host+"/image?com=start"
}
 function cameraRight(id){ }
function Pitch2HUD(pitch){ 
	document.getElementById('myTable').rows[1].cells[1].innerHTML=pitch;
	document.getElementById('horizon1').style.top=document.getElementById('horizon').style.top =(parseInt(pitch)-75)*2+"%";
	}
function changePitch(id)
{
	v=parseInt(document.getElementById(id).value);// (-210,-150) (-30,30)
	document.getElementById('myTable').rows[1].cells[3].innerHTML = 75+.5*v;
	document.getElementById('horizon1').style.top=document.getElementById('horizon').style.top =v+"%";		
}
function Yaw2HUD(yaw){ 
	document.getElementById('myTable').rows[1].cells[5].innerHTML=yaw;
	document.getElementById('yawbar').style.left=(parseInt(yaw)-75)*2+"px";
	document.getElementById('yawname').innerHTML = yaw;
	}
function changeYaw(id)
{
	v=parseInt(document.getElementById(id).value);  
	document.getElementById('myTable').rows[1].cells[5].innerHTML = v; //y=ax+b, -.5x-80 x=(y-b)/a
	 document.getElementById('yawbar').style.left= (-(v+80)*2 )+"px";
    document.getElementById('yawname').innerHTML = v;	
}
function Roll2HUD(roll){ 
	document.getElementById('myTable').rows[1].cells[1].innerHTML=roll;
	document.getElementById('RoLL_S').style.transform="rotate("+roll+"deg)";
	}
function changeRoll(id)
{
	v=document.getElementById(id).value
	//document.getElementById('Roll').innerHTML=v;
	document.getElementById('myTable').rows[1].cells[1].innerHTML = v;
	document.getElementById('RoLL_S').style.transform="rotate("+v+"deg)";		
}
function changepAltitude(id){
v=parseInt(document.getElementById(id).value)
//d=Math.sign(v-lastAirspeed);
x=parseInt( v / 5);// alert(v+" "+x)
document.getElementById('altSp2').innerHTML = x*5+10;
document.getElementById('altSp1').innerHTML = x*5+5;
document.getElementById('altSX').innerHTML = v;
document.getElementById('altS0').innerHTML = x*5;
document.getElementById('altSm1').innerHTML = x*5-5;
document.getElementById('altSm2').innerHTML = x*5-10;
document.getElementById('altSp2').style.marginTop= ((v%5)*8+8)+"px"; //alert("new="+v+" dif="+d+" move="+d*(v%5))
//document.getElementById('myTable').rows[2].cells[1].innerHTML=d;
//document.getElementById('myTable').rows[2].cells[3].innerHTML=lastAirspeed;
//document.getElementById('myTable').rows[2].cells[5].innerHTML=((v%5)*7+4);
//lastAirspeed=v;id="altSE" 
}
function changeAirspeed(id){
v=parseInt(document.getElementById(id).value)
//d=Math.sign(v-lastAirspeed);
x=parseInt( v / 5);// alert(v+" "+x)
document.getElementById('airSp2').innerHTML = x*5+10;
document.getElementById('airSp1').innerHTML = x*5+5;
document.getElementById('airSX').innerHTML = v;
document.getElementById('airS0').innerHTML = x*5;
document.getElementById('airSm1').innerHTML = x*5-5;
document.getElementById('airSm2').innerHTML = x*5-10;
document.getElementById('airSp2').style.marginTop= ((v%5)*8+8)+"px"; //alert("new="+v+" dif="+d+" move="+d*(v%5))
//document.getElementById('myTable').rows[2].cells[1].innerHTML=d;
//document.getElementById('myTable').rows[2].cells[3].innerHTML=lastAirspeed;
//document.getElementById('myTable').rows[2].cells[5].innerHTML=((v%5)*7+4);
//lastAirspeed=v;id="altSE" 
}
function move() {			   
  var h=0;
  var id = setInterval(frame, 10);
  function frame() {
					if (h >= 100) {
					  clearInterval(id);
					} else {
					  h++;
					  battery2shape(h)
					  document.getElementById("battery").value=document.getElementById("batteryB").value=h+"%";	
					  document.getElementById('batteryval').innerHTML =h + '%'					  
					}
				  }
}
function battery2shape(Bat){
	var hMax=parseInt(document.getElementById("batteryB").style.height)-5;
	var bat=parseInt(Bat) ; 
	var per=(((5-hMax)/100)*bat+hMax); // alert(hMax+":"+per+"  "+bat) 
	document.getElementById("battery").style.height = per + 'px';
	document.getElementById('batteryval').innerHTML =bat + '%';	
}

function changepx(id){
v=parseInt(document.getElementById(id).value)
document.getElementById('airSp2').style.marginTop= v+"px";
}
function Disable1(){var x= document.querySelectorAll(".shouldDis");for (i = 0; i < x.length; i++)   x[i].style.visibility = 'hidden';}
function Enable1() {var x= document.querySelectorAll(".shouldDis");for (i = 0; i < x.length; i++)   x[i].style.visibility = 'visible';} 		
function send_raw_command(){
	var v=document.getElementById("send_command_value").value;
	if(v) _Connection.send(v )
	document.getElementById("send_command_value").value="";
}	

function openCity(cityName) {
  var i;
  var x = document.getElementsByClassName("city");
  for (i = 0; i < x.length; i++) {
    x[i].style.display = "none";  
  }
  document.getElementById(cityName).style.display = "block";  
}
function myFunction() {
  var x = document.getElementById("demo");
  if (x.className.indexOf("w3-show") == -1) {
    x.className += " w3-show";
  } else { 
    x.className = x.className.replace(" w3-show", "");
  }
}
function clicktohide() {
  var x = document.getElementById("Demop");
  if (x.className.indexOf("w3-show") == -1) {
    x.className += " w3-show";
  } else {
    x.className = x.className.replace(" w3-show", "");
  }
}



var startCounting,COUNT=0,setNatural;

function omdMove(type){
	startCounting=setInterval(function(){
											COUNT += 50;
											document.getElementById("outputsend").innerText = COUNT;
										  }, 100);
}
function omuMove(type){
		
  clearInterval(startCounting);
  send_command(type,COUNT);
  setNatural= setInterval(function(){
                                     sendcommandandclear(type)
                                     },150) ; 
}

function sendcommandandclear(type){

clearInterval(setNatural);
COUNT = 0;
document.getElementById("outputsend").innerText = COUNT;
send_command(type,0);
}

function send_command(type,COUNT){
	document.getElementById("send_command_value").value=type+":"+COUNT;
	  _Connection.send(type+":"+COUNT ) 
	
}
















