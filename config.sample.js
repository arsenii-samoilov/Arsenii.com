let config = {};
config.host= 'smtp.mailgun.com';
config.fromEmail= 'fortesting@test.com' || process.env.FROM_EMAIL;
config.toEmail= 'test@gmail.com' || process.env.TO_EMAIL;
config.mailgun= 'key-xxxx' || process.env.MAILGUN_API_KEY;
config.domain= 'website.com' || process.env.DOMAIN;

module.exports = config;
