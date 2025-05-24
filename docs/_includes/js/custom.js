/** 
 * All the catalog tables on this page. 
 */
var dataTables = {};

/**
 * Function to render a Tabulator table for a keyword's data.
 * uniqueID:       For defining a unique id for the table object.
 * keyword:        The primary keyword for data in this table.
 * data:           The JS array to show in the table. See how the
 *                 columns are set up for documentation on the 
 *                 expected fields in the objects in "data".
 * showKeywordCol: Whether or not to show the "keyword" column. This 
 *                 is usually only true if a table has data from more
 *                 than one keyword. Otherwise, it's wasted space!
 * detailsID:      The HTML object that is replaced by a record's
 *                 details when the corresponding row is clicked.
 * Notes:
 * 1. Using minHeight and maxHeight doesn't permit user resizing beyond those limits.
 * 2. A fixed height of 300 means that short tables have an empty gray area at the bottom
 *    so we use a "hack" calculation to estimate the size.
 */
function makeCatalogTable(uniqueID, keyword, data, showKeywordCol, detailsID, saveJSONFileName) {
  var keywordArray = [];
  if (showKeywordCol) {
    keywordArray = [{title:"Keyword", field:"keyword"}];
  };
  const startingHeight = data.length * 35 < 300? data.length * 35: 300;
  const tableID = `${uniqueID}-table`;
  const dataTable = new Tabulator(`#${tableID}`, {
    data: data, 
    height: startingHeight, // Set the height of the table (in CSS or here), this enables the Virtual DOM and improves render speed dramatically (can be any valid css height value).
    layout: "fitColumns", // Fit columns to width of table (optional).
    responsizeLayout: "hide", // Hide columns that don't fit on the table.
    tooltips: true,
    history: true,  // When table is editable, allow undo and redo actions.
    addRowPos: "top", // When editable, new elements go on top.
    movableColumns: true, // Allow columns to be reordered.
    columns: Array.prototype.concat( [ //Define Table Columns
      {title:"Name", field:"name", formatter:"link", formatterParams:{
        labelField:"name",
        urlField:"dataset_url",
        target:"_blank",
      }}],
      keywordArray,
      [{title:"License", field:"license", formatter:"link", formatterParams:{
        labelField:"license",
        urlField:"license_url",
        target:"_blank",
      }},
      {title:"Creator", field:"creator_name", formatter:"link", formatterParams:{
        labelField:"creator_name",
        urlField:"creator_url",
        target:"_blank",
      }}])
  });
  dataTables[uniqueID] = dataTable;

  dataTable.on("rowClick", function(e, row){ 
    const data = row.getData();
    var   keywords_str = data.first_N_keywords.join(', ')
    if (data.keywords_longer_than_N) {
        keywords_str += "... (see dataset for all keywords)";
    };
    const desc = data.description.replace(/\\+[nr]/g, "\n").replace(/\\+t/g, "\t"); // clean up escape quoting!
    const message = `
      <table>      
        <tr><td><strong>Name:</strong></td><td><a href="${data.dataset_url}" target="_blank">${data.name}</a></td></tr>
        <tr><td><strong>Keyword:</strong></td><td>${data.keyword}</td></tr>      
        <tr><td><strong>Other Keywords:<sup>1</sup></strong></td><td>${keywords_str}</td></tr>      
        <tr><td><strong>License:</strong></td><td><a href="${data.license_url}" target="_blank">${data.license}</a></td></tr>
        <tr><td><strong>Creator:</strong></td><td><a href="${data.creator_url}" target="_blank">${data.creator_name}</a></td></tr>
        <tr><td><strong>Description:</strong></td><td><p class="description">${desc}</p></td></tr>
      </table>
      <span class="text-small text-grey-dk-100 mb-0">1: The list of keywords in the dataset itself, not the &ldquo;additional keywords&rdquo; (if any) grouped with <code>${keyword}</code>.</span>
    `;
    setInnerHTML(detailsID, message);
  });
  return {"id": tableID, "table": dataTable, "numRows": data.length};
}

function setInnerHTML(id, content, ignoreMissing = false) {
  const elem = document.getElementById(id);
  if (elem) {
    elem.innerHTML = content;
  } else if (! ignoreMissing) {
    console.log(`ERROR: setInnerHTML(): no element found with id ${id}.`);
  }
}

function setDownloadMessage(id_prefix, message) {
  setInnerHTML(`${id_prefix}-download-message`, message);
}

function saveTableAsJSON(id_prefix, id_message) {
  let table = dataTables[id_prefix];
  if (! table) {
    console.log(`ERROR: No table for id ${id_prefix}!`);
  } else {
    allData = table.getData();
    filteredData = table.getData("active");
    filteredStr = allData.length != filteredData.length ? "_filtered" : "";
    filteredMsg = allData.length != filteredData.length ? "filtered" : "all";
    fileName = `${id_prefix}${filteredStr}.json`;
    message = `Writing ${filteredMsg} data to "${fileName}" in your downloads folder.`;
    setDownloadMessage(id_prefix, message);
    setInnerHTML(id_message, message);
    saveJSON(filteredData, fileName);
  }
}

function saveJSON(data, fileName, id_message, message) {
  var jsonToSave = new Blob([JSON.stringify(data, undefined, 2)], {
    type: 'application/json'
  });
  var a = document.createElement("a");
  a.href = window.URL.createObjectURL(jsonToSave);
  a.download = fileName;
  a.click();
}

/**
 * Functions to make a resizable div surrounding a Tabulator table.
 * The only place the table is assumed is in the "resize" method,
 * so this code could be generalized for other objects...
 * Adapted from https://stackoverflow.com/questions/64854699/change-table-height-resize-by-dragging-the-bottom-border
 */
function makeResizableTableDiv(divID, table) {
  if (!table) { 
    console.log(`Warning: makeResizableTableDiv(): input table is null!`);
    return; 
  }
  const element  = document.getElementById(divID);
  if (!element) { 
    console.log(`Warning: makeResizableTableDiv(): no element found for id = ${divID}!`);
    return; 
  }
  const resizers = element.querySelectorAll('.resizer-line')
  const minimum_size = 90;
  let original_width = 0;
  let original_height = 0;
  let original_x = 0;
  let original_y = 0;
  let original_mouse_x = 0;
  let original_mouse_y = 0;
  for (let i = 0; i < resizers.length; i++) {
    const currentResizer = resizers[i];
    currentResizer.addEventListener('mousedown', function(e) {
      e.preventDefault()
      original_width = parseFloat(getComputedStyle(element, null).getPropertyValue('width').replace('px', ''));
      original_height = parseFloat(getComputedStyle(element, null).getPropertyValue('height').replace('px', ''));
      original_x = element.getBoundingClientRect().left;
      original_y = element.getBoundingClientRect().top;
      original_mouse_x = e.pageX;
      original_mouse_y = e.pageY;
      window.addEventListener('mousemove', resize)
      window.addEventListener('mouseup', stopResize)
    })
    
    function resize(e) {
      if (currentResizer.classList.contains('bottom-line')) {
        const height = original_height + (e.pageY - original_mouse_y);
        if (height > minimum_size) {
          table.setHeight(height - 23); // TODO: This magic number was in the example. What is it??
          element.style.height = height + 'px';
        }
      }
    }
    
    function stopResize() {
      window.removeEventListener('mousemove', resize)
    }
  }
}

/**
 * The num argument is a hack; we apparently call this function during setup before
 * table.getData("active") has "active" rows, so 0 is returned.
 */
function setNumRows(id_prefix, table, num = -1) {
  const id = `${id_prefix}-num-rows`;
  const length = num < 0? table.getData("active").length: num;
  if (length == 0) {
    console.log("0 rows");
  }
  numRowsMessage = length == 1 ? `${length} row.`: `${length} rows.`;
  setInnerHTML(id, numRowsMessage);
}

function enableTableFilters(id_prefix, table) {

  // Define variables for input elements
  var fieldElem = document.getElementById(`${id_prefix}-filter-field`);
  var typeElem  = document.getElementById(`${id_prefix}-filter-type`);
  var valueElem = document.getElementById(`${id_prefix}-filter-value`);
  var clearElem = document.getElementById(`${id_prefix}-filter-clear`);

  // Trigger setFilter function with correct parameters
  function updateFilter(){
    var filterVal = fieldElem.options[fieldElem.selectedIndex].value;
    var typeVal = typeElem.options[typeElem.selectedIndex].value;
    table.setFilter(filterVal, typeVal, valueElem.value);
    setNumRows(id_prefix, table);
    setDownloadMessage(id_prefix, "");
  }

  //Update filters on value change
  fieldElem.addEventListener("change", updateFilter);
  typeElem.addEventListener("change", updateFilter);
  valueElem.addEventListener("keyup", updateFilter);

  //Clear filters on "Clear Filters" button click
  clearElem.addEventListener("click", function(){
    fieldElem.value = "";
    typeElem.value = "Like";
    valueElem.value = "";
    table.clearFilter()
    setNumRows(id_prefix, table);
    setDownloadMessage(id_prefix, "");
  });
  clearElem.click
}