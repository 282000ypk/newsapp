fetch("./test.json")
.then(response => {
   return response.json();
})
.then(data => display(data))

function display(data)
{
   document.getElementById("testimg").src=data["articles"][0]["urlToImage"];
   document.getElementById("testh2").innerText=data["articles"][0]["content"];
}
