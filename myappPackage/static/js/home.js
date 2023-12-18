

let msgFlash = document.getElementById('FlashMSG')
let ArrowButton = document.getElementById('btn');

// event that work when user use the scroll
onscroll = function(){
    if(this.scrollY>=400){
        ArrowButton.style.display='block'
    }
    else{
        ArrowButton.style.display='none'
    }
}

ArrowButton.onclick = function(){
    scroll({
        top:0,
        behavior:"smooth",  //these make the back to start of the page done smothly and not faster (like the transition in css)
    })
}

//when user make signIn,he get a flash msg about login successfully. this function delete this flash msg after 10 second
setTimeout(function(){
msgFlash.style.display='none'
},10000)