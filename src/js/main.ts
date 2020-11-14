declare var Masonry: any;
declare var imagesLoaded: any;

const gallery = document.getElementById('gallery')

const m = new Masonry(gallery, {
  itemSelector: '.painting',
  columnWidth: 140,
  isFitWidth: true,
  transitionDuration: 0
})

imagesLoaded(gallery).on('always', function(e: any) {
  m.layout();
})