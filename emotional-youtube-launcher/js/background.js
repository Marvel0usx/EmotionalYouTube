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

// parse vid when extension is onClick
chrome.browserAction.onClicked.addListener(
    function(tab) {
        var vid = parseVid(tab.url);
        if (vid !== null) {
            chrome.tabs.query({
                active: true,
                currentWindow: true
            }, function(tabs) {
                chrome.tabs.sendMessage(tabs[0].id, {
                    vid: vid
                });
            });
        }
    }
);