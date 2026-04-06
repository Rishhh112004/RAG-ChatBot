let uploadedData="";
let documents={};

const fileInput=document.getElementById("fileInput");
const fileList=document.getElementById("fileList");
const chatBox=document.getElementById("chatBox");
const preview=document.getElementById("previewContent");
const status=document.getElementById("uploadStatus");
const darkToggle=document.getElementById("darkToggle");

/* Welcome message */

window.onload=function(){
addMessage("Hello! Upload documents and ask questions.","bot");
};

/* Upload files */

fileInput.addEventListener("change",function(){

const files=fileInput.files;

for(let file of files){

status.innerText="Uploading "+file.name+"...";

const reader=new FileReader();

reader.onload=function(e){

const content=e.target.result.toLowerCase();

documents[file.name]=content;

uploadedData+=content+" ";

status.innerText="Uploaded "+file.name;

};

reader.readAsText(file);

const li=document.createElement("li");

li.innerHTML="📄 "+file.name+" <span class='delete-btn'>❌</span>";

li.onclick=()=>previewFile(file.name);

li.querySelector(".delete-btn").onclick=(event)=>{

event.stopPropagation();

delete documents[file.name];

li.remove();

};

fileList.appendChild(li);
}

});

/* Preview document */

function previewFile(name){
preview.innerText=documents[name].substring(0,300)+"...";
}

/* Send message */

function sendMessage(){

const input=document.getElementById("userInput");

const question=input.value.trim();

if(question==="") return;

addMessage("👤 "+question,"user");

setTimeout(()=>{
searchAnswer(question);
},500);

input.value="";
}

/* Add message */

function addMessage(text,type){

const msg=document.createElement("div");

msg.classList.add("message",type);

const time=new Date().toLocaleTimeString();

msg.innerHTML=text+"<div class='timestamp'>"+time+"</div>";

chatBox.appendChild(msg);

chatBox.scrollTop=chatBox.scrollHeight;
}

/* Search answer */

function searchAnswer(question){

if(!uploadedData){
addMessage("⚠ Please upload data first.","bot");
return;
}

const words=question.toLowerCase().split(" ");

for(let word of words){

if(word.length>3){

for(let doc in documents){

if(documents[doc].includes(word)){

const highlighted=documents[doc]
.replace(word,"<span class='highlight'>"+word+"</span>")
.substring(0,200);

addMessage(
" Answer related to '"+word+"'<br><br>"+
highlighted+
"<br><br>Source: 📄 "+doc,
"bot"
);

return;
}
}
}
}

addMessage("⚠ No answer found in uploaded data","bot");
}

/* Enter key support */

document.getElementById("userInput").addEventListener("keypress",function(e){

if(e.key==="Enter") sendMessage();

});

/* Clear chat */

function clearChat(){
chatBox.innerHTML="";
}

/* Dark mode */

if(localStorage.getItem("theme")==="dark"){
document.body.classList.add("dark-mode");
darkToggle.innerText="☀ Light Mode";
}

darkToggle.addEventListener("click",()=>{

document.body.classList.toggle("dark-mode");

if(document.body.classList.contains("dark-mode")){
localStorage.setItem("theme","dark");
darkToggle.innerText="☀ Light Mode";
}
else{
localStorage.setItem("theme","light");
darkToggle.innerText="🌙 Dark Mode";
}

});