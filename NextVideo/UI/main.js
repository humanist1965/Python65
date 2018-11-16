
// local datastore for the App
var data = {
  product: "NextVideo App",
  isActive: isActiveAux,
  seriesList: [1,2,3]
}

var app = new Vue({
  el:"#app",
  data: data,
  methods: {
    PlayNextEpisode: function () {
      series = data.seriesList[currentSelectedCarouselIndex];
      console.log("PlayNextEpisode for " + series.name);
      //console.log("Season: " + series.currentSeasonNumber);
      //console.log("Episode: " + series.nextEpisodeNumber);
      //console.log("URL: " + series.url);
      toPlayURL = series.url;
      this.$root.GotoNextEpisode(); // Move on to next episode before we play
      app.$forceUpdate();
      window.open(series.url,"_self"); 
    },
    GotoPrevSeason: function (series) {
      series = data.seriesList[currentSelectedCarouselIndex];
      console.log("GotoPrevSeason");
      console.log( "SeriesID: " + series.seriesID );
      callJSON("http://127.0.0.1:5000/Series/" + series.seriesID + "/DecSeason",
        // Not sure why but I need to do a $forceUpdate() on the Vue App to get it to refresh properly
        function (data2){data.seriesList[currentSelectedCarouselIndex] = data2; app.$forceUpdate();},
        function (error){console.log("Server Error:" + error);},
      );
    },
  
    GotoPrevEpisode: function () {
      console.log("GotoPrevEpisode");
      series = data.seriesList[currentSelectedCarouselIndex];
      callJSON("http://127.0.0.1:5000/Series/" + series.seriesID + "/Dec",
        // Not sure why but I need to do a $forceUpdate() on the Vue App to get it to refresh properly
        function (data2){data.seriesList[currentSelectedCarouselIndex] = data2; app.$forceUpdate();},
        function (error){console.log("Server Error:" + error);},
      );
      
    },
    GotoNextSeason: function () {
      console.log("GotoNextSeason");
      series = data.seriesList[currentSelectedCarouselIndex];
      callJSON("http://127.0.0.1:5000/Series/" + series.seriesID + "/IncSeason",
        // Not sure why but I need to do a $forceUpdate() on the Vue App to get it to refresh properly
        function (data2){data.seriesList[currentSelectedCarouselIndex] = data2; app.$forceUpdate();},
        function (error){console.log("Server Error:" + error);},
      );
      
    },
    GotoNextEpisode: function () {
      console.log("GotoNextEpisode");
      series = data.seriesList[currentSelectedCarouselIndex];
      callJSON("http://127.0.0.1:5000/Series/" + series.seriesID + "/Inc",
        // Not sure why but I need to do a $forceUpdate() on the Vue App to get it to refresh properly
        function (data2){data.seriesList[currentSelectedCarouselIndex] = data2; app.$forceUpdate();},
        function (error){console.log("Server Error:" + error);},
      );
      
    }
  }
})

function HelperMeth() {
  alert("HelperMeth");
}

// Helper function to hide some of the complexity of using fetch and promises
// NOTE: Just using a single errorHandler for 2 promises here (to make it easier)
function callJSON(url, responseHandler, errorHandler) {
  fetch(url)
      .then(function(response) {
         // Your code for handling the data you get from the API
        response.json().then(responseHandler).catch(errorHandler);
      })
      .catch(errorHandler); 
}

function isActiveAux (index) { 
  return (index == 0 ? "carousel-item active" : "carousel-item") 
}

function getSeriesList(){
  console.log("getSeriesList called");
  //getSeriesListMockUp();
  getSeriesListReal()
}

function getSeriesListMockUp(){
  console.log("getSeriesListMockUp called");
  data.seriesList = [{"seriesID": "GOT", "currentSeasonNumber": 1, "nextEpisodeNumber": 9, "lastWatchedDate": "2020-11-14", "name": "Game of Thrones", "image": null, "url": "http://tvhome.cc/play.php?tid=yweywzy|nktlyeykvy"}, {"seriesID": "Billions", "currentSeasonNumber": 1, "nextEpisodeNumber": "1", "lastWatchedDate": "2018-11-14", "name": "Billions", "image": null}, {"seriesID": "BigBang", "name": "The Big Bang Theory", "image": null, "currentSeasonNumber": 1, "nextEpisodeNumber": 1, "lastWatchedDate": "1900-01-01"}, {"seriesID": "WestWorld", "name": "WestWorld", "image": null, "currentSeasonNumber": 1, "nextEpisodeNumber": 1, "lastWatchedDate": "1900-01-01"}];
}

function getSeriesListReal(){
  callJSON("http://127.0.0.1:5000/WatchList",
        function (data2){data.seriesList = data2;},
        function (error){console.log("Server Error:" + error);},
      );
}

var currentSelectedCarouselIndex = 0;
function init(){
  console.log("init called");
  getSeriesList();
 
  $('.carousel').on('slide.bs.carousel',function(e){
    var slideFrom = $(this).find('.active').index();
    currentSelectedCarouselIndex = $(e.relatedTarget).index();
    $(this).carousel("pause"); // prevent the carousel from auto sliding
    //console.log(slideFrom+' => '+currentSelectedCarouselIndex);
  });
}

init();

