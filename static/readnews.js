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

function vote()
{
    
}