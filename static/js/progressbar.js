
window.onload = function() {
    var can = document.getElementById('canvas'),
        spanProcent = document.getElementById('procent'),
        stars = document.getElementById('stars'),
        c = can.getContext('2d');
   
    can.width = 100;
    can.height = 100;

    var posX = can.width / 2,
        posY = can.height / 2,
        radius = 30;
        fps = 1000 / 200,
        procent = 0,
        oneProcent = 360 / 100,
        // result = oneProcent * 64;
        result = oneProcent * (parseFloat(stars.textContent) / 5 * 100);
    
    c.lineCap = 'round';
    arcMove();
    
    function arcMove(){
      var deegres = 0;
      var acrInterval = setInterval (function() {
        deegres += 1;
        c.clearRect( 0, 0, can.width, can.height );
        procent = deegres / oneProcent;
  
        // spanProcent.innerHTML = procent.toFixed();
  
        c.beginPath();
        c.arc( posX, posY, radius, (Math.PI/180) * 270, (Math.PI/180) * (270 + 360) );
        c.strokeStyle = '#b1b1b1';
        c.lineWidth = '5';
        c.stroke();
  
        c.beginPath();
        c.strokeStyle = '#3949AB';
        c.lineWidth = '5';
        c.arc( posX, posY, radius, (Math.PI/180) * 270, (Math.PI/180) * (270 + deegres) );
        c.stroke();
        if( deegres >= result ) clearInterval(acrInterval);
      }, fps);

    //   stars.innerHTML = stars;
      
    }
    
    
  }