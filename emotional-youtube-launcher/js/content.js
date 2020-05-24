const api = "http://127.0.0.1:5000/analysis/"

function displayResponse() {
    if (this.readyState == XMLHttpRequest.DONE && this.status == 200) {
        // TODO
        let responseObj = this.response;
        alert(responseObj.attitude);
        // return XMLHttpRequest.response;
    } else {
        document.getElementById("report").innerHTML = "No result available for this video.";
    }
};

// function to call api
function getReport(vid) {
    let httpRequest = new XMLHttpRequest();
    httpRequest.open("GET", api + vid, true);
    httpRequest.responseType = 'json';
    httpRequest.setRequestHeader("Content-Type", "application/json");
    httpRequest.send();
    httpRequest.onload = displayResponse;
}

function showReport(response) {
    // TODO change mocking showing
    document.getElementById('report').innerHTML = report.toString();
}

// parse video id from url
function parseVid(url) {
    // use positive lookahead, starting to match after '?v='
    const regex = /(?<=\?v\=)([A-Za-z0-9_-]+)/;
    const found = url.match(regex);

    if (found !== null) {
        return found[0];
    } else {
        return null;
    }
}

// logic runs after DOM is loaded
document.addEventListener("DOMContentLoaded", 
    function() {
        var vid;
        // find the tab that the extension is evoked on
        chrome.tabs.query({active: true, lastFocusedWindow: true}, 
            function(tabs) {
                if (tabs !== null) {
                    vid = parseVid(tabs[0].url);
                    document.getElementById("idbox").value = vid;
                }
            }
        );
        // listen to button clicks
        document.getElementById("btn-analyze").addEventListener("click", 
            function() {
                // fetch report json and diplay
                getReport(document.getElementById("idbox"));
            }
        );
    }, false
);