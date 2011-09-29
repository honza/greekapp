var nt = {};

nt.Models = nt.Models || {};

nt.Models.url = 'http://localhost:8000/nt/book';

nt.Models.books = [
  'Matthew',
  'Mark',
  'Luke',
  'John',
  'Acts',
  'Romans',
  'Galatians',
  'Ephesians',
  'Phillipians',
  'Colossians',
  '1 Thessalonians',
  '2 Thessalonians',
  '1 Timothy',
  '2 Timothy',
  'Titus',
  'Philemon',
  'Hebrews',
  'James',
  '1 Peter',
  '2 Peter',
  '3 Peter',
  'Jude',
  'Revelation'
];

nt.Models.full2abbr = {
  '1 Corinthians': 'cor1',
  '1 John': 'john1',
  '1 Peter': 'peter1',
  '1 Thessalonians': 'thess1',
  '1 Timothy': 'tim1',
  '2 Corinthians': 'cor2',
  '2 John': 'john2',
  '2 Peter': 'peter2',
  '2 Thessalonians': 'thess2',
  '2 Timothy': 'tim2',
  '3 John': 'john3',
  'Acts': 'acts',
  'Colossians': 'col',
  'Ephesians': 'eph',
  'Galatians': 'gal',
  'Hebrews': 'heb',
  'James': 'james',
  'John': 'john',
  'Jude': 'jude',
  'Luke': 'luke',
  'Mark': 'mark',
  'Matthew': 'matthew',
  'Philemon': 'phm',
  'Phillipians': 'phil',
  'Revelation': 'revelation',
  'Romans': 'romans',
  'Titus': 'titus'
};

nt.Models.Verse = function(book, chapter, verse, callback) {
  this.book = nt.Models.full2abbr[book];
  this.chapter = chapter;
  this.verse = verse;
  this.callback = callback;
  this.html = '';
};

nt.Models.Verse.prototype.get = function() {
  $.getJSON(this.getUrl_(), null, $.proxy(function(data) {
    this.parse(data);
    this.callback(this.html);
  }, this));
};

nt.Models.Verse.prototype.getUrl_ = function() {
  return nt.Models.url + '/' + this.book + '/' + this.chapter + '/' + this.verse + '/';
};

nt.Models.Verse.prototype.parse = function(data) {
  var html = $('<p/>');  

  $.each(data, $.proxy(function(index, item) {
    var word = new nt.Models.Word(item);
    html.append(word.getWidget());
  }, this));

  this.html = html;

};

nt.Models.Word = function(word) {
  this.strong = word.strong;
  this.parse = word.parse;
  this.word = word.word;
  this.lexicon = word.lexicon;
};


nt.Models.Word.prototype.getWidget = function() {
  this.span = $('<span/>');
  this.span.html(this.word + ' ');

  this.span.hover(
    $.proxy(function() {
    this.container.show();
  }, this),
    $.proxy(function() {
    this.container.hide();
  }, this));

  this.container = $('<div class="word"></div>');
  this.container.append($('<p/>').html('Type: ' + this.parse.type));
  this.container.append($('<p/>').html(this.lexicon));

  this.span.append(this.container);

  return this.span;
};
