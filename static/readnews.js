
var data;

fetch('static/test.json')
.then(response => {
   return response.json();
})
.then(data => display(data))

function display(data)
{
   console.log(data["articles"][0])
   for(let i=0;i<data["articles"].length;i++)
   {
      /*
      <a href="#" class="news">
            <div class="card">
                <h2>
                    News Heading
                </h2>
                <img src="static/image1.jpg" alt="news description" loading="lazy">
                
                <p>
                    Two people were released Saturday after being detained in an investigation of airsoft guns and rifles found in a U-Haul truck near the National Mall.
                </p>
            </div>
        </a>
        */
      let news=document.createElement("a")
      news.classList.add("news")
      news.setAttribute("href",data["articles"][i]["url"]

      let card=document.createElement("div")
      card.classList.add("card")

      let h2=document.createElement("h2")
      h2.innerText=data["articles"][i]["title"]

      let img=document.createElement("img")
      img.alt="news description"
      img.loading="lazy"
      img.src=data["articles"][i]["urlToImage"]
      img.setAttribute("src", data["articles"][i]["urlToImage"]);

      let para=document.createElement("p")
      para.innerText=data["articles"][i]["description"]
      
      card.innerHTML+=h2
      card.innerHTML+=img
      card.innerHTML+=para


      news.innerHTML=card
      document.getElementById("allnewsid").innerHTML += news
   }
   console.log("done")
}

