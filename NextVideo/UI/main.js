
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
      // callJSON(getURL("/Series/") + series.seriesID + "/Play",
      //   // Not sure why but I need to do a $forceUpdate() on the Vue App to get it to refresh properly
      //   function (data2){},
      //   function (error){console.log("Server Error:" + error);},
      // );
      
      this.$root.GotoNextEpisode(null, toPlayURL); // Move on to next episode before we play
      //app.$forceUpdate();
      //window.open(series.url,"_self"); 
    },
    GotoPrevSeason: function (series) {
      series = data.seriesList[currentSelectedCarouselIndex];
      console.log("GotoPrevSeason");
      console.log( "SeriesID: " + series.seriesID );
      callJSON(getURL("/Series/") + series.seriesID + "/DecSeason",
        // Not sure why but I need to do a $forceUpdate() on the Vue App to get it to refresh properly
        function (data2){data.seriesList[currentSelectedCarouselIndex] = data2; app.$forceUpdate();},
        function (error){console.log("Server Error:" + error);},
      );
    },
  
    GotoPrevEpisode: function () {
      console.log("GotoPrevEpisode");
      series = data.seriesList[currentSelectedCarouselIndex];
      callJSON(getURL("/Series/") + series.seriesID + "/Dec",
        // Not sure why but I need to do a $forceUpdate() on the Vue App to get it to refresh properly
        function (data2){data.seriesList[currentSelectedCarouselIndex] = data2; app.$forceUpdate();},
        function (error){console.log("Server Error:" + error);},
      );
      
    },
    GotoNextSeason: function () {
      console.log("GotoNextSeason");
      series = data.seriesList[currentSelectedCarouselIndex];
      callJSON(getURL("/Series/") + series.seriesID + "/IncSeason",
        // Not sure why but I need to do a $forceUpdate() on the Vue App to get it to refresh properly
        function (data2){data.seriesList[currentSelectedCarouselIndex] = data2; app.$forceUpdate();},
        function (error){console.log("Server Error:" + error);},
      );
      
    },

    GotoNextEpisode: function (event=null, toPlayURL=null) {
      console.log("GotoNextEpisode");
      // GotoNextEpisode is used by PlayNextEpisode to increment to next and also play
      // Need to get the toPlayURL into the JSON callback function!!!
      // Don't know how to do this neatly so having to use a global - globalToPlayURL
      globalToPlayURL = toPlayURL
      series = data.seriesList[currentSelectedCarouselIndex];
      actionStr = "/Inc";
      if (toPlayURL != null) actionStr = "/Play";
      callJSON(getURL("/Series/") + series.seriesID + actionStr,
        // Not sure why but I need to do a $forceUpdate() on the Vue App to get it to refresh properly
        function (data2){
          data.seriesList[currentSelectedCarouselIndex] = data2;
          app.$forceUpdate();
          if (globalToPlayURL != null) {
            console.log("About to play: " + globalToPlayURL);
            window.open(globalToPlayURL,"_self");
          }
        },
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

function getURL(relPath){
  //var base1 = "http://18.130.245.71:5000/"; //AWS Server
  var base1 = "http://ec2-18-130-245-71.eu-west-2.compute.amazonaws.com:5000"
  var base2 = "http://127.0.0.1:5000";
  var base = base1;
  //console.log("getURL: " + base + relPath);
  return base + relPath;
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
  callJSON(getURL("/WatchList"),
        function (data2){data.seriesList = data2;},
        function (error){console.log("Server Error:" + error);},
      );
}

var currentSelectedCarouselIndex = 0;
var globalToPlayURL = null;

function init(){
  console.log("init called");
  getSeriesList();
 
  $('.carousel').on('slide.bs.carousel',function(e){
    var slideFrom = $(this).find('.active').index();
    currentSelectedCarouselIndex = $(e.relatedTarget).index();
    $(this).carousel("pause"); // prevent the carousel from auto sliding
    //console.log(slideFrom+' => '+currentSelectedCarouselIndex);
  });

  // Getting a strange behaviour with back button on Amazon Fire TV Stick browsers
  // Both Silk and Firefox behave the same and are returning to the original page rather than the updated page
  // Lots of debris code below where I was hunting for an event that gets triggered on the Amazon Fire Stick browsers (I couldn't find one)
  // Settled for the setInterval kludge in the end (see below)
  $(window).focus(function() {
    //DEBUG("focus - welcome (back)");
    console.log('welcome (back)');
    //app.$forceUpdate();
  });

  window.onpageshow = function(event) {
    //DEBUG("onpageshow");
    console.log('onpageshow');
    if (event.persisted) {
      console.log('onpageshow - persisted');
      app.$forceUpdate();
    }
  };

  window.onload = function(event) {
    //DEBUG("onload");
  };

  window.onunload = function(event) {
    //DEBUG("onunload");
    console.log('onunload');
  };

  $("#topLeft").click(function() {
    refreshApp();
  });

  history.navigationMode = 'compatible';
  $(document).ready(function(){
    //DEBUG("READY OR NOT. HERE I COME - Going Find you...");
  })

  
  
}

jQuery(document).ready(function($){
  //DEBUG("JQuery Ready called");

  $(window).on('popstate',function(){
    //DEBUG("POPSTATE Force Reload");
    console.log('POPSTATE Force Reload');
    location.reload(true);
  });

  
  
  // The below simulates the behaviour I am getting on the Fire Stick
  // Commenting this out (only for debugging if specific problem on Fire TV Stick browsers)
  //window.onbeforeunload = function () {
    // This function does nothing.  It won't spawn a confirmation dialog
    // But it will ensure that the page is not cached by the browser.
  //}
  
  // Was using the following as a kludge to detect that BACK button had been pressed on 
  // Browsers that go back to a cached state (i.e. Amazon Fire stick browsers) and do not
  // trigger any events (that I can find - sure there will be some but..)
  //
  // BUT I am abandoning this approach in favour of the setInterval kludge below
  // var mmCount = 0;
  // $(document).mousemove(function(){
  //   DEBUG("Mouse move - " + mmCount);
  //   console.log("Mouse move - " + mmCount++);
  //   $(document).unbind('mousemove');
  //   refreshApp();
  //   //window.setTimeout(refreshApp, 1000);
  // })
})

// Kludge to fix a problem on browsers whose back button take you to a cached original state of the page
// If the page is a SPA/Ajax page and was changed then these changes will not be reflected.
// To make the problem worse: I cannot find any events that are triggered after back button is pressed
//
// The kludge sets up a repeating timer that gets re-run in the situation above
var intCount = 0;
var INTERVAL_TIMER = window.setInterval(function(){
  //DEBUG("Interval called: " + intCount++); 
  window.setTimeout(refreshApp, 100);     // Watch out for this value (and corresponding one below). May be too quick for some browsers! Didin't work on MacOS desktop machine.
  window.clearInterval(INTERVAL_TIMER);
}, 100);

function DEBUG(msg){
  debugConsole = $("#debugConsole");
  curInner = debugConsole.html(); 
  console.log("DEBUG called - Current InnerText:");
  console.log(curInner);
  curInner += "<br/>" + msg;
  var res = curInner.split("<br>");
  if (res.length > 100){
    console.log("Clearing debug Console");
    curInner = msg;
  }

  debugConsole.html(curInner);
}

function refreshApp(){
  //DEBUG("Refresh App");
  init();
  app.$forceUpdate();
  
}

init();
