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
                userQuery = userQuery.replace(/[\u4e00-\u9fa5]{2}/g, '$& '); // if the input isn't English characters, split every given Chinese input (string) by separating every two Chinese chars by spaces.
                var originalUserQuery = userQuery.replace(/ /g, ''); // Restore the original form of the search string before string split.
                $('#textToSearch').val(originalUserQuery);
            }
            executed = true;
        }
    });

    // Scoring weight for each HTML tag element
    var scoringWeight = {
        "h1": 100,
        "h2": 40,
        "h3": 30,
        "h4": 20,
        "h5": 10,
        "h6": 10,
        "b": 10,
        "strong": 5,
        "em": 5,
        "i": 5,
        "u": 5,
        "p": 50,
        "div.toc": 10,
        "title": 150,
        "div.ignore": "ignored",
        "meta_keywords": 60,
        "meta_indexterms": 60,
        "meta_description": 1,
        "shortdesc": 10
    };

    // Use scoring weight to rank topic pages in search results
    function rankTopicPages() {
        // Add code here to rank topic pages based on the scoring weight for each HTML tag element
    }
});
