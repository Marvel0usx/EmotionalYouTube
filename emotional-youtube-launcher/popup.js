// function to trigger analysis
function Analyze() {
    var vid = document.getElementById('idbox').value;
    document.getElementById('report').innerHTML = vid;
}

document.addEventListener("DOMContentLoaded",
    function setup() {
        document.getElementById("btn-analyze").addEventListener("click", Analyze);
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
    }, false);