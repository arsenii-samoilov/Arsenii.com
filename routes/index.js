const express = require('express');
const admin = require('firebase-admin');
const router = express.Router();

/* GET home page. */
router.get('/', function (req, res, next) {
  const db = admin.firestore();
  console.log(db);
  res.render('index', { title: 'Pops' });
});

module.exports = router;
