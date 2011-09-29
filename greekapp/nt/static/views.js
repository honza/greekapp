nt.Views = nt.Views || {};


nt.Views.Reader = function() {
  this.el = $('#reader');
  this.showVerse('John', 3, 16, $.proxy(function(html) {
    this.el.append(html); 
  }, this));
};


nt.Views.Reader.prototype.showVerse = function(book, chapter, verse, callback) {
  var v = new nt.Models.Verse(book, chapter, verse, callback);
  v.get();
};


nt.Views.Books = function() {
  this.el = $('#sidebar');
};


nt.Views.App = function() {
  this.reader = new nt.Views.Reader;
};
