// JavaScript from this video: https://www.youtube.com/watch?v=9lo_W9RXJKw

const outputDiv = document.getElementById("slow-type");
const txt = 'Hello! Welcome to Blendie Bot!\nI am an AI model designed to help you feel better!\nPress the button on my body to begin.'

function typeText(text) {
    // Split text by custom tag for new paragraph into array
    const splittedTxt = txt.split('\n');
    // Create an array of new  element and append to output element
    let pElements = [];
    splittedTxt.forEach((item, index) => {
      const p = document.createElement('p');
      outputDiv.appendChild(p);
    });
    
    // Select all newly appended  elements
    const allParas = outputDiv.querySelectorAll('p');
    let i = 0; // Current character
    let currentPara = 0; // Current paragraph
    const timerId = setInterval(() => {
      // Start writing in current paragraph in DOM text from corresponding splitted array item
      allParas[currentPara].innerHTML += splittedTxt[currentPara].charAt(i);
      i++;
      // When reach the end of current splitted text item
      if (i === splittedTxt[currentPara].length) {
        currentPara++; // Move to next paragraph
        i=0; // Reset i
        // If end of splitted array has been reached
        if (currentPara === splittedTxt.length) {
          clearInterval(timerId); // ...clear interval
        }
      }
    },20);
  }

typeText(txt)