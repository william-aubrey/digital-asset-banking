// Get the total screen resolution (width and height)
let screenWidth = screen.width;
let screenHeight = screen.height;

// Get the available screen resolution (excluding browser toolbars and the dock/taskbar)
let availableWidth = screen.availWidth;
let availableHeight = screen.availHeight;

console.log("Your total screen resolution is: " + screenWidth + "x" + screenHeight);
console.log("The available space is: " + availableWidth + "x" + availableHeight);