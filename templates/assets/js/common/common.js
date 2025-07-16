function showLoadingSpinner() {
    $('#loading_spinner').show();
    $('#loading_overlay').show();
}

function hideLoadingSpinner() {
    $('#loading_spinner').hide();
    $('#loading_overlay').hide();
}

const numberWithCommas = (x) => {
  return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

const getUrlParams = () => {
  let params = {};
  decodeURI(window.location.search).replace(
    /[?&]+([^=&]+)=([^&]*)/gi,
    function (str, key, value) {
      params[key] = value;
    }
  );
  return params;
}

const jsonToQueryString = (jsonData) =>{
  return Object.entries(jsonData)
    .map((e) => e.join("="))
    .join("&");
}

