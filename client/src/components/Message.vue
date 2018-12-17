<template>
  <div class="container">

    <div class="row">
      <div class="py-3 col-md-12 mb-12 text-center">
        <img class="d-block mx-auto mb-4" src="https://www.twilio.com/marketing/bundles/company-brand/img/logos/red/twilio-logo-red.svg" alt="" width="172">
        <!-- <img class="d-block mx-auto mb-4" src="https://www.clp.com.hk/en/_layouts/15/clp/styles/images/clp-logo-en.png" alt="" width="172"> -->
        <h2>Omnichannel notifications</h2>
        <p class="lead">
          Below is an example of omnichannel notifications using Twilio and SendGrid.<br>
          Fill in phone numbers and email address,
          your notification text and click send to see it go!
        </p>
      </div>
    </div>

    <form @submit.prevent="handleSubmit">
    <div class="row">

      <div class="col-md-4 order-md-1 mb-4">

        <!-- <label for="contactPerson"> -->
          <h4 class="d-flex justify-content-between align-items-center mb-3">
            Contacts
          </h4>
        <!-- </label> -->
<!--         <select class="custom-select custom-select-lg mb-3"
                id="contactPerson"
                v-model="selectedContact">
          <option v-for="(contact, index) in contacts" :key="index" :value="contact">
            {{ contact.name }}
          </option>
        </select>

        <div>Selected: <strong>{{ selectedContact }}</strong></div> -->

        <ul class="list-group mb-3">
          <li class="list-group-item d-flex justify-content-between lh-condensed">
            <div>
              <h6 class="my-0">SMS</h6>
              <input type="text" class="form-control" placeholder="Phone #" v-model="form.sms">
            </div>
          </li>
          <li class="list-group-item d-flex justify-content-between lh-condensed">
            <div>
              <h6 class="my-0">Voice</h6>
              <input type="text" class="form-control" placeholder="Phone #" v-model="form.voice">
            </div>
          </li>
          <li class="list-group-item d-flex justify-content-between lh-condensed">
            <div>
              <h6 class="my-0">WhatsApp</h6>
              <input type="text" class="form-control" placeholder="Phone #" v-model="form.whatsapp">
            </div>
          </li>
          <li class="list-group-item d-flex justify-content-between lh-condensed">
            <div>
              <h6 class="my-0">Email</h6>
              <input type="text"
                     class="form-control"
                     placeholder="email@domain.com"
                     v-model="form.email">
            </div>
          </li>
        </ul>
        <!-- <span>Contacts: {{ userContact }}</span> -->

      </div>

      <div class="col-md-8 order-md-2">
        <label for="message">
          <h4 class="mb-3">Your message</h4>
        </label>

        <div class="mb-3">
          <textarea class="form-control" id="message" rows="5" v-model="form.body">
          </textarea>
        </div>

        <!-- <h4 class="mb-3">Priority</h4> -->
        <div class="d-block my-3">
          <div class="custom-control custom-radio">
            <input type="radio"
                   id="normal-priority"
                   name="priority"
                   class="custom-control-input"
                   checked="yes">
            <label class="custom-control-label" for="normal-priority">Normal Priority</label>
          </div>
            <div class="custom-control custom-radio">
            <input type="radio"
                   id="high-priority"
                   name="priority"
                   class="custom-control-input">
            <label class="custom-control-label" for="high-priority">High Priority</label>
          </div>
        </div>

        <hr class="mb-4">
        <button class="btn btn-primary btn-lg btn-block" type="submit">Send Message</button>
        <div> {{ message }} </div>
      </div>

    </div>
  </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      // selectedContact: null,
      // contacts: [],
      message: '',
      form: {
        sms: '',
        voice: '',
        whatsapp: '',
        email: '',
        body: '',
      },
    };
  },
  methods: {
    initForm() {
      this.form.sms = '';
      this.form.voice = '';
      this.form.whatsapp = '';
      this.form.email = '';
      this.form.body = '';
    },
    handleSubmit() {
      axios.post('http://localhost:5000/notifications', this.form)
        .then((response) => {
          this.message = response.data.message;
          // eslint-disable-next-line
          console.log(response);
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    getContacts() {
      const uri = 'http://localhost:5000/contacts';
      axios.get(uri)
        .then((response) => {
          this.contacts = response.data.contacts;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
  },
  created() {
    this.getContacts();
  },

};
</script>
