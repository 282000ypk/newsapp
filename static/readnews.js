function expandbox()
{
    document.querySelector(".filter-box").classList.toggle("expand")
}
function collapsebox()
{
    document.querySelector(".filter-box").classList.toggle("expand")
}

function filterbyanalysis()
{
    if(document.querySelector("#negative-filter:checked")!==null)
    {
        let news = document.querySelectorAll(".neutral")
        news.forEach(function(n)
        {
            n.style.display = "none"
        }
        )
    }
    else
    {
        let news = document.querySelectorAll(".news")
        news.forEach(function(n)
        {
            n.style.display = "flex"
        }
        )    
    }
    
}

function load(title)
{
    alert("#"+title)
    document.querySelector("#"+title).classList.toggle("view")
}

function vote(news_id, vote)
{
    url = "https://localhost:5000/vote_news/" + news_id + "/" + vote
    x = fetch(url, {method: 'get'})
    x.then(()=>{
        alert("voted successfully")
    })
    x.catch(()=>{
        alert("voting error"+x.JSON)
    })
}