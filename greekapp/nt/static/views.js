nt.Views = nt.Views || {};


nt.Views.Reader = function() {
  this.el = document.getElementById('reader');
  this.showVerse('John', 3, 16, _(function(html) {
    this.el.appendChild(html); 
  }, this));
};


nt.Views.Reader.prototype.showVerse = function(book, chapter, verse, callback) {
  var v = new nt.Models.Verse(book, chapter, verse, callback);
  v.get();
};


nt.Views.App = function() {
  this.reader = new nt.Views.Reader;
};
