const express = require('express');
const router = express.Router();
const admin = require('firebase-admin');
const db = admin.firestore();

router.get('/', async function (req, res, next) {
  const snapshot = await db.collection('images').get();
  const result = { images: [], total: +snapshot.size };

  snapshot.forEach((doc) => {
    result.images.push({ ...doc.data() });
  });

  res.render('index', {
    title: 'Arsenii.com',
    imageData: result,
  });
});

module.exports = router;
