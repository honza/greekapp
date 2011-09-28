nt.Views = nt.Views || {};


nt.Views.Reader = function() {
  this.el = $('#reader');
  this.showVerse('John', 15, 9, $.proxy(function(html) {
    this.el.append(html); 
  }, this));
};

nt.Views.Reader.prototype.showVerse = function(book, chapter, verse, callback) {
  var v = new nt.Models.Verse(book, chapter, verse, callback);
  //console.log(v);
  v.get();
};


nt.Views.Books = function() {
  this.el = $('#books');
  this.books = nt.Models.books;

  $.each(this.books, $.proxy(function(index, item) {
    var li = $('<li/>').text(item);
    this.el.append(li); 
  }, this));
};


nt.Views.App = function() {
  this.reader = new nt.Views.Reader;
  this.books = new nt.Views.Books;
};
