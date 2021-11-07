

/*functions to expand nad colapse menu box*/
function expandbox()
{
    document.querySelector(".filter-box").classList.toggle("expand")
}
function collapsebox()
{
    document.querySelector(".filter-box").classList.toggle("expand")
}

/*function to filter negarive news*/
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


/*function to send async request to vote for news*/
function vote(news_id, vote)
{
    url = "https://localhost:5000/vote_news/" + news_id + "/" + vote
    x = fetch(url, {method: 'get'})
    x.then(()=>{
        url = "https://localhost:5000/get_votes/" + news_id
        x = fetch(url, {method: 'get'})
        x.then(response=> response.json()).then(data => {
            /*console.log(data)*/
            positive_num = document.querySelector(".positive_votes."+news_id).innerHTML = data['positive_vote']
            negative_num = document.querySelector(".negative_votes."+news_id).innerHTML = data['negative_vote']
            /*console.log("succcess"+ negative_num)*/
        })
    })
    x.catch(()=>{
        alert("voting error"+x.JSON)
    })
}


/*function  and flag for fullscreen news box */
var fullscreen_flag = true
function fullview(news_id)
{
    if(fullscreen_flag === false)
    {
        fullscreen_flag = true
        return
    }
    else
    {
    console.log("clicked news")
    //function to update votes
    url = "https://localhost:5000/get_votes/" + news_id
    x = fetch(url, {method: 'get'})
    x.then(response=> response.json()).then(data => {
        //console.log(data)
        positive_num = document.querySelector(".positive_votes."+news_id).innerHTML = data['positive_vote']
        negative_num = document.querySelector(".negative_votes."+news_id).innerHTML = data['negative_vote']
        //console.log("succcess"+ negative_num)

        //function to enlarg screen
        news = document.querySelectorAll(".news")
        news.forEach(function(n)
        {
            n.classList.remove("fullscreen")
        })
        document.querySelector("#"+news_id).classList.add("fullscreen")   
        document.querySelector("#"+news_id).disbled = "true"
    })
    }
}   

function close_news(news_id) {
    fullscreen_flag = false
    news = document.querySelectorAll(".news")
    news.forEach(function(n)
    {
        n.classList.remove("fullscreen")
    })
}


