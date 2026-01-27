#@django_db
#Feature: Create a form with a Label

  #Background:
  #  Given an empty form named 'Event Registration' exists

  #Scenario: Add subtitles to the form and visit it
  #  Given I am editing the form 'Event Registration'
  #  And I add a Label field as follow:
  #    | subtitle     | Part 1: Personal Information |
  #    | help message |                              |
  #  And I add a Label field as follow:
  #    | subtitle     | Part 2: Participation Options |
  #    | help message |                               |
  #  When I visit the form named 'Event Registration'
  #  Then I should see the following elements:
  #    | subtitle | Part 1: Personal Information  |
  #    | subtitle | Part 2: Participation Options |
  #  But I should not see any form subtitle help

  #Scenario: Add subtitles with help messages to the form and visit it
  #  Given I am editing the form 'Event Registration'
  #  And I add a Label field as follow:
  #    | subtitle     | Part 1: Personal Information         |
  #    | help message | Please provide your contact details. |
  #  And I add a Label field as follow:
  #    | subtitle     | Part 2: Participation Options         |
  #    | help message | Select activities you wish to attend. |
  #  When I visit the form named 'Event Registration'
  #  Then I should see the following elements:
  #    | subtitle | Part 1: Personal Information          |
  #    | message  | Please provide your contact details.  |
  #    | subtitle | Part 2: Participation Options         |
  #    | message  | Select activities you wish to attend. |
