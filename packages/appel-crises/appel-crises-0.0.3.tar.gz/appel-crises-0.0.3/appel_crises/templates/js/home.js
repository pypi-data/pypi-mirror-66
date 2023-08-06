function displayIfJsElements() {
  var elements = document.getElementsByClassName("display-if-js");
  [].forEach.call(elements, function(el) {
      el.style.display = 'block';
  });

  elements = document.getElementsByClassName("remove-if-js");
  [].forEach.call(elements, function(el) {
      el.style.display = 'none';
  });
}

displayIfJsElements();
