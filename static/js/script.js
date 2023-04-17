const searchField = document.querySelector("#searchText")
const tableOutPut = document.querySelector(".search-output")
const listTemperature = document.querySelector(".list-temperature")
const paginationSection = document.querySelector(".pagination")
const listDataSearch = document.querySelector(".list-data-search")
tableOutPut.style.display = "none";


vueApp = new Vue({
        el: "#app",
        delimiters: ["[[", "]]"],
        data() {
          return {
            temperatures: [],
          };
        },
      });

searchField.addEventListener('keyup',(e)=>{
    const  searchValue = e.target.value;
    if (searchValue.length >0){
        paginationSection.style.display = "none";
        console.log('object:', searchValue)
        fetch("search",{
            body: JSON.stringify({searchText: searchValue}),
            method: "POST"
        }).then((res) => res.json()).then((data) =>{
            console.log("data:",data)
            listTemperature.style.display = "none";
            tableOutPut.style.display = "block";
            if (data.length === 0){
                tableOutPut.innerHTML = "No results"
            }else{
             vueApp.$data.posts.push(data);
            }
        });
    }else{
         listTemperature.style.display = "block";

    }
})

console.log("Paci");