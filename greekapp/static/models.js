nt.Models = nt.Models || {};

nt.Models.url = 'http://localhost:8000/nt/book';

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

  nt.ajax({
    type: 'get',
    url: this.getUrl_(),
    data: {},
    timeout: 5000,
    onSuccess: _(function(data) {
      data = JSON.parse(data);
      this.parse(data);
      this.callback(this.html);
    }, this)
  });

};

nt.Models.Verse.prototype.getUrl_ = function() {
  return nt.Models.url + '/' + this.book + '/' + this.chapter + '/' + this.verse + '/';
};

nt.Models.Verse.prototype.parse = function(data) {
  var html = document.createElement('p');

  for (var i=0; i < data.length; i++) {
    var word = new nt.Models.Word(data[i]);
    html.appendChild(word.getWidget());
  }

  this.html = html;

};

nt.Models.Word = function(word) {
  this.strong = word.strong;
  this.parse = word.parse;
  this.word = word.word;
  this.lexicon = word.lexicon;
};


nt.Models.Word.prototype.getWidget = function() {
  this.span = document.createElement('span');
  this.span.innerHTML = this.word + ' ';

  this.span.onmouseover = _(function() {
    this.container.style.display = 'block';
  }, this);

  this.span.onmouseout = _(function() {
    this.container.style.display = 'none';
  }, this);

  this.container = document.createElement('div');
  this.container.className = 'word';

  for (var k in this.parse) {
    var el = document.createElement('p');
    el.innerHTML = k + ': ' + this.parse[k];
    this.container.appendChild(el);
  }

  this.lexiconData = document.createElement('p');
  this.lexiconData.innerHTML = this.lexicon;

  this.container.appendChild(this.lexiconData);

  this.span.appendChild(this.container);

  return this.span;
};
