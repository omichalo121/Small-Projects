document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');

  // Handling the compose of e-mail
  const submit = document.querySelector('#submit');
  const recipients = document.querySelector('#compose-recipients');
  const title = document.querySelector('#compose-subject');
  const body = document.querySelector('#compose-body');
  function updateSB() {
    submit.disabled = (body.value === '' || title.value === '' || recipients.value === '');
  }
  window.addEventListener('input', updateSB);
  submit.addEventListener('click', function(event) {
    sendEmail(event);
  })
});

function compose_email(recipient, subject, body, timestamp, prefill) {
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#submit').disabled = true;

  // Clear out composition fields or prefill them
  if(prefill === true) {
    document.querySelector('#compose-recipients').value = recipient;
    const checker = 'Re: ';
    if(checker === subject.substring(0, 4)) {
      document.querySelector('#compose-subject').value = `${subject}`;
    } else {
      document.querySelector('#compose-subject').value = `Re: ${subject}`;
    }
    document.querySelector('#compose-body').value = `On ${timestamp} ${recipient} wrote:\n\n"${body}"`;
  } else {
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';
  }
}

function load_mailbox(mailbox) {

  // Show the mailbox and hide other views
  const email_block = document.querySelector('#emails-view');
  email_block.style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  email_block.innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`, {
    method: 'GET'
  })
  .then(response => response.json())
  .then(result => {
    console.log(result);
    for(let i = 0, n = result.length; i < n; i++) {
      const email = document.createElement('div');
      const email_redirect = document.createElement('a');
      email.classList.add('email');
      const sender_block = document.createElement('p');
      const subject_block = document.createElement('p');
      const timestamp_block = document.createElement('p');
      sender_block.innerHTML = `From: ${result[i].sender}`;
      subject_block.innerHTML = `Subject: ${result[i].subject}`;
      timestamp_block.innerHTML = `${result[i].timestamp}`;
      email.append(sender_block);
      email.append(subject_block);
      email.append(timestamp_block);
      if(result[i].read === true) {
        email.style.backgroundColor = 'lightgray';
      }
      email_redirect.append(email);
      email_redirect.classList.add('email_a');
      email_redirect.addEventListener('click', () => {
        emailRedirect(result[i].id);
      })
      email_redirect.addEventListener('click', () => false);
      email_block.append(email_redirect);
    }
  })
  .catch(err => {
    console.log(err);
  })
}

function sendEmail(event) {
  event.preventDefault();

  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: document.querySelector('#compose-recipients').value,
        subject: document.querySelector('#compose-subject').value,
        body: document.querySelector('#compose-body').value
    })
  })
  .then(response => response.json())
  .then(result => {
      load_mailbox('sent');
      console.log(result);
  })
  .catch(err => console.log(err));
}

function emailRedirect(id) {
  fetch(`/emails/${id}`, {
    method: 'GET'
  })
  .then(response => response.json())
  .then(result => {
    const email = document.querySelector('#emails-view');

    while (email.firstChild) {
      email.removeChild(email.firstChild);
    }
    const email_child1 = document.createElement('div');
    email_child1.classList.add('email');
    email_child1.style.border = 'none';

    const sender_block = document.createElement('p');
    const timestamp_block = document.createElement('p');
    sender_block.innerHTML = `From: ${result.sender}`;
    timestamp_block.innerHTML = `${result.timestamp}`;
    email_child1.append(sender_block);
    email_child1.append(timestamp_block);
    email.append(email_child1);

    const email_child2 = document.createElement('div');
    email_child2.classList.add('email_child');
    const subject_block = document.createElement('p');
    subject_block.innerHTML = `Subject: ${result.subject}`;
    email_child2.append(subject_block);
    email.append(email_child2);

    const email_child3 = document.createElement('div');
    email_child3.classList.add('email_child');
    const recipients_block = document.createElement('p');
    recipients_block.innerHTML = `Recipients: ${result.recipients}`;
    email_child3.append(recipients_block);
    email.append(email_child3);

    const email_text = document.createElement('div');
    const text_block = document.createElement('p');
    text_block.innerHTML = result.body;
    text_block.classList.add('email_text');
    email_text.append(text_block);
    email.append(email_text);

    const user = document.querySelector('#user').innerHTML;
    if(result.sender !== user) {
      const archive = document.createElement('input');
      archive.type = 'submit';
      if(result.archived === false) {
        archive.value = 'Archive this e-mail';
      } else {
        archive.value = 'Unarchive this e-mail';
      }
      archive.addEventListener('click', function() {
        archiveMail(id, result.archived);
      });
      email.append(archive);

      const unread = document.createElement('input');
      unread.type = 'submit';
      unread.value = 'Mark this e-mail as unread';
      unread.style.marginLeft = '15px';
      unread.addEventListener('click', function() {
        unreadMail(id, false);
      });
      email.append(unread);

      const reply = document.createElement('input');
      reply.type = 'submit';
      reply.value = 'Reply';
      reply.style.marginLeft = '612px';
      reply.addEventListener('click', function() {
        compose_email(result.sender, result.subject, result.body, result.timestamp, true);
      })
      email.append(reply);

    }
    fetch(`/emails/${id}`, {
      method: 'PUT',
      body: JSON.stringify({
        read: true
      })
    })

    console.log(result);
  })
  .catch(err => console.log(err));
}

function archiveMail(id, archived) {
  if(archived === false) {
    archived = true;
  } else { archived = false; }

  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: archived
    })
  })
  .then(response => {
      load_mailbox('inbox');
  })
  .catch(err => console.log(err));
}

function unreadMail(id, status) {
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
      read: status
    })
  })
  .then(response => {
      load_mailbox('inbox');
  })
  .catch(err => console.log(err));
}