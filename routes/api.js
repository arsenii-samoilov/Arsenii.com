const express = require('express');
const router = express.Router();
const admin = require('firebase-admin');
const db = admin.firestore();

router.get('/images', async function (req, res, next) {
  const snapshot = await db.collection('images').get();
  const result = { images: [], total: +snapshot.size };

  snapshot.forEach((doc) => {
    result.images.push({ ...doc.data() });
  });

  res.json(result);
});

module.exports = router;
