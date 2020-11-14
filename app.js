require('dotenv').config();

const createError = require('http-errors');
const serviceAccount = require(process.env.FIREBASE_SERVICE_ACCOUNT);
const admin = require('firebase-admin');
const cookieParser = require('cookie-parser');
const express = require('express');
const fs = require('fs');
const hbs = require('hbs');
const logger = require('morgan');
const path = require('path');

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
});

// Need to require routes _after_ firebase initialization
const apiRoutes = require('./routes/api');
const baseRoutes = require('./routes/main');

var app = express();

// view engine setup
app.set('views', path.join(__dirname, 'dist'));
app.set('view engine', 'hbs');

// Register partials
const partialsDir = path.resolve(__dirname, 'src/views/partials');
const partials = fs.readdirSync(partialsDir);
partials.forEach((filename) => {
  const matches = /^([^.]+).hbs$/.exec(filename);
  if (!matches) {
    return;
  }
  const name = matches[1];
  const template = fs.readFileSync(partialsDir + '/' + filename, 'utf8');
  hbs.registerPartial(name, template);
});
// End partial registering

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
  console.log(err);
  res.render('error');
});

module.exports = app;
