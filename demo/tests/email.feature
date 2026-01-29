@django_db
Feature: Use form validation
 Background:

  Scenario: Test sending test emails
     When I send a test email
      And I send a test email
     Then I should have 2 emails in my mailbox
     Then I should receive an email
      And I should receive an email
     Then I should have 0 email in my mailbox
