/**
 * Function to render a Tabulator table for a keyword's data.
 * uniqueID:       For defining a unique id for the table object.
 * data:           The JS array to show in the table. See how the
 *                 columns are set up for documentation on the 
 *                 expected fields in the objects in "data".
 * showKeywordCol: Whether or not to show the "keyword" column. This 
 *                 is usually only true if a table has data from more
 *                 than one keyword. Otherwise, it's wasted space!
 * detailsID:      The HTML object that is replaced by a record's
 *                 details when the corresponding row is clicked.
 */
function make_catalog_table(uniqueID, data, showKeywordCol, detailsID, saveJSONFileName) {
  var keywordArray = [];
  if (showKeywordCol) {
    keywordArray = [{title:"Keyword", field:"keyword"}];
  };
  const tableID = `#${uniqueID}-table`;
  const dataTable = new Tabulator(tableID, {
    height:305, // set height of table (in CSS or here), this enables the Virtual DOM and improves render speed dramatically (can be any valid css height value)
    data: data, 
    layout: "fitColumns", //fit columns to width of table (optional)
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
  dataTable.on("rowClick", function(e, row){ 
    const data = row.getData();
    const desc = data.description.replace(/\\+[nr]/g, "\n").replace(/\\+t/g, "\t"); // clean up escape quoting!
    const descDiv = document.getElementById(detailsID);
    const message = `<strong>Name:</strong> <a href="${data.dataset_url}" target="_blank">${data.name}</a><br/><strong>Keyword:</strong> ${data.keyword}<br/><strong>License:</strong> <a href="${data.license_url}" target="_blank">${data.license}</a><br/><strong>Creator:</strong> <a href="${data.creator_url}" target="_blank">${data.creator_name}</a><br/><strong>Description:</strong><p class="description">${desc}</p>`;
    descDiv.innerHTML = message;
  });
}

function save_json(data, fileName, messageSpanID) {
  var jsonToSave = new Blob([JSON.stringify(data, undefined, 2)], {
    type: 'application/json'
  });
  var a = document.createElement("a");
  a.href = window.URL.createObjectURL(jsonToSave);
  a.download = fileName;
  const span = messageSpanID ? document.getElementById(messageSpanID) : null;
  a.click();
  if (span) {
    span.innerHTML = `Writing "${fileName}" to your downloads folder.`;
  }
}
