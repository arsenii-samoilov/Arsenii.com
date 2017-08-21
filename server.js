const express = require('express')
const Mailgun = require('mailgun-js');
const bodyParser = require('body-parser');
const logger = require('morgan')
const config = require('./config')
const app = express();

function crossOrgin(req, res, next) {
    res.header('Access-Control-Allow-Origin', '*');
    res.header('Access-Control-Allow-Headers', 'X-Requested-With');
    return next();
  }

app.use(logger('dev'));
/**
* API Status for mailgun endpoint
*
*/
app.get('/apiTest', (req, res, next) => {
  const mailgun = new Mailgun({apiKey: config.mailgun, domain: config.domain});
    console.log(`Mailgun parameters: ${mailgun}`);
    console.log(`================================`)
    const data = {
      from: 'test@test.com',
      to: 'benhalverson@me.com',
      subject: 'test',
      text: 'test message'
    };

    mailgun.messages().send(data, (error, body) => {
      console.log(`body ${body}`);
      if(error) {
        console.log(`Error: ${error}`)
        res.send(`Mail not sent check the error log`);
      } else {
        res.send('Mail sent');
      }
    });
});

/**
* API endpoint for sending emails
*
* @param {string} subject The subject title of the email to send
* @param {string} message The email message
*/


app.post('/contact',(req, res, next) => {
const mailgun = new Mailgun({apiKey: config.mailgun, domain: config.domain});

 const data = {
   from: config.fromEmail,
   to: config.toEmail,
   subject: req.body.subject,
   text: req.body.message
 };

 mailgun.messages().send(data, (error, body) => {
   console.log(`body ${body}`);
   if(error) {
     res.send(`Mail not sent check the error log`);
     return next(new Error(`Error: ${error}`));
   } else {
     res.send('Mail sent');
   }
 });
});
const PORT = 8080 || process.env.PORT;
app.listen(PORT, () => {
  console.log(`listening on port ${PORT}`);
});
