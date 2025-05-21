// Include the Fuse.js library (make sure to add the script tag in your HTML)
// <script src="https://cdn.jsdelivr.net/npm/fuse.js"></script>

// Define the data to be searched (e.g., an array of objects with text content)
const data = [
  { id: 1, text: "Apple" },
  { id: 2, text: "Banana" },
  { id: 3, text: "Orange" },
  // Add more items as needed
];

// Create a new instance of Fuse.js with the desired options
const options = {
  keys: ["text"], // Specify the object property to search within
  includeScore: true, // Include a relevance score for each match
};

const fuse = new Fuse(data, options);

// Function to perform the fuzzy search
function performFuzzySearch(query) {
  const results = fuse.search(query);

  // Process the search results
  results.forEach((result) => {
    const { item, score } = result;
    console.log(`Matched item: ${item.text}, Score: ${score}`);
    // Do something with the matched item (e.g., display it on the web page)
  });
}

// Example usage:
const searchQuery = "app"; // The search query
performFuzzySearch(searchQuery);
