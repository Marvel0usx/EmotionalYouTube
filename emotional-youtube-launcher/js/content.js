// function to trigger analysis
function analyze(vid) {
    alert("analysis begins!");
    // TODO change mocking report
    return "report for" + vid;
}

// listen to click on button
document.addEventListener("DOMContentLoaded", 
    function() {
        document.getElementById("btn-analyze").addEventListener("click", 
            function() {
                const report = analyze(document.getElementById("idbox"));
                if (report) {
                    showReport(report);
                }
            }
        );
    }, false
);

// listen to message from background, and set vid input box
chrome.runtime.onMessage.addListener(
    function (request) {
        if (request.vid) {
            document.getElementById('idbox').value = request.vid;
        }
    }
);

function showReport(report) {
    alert("showing result!");
    // TODO change mocking showing
    document.getElementById('report').innerHTML = report;
}
