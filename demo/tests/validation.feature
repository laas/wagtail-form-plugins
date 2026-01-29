@django_db
Feature: Use form validation
  Background:
    Given the form index page exists

  Scenario: Validate a form
    Given a form named "Event Registration" exists
      And the form "Event Registration" is created by the user admin (admin@example.com)

     When I visit "/forms/event-registration"
     Then I should see the form validation page of "Event Registration"

     When I fill the "validation_email" input with "hello@example.com"
      And I validate the form

     Then I should see the token-validation info message
     And  I should receive at hello@example.com a validation email from noreply@example.com

     When I click on the validation link
     Then I should see the form page "Event Registration"
      And I should see the token-validation success message
      And I should see 0 form field

     When I validate the form
     Then I should see the form landing page "Event Registration"
      And the page should contain a form-thank-you element
      And I should receive at hello@example.com a confirmation email from noreply@example.com about the form "Event Registration"
      And the form admin (admin@example.com) should receive an information email from noreply@example.com about the form "Event Registration"
