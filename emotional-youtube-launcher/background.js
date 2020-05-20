function parseVid(url) {
    // use positive lookahead, starting to match after '?v='
    const regex = /(?<=\?v\=)([A-Za-z0-9_-]+)/;
    const found = url.match(regex);

    if (found !== null) {
        chrome.storage.sync.set({'vid': found[0]});
    } else {
        chrome.storage.sync.set({'vid': null});
    }
}

// parse vid when extension is onClick
chrome.browserAction.onClicked.addListener(function(tab) {
    // No tabs or host permissions needed!
    parseVid(tab.url);
});
