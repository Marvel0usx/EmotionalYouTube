// function to trigger analysis
function Analyze() {
    var vid = document.getElementById('idbox').value;
    document.getElementById('report').innerHTML = vid;
}

// function to retrieve vid from storage
function setVid() {
    // vid = "";
    // chrome.storage.sync.get(['vid'], function (result) {
    //     if (result.vid !== null) {
    //         vid = result.vid;
    //     } else {
    //         return;
    //     }
    // });
    // document.getElementById('idbox').value = vid;
    // chrome.storage.sync.set({'vid': null});
}