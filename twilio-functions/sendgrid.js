// using SendGrid's v3 Node.js Library
// https://github.com/sendgrid/sendgrid-nodejs
const sgMail = require("@sendgrid/mail");

exports.handler = function(context, event, callback) {
  sgMail.setApiKey(context.SENDGRID_API_KEY);

  const msg = {
    to: event.TO_EMAIL,
    from: context.FROM_EMAIL,
    subject: "-",
    text: "-",
    html: "-",
    templateId: "d-xxxxxxxxxxxxxxxxxxxxx", // Create at https://sendgrid.com/dynamic_templates
    dynamic_template_data: {
      subject: "Notification from Twilio",
      body: "<strong>" + event.EMAIL_BODY + "</strong>"
    }
  };

  console.log(msg);

  sgMail
    .send(msg)
    .then(response => {
      console.log("Success: Accepted");
      callback(null, response);
    })
    .catch(error => {
      const { message, code, response } = error;
      console.error("Error: " + error.message);
      callback(null, error);
    });
};
