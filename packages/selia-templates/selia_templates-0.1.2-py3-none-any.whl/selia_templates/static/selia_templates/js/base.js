var itemFileList = [];
var errorList = [];
var successList = [];
var req_count = 0;
var error_page_number = 0;
var total_error_pages = 0;
var error_page_step = 5;


$(function() {
  $('.datepicker').datepicker({dateFormat: 'yy-mm-dd'});
});

// Add animation to navbar collapse button
window.addEventListener('load', function() {
  var navbarButton = document.getElementById('navbarButton');
  var navbarButtonIcon = document.getElementById('navbarButtonIcon');
  var collapsedNavbar = false;

  if (navbarButton) {
    navbarButton.addEventListener('click', function(){
      if(collapsedNavbar){
        navbarButtonIcon.className = 'fas fa-chevron-down';
      } else{
        navbarButtonIcon.className = 'fas fa-chevron-down open';
      }

      collapsedNavbar = !collapsedNavbar;
    });
  }
});


function submitSingle(fileIndex, file, url, total_files) {
  var formData = new FormData($('#addItemForm')[0]);
  var request = new XMLHttpRequest();

  formData.set('item_file', file);
  request.open('POST', url, false);
  request.send(formData);

  try {
    response_obj = JSON.parse(request.responseText);
    if (request.status == 200) {
      successList.push([file.name, request.status, response_obj]);
    } else {
      errorList.push([file.name, request.status, response_obj]);
    }
  } catch (error) {
    console.error(error);
  }
  req_count = req_count + 1;
  percent = Math.round((req_count * 100) / total_files);
  $('#progress_upload_bar')
    .css('width', percent + '%')
    .attr('aria-valuenow', percent);
  $('#progress_upload_bar span').html(percent + '%');

  if (fileIndex == total_files - 1) {
    showResults(url, errorList, successList);
  }
}
function parseDate(fileName,parser_map){
  var date_context = fileName.match(parser_map["regexp"]);
  if (date_context){
    var date = ""

    date = date + date_context.toString().substring(parser_map["year"]["limits"][0],parser_map["year"]["limits"][1]);
    date = date + "-" + date_context.toString().substring(parser_map["month"]["limits"][0],parser_map["month"]["limits"][1]);
    date = date + "-" + date_context.toString().substring(parser_map["day"]["limits"][0],parser_map["day"]["limits"][1]);
    date = date+" "+date_context.toString().substring(parser_map["hour"]["limits"][0],parser_map["hour"]["limits"][1]);
    date = date + ":" + date_context.toString().substring(parser_map["minute"]["limits"][0],parser_map["minute"]["limits"][1])
    date = date + ":" + date_context.toString().substring(parser_map["second"]["limits"][0],parser_map["second"]["limits"][1])

    return date;
  }

  return "";

}
function validate_date(dateString,format="YYYY-MM-DD"){
  if (dateString != ""){
    if (moment(dateString, format,true).isValid()){
      return dateString;
    }
  }

  return false;
}
function validateFile(fileIndex, file, url, total_files, date_parser_map,date) {
  file["file_index"] = fileIndex;
  file["veto"] = false;

  if (date_parser_map){
    date = validate_date(parseDate(file.name,date_parser_map),format="YYYY-MM-DD hh:mm:ss");
  } else {
    date = validate_date(date);
  }

  if (date){
    file["captured_on"] = date;
  } else {
    file["captured_on"] = null;
  }

  switch (file.type){
    case 'image/jpeg':
    case 'image/jpg':{
      file["item_type"] = "Foto de Camara Trampa (jpg)";
      break;
    }
    case 'image/png':{
      file["item_type"] = "Foto de Camara Trampa (png)";
      break;
    }
    default:{
      file["item_type"] = null;
      break;
    }
  }

}
function validate_parser_map(pvalue){
      var example_date = {"year":"1985","month":"09","day":"19"}
      var pattern_mask = "";
      var pieces = [];
      var date_parser_map = {};
      var bad_date_map = false;
      var date_regexp = null;

      if (pvalue.includes('<') && pvalue.includes('>')){

        for(var i=0; i<pvalue.length;i++) {
          if (pvalue[i] == "<"){
            pattern_mask = pattern_mask + pvalue[i];
            for (var j=i+1; j<pvalue.length; j++){
              pattern_mask = pattern_mask + pvalue[j];
              if (pvalue[j] == ">"){
                pieces.push([i+1,j]);
                i = j;
                break;
              } else if (pvalue[j] == "<") {
                i = pvalue.length;
                break;
              }
            }
          } else {
            pattern_mask = pattern_mask + "_";
          }
        }

        if (pieces.length > 0){
          date_regexp = pvalue.substring(pieces[0][0]-1,pieces[pieces.length-1][1]+1);
          var cut_pattern = pattern_mask.substring(pieces[0][0]-1,pieces[pieces.length-1][1]+1).replace(/</g,"").replace(/>/g,"");

          for (var p=0;p<pieces.length;p++){
            var substr = pvalue.substring(pieces[p][0],pieces[p][1]);
            var substr_length = substr.length;
            var cat = distinctStr(substr);
            var parser_key = null;
            var start = 0;
            if (substr_length > 0 && cat.length == 1){
              switch(cat){
                case 'Y':{
                  if (substr_length == 4 || substr_length == 2){
                    parser_key = 'year';
                  } else {
                    bad_date_map = true;
                  }
                  break;
                }
                case 'M':{
                  if (substr_length == 2){
                    parser_key = 'month';
                  } else {
                    bad_date_map = true;
                  }
                  break;
                }
                case 'D':{
                  if (substr_length == 2){
                    parser_key = 'day';
                  } else {
                    bad_date_map = true;
                  }
                  break;
                }
                case 'h':{
                  if (substr_length == 2){
                    parser_key = 'hour';
                  } else {
                    bad_date_map = true;
                  }
                  break;
                }
                case 'm':{
                  if (substr_length == 2){
                    parser_key = 'minute';
                  } else {
                    bad_date_map = true;
                  }
                  break;
                }
                case 's':{
                  if (substr_length == 2){
                    parser_key = 'second';
                  } else {
                    bad_date_map = true;
                  }
                  break;
                }
                default:{
                  bad_date_map = true;
                  break;
                }
              }

              if (!bad_date_map){
                date_regexp = date_regexp.replace("<"+substr+">","\\d{"+substr_length+"}");
                start = cut_pattern.indexOf(substr);
                date_parser_map[parser_key] = {'limits':[start,start+substr_length],'length':substr_length,"order":p};
              }

            } else {
              bad_date_map = true;
            }

          }
          if (!bad_date_map){
            if ('year' in date_parser_map && 'month' in date_parser_map && 'day' in date_parser_map && 'second' in date_parser_map){
              date_parser_map["regexp"] = date_regexp;
              return date_parser_map;
            }
          }
        }
      }

      return false;
}

function get_file_page(items, page, per_page, filter) {
  var page = page || 1,
  per_page = per_page || 10,
  offset = (page - 1) * per_page,
  filteredItems = items.filter(filter),
  paginatedItems = filteredItems.slice(offset).slice(0, per_page),
  total_pages = Math.ceil(filteredItems.length / per_page);


  if (filteredItems.length <= per_page && filteredItems.length > 0){
    total_pages = 1;
  }
  return {
          page: page,
          per_page: per_page,
          pre_page: page - 1 ? page - 1 : null,
          next_page: (total_pages > page) ? page + 1 : null,
          total: filteredItems.length,
          total_pages: total_pages,
          data: paginatedItems
          };
}

function check_errors(f){
  if ((!f.item_type || !f.captured_on) && !f.veto){
    return true;
  } else {
    return false;
  }
}

var showResults = function(url, errors, successes) {
  var duplicate_pks = [];
  var success_pks = [];

  for (var i = 0; i < errors.length; i++) {
    var error = errors[i];
    var error_data = error[2];
    if (error_data['error_type'] == 'duplicate') {
      duplicate_pks.push(error_data['duplicate_pk']);
    }
  }
  for (var i = 0; i < successes.length; i++) {
    var success = successes[i];
    var success_data = success[2];
    success_pks.push(success_data['success_pk']);
  }

  window.location.href =
    url +
    '&duplicate_pks=' +
    JSON.stringify(duplicate_pks) +
    '&success_pks=' +
    JSON.stringify(success_pks);
};

function toTitleCase(str) {
  str = str || '';
  str = str.replace('_', ' ');
  return str.replace(/\w\S*/g, function(txt) {
    return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
  });
}

function toTitleCase2(str) {
  str = str || '';
  str = str.replace('_', ' ');
  return str.replace(/\w\S*/, function(txt) {
    return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
  });
}

function distinctStr(str) {
  return String.prototype.concat(...new Set(str))
}

$(document).ready(function() {
  var upload_item_form = document.getElementById('upload_item_form');
  var uploader_section = document.getElementById('uploader_section');

  function renderErrorList(page,parent){
    while (parent.firstChild) {
      parent.removeChild(parent.firstChild);
    }
    for (var i=0;i<page.data.length;i++){
        var errorRow = document.createElement('div');
        errorRow.className = 'row d-flex justify-content-between list_item';
        errorRow.align = "center";
        errorRow.style["margin"] = "10px";

        var descrCol = document.createElement('div');
        descrCol.className = 'col-3';
        var errorTypeCol = document.createElement('div');
        errorTypeCol.className = 'col-3';
        var fixerCol =  document.createElement('div');
        fixerCol.className = 'col-4';

        errorRow.appendChild(descrCol);
        errorRow.appendChild(errorTypeCol);
        errorRow.appendChild(fixerCol);

        var fileTitle = document.createElement('h5');
        fileTitle.textContent = 'File:';
        var fileName = document.createElement('div');
        fileName.className = "text-muted ml-4 ellipsise";
        fileName.textContent = page.data[i].name;

        var errorTitle = document.createElement('h5');
        errorTitle.textContent = 'Error type:';
        var errorName = document.createElement('div');
        errorName.className = "text-muted ml-4";

        errorTypeCol.appendChild(errorTitle);
        errorTypeCol.appendChild(errorName);
        descrCol.appendChild(fileTitle);
        descrCol.appendChild(fileName);

        var omitBtn = document.createElement('button');
        omitBtn.className = "btn btn-primary omit_btn"
        omitBtn.textContent = "Omit"
        omitBtn["file_index"] = page.data[i]["file_index"];

        omitBtn.onclick = function(e){
          itemFileList[this.file_index]["veto"] = true;
          var new_zero = get_file_page(itemFileList,0,error_page_step,filter=check_errors);
          error_page_number = Math.min(new_zero["total_pages"],error_page_number);
          var error_page = get_file_page(itemFileList,error_page_number,error_page_step,filter=check_errors);

          if (error_page.data.length > 0){
              total_error_pages = error_page["total_pages"];
              renderErrorList(error_page,dateErrors);
              $('#error_paginator_label').html("Page "+error_page["page"]+"/"+error_page["total_pages"]);
              dateErrorsContainer.style.display = "block";
          }
        }

        if (!page.data[i].item_type){
          errorName.textContent = "Wrong file type.";
          fixerCol.appendChild(omitBtn);

        } else if (!page.data[i].captured_on){
          errorName.textContent = "Date could not be parsed.";

          var new_input = document.createElement('input');
          new_input.type = "text";
          new_input.id = "date_input_file_"+page.data[i]["file_index"];
          $(new_input).datepicker({dateFormat: 'YYYY-MM-DD'});
          new_input.placeholder = "YYYY-MM-DD";

          var fixBtn = document.createElement('button');
          fixBtn.className = "btn btn-primary"
          fixBtn.textContent = "Fix"
          fixBtn["file_index"] = page.data[i]["file_index"];

          fixBtn.onclick = function(e){
            var raw_date = document.getElementById("date_input_file_"+this.file_index).value;
            var new_date = validate_date(raw_date);
            if (new_date){
              itemFileList[this.file_index]["captured_on"] = new_date;

              var new_zero = get_file_page(itemFileList,0,error_page_step,filter=check_errors);
              error_page_number = Math.min(new_zero["total_pages"],error_page_number);
              var error_page = get_file_page(itemFileList,error_page_number,error_page_step,filter=check_errors);

              if (error_page.data.length > 0){
                  total_error_pages = error_page["total_pages"];
                  renderErrorList(error_page,dateErrors);
                  $('#error_paginator_label').html("Page "+error_page["page"]+"/"+error_page["total_pages"]);
                  dateErrorsContainer.style.display = "block";
              }
            } else {
              alert("Please provide a valid date")
            }
          }

          fixerCol.appendChild(new_input);
          fixerCol.appendChild(fixBtn);
          fixerCol.appendChild(omitBtn);
        }
        parent.appendChild(errorRow);
      }
  }
});
