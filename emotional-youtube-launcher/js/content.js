const URL = "http://127.0.0.1:5000/analysis/";
const NO_RESULT = "No result available for this video.";

function removeOldTags() {
    var container = document.getElementsByClassName("flex-container")[0];
    while (container.firstChild) {
        container.removeChild(container.lastChild);
    }
}

function displayResponse() {
    removeOldTags();
    if (this.readyState == XMLHttpRequest.DONE && this.status == 200) {
        let responseObj = this.response;
        if (Object.keys(responseObj).length === 0 && responseObj.constructor === Object) {
            document.getElementById("report").innerHTML = NO_RESULT;
            return;
        }
        document.getElementById("report").innerHTML = responseObj.attitude + responseObj.emoji;
        if (responseObj.wcloud === null) {
            document.getElementById("wcloud").src = "../images/well.png";
        } else {
            document.getElementById("wcloud").src = "data:image/png;base64," + responseObj.wcloud;
        }
        var container = document.getElementsByClassName("flex-container")[0];
        for (tag in responseObj.tags) {
            var flex = document.createElement("div");
            flex.textContent = responseObj.tags[tag];
            flex.setAttribute("class", "flex");
            container.appendChild(flex);
        }
    } else {
        document.getElementById("report").innerHTML = NO_RESULT;
    }
};

// function to call api
function getReport(vid) {
    let httpRequest = new XMLHttpRequest();
    httpRequest.open("GET", URL.concat(vid), true);
    httpRequest.onload = displayResponse;
    httpRequest.responseType = "json";
    httpRequest.setRequestHeader("Content-Type", "application/json");
    httpRequest.send();
}

function showReport(response) {
    // TODO change mocking showing
    document.getElementById("report").innerHTML = report.toString();
}

// parse video id from url
function parseVid(url) {
    // use positive lookahead, starting to match after "?v="
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
                getReport(document.getElementById("idbox").value);
            }
        );
    }, false
);