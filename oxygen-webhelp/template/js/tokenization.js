var executed = false;
$(document).ready(function() {
    $("#searchForm").on("submit", (e) => {
        // WebHelps triggers the submit event handler multiple times.
        if (!executed) { // We make sure that we execute it only one time.
            e.stopPropagation();
            var userQuery = $('#textToSearch').val();
            if (userQuery.trim() === '') {
                e.preventDefault();
                return false;
            }

            if (!/^[a-zA-Z]+$/.test(userQuery)) {
                userQuery = tokenizeChineseInput(userQuery);
            }
            $('#textToSearch').val(userQuery);
            executed = true;
        }
    });

    $("#searchForm").on("reset", () => {
        executed = false; // Reset the executed flag when the form is reset
    });
});

function tokenizeChineseInput(input) {
    var chineseRegex = /[\u4e00-\u9fa5]/g;
    var matches = input.match(chineseRegex);
    if (matches) {
        return input.replace(chineseRegex, function(match) {
            return match.split('').join(' ');
        });
    }
    return input;
}

// Restore the split substrings back to the original string
$("#searchForm").on("submit", () => {
    var userQuery = $('#textToSearch').val();
    if (!/^[a-zA-Z]+$/.test(userQuery)) {
        userQuery = restoreChineseInput(userQuery);
        $('#textToSearch').val(userQuery);
    }
});

function restoreChineseInput(input) {
    return input.replace(/([\u4e00-\u9fa5]) /g, '$1');
}
