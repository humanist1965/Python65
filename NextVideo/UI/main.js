
// local datastore for the App
var data = {
  product: "Socks",
  seriesList: [1,2,3]
}

var app = new Vue({
  el:"#app",
  data: data
})



function getSeriesList(){
  console.log("getSeriesList called");
  sl = getSeriesListMockUp();
  data.seriesList = sl;
}

function getSeriesListMockUp(){
  console.log("getSeriesListMockUp called");
  return [{"seriesID": "GOT", "name": "Game of Thrones", "image": null}, {"seriesID": "BigBang", "name": "The Big Bang Theory", "image": null}, {"seriesID": "Billions", "name": "Billions", "image": null}, {"seriesID": "WestWorld", "name": "WestWorld", "image": null}];
}

function init(){
  console.log("init called");
  getSeriesList();
}

init();

