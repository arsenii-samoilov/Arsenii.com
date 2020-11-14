const env = require('dotenv').config();

const createError = require('http-errors');
const serviceAccount = require(process.env.FIREBASE_SERVICE_ACCOUNT);
const express = require('express');
const path = require('path');
const cookieParser = require('cookie-parser');
const logger = require('morgan');
const admin = require('firebase-admin');

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
});

// Need to require routes _after_ firebase initialization
const apiRoutes = require('./routes/api');
const baseRoutes = require('./routes/main');

var app = express();

// view engine setup
app.set('views', path.join(__dirname, 'dist'));
app.set('view engine', 'ejs');

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());

// Handled by NGINX in prod
if (process.env.NODE_ENV !== 'production') {
  app.use(express.static(path.join(__dirname, 'dist')));
}

app.use('/', baseRoutes);
app.use('/api', apiRoutes);

// catch 404 and forward to error handler
app.use(function (req, res, next) {
  next(createError(404));
});

// error handler
app.use(function (err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.render('error');
});

module.exports = app;
