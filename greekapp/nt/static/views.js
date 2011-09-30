nt.Views = nt.Views || {};


nt.Views.Reader = function() {
  this.el = document.getElementById('reader');
  this.showVerse('John', 3, 16);

  this.text = document.getElementById('text');
  this.go = document.getElementById('go');

  this.go.onclick = _(function() {
    var value = this.text.value;
    var ref;

    var parts = value.split(' ');

    if (parts.length === 2) {
      ref = parts[1].split(':');
      this.showVerse(parts[0], ref[0], ref[1]);
      return;
    }

    if (parts.length === 3) {
      ref = parts[2].split(':');
      this.showVerse(parts[0] + ' ' + parts[1], ref[0], ref[1]);
      return;
    }

  }, this);

};


nt.Views.Reader.prototype.showVerse = function(book, chapter, verse) {
  var v = new nt.Models.Verse(book, chapter, verse, _(this.renderVerse, this));
  v.get();
};

nt.Views.Reader.prototype.renderVerse = function(html) {
    this.el.innerHTML = ''; 
    this.el.appendChild(html); 
};


nt.Views.App = function() {
  this.reader = new nt.Views.Reader;
};
