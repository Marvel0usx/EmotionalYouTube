// function to trigger analysis
function analyze(vid) {
    alert("analysis begins!");
    // TODO change mocking report
    var report = "Report for "
    return report.concat(vid);
}

function showReport(report) {
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
                var report = analyze(document.getElementById("idbox"));
                if (report) {
                    showReport(report);
                }
            }
        );
    }, false
);