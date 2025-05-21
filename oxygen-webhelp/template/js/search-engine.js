// WebHelpAPI.SearchMeta is a JavaScript object used to hold additional information for the search result. To create such an object, the following fields are required:
//     String: searchEngineName - The name of the search engine used to retrieve the search result.
//     Integer: totalSearchItems - The total number of search items the search engine returned.
//     Integer: currentPage - The current page to display.
//     Integer: maxItemsPerPage - The maximum number of items that can be displayed on a page.
//     Integer: totalPages - The number of total pages for the search result.
//     String: originalSearchExpression - The query string the user typed in the search input field.


// WebHelpAPI.SearchDocument is a JavaScript object used to hold the search result for a single topic/HTML page. To create such an object, the following fields are required:
//     String: linkLocation - The URL to the topic.
//     String: title - The topic title.
//     String: shortDescription - The topic short description.

// WebHelpAPI.SearchResult is a JavaScript object used to display the search results in the search page. To create such an object, the following fields are required:
//     WebHelpAPI.SearchMeta: searchMeta - Contains additional information for the search result.
//     Array[WebHelpAPI.SearchDocument]: documents - An array with the matching documents (HTML pages) for the search result.


const versions = ['1.30.22', '1.30.23', '2.00.10', '2.00.11', '2.00.12', '2.00.13', '2.00.14', '2.00.15', '2.00.16', '3.00.0', '3.00.1', '3.00.2', '3.00.3']
const languages = ['zh', 'en']

// implement search engine
async function externalSearchEngine(query, pageToShow = 1, maxItemsPerPage = 50){
  const url_info = location.pathname.split('/')
  const language = languages.find(_langauge => _langauge === url_info[1]) ? url_info[1] : languages[0]
  const version = versions.find(_version => _version === url_info[2]) ? url_info[2] : ''
  const hostname = window.location.hostname
  const api_hostname = hostname.replace(/docs\.dolphindb\.(cn|com)/,"dolphindb.cn")
  
  const { totalSearchItems, totalPage, items }= await (await fetch(`https://${api_hostname}/api/search`,{
    method:'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({query, pageToShow, maxItemsPerPage, language, version})
  })).json()
  
  return new WebHelpAPI.SearchResult(
    new WebHelpAPI.SearchMeta('ddb', totalSearchItems, pageToShow, maxItemsPerPage, totalPage, query), 
    items.map(({url, title, content})=>new WebHelpAPI.SearchDocument(url, title, content))
  )
}

/**
 * Object that implements the methods required by WebHelp to run a search engine.
 */
function CustomSearchEngine() {
     
    /**
     * Method required to run the search engine in webhelp. Handler when the users 
     * executes the query in the search page. 
     */
    this.performSearchOperation = async function(query, successHandler, errorHandler) {
        try {
          successHandler(await externalSearchEngine(query))
        } catch (error) {
          errorHandler(error.message)
        } 
    }
  
    /**
     * Method required to run the search engine in webhelp. Handler when the 
     * page is changed in the search page.
     */
    this.onPageChangedHandler = async function(pageToShow, maxItemsPerPage, query, successHandler, 
  errorHandler) {
        try {
          successHandler(await externalSearchEngine(query, pageToShow, maxItemsPerPage))
        } catch (error) {
          errorHandler(error.message)
        }
    }
  }
  
  // Set the Search Engine to WebHelp
  WebHelpAPI.setCustomSearchEngine(new CustomSearchEngine());