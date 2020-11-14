declare var PhotoSwipe: any;
declare var PhotoSwipeUI_Default: any;

let items = [];
const psOptions = {
  index: 0,
};

(() => {
  const images = Array.from(
    document.querySelectorAll<HTMLImageElement>('#gallery img')
  );

  const promises = [];

  for (let image of images) {
    promises.push(
      getSize(image).then(([width, height]) => {
        image.dataset.size = `${width}x${height}`;
        return {
          src: image.src,
          w: width,
          h: height,
        };
      })
    );
  }

  // Ideally this isn't needed and the sizes would be stored in the
  // database. For now, wait for all images to load and grab their
  // sizes to pass to the items array.
  Promise.all(promises).then((result) => {
    items = result;
    document.getElementById('gallery').addEventListener('click', (e) => {
      const target = e.target as HTMLElement;
      const parent = target.closest<HTMLElement>('.painting');

      if (!parent) {
        return;
      }

      const index = +parent.dataset.index;
      initializeGallery(index);
    });
  });

  function getSize(img): Promise<[number, number]> {
    return new Promise((resolve) => {
      img.addEventListener('load', () => {
        resolve([img.naturalWidth, img.naturalHeight]);
      });
    });
  }
})();

function initializeGallery(index) {
  const pswpElement = document.querySelector('.pswp');
  psOptions.index = index;
  const gallery = new PhotoSwipe(
    pswpElement,
    PhotoSwipeUI_Default,
    items,
    psOptions
  );
  gallery.init();
}
