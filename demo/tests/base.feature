@django_db
@wip
Feature: Create some basic forms

  Background:

  Scenario: Visit the index form page
    Given the form index page exists
    When I visit 'http://localhost:8000/forms'
    Then the page title should be 'Forms'
    And I should see the title 'Forms'

  Scenario: Create a simple form
    Given the form index page exists
    Given a form named 'Event Registration' exists
    When I visit 'http://localhost:8000/forms/event-registration'
    Then I should see 'Event Registration'
    #And I should see a hidden input named 'csrfmiddlewaretoken'
    And I should see 1 inputs in total
