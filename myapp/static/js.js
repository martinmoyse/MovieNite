window.addEventListener('DOMContentLoaded', (event) => {
    
    if(document.querySelector('#_i').getAttribute('value') == ''){
        index = 0;
        loadIndexedCategory('/static/top250m.json',index);
    }
    else{
        let id_tmp = document.querySelector('#_i').getAttribute('value');
        let cat_tmp = document.querySelector('#_c').getAttribute('value');
        index = parseInt(id_tmp);
        loadIndexedCategory(cat_tmp, id_tmp);
    }
}); 

// explore page
let index;
let obj;

function loadIndexedCategory(category, ind){
    /* let */ temp = document.querySelector('#_i').getAttribute('value');
    if((temp=='') ? index=0 : index = parseInt(temp));
    fetch(category)
        .then(res => res.json())
        .then(data => obj = data)
        .then( () => {
            document.querySelector('#show-display-container').style.display = 'flex';
            document.querySelector("#categ").setAttribute("value", category);
            loadShowInfo(ind);
    });
}

// explore page
 function searchByTitle(){

    const t = document.getElementById("title").value;
    const year = document.getElementById("year").value;
    const api_url = 'http://www.omdbapi.com/?i=tt3896198&apikey=8f401f8e&'
    const title = t.replace(/\s/g, '+') // replace whitespaces with '+'
    //console.log(title.toLowerCase());
    const api = api_url+'t='+title.toLowerCase()+'&y='+year;
    //console.log(api)
    fetch(api)
    .then(res => res.json())
    .then(data => obj = data)
    .then( () => {
        loadShowInfo_titleAPI();
    });
} 

function loadNewCategory(category){
    index = 0;
    document.querySelector('#show-not-found').style.display = 'none';
    document.querySelector('#categ').setAttribute('value', category);
    fetch(category)
    .then(res => res.json())
    .then(data => obj = data)
    .then( () => {
        loadShowInfo(index);
    });
 } 

function loadShowInfo(index){
    //fill show details into display box
    $('.buttons-container').show();
    document.getElementById("show-title").innerHTML = obj[index]['title'];
    document.getElementById("show-year").style.display = 'none';
    document.getElementById("show-rank").style.display = 'block';
    document.getElementById("show-rank").innerHTML = 'Rank: '+ obj[index]['rank'];
    let rating;
    if((obj[index]['imDbRating'] == '') ? rating='N/A' : rating=('Rating: ' + obj[index]['imDbRating']));
    document.getElementById("show-rating").innerHTML = rating;
    document.getElementById("show-poster").setAttribute("src", obj[index]['image']);
    
    //fill add_to_list view form info
    document.getElementById("tt").setAttribute("value", obj[index]['id']);
    document.getElementById("t").setAttribute("value", obj[index]['title']);
    /* document.getElementById("y").setAttribute("value", obj[index]['year']); */
    document.getElementById("rt").setAttribute("value", obj[index]['imDbRating']);
    document.getElementById("im").setAttribute("value", obj[index]['image']);
    document.getElementById("i").setAttribute("value", obj[index]['rank']-1);
}

function loadShowInfo_titleAPI(){
    if(obj['Response'] == 'False'){
        document.querySelector('#show-not-found').style.display = 'block';
        /* document.querySelector("#categ").setAttribute("value", '/static/top250m.json');
        index = 0; */
        let id_tmp = document.querySelector('#_i').getAttribute('value');
        let cat_tmp = document.querySelector('#_c').getAttribute('value');
        index = parseInt(id_tmp);
        loadIndexedCategory(cat_tmp, id_tmp);
    }
    else{
        //fill show details into display box
        $('.buttons-container').hide();
        document.querySelector("#show-not-found").style.display = 'none';
        document.querySelector('#show-display-container').style.display = 'flex';
        document.getElementById("show-title").innerHTML = obj['Title'];
        document.getElementById("show-year").style.display = 'block';
        document.getElementById("show-year").innerHTML = 'Year: '+ obj['Year'];
        document.getElementById("show-rank").style.display = 'none';
        let rating;
        if((obj['imdbRating'] == '') ? rating='N/A' : rating=('Rating: ' + obj['imdbRating']));
        document.getElementById("show-rating").innerHTML = rating;
        document.getElementById("show-poster").setAttribute("src", obj['Poster']);

        //fill add_to_list view form info
        document.getElementById("tt").setAttribute("value", obj['imdbID']);
        document.getElementById("t").setAttribute("value", obj['Title']);
        document.getElementById("y").setAttribute("value", obj['Year']);
        document.getElementById("rt").setAttribute("value", obj['imdbRating']);
        document.getElementById("im").setAttribute("value", obj['Poster']);
    }
    
}

function updateIndex(value){
    if(value == -1 && index == 0) index = 0;
    else{
        index = index + value;
        loadShowInfo(index);
    }
}

function copyToClipboard(element) {
    var $temp = $("<input>");
    $("body").append($temp);
    $temp.val($(element).text()).select();
    document.execCommand("copy");
    $temp.remove();
}
