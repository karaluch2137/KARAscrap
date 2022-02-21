//////////////////////////////////////////////   KARAscrap   ////////////////////////////////////////////////////////
var host = 'localhost';
var port = 1488;

window.addEventListener('DOMContentLoaded', (event) => 
{
   KARAscrap_spawn_buttons();
   var KARAscrap_expander_buttons = document.getElementsByClassName("expander");
   for (let item of KARAscrap_expander_buttons) 
   {
      item.addEventListener('click', KARAscrap_cooldown , false);
   }
   var KARASCRAP_panel = '<div class="postMessage reply" style="position: fixed;right: 0;'+
   'top: 50vh;'+
   'margin-right:5px;'+
   'border:solid 3px black;'+
   'z-index:100;'+
   '">'+
   '<h3 style="margin-top:0;text-align:center;" >KARA scrap</h3>'+
   '<label for="KARAscrap_select">format:</label>'+
    '<select name="KARAscrap_select" id="KARAscrap_select">'+
       '<option value="json">json</option>'+
       '<option value="html">html</option>'+
       '<option value="both">both</option>'+
   '</select>'+
   '<div>'+
   '<button id ="KARAscrap_save_page" style="margin:5px;display:inline-block;">save page</button>'+
   '<input style="margin:5px;width:5ch;display:inline-block;" id="KARAscrap_save_page_number" type="number" min-value="0" value="0" max-   value="100">'+
   '</div>'+
   '<button id ="KARAscrap_save_board" style="display:block;margin:auto;margin-bottom:5px;">save board</button>'+
   '</div>';
   document.body.insertAdjacentHTML( 'beforeend', KARASCRAP_panel );
   let KARAscrap_board = String(window.location.pathname.split('/')[1]);
   document.getElementById("KARAscrap_save_page").onclick = function(){  window.open('http://'+host+':'+port+'/scrap/page/'+document.getElementById("KARAscrap_select").value+'/'+KARAscrap_board+'/'+document.getElementById("KARAscrap_save_page_number").value , '_blank').focus(); };
   document.getElementById("KARAscrap_save_board").onclick = function(){  window.open('http://'+host+':'+port+'/scrap/board/'+document.getElementById("KARAscrap_select").value+'/'+KARAscrap_board, '_blank').focus(); };
});

function KARAscrap_cooldown()
{
   setTimeout(function(){  KARAscrap_spawn_buttons(); }, 5000);
}

function KARAscrap_spawn_buttons()
{
  console.log('buttons update');
  var KARAscrap_posts = document.getElementsByClassName("postInfo");
  for (var i = 0; i < KARAscrap_posts.length; i++) 
  {
      if(KARAscrap_posts[i].getElementsByClassName("KARAscrap_button").length == 0)
      {
         let KARAscrap_button = document.createElement("button");
         KARAscrap_button.innerHTML = "save post";
         KARAscrap_button.setAttribute('type', 'button');
         KARAscrap_button.classList.add("KARAscrap_button");
         KARAscrap_button.classList.add("BBButton");
         KARAscrap_button.style.fontSize = "10px";
         KARAscrap_button.style.cursor = "pointer";
         let KARAscrap_thread_id = String(KARAscrap_posts[i].parentElement.parentElement.parentElement.id).substring(1);
         let KARAscrap_id = String(KARAscrap_posts[i].id).substring(2);
         let KARAscrap_board = String(window.location.pathname.split('/')[1]);
         KARAscrap_button.onclick = function(){  window.open('http://'+host+':'+port+'/scrap/post/'+document.getElementById("KARAscrap_select").value+'/'+KARAscrap_board+'/'+KARAscrap_thread_id+'/'+KARAscrap_id , '_blank').focus(); };
         KARAscrap_posts[i].append(KARAscrap_button);
        
      }
  }

  var KARAscrap_threads = document.getElementsByClassName("op");
  for (var i = 0; i < KARAscrap_threads.length; i++) 
  {
      if(KARAscrap_threads[i].getElementsByClassName("KARAscrap_button_thread").length == 0)
      {
         let KARAscrap_button = document.createElement("button");
         KARAscrap_button.innerHTML = "save thread";
         KARAscrap_button.setAttribute('type', 'button');
         KARAscrap_button.classList.add("KARAscrap_button_thread");
         KARAscrap_button.classList.add("BBButton");
         KARAscrap_button.style.fontSize = "10px";
         KARAscrap_button.style.cursor = "pointer";
         let KARAscrap_id = String(KARAscrap_threads[i].id).substring(1);
         let KARAscrap_board = String(window.location.pathname.split('/')[1]);
         KARAscrap_button.onclick = function(){  window.open('http://'+host+':'+port+'/scrap/thread/'+document.getElementById("KARAscrap_select").value+'/'+KARAscrap_board+'/'+KARAscrap_id , '_blank').focus(); };
         KARAscrap_threads[i].children[0].append(KARAscrap_button);       
      }
   }
}

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
