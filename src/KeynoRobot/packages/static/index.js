
function check_WS(){//if(!_Connection ||
  // document.getElementById('_link').value= _Connection.readyState;
      if(  _Connection.readyState == 3 ) {document.getElementById('_link').style.backgroundColor ="#FFA500"; ini_ws();}
else  if(  _Connection.readyState == 0 ) {document.getElementById('_link').style.backgroundColor ="#DC143C";  } 
else  if(  _Connection.readyState == 2 ) {document.getElementById('_link').style.backgroundColor ="#FF0000";  }
  }
function ini_ws()
{

_Connection = new WebSocket( link); 
_Connection.onerror = function (error){document.getElementById('_link').value="Link Broken";  document.getElementById('_link').style.backgroundColor ="#FFA500"; }
_Connection.close = function (error)  {document.getElementById('_link').value="Disconnected"; document.getElementById('_link').style.backgroundColor ="#FFE4E1";} //gray
_Connection.onopen = function (evt)   {document.getElementById('_link').value="Connected";    document.getElementById('_link').style.backgroundColor ="#7FFF00";_Connection.send('Hello web server on Firefly' ); }
_Connection.onmessage = function(INCOME){parsing(INCOME.data); }	 
	
setInterval(check_WS, 500);	
}
 
 function parsing(_income)
 {
 }
 
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