// function to trigger analysis
function Analyze() {
    var vid = document.getElementById('vid-box').value;
    document.getElementById('report').innerHTML = vid;
}

// function to retrieve vid from storage
// function setVid() {
//     vid = "";
//     chrome.storage.sync.get(['vid'], function (result) {
//         if (result.vid !== null) {
//             vid = result.vid;
//         } else {
//             return;
//         }
//     });
//     document.getElementById('idbox').value = vid;
//     chrome.storage.sync.set({'vid': null});
// }

function setVid() {
    alert("hello!");
}


// logic without loaded DOM
if (document.readyState === 'loading') {  // Loading hasn't finished yet
    document.addEventListener('DOMContentLoaded', setVid(), false);
    document.getElementById("btn-analyze").addEventListener("click", Analyze());
} else {                                  // 'DOMContentLoaded' has already fired
    setVid();
    document.getElementById("btn-analyze").addEventListener("click", Analyze());
};

// document.getElementById("btn-analyze").addEventListener("click", Analyze());